from abc import ABC, abstractmethod


class PatentRepository(ABC):
    @abstractmethod
    def save(self) -> None:
        pass
