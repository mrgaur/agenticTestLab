from threading import Lock
from app.models import LoanDecisionResponse

class InMemoryDecisionRepository:
    def __init__(self):
        self._items: dict[str, LoanDecisionResponse] = {}
        self._lock = Lock()

    def save(self, item: LoanDecisionResponse) -> None:
        with self._lock:
            self._items[item.case_id] = item

    def get(self, case_id: str) -> LoanDecisionResponse | None:
        with self._lock:
            return self._items.get(case_id)

decision_repository = InMemoryDecisionRepository()
