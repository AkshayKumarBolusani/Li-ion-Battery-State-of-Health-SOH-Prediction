# Li-ion Battery State of Health (SOH) Prediction

A complete end-to-end machine learning pipeline for predicting battery health using physics-guided features and multimodal deep learning.

**Author:** Akshay Kumar  
**Completed:** February 2026  
**Status:** ✅ All 3 Phases Complete

---

## What This Project Does

This project predicts how healthy a Li-ion battery is (State of Health / SOH) by:
1. Analyzing voltage, current, and temperature data from battery cycles
2. Extracting physics-based features (capacity fade, internal resistance, etc.)
3. Using machine learning models to predict SOH percentage
4. Providing a REST API for real-time predictions

**Final Results:**
- **R² Score:** 0.96 (96% accuracy)
- **MAE:** 3.3% (predictions within 3.3% of actual SOH)
- **Deployment:** Docker-ready FastAPI server

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BATTERY SOH PREDICTION PIPELINE                       │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │  Raw Data   │
                              │ (.mat/.csv) │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │   Cycles    │
                              │ Segmentation│
                              └──────┬──────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Physics Features    │
                         │ (ICA, DCIR, Capacity) │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
           ┌───────────────┐                ┌───────────────┐
           │Numeric Encoder│                │ Text Templates│
           │  (CNN+LSTM)   │                │  (Feature→NL) │
           └───────┬───────┘                └───────┬───────┘
                   │                                │
                   │                                ▼
                   │                        ┌───────────────┐
                   │                        │LLM Embeddings │
                   │                        │(Sentence-BERT)│
                   │                        └───────┬───────┘
                   │                                │
                   └────────────┬───────────────────┘
                                │
                                ▼
                      ┌───────────────────┐
                      │  Multimodal Fusion│
                      │ (Cross-Attention) │
                      └─────────┬─────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ SOH (0-100%)│
                         └──────┬──────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   REST API (FastAPI)  │
                    │   + Web Frontend      │
                    └───────────────────────┘
```

**Simplified Flow:**
```
Raw Data → Cycles → Physics Features → [Numeric Model + Text→Embeddings] → Fusion → SOH → API
```

---

## Project Phases Overview

| Phase | Goal | Key Achievement |
|-------|------|-----------------|
| **Phase 1** | Proof of Concept | End-to-end pipeline with NASA data |
| **Phase 2** | Research Validation | Rigorous testing, ablation studies, explainability |
| **Phase 3** | Scale & Deploy | Multi-dataset, improved model, REST API |

---

## Quick Start (For Beginners)

### Step 1: Clone/Download the Project

Make sure you have the project folder on your computer.

### Step 2: Install Python

You need Python 3.8 or higher. Check with:
```bash
python --version
```

### Step 3: Create Virtual Environment

```bash
# Navigate to project folder
cd "/Users/kumar/Documents/projects/li-ion battery"

# Create virtual environment
python -m venv .venv

# Activate it (Mac/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Pipeline

**Option A: Run Complete Pipeline (Recommended for first time)**
```bash
python main_pipeline.py
```

**Option B: Use Jupyter Notebooks (Interactive)**
```bash
jupyter notebook
```
Then open notebooks in the `notebooks/` folder.

**Option C: Start the API Server**
```bash
uvicorn api.main:app --reload --port 8000
```
Visit http://localhost:8000 for the web interface.

**Option D: Run with Docker (Any OS)**
```bash
# 1) Create env file
cp .env.example .env

# 2) Build and run production API
docker compose up -d --build
```
Visit http://localhost:8000 - works on Windows, macOS, Linux!

---

## Complete File Structure

