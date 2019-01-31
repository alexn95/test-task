from django import template

register = template.Library()


# Add a new parameter to the GET query and keep the old
@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
