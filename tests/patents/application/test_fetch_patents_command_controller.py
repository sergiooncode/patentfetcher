from datetime import datetime

from src.app import app
from src.patents.application.fetch_patents_use_case import FetchPatentsUseCase
from src.patents.infrastructure.models import Patent as PatentModel
from src.patents.domain.patent import Patent
from src.patents.infrastructure.sqlalchemy_patent_repository import (
    SqlalchemyPatentRepository,
)
from tests.patents.application.mock_patent_acl_adapter import MockPatentAclAdapter


def test_fetch_patents_command_fetches_and_saves_patents():
    patents_fixture = [
        Patent(
            patent_number="09532583",
            patent_application_number="US13650756",
            assignee_entity_name="LAND O'LAKES, INC.",
            filing_date="10-12-2012",
            grant_date="01-03-2017",
            invention_title="Brown butter and systems and methods for the continuous production thereof",
        ),
        Patent(
            patent_number="09532581",
            patent_application_number="US14546114",
            assignee_entity_name="Meyn Food Processing Technology B.V.",
            filing_date="11-18-2014",
            grant_date="05-03-2017",
            invention_title="Apparatus and method for removing the entrails from the abdominal cavity of poultry",
        )
    ]
    with app.app_context():
        service = FetchPatentsUseCase(
            patent_acl_adapter=MockPatentAclAdapter(patents=patents_fixture),
            patent_repository=SqlalchemyPatentRepository(),
        )
        service.execute(from_date="01-03-2017", to_date="05-03-2017")

        saved_patents = PatentModel.query.all()

        assert 2 == len(saved_patents)
        assert patents_fixture[0].patent_number == saved_patents[0].patent_number
        assert patents_fixture[0].patent_application_number == saved_patents[0].patent_application_number
        assert patents_fixture[0].assignee_entity_name == saved_patents[0].assignee_entity_name
        assert datetime.strptime(patents_fixture[0].filing_date, "%m-%d-%Y") == saved_patents[0].filing_date
        assert datetime.strptime(patents_fixture[0].grant_date, "%m-%d-%Y") == saved_patents[0].grant_date
        assert patents_fixture[0].invention_title == saved_patents[0].invention_title

        assert patents_fixture[1].patent_number == saved_patents[1].patent_number
        assert patents_fixture[1].patent_application_number == saved_patents[1].patent_application_number
        assert patents_fixture[1].assignee_entity_name == saved_patents[1].assignee_entity_name
        assert datetime.strptime(patents_fixture[1].filing_date, "%m-%d-%Y") == saved_patents[1].filing_date
        assert datetime.strptime(patents_fixture[1].grant_date, "%m-%d-%Y") == saved_patents[1].grant_date
        assert patents_fixture[1].invention_title == saved_patents[1].invention_title


