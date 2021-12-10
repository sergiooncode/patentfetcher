from unittest.mock import patch, MagicMock

from requests.exceptions import HTTPError

from src.patents.domain.patent import Patent
from src.patents.infrastructure.adapter.http_patent_acl_adapter import (
    HttpPatentAclAdapter,
)


def test_patent_api_returns_patent_data_and_status_200():
    response_content = (
        b'{"results": [{"inventionSubjectMatterCategory": "utility", "patentApplicationNumber": "US14398026", '
        b'"filingDate": "05-02-2013", "mainCPCSymbolText": "A01B63/10", '
        b'"furtherCPCSymbolArrayText": ["A01B61/046", "A01D41/14", "A01D41/145", "A01D69/03", "A01D2101/00"], '
        b'"inventorNameArrayText": ["Lohrentz Randy", "Magisson Emmanuel R."], '
        b'"abstractText": ["A harvesting header for use with a crop harvesting machine has a feederhouse '
        b'least one hydraulic ram."], "assigneeEntityName": "AGCO Corporation", '
        b'"assigneePostalAddressText": "Duluth, US", "inventionTitle": "Variable precharge accumulator '
        b'for agricultural header", '
        b'"filelocationURI": "https://dh-opendata.s3.amazonaws.com/grant_pdf/grant_pdf_20170103/'
        b'P20170103-20170103/09/532/497/09532497.pdf", '
        b'"archiveURI": "https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/2017/'
        b'ipgb20170103_wk01.zip", '
        b'"claimText": ["1. A harvesting header and feederhouse for use with a crop harvesting machine  , '
        b'header frame providing structural support for the harvesting header."], '
        b'"grantDocumentIdentifier": "US09532497B2", "grantDate": "01-03-2017", "patentNumber": "09532497"}], '
        b'"recordTotalQuantity": 200}'
    )
    with patch(
        "src.patents.infrastructure.adapter.http_patent_acl_adapter.requests"
    ) as mock_requests:
        mock_response = MagicMock()
        mock_response.content = response_content
        mock_response.status_code = 200
        mock_response.iter_content.return_value = (
            response_content[: len(response_content) // 2],
            response_content[len(response_content) // 2 :],
        )
        mock_requests.get.return_value = mock_response
        patents = HttpPatentAclAdapter().list_patents(
            from_date="05-02-2013", to_date="15-02-2013"
        )

        assert [
            Patent(
                patent_number="09532497",
                patent_application_number="US14398026",
                assignee_entity_name="AGCO Corporation",
                filing_date="05-02-2013",
                grant_date="01-03-2017",
                invention_title="Variable precharge accumulator for agricultural header",
            ),
        ] == patents


def test_patent_api_returns_exception_with_status_404():
    with patch(
        "src.patents.infrastructure.adapter.http_patent_acl_adapter.requests"
    ) as mock_requests:
        mock_response = MagicMock(side_effect=HTTPError)
        mock_response.status_code = 404
        mock_requests.get.side_effect = mock_response

        try:
            HttpPatentAclAdapter().list_patents(
                from_date="05-02-2013", to_date="15-02-2013"
            )
        except Exception as e:
            assert isinstance(e, HTTPError)
