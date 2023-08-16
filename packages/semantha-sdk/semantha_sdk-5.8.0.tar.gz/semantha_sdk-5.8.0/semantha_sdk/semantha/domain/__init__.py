from semantha_sdk import SemanthaAPI
from semantha_sdk.api.documents import DocumentsEndpoint
from semantha_sdk.api.domain import DomainEndpoint
from semantha_sdk.api.referencedocuments import ReferencedocumentsEndpoint
from semantha_sdk.api.references import ReferencesEndpoint
from semantha_sdk.model import Domain
from semantha_sdk.model.settings import Settings
from semantha_sdk.semantha.domain.settings import DomainSettings


class SemanthaDomain:
    __api: SemanthaAPI
    __domain: DomainEndpoint

    __reference_documents: ReferencedocumentsEndpoint
    __references: ReferencesEndpoint
    __documents: DocumentsEndpoint

    __id: str
    __name: str

    def __init__(self, api: SemanthaAPI, domain: Domain):
        self.__api = api
        self.__domain = self.__api.domains(domainname=domain.name)
        self.__id = domain.id
        self.__name = domain.name

        self.__reference_documents = self.__domain.referencedocuments
        self.__references = self.__domain.references
        self.__documents = self.__domain.documents

    def api(self):
        return self.__api

    def domain(self):
        return self.__domain

    def name(self):
        return self.__name

    def reference_documents(self):
        return self.__reference_documents

    def reference_document(self, id: str):
        return self.__reference_documents(id)

    def references(self):
        return self.__references

    def documents(self):
        return self.__documents

    def change_model(self, model_id: str):
        settings = self.__domain.settings.patch(Settings(similarity_model_id=str(model_id)))
        return int(settings.similarity_model_id)

    def settings(self):
        return DomainSettings()

    @classmethod
    def from_domain(cls, api: SemanthaAPI, domain: Domain):
        return SemanthaDomain(
            api=api,
            domain=domain
        )