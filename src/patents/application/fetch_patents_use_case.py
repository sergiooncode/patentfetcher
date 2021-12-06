from src.patents.application.adapter.patent_acl_adapter import PatentAclAdapter
from src.patents.domain.patent_repository import PatentRepository


class FetchPatentsUseCase:
    def __init__(
        self,
        patent_acl_adapter: PatentAclAdapter,
        patent_repository: PatentRepository,
    ):
        self.__patent_acl_adapter: PatentAclAdapter = patent_acl_adapter
        self.__patent_repository: PatentRepository = patent_repository

    def execute(self, from_date: str, to_date: str):
        patents = self.__patent_acl_adapter.list_patents(
            from_date=from_date, to_date=to_date
        )

        self.__patent_repository.save(patents)
