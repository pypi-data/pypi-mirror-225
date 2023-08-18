"""
    QuaO Project job_fetching_handler.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from .handler import Handler
from ..component.backend.job_fetching import JobFetching
from ..data.request.job_fetching_request import JobFetchingRequest


class JobFetchingHandler(Handler):
    def __init__(self,
                 request_data: dict,
                 post_processing_fn):
        super().__init__(request_data, post_processing_fn)

    def handle(self):
        request = JobFetchingRequest(self.request_data)

        job_fetching = JobFetching(request)

        fetching_result = job_fetching.fetch(post_processing_fn=self.post_processing_fn)

        return fetching_result

