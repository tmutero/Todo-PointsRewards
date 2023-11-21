from pydantic import BaseModel, ConfigDict

class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoleIn(RoleBase):
    name: str | None


class RoleOut(RoleBase):
    id: int
    name: str | None



