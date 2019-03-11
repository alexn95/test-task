"""
Module contain application views realisation
"""

from datetime import datetime

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import F
from django.views.generic import ListView, DetailView, DeleteView, FormView
from django.views.generic import UpdateView, CreateView

from openpyxl.writer.excel import save_virtual_workbook

from .tasks import set_like
from .enums import OrderBy
from .forms import ClientPhotoForm, ClientListForm
from .services import get_clients_in_xlsx
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
    Client list view
    """
    context_object_name = 'clients'
    template_name = 'clientbase/clients_list.html'
    paginate_by = settings.CLIENTS_PER_PAGE

    def get_queryset(self):
        """
        List of clients by query string
        :return: list of clients
        """
        self.form = ClientListForm(self.request.GET)
        if not self.form.is_valid():
            return HttpResponse(self.form.errors, status=400)
        clients_data = Client.objects.get_clients_by_name(
            self.form.cleaned_data['query_string'],
            self.form.cleaned_data['order_by'] or OrderBy.fn.value[0]
        )
        return list(map(lambda client: client.get_client_data(),
                        clients_data))

    def get_context_data(self, **kwargs):
        """
        Add query_string to context
        :param kwargs: kwargs
        :return: context
        """
        context = super().get_context_data(**kwargs)
        context['query_string'] = self.form.cleaned_data['query_string']
        return context


class ClientCreate(FormView, CreateView):
    """
    Create a new client view
    """
    template_name = 'clientbase/client_create.html'
    form_class = ClientForm
    success_url = reverse_lazy('client_list')


class ClientDelete(DeleteView):
    """
    Delete client by id view
    """
    model = Client
    success_url = reverse_lazy('client_deleted')


class ClientPhotoList(ListView):
    """
    The client photo list view
    """
    context_object_name = 'clients'
    template_name = 'clientbase/client_photo.html'
    model = Client

    def get_queryset(self):
        """
        List of all client photo
        :return: list of client photo
        """
        queryset = super().get_queryset()
        format_queryset = list(map(
            lambda client: client.get_client_photo_data(),
            queryset
        ))
        return format_queryset


class LikeClientPhotoView(UpdateView):
    """
    The view witch set "like" to client photo by id
    """
    def post(self, request, *args, **kwargs):
        """
        Get client by id and increment client likes counter if it possible
        """
        form = ClientPhotoForm(request.POST)
        if form.is_valid():
            client_id = form.cleaned_data['client_id']
            with transaction.atomic():
                result = Client.objects.select_for_update().filter(
                    id=client_id, likes__lt=settings.MAX_LIKES
                ).update(likes=F('likes') + 1)
                if result:
                    return HttpResponse(status=200)
                else:
                    return HttpResponse('Maximum like counter', status=200)
        else:
            return HttpResponse(form.errors.as_json(), status=400)


class LikeClientPhotoAsyncView(UpdateView):
    """
    The view witch set "like" to client photo by id async
    """
    def post(self, request, *args, **kwargs):
        """
        Get client by id and increment client likes counter if it possible
        """
        form = ClientPhotoForm(request.POST)
        if form.is_valid():
            client_id = form.cleaned_data['client_id']
            result = set_like(client_id)
            if result:
                return HttpResponse(status=200)
            else:
                return HttpResponse('Maximum like counter', status=200)
        else:
            return HttpResponse(form.errors.as_json(), status=400)


def data_to_xlsx(request):
    """
    Download all clients data in xlsx file view
    :param request: view request
    :return: xlsx document for download
    """
    book = get_clients_in_xlsx()
    response = HttpResponse(save_virtual_workbook(book),
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = \
        'attachment; filename="client_data_%s.xlsx"' % datetime.now().date()
    return response
