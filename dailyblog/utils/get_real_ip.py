__author__ = 'haibo'



def get_real_ip(request):
    """
    the http_x_forwarded_for only exists when using proxy or load balance.
    :param request:
    :return:
    """

    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
        #'proxy_add_x_forwarded_for'
    ]

    for field in FORWARDED_FOR_FIELDS:
        if field in request.META:
            if ',' in request.META[field]:
                parts = request.META[field].split(',')
                #the real ip is in the end of array
                request.META['REMOTE_ADDR'] = parts[-1].strip()
            else:
                request.META['REMOTE_ADDR'] = request.META[field]
            break

    return request.META.get('REMOTE_ADDR')


