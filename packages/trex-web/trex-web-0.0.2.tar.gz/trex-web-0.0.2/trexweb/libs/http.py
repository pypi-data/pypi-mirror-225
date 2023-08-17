'''
Created on Apr 27, 2012

@author: lokjac
'''
import six
from six import string_types
import logging

class StatusCode(object):
    OK                          = 200
    CREATED                     = 201
    ACCEPTED                    = 202
    NO_CONTENT                  = 204
    RESET_CONTENT               = 205
    BAD_REQUEST                 = 400
    UNAUTHORIZED                = 401
    FORBIDDEN                   = 403
    NOT_FOUND                   = 404
    METHOD_NOT_ALLOW            = 405
    PRECONDITION_FAILED         = 412
    RESOURCE_LOCKED             = 423
    INTERNAL_SERVER_ERROR       = 500
    SERVICE_NOT_AVAILABLE       = 503
    GATEWAY_TIMEOUT             = 504
    HTTP_VERSION_NOT_SUPPORT    = 505
    # add more status code according to your need

def create_rest_message(message=None, status_code=StatusCode.BAD_REQUEST, **kwargs):
    reply_message = {}
    logging.debug('create_rest_message: message=%s', message)
    
    if kwargs is not None:
        for key, value in six.iteritems(kwargs):
            reply_message[key] = value
        
    if message:
        if isinstance(message, string_types):
            reply_message['msg'] = [message]
        
        elif isinstance(message, (tuple, list)):
            reply_message['msg'] = message
            
        elif isinstance(message, dict):
            reply_message['msg'] = message['msg']    
    else:
        reply_message['msg'] = []
    
    logging.debug('reply_message=%s', reply_message)
    
    return reply_message, status_code
