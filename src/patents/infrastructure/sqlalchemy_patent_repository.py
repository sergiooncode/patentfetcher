import dataclasses
from typing import List

from src.patents.domain.patent_repository import PatentRepository
from src.patents.infrastructure.models import Patent as PatentModel
from src.patents.domain.patent import Patent


class SqlalchemyPatentRepository(PatentRepository):
    def save(self, patents: List[Patent]) -> None:
        patent_objects = [
            PatentModel(**dataclasses.asdict(patent)) for patent in patents
        ]
        PatentModel.bulk_save(patent_objects)
