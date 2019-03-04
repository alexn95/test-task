from datetime import datetime

from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import F
from django.views.generic import ListView, DetailView, DeleteView, FormView

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from openpyxl.writer.excel import save_virtual_workbook

from .serializers import ClientPhotoSerializer, AuthenticateSerializer
from .services import get_clients_in_xlsx, is_string_represent_an_int
from .forms import ClientForm
from .models import Client
from app import settings


class ClientCard(DetailView):
    """
    Client card view
    """
    context_object_name = 'client'
    model = Client
    template_name = 'clientbase/client_card.html'

    def get_object(self, queryset=None):
        """
        Client data by queryset
        :param queryset: client queryset
        :return: client object
        """
        obj = super(ClientCard, self).get_object(queryset=queryset)
        return obj.get_client_data()


class ClientsList(ListView):
    """
    The client list view
    """
    context_object_name = 'clients'
    template_name = 'clientbase/clients_list.html'
    paginate_by = settings.CLIENTS_PER_PAGE

    def get_queryset(self):
        """
        List of clients by query string
        :return: list of clients
        """
        self.query_string = self.request.GET.get('query_string', '')
        self.order_by = self.request.GET.get('order_by', settings.ORDER_BY_LIST[0])
        if not any(self.order_by == s for s in settings.ORDER_BY_LIST):
            raise Http404('Bad request params.')
        page = self.request.GET.get('page', None)
        if page and not is_string_represent_an_int(page):
            raise Http404('Page does not exist.')
        clients_data = Client.objects.get_clients_by_name(self.query_string, self.order_by)
        list_of_client = list(map(lambda client: client.get_client_data(), clients_data))
        return list_of_client

    def get_context_data(self, **kwargs):
        """
        Add query_string to context
        :param kwargs: kwargs
        :return: context
        """
        context = super(ClientsList, self).get_context_data(**kwargs)
        context['query_string'] = self.query_string
        return context


class ClientCreate(FormView):
    """
    Create a new client view
    """
    template_name = 'clientbase/client_create.html'
    form_class = ClientForm
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        """
        Validation and save form data
        :param form: create client form
        :return: form validation result
        """
        form.save()
        return super(ClientCreate, self).form_valid(form)


class ClientDelete(DeleteView):
    """
    Delete client by id view
    """
    model = Client
    success_url = reverse_lazy('client_deleted')


def data_to_xlsx(request):
    """
    Download all clients data in xlsx file view
    :param request: view request
    :return: xlsx document for download
    """
    book = get_clients_in_xlsx()
    response = HttpResponse(save_virtual_workbook(book), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="client_data_%s.xlsx"' % datetime.now().date()
    return response


class ClientPhotoList(ListView):
    """
    The client photo list view
    """
    context_object_name = 'clients'
    template_name = 'clientbase/client_photo.html'

    def get_queryset(self):
        """
        List of all client photo
        :return: list of client photo
        """
        clients_data = Client.objects.all()
        list_of_client = list(map(lambda client: client.get_client_photo_data(), clients_data))
        return list_of_client


class ClientPhotoViewSet(generics.ListAPIView):
    """
    Client photo api view
    Return all client photo with likes
    """
    queryset = Client.objects.all()
    serializer_class = ClientPhotoSerializer
    http_method_names = ['get']


class LikeClientPhotoView(generics.UpdateAPIView):
    """
    Api view witch set like client photo by id
    """
    queryset = Client.objects.all()
    serializer_class = ClientPhotoSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        """
        Get client by id and increment client likes counter if it possible
        """
        try:
            with transaction.atomic():
                client_id = request.data['client_id']
                result = Client.objects.select_for_update().filter(id=client_id, likes__lt=settings.MAX_LIKES)\
                    .update(likes=F('likes') + 1)
                return Response(status=status.HTTP_200_OK) if result else Response(status=status.HTTP_304_NOT_MODIFIED)
        except KeyError:
            return Response(data='Client id not found', status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Login REST API view
    """
    def post(self, request):
        """
        Check if user exist and return token key if user exist
        :param request: post request
        :return: token key
        """
        serializer = AuthenticateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
