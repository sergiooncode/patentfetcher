from abc import ABC, abstractmethod


class PatentAclAdapter(ABC):
    @abstractmethod
    def list_patents(self, from_date: str, to_date: str, log_console_progress_bar=True):
        pass