```
li-ion battery/
│
├── 📄 README.md                    # This file - project overview
├── 📄 requirements.txt             # Python packages needed
├── 📄 requirements-api.txt         # API-specific packages
├── 📄 config.yaml                  # Configuration settings
├── 📄 phase2_config.yaml           # Phase 2 configuration
├── 📄 main_pipeline.py             # Main script to run Phase 1
├── 📄 test_installation.py         # Verify everything is installed
│
├── 📁 NASA_DataSets/               # Raw NASA battery data (.mat files)
│   ├── B0005.mat                   # Battery B0005 data
│   ├── B0006.mat                   # Battery B0006 data
│   └── B0007.mat                   # Battery B0007 data
│
├── 📁 MENDELEY_Lithium-ion.../     # Mendeley forklift battery data
│   ├── Cell1/                      # Cell 1 data
│   │   ├── Round00/RPT.csv
│   │   ├── Round01/RPT.csv
│   │   └── ...
│   └── Cell2-8/                    # Other cells
│
├── 📁 src/                         # Source code modules
│   ├── __init__.py
│   ├── utils.py                    # Helper functions
│   ├── data_loader.py              # Load NASA .mat files
│   ├── cycle_segmentation.py       # Filter and segment cycles
│   ├── feature_extraction.py       # Extract physics features
│   ├── baseline_model.py           # CNN-LSTM model (Phase 1)
│   │
│   ├── 📁 phase2/                  # Phase 2 modules
│   │   ├── __init__.py
│   │   ├── data_audit.py           # Data quality checks
│   │   ├── data_harmonization.py   # Combine datasets
│   │   ├── data_splits.py          # Train/val/test splitting
│   │   ├── baseline_models.py      # LSTM, CNN-LSTM, Transformer
│   │   ├── multimodal_model.py     # Numeric + Semantic fusion
│   │   ├── feature_to_text.py      # Convert features to text
│   │   └── text_templates.yaml     # Templates for text generation
│   │
│   └── 📁 phase3/                  # Phase 3 modules
│       ├── __init__.py
│       ├── mendeley_loader.py      # Load Mendeley dataset
│       ├── combined_dataset.py     # Combine NASA + Mendeley
│       └── cross_attention_model.py # Advanced neural network
│
├── 📁 api/                         # REST API for deployment
│   ├── main.py                     # FastAPI server
│   ├── Dockerfile                  # Docker container config
│   └── client_example.py           # Example API client code
│
├── 📁 frontend/                    # Web user interface
│   └── index.html                  # Single-page web app
│
├── 📄 Dockerfile                   # Docker container build file
├── 📄 docker-compose.yml           # Docker Compose configuration
├── 📄 .dockerignore                # Files to exclude from Docker
├── 📄 DOCKER_QUICKSTART.md         # Docker setup guide
│
├── 📁 notebooks/                   # Jupyter notebooks (interactive)
│   │
│   │ # Phase 1 Notebooks
│   ├── 01_data_exploration.ipynb   # Explore NASA data
│   ├── 02_ica_analysis.ipynb       # Understand ICA features
│   ├── 03_baseline_training.ipynb  # Train first model
│   │
│   │ # Phase 2 Notebooks
│   ├── PHASE2_RUN_ALL.ipynb        # Run all Phase 2 steps
│   ├── phase2_step1_data_audit.ipynb
│   ├── phase2_step2_harmonization.ipynb
│   ├── phase2_step3_baselines.ipynb
│   ├── phase2_step3_baselines_corrected.ipynb
│   ├── phase2_step4_multimodal.ipynb
│   ├── phase2_step5_ablation.ipynb
│   ├── phase2_step6_generalization.ipynb
│   ├── phase2_step7_robustness.ipynb
│   ├── phase2_step8_explainability.ipynb
│   ├── phase2_step9_statistical.ipynb
│   ├── phase2_step10_final_report.ipynb
│   │
│   │ # Phase 3 Notebooks
│   ├── phase3_step1_mendeley.ipynb # Load Mendeley data
│   ├── phase3_step2_cross_attention.ipynb # Train advanced model
│   └── phase3_step3_deployment.ipynb # Deploy API
│
├── 📁 models/                      # Saved trained models
│   ├── best_model.pkl              # Production Ridge model
│   ├── scaler.pkl                  # Feature normalizer
│   ├── feature_cols.pkl            # Feature column names
│   └── cross_attention_model.pt    # Deep learning model
│
├── 📁 data/                        # Processed data
│   ├── 📁 processed/               # Segmented cycles
│   ├── 📁 features/                # Extracted features
│   ├── 📁 phase2/harmonized/       # Phase 2 processed data
│   └── 📁 phase3/                  # Phase 3 combined data
│
├── 📁 results/                     # Output results
│   ├── 📁 plots/                   # Visualizations
│   ├── 📁 phase2/                  # Phase 2 results
│   │   ├── audit_reports/
│   │   ├── figures/
│   │   └── final_report/
│   └── 📁 phase3/                  # Phase 3 results
│
└── 📁 Documentation Files
    ├── QUICKSTART.md               # Quick setup guide
    ├── PHASE2_ROADMAP.md           # Phase 2 plan
    ├── PHASE2_STATUS.md            # Progress tracker
    ├── PHASE2_KICKOFF.md           # How to start Phase 2
    ├── PHASE3_ROADMAP.md           # Phase 3 plan
    ├── PHASE3_FINAL_REPORT.md      # Final summary
    └── IMPLEMENTATION_SUMMARY.md   # Technical details
```

