from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class BaseEvent:
    id: UUID = uuid4()
    created_at: datetime = datetime.now()
    version: str = "1.0"
    payload: dict = None


