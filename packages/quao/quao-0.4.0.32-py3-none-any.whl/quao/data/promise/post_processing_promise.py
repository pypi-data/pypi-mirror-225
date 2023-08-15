"""
    QuaO Project post_processing_promise.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..callback.callback_url import CallbackUrl
from ..response.authentication import Authentication
from ...data.promise.promise import Promise


class PostProcessingPromise(Promise):
    def __init__(
        self, callback_url: CallbackUrl, authentication: Authentication, job_result
    ):
        super().__init__(callback_url, authentication)
        self.job_result = job_result
