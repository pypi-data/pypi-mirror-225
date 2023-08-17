from pydantic import BaseModel


class MouseRecord(BaseModel):

    id: str
    labtracks_id: str
    age: int
    state: str
    status: int  # 0 = not started, 1 = started, 2 = finished
    created_at: int
    updated_at: int
