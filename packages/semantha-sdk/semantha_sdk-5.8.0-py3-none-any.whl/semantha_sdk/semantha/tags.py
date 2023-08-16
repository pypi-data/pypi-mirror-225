from semantha_sdk import SemanthaAPI
from semantha_sdk.semantha.library import LibraryDocument
from semantha_sdk.semantha import SemanthaDomain


class Tags:
    def __init__(
            self,
            domain: SemanthaDomain
    ):
        self.__domain = domain

    def get_all(self) -> list[str]:
        return self.__tags.get()

    def get_documents_with_tag(self, tag: str) -> list[LibraryDocument]:
        return [
            LibraryDocument.from_document_id(
                domain=self.__domain,
                document_id=doc.id
            ) for doc in self.__domain.domain().tags(tagname=tag).referencedocuments.get()
        ]
