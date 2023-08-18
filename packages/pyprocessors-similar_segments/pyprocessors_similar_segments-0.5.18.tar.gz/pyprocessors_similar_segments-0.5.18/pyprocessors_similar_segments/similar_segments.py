import os
import re
from functools import lru_cache
from typing import List, cast, Type

import requests
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Sentence, AltText

VECTORSTORE_URL = os.getenv("VECTORSTORE_URL", "http://localhost:10011")


class SimilarSegmentsParameters(ProcessorParameters):
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
    certainty: float = Field(
        0.5,
        description="use the limit argument to only fetch a given number of segments.",
    )


class SimilarSegmentsProcessor(ProcessorBase):
    __doc__ = """Replace text of the input document by the similar segments."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        # supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)
        params: SimilarSegmentsParameters = cast(SimilarSegmentsParameters, parameters)
        vector_session = get_vector_session()
        try:
            for document in documents:
                altTexts = document.altTexts or []
                altTexts.append(
                    AltText(name=params.question_altText, text=document.text)
                )
                sentences = []
                text = ""
                resp = vector_session.post(
                    VECTORSTORE_URL + f"/projects/{params.project_name}/segments/_near",
                    params={"limit": params.limit, "certainty": params.certainty},
                    json={"text": document.text},
                    timeout=(30, 300),
                )
                if resp.ok:
                    hits = resp.json()
                    for i, hit in enumerate(hits):
                        htext = hit["hit"]["text"]
                        htext = re.sub(r"\s+", " ", htext)
                        stext = f"{i + 1}. {htext}"
                        sstart = len(text)
                        text += stext
                        send = len(text)
                        sentences.append(
                            Sentence(
                                start=sstart,
                                end=send,
                                metadata={
                                    "documentIdentifier": hit["hit"][
                                        "documentIdentifier"
                                    ],
                                    "documentTitle": hit["hit"]["documentTitle"],
                                },
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
        return SimilarSegmentsParameters


@lru_cache(maxsize=None)
def get_vector_session():
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )
    return session
