function deleteClient(id) {
    if (confirm('Are you sure?')) {
        form = document.getElementById("deleteClientForm_" + id);
        form.submit();
    } else {
        return false;
    }
}