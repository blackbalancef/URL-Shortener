from pydantic import BaseModel


class Statistics(BaseModel):
    visits_by_date: dict[str, int]
    visits_by_hour: dict[str, int]
    total_visits: int
