from typing import Dict, List

from src.patents.application.adapter.patent_acl_adapter import PatentAclAdapter


class MockPatentAclAdapter(PatentAclAdapter):
    def __init__(self, patents: List[Dict[str, str]]):
        self.__patents = patents

    def list_patents(self, from_date: str, to_date: str, log_console_progress_bar=True):
        return self.__patents
