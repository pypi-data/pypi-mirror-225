import logging
from http import HTTPStatus
from time import sleep

from sherpa_client.api.jobs import get_job
from sherpa_client.api.projects import get_project_info
from sherpa_client.api.segments import search_segments
from sherpa_client.api.services import get_services
from sherpa_client.client import SherpaClient
from sherpa_client.models import (
    Credentials,
    SherpaJobBeanStatus,
    SherpaJobBean,
    SegmentHits,
)
from tenacity import retry, stop_after_delay, stop_after_attempt, wait_fixed

logger = logging.getLogger("kt-client")


class KTClient:
    def __init__(self, sherpa_url, sherpa_user, sherpa_pwd):
        self.user = sherpa_user
        self.pwd = sherpa_pwd
        self.url = sherpa_url
        self.connect()

    def connect(self):
        self.sherpa_client = SherpaClient(
            base_url=f"{self.url}/api", verify_ssl=False, timeout=100
        )
        self.sherpa_client.login_with_cookie(
            Credentials(email=self.user, password=self.pwd)
        )

    @retry(stop=(stop_after_delay(120) | stop_after_attempt(10)), wait=wait_fixed(10))
    def check_resource(self):
        r = get_services.sync_detailed(client=self.sherpa_client)
        if not r.is_success:
            if r.status_code == HTTPStatus.UNAUTHORIZED:
                self.connect()
            r.raise_for_status()
        return r.is_success

    @retry(stop=(stop_after_delay(60) | stop_after_attempt(10)), wait=wait_fixed(1))
    def check_project(self, project):
        r = get_project_info.sync_detailed(project, client=self.sherpa_client)
        if not r.is_success:
            if r.status_code == HTTPStatus.UNAUTHORIZED:
                self.connect()
            r.raise_for_status()
        return r.is_success

    def get_segments(self, project, query, limit, simple):
        result = None
        r = search_segments.sync_detailed(
            project,
            client=self.sherpa_client,
            query=query,
            size=limit,
            simple_query=simple
        )
        if r.is_success:
            hits: SegmentHits = r.parsed
            result = hits.hits
        else:
            logger.warning(
                f"Error when searching segments {query} in {project}",
                exc_info=True,
            )
        return result

    @retry(stop=(stop_after_delay(120) | stop_after_attempt(2)), wait=wait_fixed(5))
    def wait_for_completion(self, job_bean: SherpaJobBean, ŵait_time=5):
        if job_bean:
            while job_bean.status not in [
                SherpaJobBeanStatus.COMPLETED,
                SherpaJobBeanStatus.CANCELLED,
                SherpaJobBeanStatus.FAILED,
            ]:
                sleep(ŵait_time)
                r = get_job.sync_detailed(
                    job_bean.project, job_bean.id, client=self.sherpa_client
                )
                if r.is_success:
                    job_bean = r.parsed
                else:
                    if r.status_code == HTTPStatus.UNAUTHORIZED:
                        self.connect()
                    r.raise_for_status()
        return job_bean

    @staticmethod
    def is_success(job_bean):
        return job_bean and job_bean.status == SherpaJobBeanStatus.COMPLETED
