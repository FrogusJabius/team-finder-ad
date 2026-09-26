from django.core.paginator import Paginator


def paginate(queryset, request, per_page):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))
