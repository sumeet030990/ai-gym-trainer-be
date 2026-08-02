import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.equipment_schemas import EquipmentResponseSchema

class AssignGymEquipmentRequest(BaseModel):
    equipments: list[str]

class GymEquipmentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    gym_id: uuid.UUID
    equipment_id: uuid.UUID
    is_active: bool
    equipment: EquipmentResponseSchema

class GymEquipmentAssignResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    gym_id: uuid.UUID
    equipment_id: uuid.UUID
    is_active: bool