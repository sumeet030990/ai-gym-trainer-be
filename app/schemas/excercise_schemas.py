
import uuid

from pydantic import BaseModel, ConfigDict

from db.schemas.exercises import LEVEL

class Muscle(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  name: str

class ExerciseSchema(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  name: str
  description: str | None = None
  excercise_level: LEVEL | None = None
  equipment_id: uuid.UUID | None = None
  muscle: Muscle | None = None