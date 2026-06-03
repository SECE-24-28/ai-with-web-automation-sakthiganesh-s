from fastapi import APIRouter, HTTPException

from  services import recommendation_service

router = APIRouter()


@router.get("/recommendation/{disease_name}")
async def get_recommendation(disease_name: str):
    info = recommendation_service.get_disease_info(disease_name)
    if not info:
        raise HTTPException(status_code=404, detail="Disease information not found")
    return {**info, **recommendation_service.build_plant_summary(info)}
