import json
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document

from pyprocessors_similar_segments.similar_segments import (
    SimilarSegmentsProcessor,
    SimilarSegmentsParameters,
)


def test_similar_segments_basic():
    model = SimilarSegmentsProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == SimilarSegmentsParameters


# noqa: E501
@pytest.mark.skip(reason="Not a test")
def test_similar_segments():
    testdir = Path(__file__).parent
    parameters = SimilarSegmentsParameters(
        project_name="grouperf_paye", limit=5, certainty=0.5
    )
    processor = SimilarSegmentsProcessor()
    docs = [Document(text="Puis-je toucher le chomage après un abandon de poste")]
    docs = processor.process(docs, parameters)
    doc = docs[0]
    assert len(doc.altTexts) == 1
    result = Path(testdir, "data/question_segments.json")
    with result.open("w") as fout:
        json.dump(doc.dict(), fout, indent=2)
    # noqa: E501
