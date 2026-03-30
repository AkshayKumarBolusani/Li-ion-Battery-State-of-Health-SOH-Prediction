"""
FastAPI Inference Server for Battery SOH Prediction

Endpoints:
- POST /predict: Predict SOH from cycle data
- POST /predict/batch: Batch prediction
- GET /health: Health check
- GET /model/info: Model information
- GET /disposal/ranges: SOH bands with disposal and analysis precautions
- GET /disposal/guidance/{soh}: Guidance for a specific SOH value
"""

import os
import sys
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import numpy as np

from api.disposal_guidance import all_bands_public, guidance_dict

# Add project to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
except Exception:
    # Keep running even if python-dotenv is unavailable.
    pass

# Import model components (lazy loading)
model = None
scaler = None
embedder = None
feature_cols = None
openai_client = None
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


# ============== Pydantic Models ==============

class CycleData(BaseModel):
    """Single cycle data for prediction."""
    voltage: List[float] = Field(..., min_items=10, description="Voltage measurements (V)")
    current: List[float] = Field(..., min_items=10, description="Current measurements (A)")
    temperature: Optional[List[float]] = Field(None, description="Temperature measurements (C)")
    battery_id: Optional[str] = Field(None, description="Battery identifier")
    cycle_number: Optional[int] = Field(None, description="Cycle number")


class FeatureData(BaseModel):
    """Pre-extracted features for prediction."""
    voltage_mean: float
    voltage_std: float
    voltage_min: float
    voltage_max: float
    voltage_range: float
    current_mean: float
    current_std: float
    capacity: float
    discharge_time: float
    temp_mean: Optional[float] = 25.0
    temp_max: Optional[float] = 25.0
    temp_delta: Optional[float] = 0.0
    temp_std: Optional[float] = 0.0
    ica_peak_voltage: Optional[float] = 0.0
    ica_peak_magnitude: Optional[float] = 0.0
    ica_mean: Optional[float] = 0.0
    ica_std: Optional[float] = 0.0
    dcir: Optional[float] = 0.0


class PredictionRequest(BaseModel):
    """Request for single prediction."""
    cycle_data: Optional[CycleData] = None
    features: Optional[FeatureData] = None
    include_explanation: bool = False


class BatchPredictionRequest(BaseModel):
    """Request for batch prediction."""
    cycles: List[CycleData]
    include_explanation: bool = False


class DisposalGuidanceResponse(BaseModel):
    """SOH-band disposal routes, lab/field analysis precautions, and transport/storage notes."""
    band_id: str
    label: str
    soh_min: float
    soh_max: float
    summary: str
    disposal_methods: List[str]
    analysis_precautions: List[str]
    transport_storage_precautions: List[str]
    is_low_soh: bool = Field(
        ...,
        description="True when SOH is below 50% — stricter recycling and testing precautions apply.",
    )


class PredictionResponse(BaseModel):
    """Single prediction response."""
    soh: float = Field(..., description="Predicted State of Health (%)")
    confidence: Optional[float] = Field(None, description="Prediction confidence")
    explanation: Optional[str] = Field(None, description="Human-readable explanation")
    recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations")
    llm_recommendation: Optional[str] = Field(None, description="OpenAI-generated recommendation summary")
    disposal_guidance: Optional[DisposalGuidanceResponse] = Field(
        None,
        description="Disposal options, analysis precautions, and transport notes for this SOH band",
    )
    processing_time_ms: float
    battery_id: Optional[str] = None
    cycle_number: Optional[int] = None


class BatchPredictionResponse(BaseModel):
    """Batch prediction response."""
    predictions: List[PredictionResponse]
    total_processing_time_ms: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    timestamp: str
    version: str


class ModelInfoResponse(BaseModel):
    """Model information response."""
    model_type: str
    features_used: List[str]
    training_dataset: str
    metrics: dict
    version: str


# ============== FastAPI App ==============

