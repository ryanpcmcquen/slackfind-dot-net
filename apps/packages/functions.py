# -*- coding: utf-8 -*-

def make_form_instance(form_class, query_dict):
    """
        parsing query dictionary for known keys
    """

    known_keys = ('name', 'distversion',)

    user_data = {}

    for key in query_dict.iterkeys():
        if key in known_keys:
            user_data[key] = query_dict[key]
    
    return form_class(user_data) 

def check_url_for_alive(path):
    """
        this function only checks one standalone function for raising execptions
    """
    from urllib2 import urlopen, URLError, HTTPError
    
    try:
       iter = urlopen(path + 'PACKAGES.TXT')
    except URLError, HTTPError:
        return False
    else:
        iter.close()
        return True
    

