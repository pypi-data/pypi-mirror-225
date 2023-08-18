"""
    QuaO Project media_type.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class MediaType(Enum):
    APPLICATION_JSON = 'application/json'
    ALL_TYPE = '*/*'
    MULTIPART_FORM_DATA = 'multipart/form-data'