app = FastAPI(
    title="Battery SOH Prediction API",
    description="Predict Li-ion battery State of Health using physics-guided features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Model Loading ==============

def load_model():
    """Load the trained model and preprocessors."""
    global model, scaler, feature_cols
    
    import pickle
    from sklearn.linear_model import Ridge
    
    model_path = os.path.join(PROJECT_ROOT, 'models', 'best_model.pkl')
    scaler_path = os.path.join(PROJECT_ROOT, 'models', 'scaler.pkl')
    feature_cols_path = os.path.join(PROJECT_ROOT, 'models', 'feature_cols.pkl')
    
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"✓ Loaded model from {model_path}")
    else:
        # Create default model for demo
        print("⚠️ No saved model found, using default Ridge")
        model = Ridge(alpha=1.0)
        # Note: Will need to be trained before use
    
    if os.path.exists(scaler_path):
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        print(f"✓ Loaded scaler from {scaler_path}")
    else:
        scaler = None
        print("⚠️ No scaler found, using raw features")
    
    if os.path.exists(feature_cols_path):
        with open(feature_cols_path, 'rb') as f:
            feature_cols = pickle.load(f)
        print(f"✓ Loaded feature columns: {len(feature_cols)} features")
    else:
        # Default feature order if not saved
        feature_cols = [
            'voltage_mean', 'voltage_std', 'voltage_min', 'voltage_max', 'voltage_range',
            'current_mean', 'current_std', 'capacity', 'discharge_time',
            'temp_mean', 'temp_max', 'temp_delta', 'temp_std',
            'ica_peak_voltage', 'ica_peak_magnitude', 'ica_mean', 'ica_std', 'dcir'
        ]
        print(f"⚠️ No feature_cols.pkl found, using defaults: {len(feature_cols)} features")
    
    return model is not None


def initialize_openai_client() -> bool:
    """Initialize OpenAI client from environment variables.

    Returns:
        True if OpenAI client is ready, otherwise False.
    """
    global openai_client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ℹ️ OPENAI_API_KEY not set. Using rule-based recommendations only.")
        openai_client = None
        return False

    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=api_key)
        print(f"✓ OpenAI client initialized ({openai_model})")
        return True
    except Exception as exc:
        print(f"⚠️ OpenAI client init failed: {exc}. Using rule-based recommendations.")
        openai_client = None
        return False


def extract_features_from_cycle(cycle: CycleData) -> dict:
    """Extract features from raw cycle data."""
    voltage = np.array(cycle.voltage)
    current = np.array(cycle.current)
    
    if cycle.temperature:
        temperature = np.array(cycle.temperature)
    else:
        temperature = np.ones(len(voltage)) * 25.0
    
    # Time estimation (assuming uniform sampling)
    time = np.linspace(0, len(voltage), len(voltage))
    
    # Compute features
    features = {
        'voltage_mean': float(np.mean(voltage)),
        'voltage_std': float(np.std(voltage)),
        'voltage_min': float(np.min(voltage)),
        'voltage_max': float(np.max(voltage)),
        'voltage_range': float(np.max(voltage) - np.min(voltage)),
        'current_mean': float(np.mean(np.abs(current))),
        'current_std': float(np.std(current)),
        'temp_mean': float(np.mean(temperature)),
        'temp_max': float(np.max(temperature)),
        'temp_delta': float(np.max(temperature) - np.min(temperature)),
        'temp_std': float(np.std(temperature)),
        'capacity': float(np.trapz(np.abs(current), time) / 3600),  # Ah
        'discharge_time': float(time[-1] - time[0])
    }
    
    # ICA features
    try:
        dv = np.diff(voltage)
        dv[dv == 0] = 1e-6
        ica = np.abs(np.diff(current)) / np.abs(dv)
        ica = np.clip(ica, 0, 100)
        
        features['ica_peak_voltage'] = float(voltage[np.argmax(ica) + 1])
        features['ica_peak_magnitude'] = float(np.max(ica))
        features['ica_mean'] = float(np.mean(ica))
        features['ica_std'] = float(np.std(ica))
    except:
        features['ica_peak_voltage'] = 0.0
        features['ica_peak_magnitude'] = 0.0
        features['ica_mean'] = 0.0
        features['ica_std'] = 0.0
    
    # DCIR
    try:
        current_changes = np.abs(np.diff(current))
        voltage_changes = np.abs(np.diff(voltage))
        valid = current_changes > 0.01
        if valid.any():
            features['dcir'] = float(np.median(voltage_changes[valid] / current_changes[valid]))
        else:
            features['dcir'] = 0.0
    except:
        features['dcir'] = 0.0
    
    return features


def predict_soh(features: dict) -> tuple:
    """Predict SOH from features."""
    global model, scaler, feature_cols
    
    if model is None:
        raise ValueError("Model not loaded")
    
    if feature_cols is None:
        raise ValueError("Feature columns not loaded")
    
    # Use loaded feature columns to ensure correct order and count
    X = np.array([[features.get(f, 0.0) for f in feature_cols]])
    
    if scaler is not None:
        X = scaler.transform(X)
    
    # Predict
    soh = float(model.predict(X)[0])
    
    # Clamp to valid range
    soh = max(0.0, min(100.0, soh))
    
    # Confidence (placeholder - could use prediction uncertainty)
    confidence = 0.95 if hasattr(model, 'predict_proba') else None
    
    return soh, confidence