---

## What Each File Does

### Core Scripts

| File | Purpose | When to Use |
|------|---------|-------------|
| `main_pipeline.py` | Runs entire Phase 1 pipeline | First time setup, quick demo |
| `test_installation.py` | Checks all dependencies | Troubleshooting |
| `config.yaml` | All settings and parameters | Customize behavior |

### Source Code (`src/`)

| File | Purpose |
|------|---------|
| `utils.py` | Helper functions (logging, file I/O, seeding) |
| `data_loader.py` | Loads NASA .mat files into Python |
| `cycle_segmentation.py` | Filters bad cycles, segments discharge data |
| `feature_extraction.py` | Extracts ICA, DCIR, temperature features |
| `baseline_model.py` | CNN-LSTM neural network for Phase 1 |

### Phase 2 Modules (`src/phase2/`)

| File | Purpose |
|------|---------|
| `data_audit.py` | Checks data quality (spikes, missing values) |
| `data_harmonization.py` | Combines multiple batteries into one dataset |
| `data_splits.py` | Creates train/val/test splits properly |
| `baseline_models.py` | LSTM, CNN-LSTM, Transformer models |
| `multimodal_model.py` | Combines numeric + text features |
| `feature_to_text.py` | Converts numbers to natural language |
| `text_templates.yaml` | Templates for text generation |

### Phase 3 Modules (`src/phase3/`)

| File | Purpose |
|------|---------|
| `mendeley_loader.py` | Loads Mendeley forklift battery data |
| `combined_dataset.py` | Merges NASA + Mendeley datasets |
| `cross_attention_model.py` | Advanced neural network with attention |

### API (`api/`)

| File | Purpose |
|------|---------|
| `main.py` | FastAPI server with prediction endpoints |
| `Dockerfile` | Container configuration for deployment |
| `client_example.py` | Example code to call the API |

### Notebooks (`notebooks/`)

**Run these in order for full understanding:**

1. `01_data_exploration.ipynb` - See what the data looks like
2. `02_ica_analysis.ipynb` - Understand physics features
3. `03_baseline_training.ipynb` - Train your first model
4. `PHASE2_RUN_ALL.ipynb` - Complete Phase 2 validation
5. `phase3_step1_mendeley.ipynb` - Add more data
6. `phase3_step2_cross_attention.ipynb` - Train best model
7. `phase3_step3_deployment.ipynb` - Deploy to production

---

## Phase 1: Proof of Concept

### What We Did
1. **Loaded NASA battery data** (B0005) from .mat files
2. **Segmented discharge cycles** and filtered bad data
3. **Extracted physics features:**
   - SOH (State of Health) - target variable
   - ICA (Incremental Capacity Analysis) - electrode health
   - DCIR (DC Internal Resistance) - resistance increase
   - Temperature statistics
4. **Trained CNN-LSTM model** to predict SOH
5. **Validated** the approach works

### Key Results
- Successfully predicted SOH from cycle data
- Established baseline metrics for comparison
- Proved the pipeline works end-to-end

### How to Run Phase 1
```bash
python main_pipeline.py
```
Or use notebooks 01-03.

---

## Phase 2: Research Validation

### What We Did
1. **Data Audit** - Verified data quality for B0005, B0006, B0007
2. **Multi-Battery Training** - Combined all 3 NASA batteries
3. **Baseline Comparison** - Tested Ridge, Random Forest, Gradient Boosting
4. **Multimodal Model** - Added text descriptions + LLM embeddings
5. **Ablation Studies** - Tested what features matter most
6. **Cross-Battery Testing** - Train on one battery, test on another
7. **Robustness Testing** - Added noise, missing data
8. **Explainability** - SHAP values, feature importance
9. **Statistical Validation** - Multiple runs, significance tests
10. **Final Report** - Comprehensive documentation

### Key Results
| Model | R² | MAE |
|-------|-----|-----|
| Ridge Regression | 0.92 | 4.28% |
| Gradient Boosting | 0.91 | 4.52% |
| Random Forest | 0.89 | 5.01% |

### How to Run Phase 2
```bash
# Open Jupyter
jupyter notebook

# Run: notebooks/PHASE2_RUN_ALL.ipynb
# Then run steps 5-10 individually
```

