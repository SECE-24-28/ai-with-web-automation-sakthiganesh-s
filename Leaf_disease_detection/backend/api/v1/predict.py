from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from  services import recommendation_service
from  schemas.prediction_schema import PredictionResponse
from  services import image_service, model_service

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    try:
        arr = await image_service.preprocess_image(image, model_service.get_input_size())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {e}")

    predicted_class, confidence = model_service.predict(arr)

    return PredictionResponse(predicted_class=predicted_class, confidence=confidence)


@router.post("/analyze")
async def analyze(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    arr = await image_service.preprocess_image(image, model_service.get_input_size())
    predicted_class, confidence = model_service.predict(arr)
    info = recommendation_service.get_disease_info(predicted_class)

    if info:
        info = {**info, **recommendation_service.build_plant_summary(info)}

    return JSONResponse({
        "predicted_class": predicted_class,
        "confidence": confidence,
        "disease_info": info,
    })
