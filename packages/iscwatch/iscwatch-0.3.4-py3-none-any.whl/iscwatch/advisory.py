import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Advisory:
    """Encapsulate an Intel Product Security Center Advisory"""

    title: str
    link: str
    id: str
    updated: datetime.date
    released: datetime.date
