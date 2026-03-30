# ⚡ Quick Start Guide - Phase 1

Get up and running in **3 simple steps**!

---

## 📋 Prerequisites

- Python 3.8+
- NASA B0005 battery dataset (already in your directory!)
- 5-10 minutes of time

---

## 🚀 Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected time:** 2-3 minutes

**What gets installed:**
- NumPy, SciPy, Pandas (data processing)
- PyTorch (deep learning)
- Matplotlib, Seaborn (visualization)
- Scikit-learn (metrics)

---

## ✅ Step 2: Verify Installation

```bash
python test_installation.py
```

**Expected output:**
```
✓ All packages installed
✓ PyTorch configured
✓ B0005.mat found
✓ Configuration OK
✓ Source code ready
```

**If tests fail:**
- Missing package? → `pip install <package-name>`
- B0005.mat not found? → Check path in `config.yaml`

---

## 🎯 Step 3: Run Phase-1 Pipeline

```bash
python main_pipeline.py
```

**What happens:**
1. **Load** B0005 battery data from NASA dataset
2. **Segment** discharge cycles (filter < 100 points, voltage anomalies)
3. **Extract** physics features: SOH, ICA peaks, DCIR, ΔT
4. **Train** CNN-LSTM baseline model
5. **Evaluate** performance (MAE, RMSE, MAPE)
6. **Save** model and results

**Expected time:** 5-10 minutes (CPU) / 2-3 minutes (GPU)

**Expected output:**
```
========================================
PHASE-1 PIPELINE COMPLETED
========================================

Baseline Performance:
  ✓ MAE: X.XX%
  ✓ RMSE: X.XX%
  ✓ MAPE: X.XX%

🎉 Phase-1 COMPLETE! Baseline established.
```

---

## 📊 Explore Results (Optional)

### Option A: Jupyter Notebooks

```bash
jupyter notebook
```

**Open in order:**
1. `01_data_exploration.ipynb` - Understand the data
2. `02_ica_analysis.ipynb` - Learn ICA step-by-step
3. `03_baseline_training.ipynb` - Train and visualize

### Option B: Check Outputs

```bash
ls data/processed/     # Segmented cycles
ls data/features/      # Extracted features CSV
ls models/             # Trained model files
ls results/plots/      # Visualizations (from notebooks)
```

---

## 🎓 What You Just Built

✅ **Complete SOH prediction pipeline**  
✅ **Physics-guided feature extraction** (ICA, DCIR)  
✅ **Deep learning baseline** (CNN-LSTM)  
✅ **Production-ready code** (modular, documented)  

**This is your Phase-1 baseline** for comparison with Phase-2 multimodal fusion!

---

## 🔧 Customization

### Change Battery

Edit `config.yaml`:
```yaml
dataset:
  path: "NASA_DataSets/1. BatteryAgingARC-FY08Q4/B0006.mat"
  battery_id: "B0006"
```

### Tune Model

Edit `config.yaml`:
```yaml
model:
  architecture:
    lstm:
      hidden_size: 256  # Increase capacity
  training:
    batch_size: 32      # Larger batches
    learning_rate: 0.0005  # Slower learning
```

### Adjust ICA

Edit `config.yaml`:
```yaml
features:
  ica:
    window_length: 15   # More smoothing
    voltage_range: [2.7, 4.1]  # Narrower range
```

Then re-run: `python main_pipeline.py`

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'torch'"
```bash
pip install torch
```

### "FileNotFoundError: B0005.mat"
- Check dataset path in `config.yaml`
- Verify file exists in `NASA_DataSets/` folder

### "CUDA out of memory"
- Reduce `batch_size` in `config.yaml` to 8 or 4
- Or let it use CPU (slower but works)

### "ICA computation failed"
- Increase `window_length` to 15 or 21 (must be odd)
- Check voltage range includes sufficient data

### Training is slow
- Using CPU? Expected (5-10 min vs 2-3 min GPU)
- Reduce `epochs` in config for faster testing

---

## 📚 Next Steps

### Understand the Code
- Read `src/data_loader.py` - See how .mat files are parsed
- Read `src/feature_extraction.py` - Learn ICA implementation
- Read `src/baseline_model.py` - Understand CNN-LSTM architecture

### Experiment
- Try different batteries (B0006, B0007)
- Tune hyperparameters in `config.yaml`
- Add new features in `feature_extraction.py`

### Phase-2 Preview
- Feature-to-text conversion
- LLM embeddings
- Multimodal fusion
- Explainability (SHAP, attention)

---

## 🎯 Summary

**You've successfully built:**
- ✅ Data pipeline (loading, segmentation, filtering)
- ✅ Feature extraction (physics-guided)
- ✅ Baseline model (CNN-LSTM)
- ✅ Evaluation framework (metrics, visualization)

**In just 3 commands:**
```bash
pip install -r requirements.txt
python test_installation.py
python main_pipeline.py
```

**Ready for Phase-2!** 🚀

---

## 💡 Pro Tips

1. **Run tests first** - `test_installation.py` catches 90% of issues
2. **Use notebooks** - Better for understanding and visualization
3. **Check logs** - `results/logs/phase1.log` has detailed output
4. **Start small** - Test with fewer epochs first, then full training
5. **Read config** - `config.yaml` controls everything

---

## 🆘 Still Stuck?

Check:
1. **README.md** - Full documentation
2. **Notebooks** - Step-by-step examples
3. **Source code** - Heavily commented

---

**That's it! You're now running Phase-1.** 🎉

Time to explore the notebooks or move to Phase-2! 🔥