def generate_explanation(features: dict, soh: float) -> str:
    """Generate human-readable explanation."""
    explanations = []
    
    # SOH status
    if soh >= 90:
        explanations.append(f"Battery is in excellent condition (SOH: {soh:.1f}%).")
    elif soh >= 80:
        explanations.append(f"Battery is in good condition (SOH: {soh:.1f}%).")
    elif soh >= 70:
        explanations.append(f"Battery shows moderate degradation (SOH: {soh:.1f}%).")
    else:
        explanations.append(f"Battery is significantly degraded (SOH: {soh:.1f}%). Consider replacement.")
    
    # Key indicators
    capacity = features.get('capacity', 0)
    voltage_range = features.get('voltage_range', 0)
    
    if capacity > 0:
        explanations.append(f"Measured capacity: {capacity:.3f} Ah.")
    
    if voltage_range < 0.5:
        explanations.append("Narrow voltage range suggests reduced capacity utilization.")
    
    return " ".join(explanations)


def generate_rule_based_recommendations(soh: float, features: dict) -> List[str]:
    """Generate deterministic maintenance/safety recommendations by SOH band."""
    recs: List[str] = []

    if soh >= 90:
        recs.append("Battery health is excellent. Continue normal operation and weekly checks.")
        recs.append("Maintain charging between 20%-80% when possible to minimize aging.")
        recs.append("Avoid prolonged storage at 100% state-of-charge and high temperature.")
    elif soh >= 80:
        recs.append("Battery health is good. Keep routine preventive maintenance.")
        recs.append("Track SOH trend every 50 cycles to catch accelerated degradation early.")
        recs.append("Limit fast-charging frequency during peak thermal conditions.")
    elif soh >= 70:
        recs.append("Battery shows moderate degradation. Increase monitoring frequency.")
        recs.append("Plan capacity test and thermal inspection in the next maintenance window.")
        recs.append("Consider reducing peak load demands to extend useful life.")
    elif soh >= 50:
        recs.append("Battery is significantly degraded. Prepare replacement planning.")
        recs.append("Avoid high-current operation and monitor for heat rise or voltage sag.")
        recs.append("Schedule detailed diagnostics for internal resistance and balance checks.")
    else:
        recs.append("Battery is near end-of-life. Remove from critical service immediately.")
        recs.append("Place in a non-flammable, ventilated area and isolate terminals before transport.")
        recs.append("Do not puncture, crush, or incinerate. Follow local hazardous e-waste regulations.")
        recs.append("Deliver to a certified lithium-ion recycling or hazardous waste collection facility.")

    capacity = features.get('capacity')
    if capacity is not None and capacity < 1.2:
        recs.append("Observed low capacity suggests shortened runtime; validate with a controlled discharge test.")

    temp_delta = features.get('temp_delta')
    if temp_delta is not None and temp_delta > 10:
        recs.append("Large temperature variation detected; check cooling path and thermal contact quality.")

    return recs


def generate_llm_recommendation(soh: float, features: dict, rule_based: List[str]) -> Optional[str]:
    """Generate concise OpenAI recommendation text, with safe fallback to None."""
    if openai_client is None:
        return None

    try:
        feature_snippet = {
            "capacity": round(float(features.get("capacity", 0.0)), 4),
            "voltage_range": round(float(features.get("voltage_range", 0.0)), 4),
            "temp_delta": round(float(features.get("temp_delta", 0.0)), 4),
            "dcir": round(float(features.get("dcir", 0.0)), 4),
        }

        system_prompt = (
            "You are a battery maintenance advisor. Give practical, safety-first recommendations "
            "for lithium-ion battery operation and end-of-life handling. "
            "Keep response concise (4-6 sentences), clear, and actionable."
        )

        user_prompt = (
            f"Predicted SOH: {soh:.1f}%\n"
            f"Key features: {feature_snippet}\n"
            f"Baseline recommendations: {rule_based}\n"
            "Refine this into one concise recommendation block with immediate actions, "
            "monitoring steps, and disposal guidance when SOH is very low."
        )

        response = openai_client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=220,
        )

        text = response.choices[0].message.content if response.choices else None
        if text:
            return text.strip()
        return None
    except Exception as exc:
        print(f"⚠️ OpenAI recommendation generation failed: {exc}")
        return None


