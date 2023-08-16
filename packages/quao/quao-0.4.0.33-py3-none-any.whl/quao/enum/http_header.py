"""
    QuaO Project http_header.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class HttpHeader(Enum):
    AUTHORIZATION = 'Authorization'
    CONTENT_TYPE = 'Content-type'
    ACCEPT = 'Accept'

