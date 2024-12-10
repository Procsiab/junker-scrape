from typing import Optional
from datetime import datetime


class CollectionBase(dict):  # inherit from dict to enable JSON serialization
    def __init__(
        self,
        date: datetime.date,
        icon: Optional[str] = None,
    ):
        dict.__init__(self, date=date.isoformat(), icon=icon)
        self._date = date  # store date also as python date object

    @property
    def date(self):
        return self._date

    @property
    def daysTo(self):
        return (self._date - datetime.datetime.now().date()).days

    @property
    def icon(self):
        return self["icon"]

    def set_icon(self, icon: str):
        self["icon"] = icon

    def set_date(self, date: datetime.date):
        self._date = date
        self["date"] = date.isoformat()


class Collection(CollectionBase):
    def __init__(
        self,
        date: datetime.date,
        t: str,
        icon: Optional[str] = None,
    ):
        CollectionBase.__init__(self, date=date, icon=icon)
        self["type"] = t

    @property
    def type(self) -> str:
        return self["type"]

    def set_type(self, t: str):
        self["type"] = t

    def __repr__(self):
        return f"Collection{{date={self.date}, type={self.type}}}"


class AreaNotFound(Exception):
    def __init__(self, areas: list[tuple[str, int]]):
        self.areas = areas
        super().__init__("Area not found")


class AreaRequired(AreaNotFound):
    ...
