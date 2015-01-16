def get_params_from_request(querystring, *args):
    """
        function returns params from querystring array
        removing values which contains in args
    """
    get_params = '&'.join(['%s=%s' % (x[0], x[1]) for x in
        querystring.iteritems() if x[0] not in args])
    
    if get_params:
        get_params = '?%s&' % get_params
    else:
        get_params = '?'
        
    return get_params

def dict_from_querystring(querystring):
    """
        function returns dict with values from querystring
    """
    result = {}

    if querystring[0] == '?':
        querystring = querystring[1:]

    for keyval in querystring.split('&'):
        vals = keyval.split('=')
        
        if len(vals) != 2:
            continue
        
        result[vals[0]] = vals[1]

    return result

def get_params_from_querystring(querystring, *args):
    """
    .querystring..
    """
    return get_params_from_request(dict_from_querystring(querystring), *args)
