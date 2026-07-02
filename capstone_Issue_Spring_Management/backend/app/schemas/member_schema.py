from pydantic import BaseModel
from pydantic import EmailStr


class ProjectMemberRequest(BaseModel):

    email: EmailStr