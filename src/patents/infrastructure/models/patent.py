from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.patents.infrastructure.models import session


class Patent(session.Model):
    __tablename__ = "patent"

    id = Column(Integer, primary_key=True)
    patent_number = Column(String(8), unique=False, nullable=False)
    patent_application_number = Column(String(10), unique=False, nullable=False)
    assignee_entity_name = Column(String(150), unique=False, nullable=True)
    filing_date = Column(DateTime(timezone=False))
    grant_date = Column(DateTime(timezone=False))
    invention_title = Column(String(200), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<Patent(id={self.id}, patent_number={self.patent_number}, "
            f"patent_application_number={self.patent_application_number}, "
            f"assignee_entity_name={self.assignee_entity_name}, "
            f"filing_date={self.filing_date}, grant_date={self.grant_date}, "
            f"invention_title={self.invention_title}, created_at={self.created_at})>"
        )
