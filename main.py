from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal, Annotated, List
from pydantic import BaseModel, Field

# File Uploaded:
df = pd.read_csv('blood_cell_anomaly_detection.csv')
current_threshold = 0.10  # Threshold ko adjust kar ke 0.10 kar diya gaya hai

# import model
with open('Blood-Cell-Anomaly-Detection.pkl', 'rb') as f:
    model = joblib.load(f)

with open('Blood-Cell-Anomaly-Detection-Scaler.pkl', 'rb') as f:
    scaler = joblib.load(f)

with open('Blood-Cell-Anomaly-Detection-Encoded.pkl', 'rb') as f:
    encoded = joblib.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model to validate incoming data
class Userinput(BaseModel):
    cell_type: Annotated[Literal[
        'Artefact', 'Basophil', 'Blast_Cell', 'Elliptocyte', 'Eosinophil', 'Hypersegmented_Neutrophil', 'Lymphocyte', 'Monocyte', 'Neutrophil', 'Normal_RBC', 'Platelet', 'Prolymphocyte', 'Reactive_Lymphocyte', 'Schistocyte', 'Sickle_Cell', 'Smudge_Cell', 'Spherocyte', 'Target_Cell', 'Toxic_Granulation'], Field(
        ..., description='Type of the Blood cell')]
    cell_diameter_um: Annotated[float, Field(..., gt=0, description='Diameter of cell in micrometers')]
    nucleus_area_pct: Annotated[
        float, Field(..., ge=0, le=100, description='Percentage of cell area occupied by nucleus')]
    chromatin_density: Annotated[
        float, Field(..., ge=0, description='Density of Chromatin material inside the nucleus')]
    cytoplasm_ratio: Annotated[float, Field(..., ge=0, description='Ratio of Cytoplasm to total area cell area')]
    circularity: Annotated[float, Field(..., ge=0, le=1, description='How Circular the shape of cell')]
    eccentricity: Annotated[float, Field(..., ge=0, le=1, description='How elongated/stretched the cell shape is')]
    granularity_score: Annotated[float, Field(..., ge=0, description='Amount of granular texture on cell surface')]
    lobularity_score: Annotated[float, Field(..., ge=0, description='Degree of Nucleus segmentation into Lobes')]
    membrane_smoothness: Annotated[
        float, Field(..., ge=0, le=1, description='Smoothness of the cell membrane boundary')]
    cell_area_px: Annotated[int, Field(..., gt=0, description='Cell Area in pixels')]
    perimeter_px: Annotated[int, Field(..., gt=0, description='Perimeter in pixels')]
    mean_r: Annotated[int, Field(..., ge=0, le=255, description='Average Red Color Channel Value')]
    mean_g: Annotated[int, Field(..., ge=0, le=255, description='Average Green Color Channel Value')]
    mean_b: Annotated[int, Field(..., ge=0, le=255, description='Average Blue Color Channel Value')]
    stain_intensity: Annotated[float, Field(..., ge=0, description='Intensity of the lab staining dye applied')]


class BulkInput(BaseModel):
    rows: List[Userinput]


@app.post("/predict")
def predict_anomaly(data: Userinput):
    global current_threshold
    input_df = pd.DataFrame([data.dict()])

    input_encoded = pd.get_dummies(input_df, columns=['cell_type'])
    for col in encoded:
        if col not in input_encoded.columns:
            input_encoded[col] = 0

    input_encoded = input_encoded[encoded]
    input_scaled = scaler.transform(input_encoded)

    score = -model.decision_function(input_scaled)[0]
    result = 'Anomaly' if score > current_threshold else "Normal"
    return JSONResponse(status_code=200, content={'Prediction': result, 'Score': float(score)})


@app.post("/predict-bulk")
def predict_bulk(data: BulkInput):
    global current_threshold
    input_df = pd.DataFrame([row.dict() for row in data.rows])

    input_encoded = pd.get_dummies(input_df, columns=['cell_type'])
    for col in encoded:
        if col not in input_encoded.columns:
            input_encoded[col] = 0

    input_encoded = input_encoded[encoded]
    input_scaled = scaler.transform(input_encoded)

    scores = -model.decision_function(input_scaled)

    results = []
    for score in scores:
        prediction = 'Anomaly' if score > current_threshold else "Normal"
        results.append({'Prediction': prediction, 'Score': float(score)})

    return JSONResponse(status_code=200, content={'results': results})


@app.get("/set-threshold")
def set_threshold(value: float):
    global current_threshold
    current_threshold = value
    return {"message": "Threshold Updated", "threshold": current_threshold}


@app.get("/get-threshold")
def get_threshold():
    global current_threshold
    return {"current_threshold": current_threshold}


@app.get("/insights")
def get_insights():
    global df
    total_records = len(df) if df is not None else 0
    cell_distribution = df['cell_type'].value_counts().to_dict() if df is not None and 'cell_type' in df.columns else {}
    return {
        "total_records": total_records,
        "cell_distribution": cell_distribution
    }


# ------------------ STATIC FRONTEND (Sabse Aakhir Mein) ------------------
app.mount("/", StaticFiles(directory="static", html=True), name="static")
