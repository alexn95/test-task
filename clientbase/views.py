from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404

from clientbase.services import get_clients_in_xlsx
from clientbase.forms import ClientForm
from clientbase.models import Client

from datetime import datetime
from openpyxl.writer.excel import save_virtual_workbook


# The client card view 
# client chosen by id
def client_card(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except ObjectDoesNotExist:
        raise Http404('Client with this id does not exist')
    return render(request, 'clientbase/client_card.html', {'client': client.get_client_data()})


# The client list view
def clients_list(request):
    # get order_by param from request and check it valid
    order_by_list = ['first_name', 'last_name', 'date_of_birth', '-date_of_birth']
    order_by = request.GET.get('order_by', 'first_name')
    if not any(order_by == s for s in order_by_list):
        raise Exception('Bad request params.')
    
    # get query_string param from request
    query_string = request.GET.get('query_string', None)

    # get and formatting client list by query_string
    clients_data = Client.objects.get_clients_by_name(query_string, order_by)
    list_of_client = list(map(lambda client: client.get_client_data(), clients_data))

    # pagination
    clients_per_page = 5
    paginator = Paginator(list_of_client, clients_per_page)
    clients = paginator.get_page(request.GET.get('page'))

    return render(request, 'clientbase/clients_list.html',
                  {'clients': clients, 'query_string': query_string if query_string else ''})


# Create a new client
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ClientForm()
    return render(request, 'clientbase/client_create.html', {'form': form})


# Delete client by id
def client_delete(request, client_id):
    try:
        Client.objects.get(id=client_id).delete()
    except ObjectDoesNotExist:
        raise Http404('Client with this id does not exist')
    return render(request, 'clientbase/client_deleted.html')


# Download all clients data in xlxs file
def data_to_xlsx(request):
    book = get_clients_in_xlsx()
    response = HttpResponse(save_virtual_workbook(book), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="client_data_%s.xlsx"' % datetime.now().date()
    return response
