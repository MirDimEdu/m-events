from pydantic import BaseModel


class CreateEvent(BaseModel):
    title: str
    description: str
    location: str
    event_date: str
