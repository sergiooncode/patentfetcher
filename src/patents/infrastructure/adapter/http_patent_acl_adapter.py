import json
import tempfile
from typing import List

import requests
from tqdm import tqdm

from src.patents.application.adapter.patent_acl_adapter import PatentAclAdapter
from src.patents.domain.patent import Patent

USPTO_API = "https://developer.uspto.gov/ibd-api/v1/application"
USPTO_API_PAGINATION_ITEM_NUMBER = 100
USPTO_API_PAGINATION_INFO = f"start=0&rows={USPTO_API_PAGINATION_ITEM_NUMBER}"
USPTO_API_TEXT_SEARCH_FLAG = "largeTextSearchFlag=N"
PATENT_RESPONSE_CHUNK_SIZE = 1024


class HttpPatentAclAdapter(PatentAclAdapter):
    def list_patents(
        self, from_date: str, to_date: str, log_console_progress_bar=True
    ) -> List[Patent]:
        url = (
            f"{USPTO_API}/grants?"
            f"grantFromDate={from_date}&"
            f"grantToDate={to_date}&"
            f"{USPTO_API_PAGINATION_INFO}&"
            f"{USPTO_API_TEXT_SEARCH_FLAG}"
        )
        response = requests.get(
            url,
            headers={"accept": "application/json"},
            stream=True,
        )
        response.raise_for_status()
        if log_console_progress_bar:
            temp_file = self.__create_temporary_file()
            self.__log_console_progress_bar(response, temp_file)
            self.__reset_temporary_file_cursor(temp_file)
            patents = json.loads(temp_file.read())
            temp_file.close()
        else:
            patents = json.loads(response.content.decode("utf-8"))

        return [
            Patent(
                patent_number=patent["patentNumber"],
                patent_application_number=patent["patentApplicationNumber"],
                assignee_entity_name=patent["assigneeEntityName"],
                filing_date=patent["filingDate"],
                grant_date=patent["grantDate"],
                invention_title=patent["inventionTitle"],
            )
            for patent in patents["results"]
        ]

    def __create_temporary_file(self):
        return tempfile.NamedTemporaryFile()

    def __reset_temporary_file_cursor(self, temp_file):
        temp_file.seek(0)

    def __log_console_progress_bar(self, response, temp_file):
        """
        The progress of fetching patents is simulated by writing the response content
        after fetching from USPTO API into a temporary file in chunks so what's actually
        logged is the progress of writing those chunks in the file, afterwards the temporary
        file is converted from json to dict and patents returned from that dict.
        :param response:
        :param temp_file:
        :return:
        """
        total_size_in_bytes = int(len(response.content))
        block_size = PATENT_RESPONSE_CHUNK_SIZE
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        for chunk in response.iter_content(chunk_size=block_size):
            temp_file.write(chunk)
            progress_bar.update(len(chunk))
