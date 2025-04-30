from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
import base64
from backend.src.utils.process_classes import process_classes
from backend.src.predict.predict import Predict
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    model: str = Form(...)
):
    try:
        # Read image
        image_data = await image.read()
        image_obj = Image.open(io.BytesIO(image_data))

        # TODO: Replace this with actual YOLO inference logic
        # For now, return the uploaded image as-is

        print("PROMPT:", prompt)
        user_classes = process_classes(prompt)
        print("USER CLASSES:", user_classes)
        print("MODEL NAME:", model)
        predictor = Predict(model, image_obj, user_classes)
        results = predictor.predict()

        # buf = io.BytesIO()
        # results[0].save(buf, format="PNG")

        annotated = results[0].plot(labels=False)  # this returns a NumPy array

        # Convert to PIL Image
        if isinstance(annotated, np.ndarray):
            annotated = Image.fromarray(annotated)

        buf = io.BytesIO()
        annotated.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        return JSONResponse({"success": True, "image": img_b64})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})
