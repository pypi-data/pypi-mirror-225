import logging
import os
import re
from functools import lru_cache
from typing import List, cast, Type

from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Sentence, AltText
from sherpa_client.models import SegmentHit

from pyprocessors_search_segments.kt_client import KTClient

logger = logging.getLogger("pymultirole")
SHERPA_URL = os.getenv("SHERPA_URL", "https://sherpa-afp.kairntech.com")
SHERPA_USER = os.getenv("SHERPA_USER")
SHERPA_PWD = os.getenv("SHERPA_PWD")


class SearchSegmentsParameters(ProcessorParameters):
    question_altText: str = Field(
        "question",
        description="""The alternative text where is stored the original question.""",
    )
    project_name: str = Field(
        None,
        description="""Find a way to inject the project name.""",
    )
    limit: int = Field(
        5,
        description="use the limit argument to only fetch a given number of segments.",
    )
    simple_query: bool = Field(
        True,
        description="use the simple query syntax that is more user-friendly. If set to false, the full lucene syntax will be used, but syntax error could occurs (for advanced users only)",
    )


class SearchSegmentsProcessor(ProcessorBase):
    __doc__ = """Replace text of the input document by the similar segments."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        # supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)
        params: SearchSegmentsParameters = cast(SearchSegmentsParameters, parameters)
        kt_client = get_kt_client()
        if not kt_client.check_project(params.project_name):
            raise ValueError(f"The project {params.project_name} cannot be found")
        try:
            if not kt_client.check_resource():
                logger.error(f"Sherpa server {SHERPA_URL} is not accessible")
            for document in documents:
                altTexts = document.altTexts or []
                altTexts.append(
                    AltText(name=params.question_altText, text=document.text)
                )
                sentences = []
                text = ""
                hits: List[SegmentHit] = kt_client.get_segments(params.project_name, document.text, params.limit, params.simple_query)
                if hits:
                    for i, hit in enumerate(hits):
                        seg = hit.segment
                        htext = seg.text
                        htext = re.sub(r"\s+", " ", htext)
                        metadata = seg.metadata.additional_properties
                        metadata['documentIdentifier'] = seg.document_identifier
                        metadata['documentTitle'] = seg.document_title
                        date = metadata.get("versionCreated", None)
                        stext = f"{date} - {htext}"
                        sstart = len(text)
                        text += stext
                        send = len(text)
                        sentences.append(
                            Sentence(
                                start=sstart,
                                end=send,
                                metadata=metadata,
                            )
                        )
                        text += "\n\n"

                document.sentences = sentences
                document.metadata = None
                document.altTexts = altTexts
                document.sentences = sentences
                document.text = text
                document.annotations = None
                document.categories = None
        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SearchSegmentsParameters


@lru_cache(maxsize=None)
def get_kt_client():
    kt_client = KTClient(SHERPA_URL, SHERPA_USER, SHERPA_PWD)
    return kt_client
