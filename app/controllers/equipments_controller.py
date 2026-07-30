from app.schemas.equipment_schemas import EquipmentResponseSchema
from app.services import equipments_services
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_equipments(db_session: AsyncSession, page: int, page_size: int) -> list[EquipmentResponseSchema]:
    equipments = await equipments_services.get_all_equipments(db_session, page, page_size)
    
    
    return [EquipmentResponseSchema.model_validate(equipment) for equipment in equipments]