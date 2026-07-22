from __future__ import annotations

from abc import ABC, abstractmethod

from .models import DocRef, DownloadedDoc, SourceAssessment, SourceConfig, SourceTarget


class SourceAdapter(ABC):
    name: str

    @abstractmethod
    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        raise NotImplementedError

    @abstractmethod
    def discover(self, config: SourceConfig) -> list[DocRef]:
        raise NotImplementedError

    @abstractmethod
    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        raise NotImplementedError
