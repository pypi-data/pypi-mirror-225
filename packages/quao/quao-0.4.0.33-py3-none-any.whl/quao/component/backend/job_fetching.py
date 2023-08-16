"""
    QuaO Project job_fetching.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from typing import Any

from qiskit import QiskitError

from ..callback.update_job_metadata import update_job_metadata
from ...async_tasks.post_processing_task import post_processing_task
from ...config.thread_config import circuit_running_pool
from ...data.callback.callback_url import CallbackUrl
from ...data.promise.post_processing_promise import PostProcessingPromise
from ...data.request.job_fetching_request import JobFetchingRequest
from ...data.response.authentication import Authentication
from ...data.response.job_response import JobResponse
from ...data.response.project_header import ProjectHeader
from ...enum.invocation_step import InvocationStep
from ...config.logging_config import logger
from ...enum.provider_type import ProviderType
from ...enum.status.job_status import JobStatus
from ...enum.status.status_code import StatusCode
from ...factory.provider_factory import ProviderFactory
from ...util.json_parser_utils import JsonParserUtils
from ...util.response_utils import ResponseUtils


class JobFetching:
    def __init__(self, request_data: JobFetchingRequest):
        self.provider_authentication: dict = request_data.provider_authentication
        self.provider_job_id: str = request_data.provider_job_id
        self.backend_authentication: Authentication = request_data.authentication
        self.project_header: ProjectHeader = request_data.project_header
        self.callback_dict: dict = {
            InvocationStep.ANALYSIS: request_data.analysis,
            InvocationStep.FINALIZATION: request_data.finalization
        }

    def fetch(self, post_processing_fn):
        """

        @param post_processing_fn:
        @return:
        """
        provider = self.__pre_execute()

        fetching_result = self.__execute(provider=provider,

                                         post_processing_fn=post_processing_fn)

        return fetching_result

    def __pre_execute(self):
        """

        @return:
        """
        return ProviderFactory \
            .create_provider(provider_type=ProviderType.IBM_QUANTUM.value,
                             authentication=self.provider_authentication) \
            .collect_providers()

    def __execute(self, provider, project_header: ProjectHeader, post_processing_fn):
        """

        @param provider:
        @param post_processing_fn:
        @return:
        """
        job_response = JobResponse(
            provider_job_id=self.provider_job_id,
            authentication=self.backend_authentication,
            project_header=project_header,
            status_code=StatusCode.DONE)

        try:
            job = provider.retrieve_job(job_id=self.provider_job_id)

            job_response.job_status = job.status().name

            if JobStatus.DONE.value.__eq__(job_response.job_status):
                circuit_running_pool.submit(self.__handle_job_result,
                                            job,
                                            job_response,
                                            self.callback_dict,
                                            post_processing_fn)
            else:
                job_response.status_code = StatusCode.POLLING

        except Exception as exception:
            logger.debug("Exception when fetch job with provider_job_id {0}: {1}".format(
                self.provider_job_id, str(exception)))

            job_response.job_result = {
                "error": "Exception when fetch job with provider_job_id {0}: {1}".format(
                    self.provider_job_id, str(exception)),
                "exception": str(exception),
            }
            job_response.status_code = StatusCode.ERROR
            job_response.job_status = JobStatus.ERROR.value

        return ResponseUtils.generate_response(job_response)

    def __handle_job_result(self,
                            job,
                            job_response: JobResponse,
                            callback_dict: dict,
                            post_processing_fn):
        """
        Fetch job from IBM Quantum

        @return: Job status
        """

        job_result = self.__on_analysis(
            callback_url=callback_dict.get(InvocationStep.ANALYSIS),
            job_response=job_response,
            job=job)

        if job_result is None:
            return

        self.__on_finalization(post_processing_fn=post_processing_fn,
                               callback_url=callback_dict.get(InvocationStep.FINALIZATION),
                               job_result=job_result)

    def __on_analysis(self,
                      callback_url: CallbackUrl,
                      job_response: JobResponse,
                      job):
        """

        @param callback_url:
        @param job_response:
        @param job:
        @return:
        """
        logger.info("Fetching - On analysis")

        update_job_metadata(job_response=job_response,
                            callback_url=callback_url.on_start)

        try:
            job_result = job.result()

            logger.debug("Producing histogram ....")
            job_response.job_histogram = self.__produce_histogram_data(job_result)
            logger.debug("Producing histogram completed!")

            logger.debug("Calculating execution time ....")
            job_result_parse = JsonParserUtils.parse(job_result)
            execution_time = self.__get_execution_time(job_result_parse)
            job_response.execution_time = execution_time
            logger.debug("Execution time calculation was: {0} seconds".format(execution_time))

            update_job_metadata(
                job_response=job_response,
                callback_url=callback_url.on_done)

            return job_result

        except Exception as exception:
            logger.error("Exception when analyst job result with provider_job_id {0}: {1}".format(
                self.provider_job_id, str(exception)))

            job_response.job_result = {
                "error": "Exception when analyst job result with provider_job_id {0}".format(
                    self.provider_job_id),
                "exception": str(exception),
            }

            job_response.status_code = StatusCode.ERROR
            job_response.job_result = JobStatus.ERROR

            update_job_metadata(
                job_response=job_response,
                callback_url=callback_url.on_error)

            return None

    def __on_finalization(self,
                          post_processing_fn,
                          callback_url: CallbackUrl,
                          job_result):
        """

        @param post_processing_fn:
        @param callback_url:
        @param job_result:
        """
        logger.info("Fetching - On finalization")

        promise = PostProcessingPromise(callback_url=callback_url,
                                        authentication=self.backend_authentication,
                                        job_result=job_result)

        post_processing_task(post_processing_fn=post_processing_fn,
                             promise=promise)

    @staticmethod
    def __produce_histogram_data(job_result) -> Any | None:
        """

        @param job_result:
        @return:
        """
        try:
            return job_result.get_counts()
        except QiskitError as qiskit_error:
            logger.debug("Can't produce histogram with error: {0}".format(str(qiskit_error)))
            return None

    @staticmethod
    def __get_execution_time(job_result):
        """

        @param job_result:
        @return:
        """
        if "metadata" not in job_result:
            return None

        metadata = job_result["metadata"]

        if (
                metadata is None
                or not bool(metadata)
                or "time_taken_execute" not in metadata
        ):
            return None

        return metadata["time_taken_execute"]
