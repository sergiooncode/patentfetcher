from dataclasses import dataclass
from datetime import datetime


@dataclass
class Patent:
    patent_number: str
    patent_application_number: str
    assignee_entity_name: str
    filing_date: datetime
    grant_date: datetime
    invention_title: str
