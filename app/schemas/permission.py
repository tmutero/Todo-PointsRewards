from pydantic import BaseModel, ConfigDict

class PermissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PermissionIn(PermissionBase):
    user_id: int
    role_id: int

class PermissionOut(PermissionBase):
    permission_id: int
    user_id: int
    role_id : int



