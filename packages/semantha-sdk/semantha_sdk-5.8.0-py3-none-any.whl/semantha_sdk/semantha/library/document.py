from collections import defaultdict
from typing import Optional, Callable

import pandas
from pandas import DataFrame

from semantha_sdk import SemanthaAPI
from semantha_sdk.model import Document, Entity, DocumentInformation, Paragraph, Reference
from semantha_sdk.semantha import SemanthaDomain
from semantha_sdk.semantha.files import _to_text_file
from semantha_sdk.semantha.library.reference import LibraryReference


class LibraryDocument:
    def __init__(
            self,
            domain: SemanthaDomain,
            document_id: Optional[str] = None,
            document: Optional[DocumentInformation] = None
    ):
        self.__api = domain.api()
        self.__domain = domain
        self.__domain_name = domain.name()

        if document_id is None and document is None:
            raise Exception("either document or document_id needs to be set")

        if document_id is None:
            document_id = document.id

        self.__document_id = document_id
        self.__reference_documents = self.__domain.reference_documents()
        self.__reference_document = self.__domain.reference_document(document_id)
        self.__references = self.__domain.references()

    @classmethod
    def from_document_id(cls, domain: SemanthaDomain, document_id: str):
        return cls(domain, document_id=document_id)

    @classmethod
    def from_document(cls, domain: SemanthaDomain, document: DocumentInformation):
        return cls(domain, document=document)

    @classmethod
    def from_reference(cls, domain: SemanthaDomain, reference: Reference):
        return cls.from_document_id(domain, document_id=reference.document_id)

    def get(self):
        return self.__reference_document.get()

    def id(self):
        return self.__reference_document.get().id

    def domain(self):
        return self.__domain

    def name(self):
        return self.__reference_document.get().name

    def document_class(self) -> Entity:
        return self.__reference_document.get().document_class

    def paragraph_by_id(self, paragraph_id: str) -> str:
        return self.__reference_document.paragraphs(id=paragraph_id).get().text

    def tags(self) -> list[str]:
        """
        Returns all tags of this document (including derived)
        :return: all tags
        """
        doc = self.__reference_document.get()
        tags = doc.tags
        derived_tags = doc.derived_tags
        return tags + derived_tags

    def add_tag(self, tag: str):
        """
        Adds a tag to this library entry
        :param tag: the tag to add
        :return: the document with the tag added
        """
        doc = self.__reference_document.get()
        return self.__reference_document.patch(DocumentInformation(
            tags=doc.tags + [tag]
        ))

    # TODO: revisit this use case
    # def references(self, tags: Optional[list[str]]=None):
    #     if tags is None:
    #         tags = []
    #
    #     doc = self.__reference_document.get()
    #     doc = self.__api.bulk.domains(self.__domain_name).references.post([doc], tags=tags, similaritythreshold=0.5)[0]
    #
    #     return [LibraryReference.from_reference(self.__api, self.__domain_name, ref) for ref in doc.references]

    # # TODO: filter keys?
    # def references_as_dataframe(self):
    #     references = self.references()
    #
    #     docs = [ref.get() for ref in references]
    #
    #     return DataFrame.from_records([doc.__dict__ for doc in docs])


    def delete(self):
        self.__reference_document.delete()

    def for_each_paragraph(self, fn: Callable[[int, Paragraph], None]):
        """
        Executes the given callable for every paragraph in the document
        :param fn: the lambda/function to be called
        """
        doc = self.__reference_document.get()

        for idx, page in enumerate(doc.pages):
            if page.contents is None:
                continue

            for content in page.contents:
                if content.paragraphs is None:
                    break

                for paragraph in content.paragraphs:
                    fn(idx, paragraph)


    def collect_paragraph_text(self):
        """
        Iterates over each paragraph and collects the paragraph texts in a list
        :return: the list of paragraph texts
        """
        texts = []
        self.for_each_paragraph(lambda page, paragraph: texts.append(paragraph.text))
        return texts

    def text(self):
        texts = self.collect_paragraph_text()
        return "\n".join(texts)

    def for_each_paragraph_reference(self, fn: Callable[[int, Paragraph, Reference], None]):
        """
        Executes the given callable for each paragraph reference of this library entry
        :param fn: the lambda/function to be called for each reference
        """
        def for_each_ref(page: int, paragraph: Paragraph):
            if paragraph.references is None:
                return

            for ref in paragraph.references:
                fn(page, paragraph, ref)

        self.for_each_paragraph(for_each_ref)


    # TODO: revisit later
    # def matches_per_page(self, filter_tags: list[str]):
    #     doc = self.__reference_document.get()
    #
    #     matches = defaultdict(lambda: defaultdict(int))
    #     tags_cache: dict[str, list[str]] = {}
    #
    #     def handle_ref(page_idx: int, _paragraph: Paragraph, ref: Reference):
    #         if ref.document_id in tags_cache:
    #             tags = tags_cache[ref.document_id]
    #         else:
    #             tags = self.__domain.referencedocuments(ref.document_id).get().tags
    #             tags_cache[ref.document_id] = tags
    #
    #         for tag in tags:
    #             matches[str(page_idx)][tag] += 1
    #
    #     self.for_each_paragraph_reference(handle_ref)
    #
    #     rows = []
    #
    #     for page, tags in matches.items():
    #         for tag, count in tags.items():
    #             if tag in filter_tags or len(filter_tags) == 0:
    #                 page_num = str(int(page) + 1)
    #                 rows.append([page_num, tag, count])
    #
    #     return pandas.DataFrame.from_records(
    #         rows,
    #         columns=["Page", "Topic", "References"]
    #     )