import json
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document

from pyprocessors_search_segments.search_segments import (
    SearchSegmentsProcessor,
    SearchSegmentsParameters,
)


def test_search_segments_basic():
    model = SearchSegmentsProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == SearchSegmentsParameters


# noqa: E501
@pytest.mark.skip(reason="Not a test")
def test_search_segments():
    testdir = Path(__file__).parent
    parameters = SearchSegmentsParameters(
        project_name="bourse_2018_2022", limit=20, simple_query=False
    )
    processor = SearchSegmentsProcessor()
    docs = [Document(text="Cours de bourse de Sodexo")]
    docs = processor.process(docs, parameters)
    doc = docs[0]
    assert len(doc.altTexts) == 1
    result = Path(testdir, "data/question_segments.json")
    with result.open("w") as fout:
        json.dump(doc.dict(), fout, indent=2)
    # noqa: E501