---

## Phase 3: Scale & Deploy

### What We Did
1. **Added Mendeley Dataset** - Forklift battery data (different chemistry)
2. **Improved Model Architecture:**
   - CNN + Transformer encoder for time-series
   - Embedding adapter for LLM features
   - Multi-head cross-attention fusion
   - Gated fusion for dynamic weighting
3. **Deployed as REST API** - FastAPI with Docker

### Key Results
| Metric | Phase 2 Baseline | Phase 3 Cross-Attention | Improvement |
|--------|------------------|-------------------------|-------------|
| R² | 0.9176 | **0.9595** | +4.2% |
| MAE | 4.28% | **3.33%** | -22% |

### How to Run Phase 3

**Train the model:**
```bash
jupyter notebook
# Run: notebooks/phase3_step2_cross_attention.ipynb
```

**Start the API:**
```bash
uvicorn api.main:app --reload --port 8000
```

**Use Docker:**
```bash
docker build -t battery-soh-api -f api/Dockerfile .
docker run -d -p 8000:8000 --name soh-api battery-soh-api
```

---

## Running with Docker (Recommended for Sharing)

Docker allows you to run this on **any operating system** without installing Python or dependencies.

### Quick Start with Docker

```bash
# Build the image
docker build -t battery-soh-predictor .

# Run the container
docker run -d -p 8000:8000 --name battery-api battery-soh-predictor

# Open browser
# http://localhost:8000
```

### Share with Others

```bash
# Export image to file
docker save -o battery-soh-predictor.tar battery-soh-predictor:latest

# Share the .tar file (USB, cloud, email, etc.)

# Recipient runs:
docker load -i battery-soh-predictor.tar
docker run -d -p 8000:8000 --name battery-api battery-soh-predictor
```

### Docker Commands Reference

| Command | Description |
|---------|-------------|
| `docker build -t battery-soh-predictor .` | Build image |
| `docker run -d -p 8000:8000 --name battery-api battery-soh-predictor` | Start container |
| `docker stop battery-api` | Stop container |
| `docker rm battery-api` | Remove container |
| `docker logs battery-api` | View logs |
| `docker-compose up -d` | Start with Compose |
| `docker-compose down` | Stop with Compose |

**Full Docker guide:** See `DOCKER_QUICKSTART.md`

---

## Using the Web Interface (Without Docker)

### Start Server
```bash
cd "/Users/kumar/Documents/projects/li-ion battery"
source .venv/bin/activate
uvicorn api.main:app --reload --port 8000
```

### Open the Web App
Visit **http://localhost:8000** in your browser.

![Battery SOH Predictor](frontend/screenshot.png)

**Features:**
- Interactive form to enter battery features
- Real-time SOH prediction with visual gauge
- Color-coded health status (Excellent/Good/Moderate/Poor)
- Quick presets for different battery conditions
- Prediction history tracking

---

## Using the API Programmatically

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Health check |
| `/model/info` | GET | Model information |
| `/predict` | POST | Single SOH prediction |
| `/predict/batch` | POST | Multiple predictions |
| `/docs` | GET | Interactive API docs |

### Example API Call

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "features": {
            "voltage_mean": 3.5,
            "voltage_std": 0.2,
            "voltage_min": 3.0,
            "voltage_max": 4.2,
            "voltage_range": 1.2,
            "current_mean": 1.5,
            "current_std": 0.1,
            "capacity": 1.8,
            "discharge_time": 3600,
            "temp_mean": 25.0,
            "temp_max": 28.0,
            "temp_delta": 3.0,
            "temp_std": 1.0,
            "ica_peak_voltage": 3.6,
            "ica_peak_magnitude": 0.5,
            "ica_mean": 0.2,
            "ica_std": 0.1,
            "dcir": 0.05
        },
        "include_explanation": True
    }
)

