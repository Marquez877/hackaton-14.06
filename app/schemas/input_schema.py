from pydantic import BaseModel

class BusinessInput(BaseModel):
    investment: int
    skills: str
    customers: str
    mobility: str
    competitors: str
    problems: str