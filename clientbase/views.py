from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from clientbase.serializers import ClientPhotoSerializer
from clientbase.services import get_clients_in_xlsx
from clientbase.forms import ClientForm
from clientbase.models import Client

from datetime import datetime
from openpyxl.writer.excel import save_virtual_workbook


def client_card(request, client_id):
    """
    The client card view
    Client chosen by client_id
    :param request: view request
    :param client_id: id of the client
    :return: client card template and client data
    """
    try:
        client = Client.objects.get(id=client_id)
    except ObjectDoesNotExist:
        raise Http404('Client id not found')
    return render(request, 'clientbase/client_card.html', {'client': client.get_client_data()})


def clients_list(request):
    """
    The client list view
    :param request: view request
    :return: client list template, data of all clients, and query string if exist
    """
    order_by_list = ['first_name', 'last_name', 'date_of_birth', '-date_of_birth']
    order_by = request.GET.get('order_by', 'first_name')
    if not any(order_by == s for s in order_by_list):
        raise Http404('Bad request params.')
    query_string = request.GET.get('query_string', None)

    clients_data = Client.objects.get_clients_by_name(query_string, order_by)
    list_of_client = list(map(lambda client: client.get_client_data(), clients_data))

    clients_per_page = 5
    paginator = Paginator(list_of_client, clients_per_page)
    clients = paginator.get_page(request.GET.get('page'))
    return render(request, 'clientbase/clients_list.html',
                  {'clients': clients, 'query_string': query_string if query_string else ''})


def client_create(request):
    """
    Create a new client view
    :param request: view request
    :return: create client form template and form data
    """
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ClientForm()
    return render(request, 'clientbase/client_create.html', {'form': form})


def client_delete(request):
    """
    Delete client by id view
    :param request: view request
    :return: client delete template
    """
    try:
        client_id = request.POST['client_id']
        Client.objects.get(id=client_id).delete()
    except ObjectDoesNotExist:
        raise Http404('Invalid client id')
    except KeyError:
        raise Http404('Client id not found')
    return render(request, 'clientbase/client_deleted.html')


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


def client_photo(request):
    """
    Client photo with likes template
    :param request: view request
    :return: client photo template and clients data
    """
    clients = Client.objects.get_clients_photo_data()
    return render(request, 'clientbase/client_photo.html', {'clients': clients})


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
            client_id = request.data['client_id']
            return set_like_transaction(client_id)
        except KeyError:
            return Response(data='Client id not found', status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    User login by username and password
    :param request: view request
    :return: user token
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)


@transaction.atomic
def set_like_transaction(client_id):
    """
    Increment client likes counter if it possible
    :param client_id: id of the client
    :return: method result status
    """
    try:
        instance = Client.objects.select_for_update().get(id=client_id)
    except ObjectDoesNotExist:
        return Response(data='Invalid client id', status=status.HTTP_400_BAD_REQUEST)
    max_like_counter = 10

    with transaction.atomic():
        if instance.likes >= max_like_counter:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        else:
            instance.likes += 1
            instance.save()

    return Response(data='Like was set', status=status.HTTP_200_OK)