result = response.json()
print(f"Predicted SOH: {result['soh']:.1f}%")
print(f"Explanation: {result['explanation']}")
```

---

## Features Explained

### What is SOH (State of Health)?
SOH measures how much capacity a battery has compared to when it was new.
- **100%** = Brand new battery
- **80%** = End of life for EVs (replace battery)
- **70%** = Significantly degraded

### Physics Features We Extract

| Feature | What It Measures | Why It Matters |
|---------|------------------|----------------|
| **Capacity** | How much charge battery holds (Ah) | Direct measure of health |
| **ICA Peak** | Voltage where most charging happens | Shifts as electrodes degrade |
| **DCIR** | Internal resistance (Ω) | Increases as battery ages |
| **Temp Delta** | Temperature rise during cycle | Higher = more degradation |
| **Voltage Range** | Difference between max and min V | Narrows as capacity fades |

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'xxx'"
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: Battery file not found"
Make sure you have the NASA data in `NASA_DataSets/` folder:
- B0005.mat
- B0006.mat
- B0007.mat

### "Cannot connect to API"
Make sure the server is running:
```bash
uvicorn api.main:app --reload --port 8000
```

### "Docker daemon not running"
Open Docker Desktop app first, then run docker commands.

### Jupyter notebooks not finding modules
Run this in the first cell:
```python
import sys
import os
PROJECT_ROOT = '/Users/kumar/Documents/projects/li-ion battery'
os.chdir(PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))
```

---

## Dependencies

Main packages used:
- `numpy`, `pandas` - Data manipulation
- `scipy` - Signal processing, .mat file loading
- `scikit-learn` - Machine learning models
- `torch` - Deep learning
- `matplotlib`, `seaborn` - Visualization
- `sentence-transformers` - LLM embeddings
- `shap` - Explainability
- `fastapi`, `uvicorn` - REST API
- `pyyaml` - Configuration

Install all:
```bash
pip install -r requirements.txt
```

---

## Project Development

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 1 | Initial development & proof of concept | ✅ Complete |
| Phase 2 | Iterative validation & ablation studies | ✅ Complete |
| Phase 3 | Extension, optimization & deployment | ✅ Complete |

---

## Limitations

This project has several limitations that should be acknowledged:

- **Laboratory Data Only:** Evaluation is based on controlled laboratory cycling data (NASA, Mendeley), not real-world EV fleet or consumer device data with variable usage patterns.

- **Limited Temperature Variation:** NASA datasets were collected at approximately room temperature (~24°C). Model performance under extreme temperatures (hot/cold climates) is not validated.

- **Frozen LLM Embeddings:** The Sentence-BERT embeddings are used as-is without domain-specific fine-tuning on battery terminology. Domain adaptation could improve semantic representations.

- **Single Chemistry Focus:** Primary validation on 18650 Li-ion cells. Generalization to other chemistries (LFP, NMC, solid-state) requires additional validation.

- **No Real-Time Constraints:** Edge deployment latency and memory constraints for onboard BMS (Battery Management System) integration are not evaluated.

- **Limited Degradation Modes:** Models trained primarily on calendar and cycle aging. Abnormal degradation (thermal runaway precursors, lithium plating) not specifically addressed.

---

## Future Improvements

1. **More Data** - Add CALCE, Oxford battery datasets
2. **Better Models** - Try Transformers, Graph Neural Networks
3. **Uncertainty** - Add confidence intervals to predictions
4. **Real-time** - Stream predictions from live batteries
5. **Mobile App** - Create user-friendly interface

---

## References

Key papers and datasets used in this work:

1. **NASA Battery Dataset:**  
   B. Saha and K. Goebel, "Battery Data Set", NASA Ames Prognostics Data Repository, 2007.  
   https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/

2. **Mendeley Forklift Battery Dataset:**  
   "Lithium-ion battery degradation dataset based on a realistic forklift operation profile"  
   https://data.mendeley.com/

3. **Incremental Capacity Analysis:**  
   M. Dubarry et al., "Identifying battery aging mechanisms in large format Li ion cells," Journal of Power Sources, 2011.

4. **Deep Learning for SOH:**  
   Y. Zhang et al., "Deep learning for battery state of health estimation," Energy, 2020.

5. **Sentence-BERT:**  
   N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," EMNLP, 2019.

---

## License

Educational/Research use only.  
Please cite appropriately if using this work in academic publications.

---

## Summary

This project demonstrates a complete machine learning pipeline:

1. **Data Loading** → NASA .mat files, Mendeley CSV files
2. **Feature Engineering** → Physics-based features (ICA, DCIR, capacity)
3. **Model Training** → Ridge, Random Forest, CNN-LSTM, Cross-Attention
4. **Validation** → Ablation studies, cross-battery testing, robustness
5. **Deployment** → FastAPI REST API with Docker

**Final Model Performance:**
- **R² = 0.96** (explains 96% of SOH variance)
- **MAE = 3.3%** (predictions within 3.3% of actual)

Ready for production use! 🚀
