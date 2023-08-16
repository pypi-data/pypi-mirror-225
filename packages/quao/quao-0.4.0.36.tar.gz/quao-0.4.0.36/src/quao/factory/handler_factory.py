"""
    QuaO Project handler_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..handler.handler import Handler
from ..handler.invocation_handler import InvocationHandler
from ..handler.job_fetching_handler import JobFetchingHandler


class HandlerFactory:
    @staticmethod
    def create_handler(event,
                       circuit_preparation_fn,
                       post_processing_fn, ) -> Handler:
        request_data = event.json()
        provider_job_id = request_data.get("providerJobId")

        if provider_job_id is None:
            return InvocationHandler(request_data=request_data,
                                     circuit_preparation_fn=circuit_preparation_fn,
                                     post_processing_fn=post_processing_fn)

        return JobFetchingHandler(request_data=request_data,
                                  post_processing_fn=post_processing_fn)
