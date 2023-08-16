"""
    QuaO Project device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import abstractmethod, ABC

from ...async_tasks.post_processing_task import post_processing_task
from ...component.callback.update_job_metadata import update_job_metadata
from ...config.logging_config import logger
from ...data.callback.callback_url import CallbackUrl
from ...data.device.circuit_running_option import CircuitRunningOption
from ...data.promise.post_processing_promise import PostProcessingPromise
from ...data.response.authentication import Authentication
from ...data.response.job_response import JobResponse
from ...data.response.project_header import ProjectHeader
from ...enum.invocation_step import InvocationStep
from ...enum.media_type import MediaType
from ...enum.status.job_status import JobStatus
from ...enum.status.status_code import StatusCode
from ...model.provider.provider import Provider
from ...util.json_parser_utils import JsonParserUtils


class Device(ABC):
    def __init__(self, provider: Provider, device_specification: str):
        self.provider = provider
        self.device = provider.get_backend(device_specification)
        self.execution_time = None

    def run_circuit(self,
                    circuit,
                    post_processing_fn,
                    options: CircuitRunningOption,
                    callback_dict: dict,
                    authentication: Authentication,
                    project_header: ProjectHeader):
        """

        @param project_header: project header
        @param callback_dict: callback url dictionary
        @param options: Options for run circuit
        @param authentication: Authentication for calling quao server
        @param post_processing_fn: Post-processing function
        @param circuit: Circuit was run
        """

        job, job_response = self.__on_execution(
            authentication=authentication,
            project_header=project_header,
            execution_callback=callback_dict.get(InvocationStep.EXECUTION),
            circuit=circuit,
            options=options)

        if job is None or job_response is None:
            return

        original_job_result, job_response = self.__on_analysis(
            job_response=job_response,
            job=job,
            analysis_callback=callback_dict.get(InvocationStep.ANALYSIS))

        if original_job_result is None or job_response is None:
            return

        self.__on_finalization(job_result=original_job_result,
                               authentication=authentication,
                               post_processing_fn=post_processing_fn,
                               finalization_callback=callback_dict.get(InvocationStep.FINALIZATION))

    def __on_execution(self, authentication: Authentication,
                       project_header: ProjectHeader,
                       execution_callback: CallbackUrl,
                       circuit,
                       options: CircuitRunningOption):
        """

        @param authentication: authentication information
        @param project_header: project header information
        @param execution_callback: execution step callback urls
        @param circuit: circuit will be run
        @param options: options will use for running
        @return: job and job response
        """
        logger.debug("Invocation - On execution")

        job_response = JobResponse(authentication=authentication,
                                   project_header=project_header,
                                   status_code=StatusCode.DONE)

        update_job_metadata(job_response=job_response,
                            callback_url=execution_callback.on_start)
        try:
            job = self._create_job(circuit=circuit, options=options)
            job_response.provider_job_id = self._get_provider_job_id(job)
            job_response.job_status = self._get_job_status(job)

            if not self._is_simulator():
                job_response.status_code = StatusCode.POLLING
                job = None

        except Exception as exception:
            logger.debug("Execute job failed with error {}".format(str(exception)))

            job_response.status_code = StatusCode.ERROR
            job_response.job_status = JobStatus.ERROR.value
            job_response.job_result = {"error": str(exception)}

            update_job_metadata(job_response=job_response,
                                callback_url=execution_callback.on_error)
            return None, None

        update_job_metadata(job_response=job_response,
                            callback_url=execution_callback.on_done)

        return job, job_response

    def __on_analysis(self, job_response: JobResponse,
                      analysis_callback: CallbackUrl,
                      job):
        """

        @param job_response:
        @param analysis_callback:
        @param job:
        @return:
        """
        logger.debug("Invocation - On analysis")

        update_job_metadata(job_response=job_response,
                            callback_url=analysis_callback.on_start)

        try:
            job_response.content_type = MediaType.APPLICATION_JSON

            original_job_result = job.result()
            job_response.job_status = self._get_job_status(job)

            logger.debug('Producing histogram ....')
            job_response.job_histogram = self._produce_histogram_data(original_job_result)
            logger.debug('Producing histogram completed!')

            logger.debug('Calculating execution time ....')
            original_job_result_dict = JsonParserUtils.parse(original_job_result)
            self._calculate_execution_time(original_job_result_dict)
            job_response.execution_time = self.execution_time
            logger.debug('Execution time calculation was: {0} seconds'
                         .format(self.execution_time))

            update_job_metadata(
                job_response=job_response,
                callback_url=analysis_callback.on_done)

            return original_job_result, job_response

        except Exception as exception:
            job_response.status_code = StatusCode.ERROR
            job_response.job_status = JobStatus.ERROR.value
            job_response.job_result = {"error": str(exception)}

            update_job_metadata(job_response=job_response,
                                callback_url=analysis_callback.on_error)
            return None, None

    @staticmethod
    def __on_finalization(job_result,
                          finalization_callback: CallbackUrl,
                          post_processing_fn,
                          authentication: Authentication):
        """

        @param job_result:
        @param finalization_callback:
        @param post_processing_fn:
        @param authentication:
        """
        logger.info("Invocation - On finalization")

        post_processing_promise = PostProcessingPromise(
            callback_url=finalization_callback,
            authentication=authentication,
            job_result=job_result)

        post_processing_task(post_processing_fn,
                             post_processing_promise)

    @abstractmethod
    def _create_job(self, circuit, options: CircuitRunningOption):
        """

        @param circuit: Circuit for create job
        @param options:
        """
        pass

    @abstractmethod
    def _is_simulator(self) -> bool:
        """

        """
        pass

    @abstractmethod
    def _produce_histogram_data(self, job_result) -> dict:
        """

        @param job_result:
        """
        pass

    @abstractmethod
    def _get_provider_job_id(self, job) -> str:
        """

        """
        pass

    @abstractmethod
    def _get_job_status(self, job) -> str:
        """

        """
        pass

    @abstractmethod
    def _get_name(self) -> str:
        """

        """
        pass

    @abstractmethod
    def _calculate_execution_time(self, job_result) -> float:
        """

        """
        pass
