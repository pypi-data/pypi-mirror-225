"""
    QuaO Project handler.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import abstractmethod


class Handler:
    def __init__(self,
                 request_data: dict,
                 post_processing_fn):
        self.request_data = request_data
        self.post_processing_fn = post_processing_fn

    @abstractmethod
    def handle(self):
        """

        """
        pass