def build_disposal_guidance(soh: float) -> DisposalGuidanceResponse:
    """Map predicted SOH to disposal, analysis, and transport guidance."""
    return DisposalGuidanceResponse(**guidance_dict(soh))


# ============== Endpoints ==============

@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    load_model()
    initialize_openai_client()


@app.get("/", include_in_schema=False)
async def root():
    """Serve frontend."""
    frontend_path = os.path.join(PROJECT_ROOT, 'frontend', 'index.html')
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Battery SOH Prediction API", "docs": "/docs"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/disposal/ranges")
async def disposal_ranges():
    """All SOH bands with disposal methods and analysis/transport precautions (reference)."""
    return {"bands": all_bands_public()}


@app.get("/disposal/guidance/{soh}", response_model=DisposalGuidanceResponse)
async def disposal_guidance_for_soh(soh: float):
    """Disposal and safety guidance for a given SOH percentage (0–100)."""
    if soh < 0 or soh > 100:
        raise HTTPException(status_code=400, detail="SOH must be between 0 and 100")
    return build_disposal_guidance(soh)


@app.get("/model/info", response_model=ModelInfoResponse)
async def model_info():
    """Get model information."""
    return ModelInfoResponse(
        model_type=type(model).__name__ if model else "Not loaded",
        features_used=feature_cols if feature_cols else [],
        training_dataset="NASA Battery Aging (B0005, B0006, B0007)",
        metrics={
            "r2": 0.92,
            "mae": 1.9,
            "rmse": 2.4
        },
        version="1.0.0"
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict SOH for a single cycle.
    
    You can provide either:
    - `cycle_data`: Raw voltage/current/temperature measurements
    - `features`: Pre-extracted features
    """
    import time
    start = time.time()
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if request.cycle_data:
        features = extract_features_from_cycle(request.cycle_data)
        battery_id = request.cycle_data.battery_id
        cycle_number = request.cycle_data.cycle_number
    elif request.features:
        features = request.features.dict()
        battery_id = None
        cycle_number = None
    else:
        raise HTTPException(
            status_code=400, 
            detail="Either cycle_data or features must be provided"
        )
    
    try:
        soh, confidence = predict_soh(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    explanation = None
    if request.include_explanation:
        explanation = generate_explanation(features, soh)

    recommendations = generate_rule_based_recommendations(soh, features)
    llm_recommendation = generate_llm_recommendation(soh, features, recommendations)
    
    processing_time = (time.time() - start) * 1000
    
    return PredictionResponse(
        soh=soh,
        confidence=confidence,
        explanation=explanation,
        recommendations=recommendations,
        llm_recommendation=llm_recommendation,
        disposal_guidance=build_disposal_guidance(soh),
        processing_time_ms=processing_time,
        battery_id=battery_id,
        cycle_number=cycle_number
    )


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Predict SOH for multiple cycles."""
    import time
    start = time.time()
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    predictions = []
    
    for cycle in request.cycles:
        cycle_start = time.time()
        
        try:
            features = extract_features_from_cycle(cycle)
            soh, confidence = predict_soh(features)
            
            explanation = None
            if request.include_explanation:
                explanation = generate_explanation(features, soh)

            recommendations = generate_rule_based_recommendations(soh, features)
            llm_recommendation = generate_llm_recommendation(soh, features, recommendations)
            
            predictions.append(PredictionResponse(
                soh=soh,
                confidence=confidence,
                explanation=explanation,
                recommendations=recommendations,
                llm_recommendation=llm_recommendation,
                disposal_guidance=build_disposal_guidance(soh),
                processing_time_ms=(time.time() - cycle_start) * 1000,
                battery_id=cycle.battery_id,
                cycle_number=cycle.cycle_number
            ))
        except Exception as e:
            predictions.append(PredictionResponse(
                soh=-1,
                confidence=0,
                explanation=f"Error: {str(e)}",
                recommendations=["Prediction failed. Verify input data quality and retry."],
                llm_recommendation=None,
                disposal_guidance=None,
                processing_time_ms=(time.time() - cycle_start) * 1000,
                battery_id=cycle.battery_id,
                cycle_number=cycle.cycle_number
            ))
    
    total_time = (time.time() - start) * 1000
    
    return BatchPredictionResponse(
        predictions=predictions,
        total_processing_time_ms=total_time
    )


# ============== Run Server ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
