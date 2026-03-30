# Data Audit Report: NASA_batteries

**Timestamp:** 20260203_022059

---

## B0005

**Status:** ✅ PASSED

**Total Cycles:** 168

### Checks

- **voltage:** ✅
  - min: 2.4556793246645583
  - max: 4.222920057935785

- **current:** ✅
  - min: -2.029098489464331
  - max: 0.0074961910680886356

- **temperature:** ✅
  - mean: 32.79131856603086
  - std_avg: 3.8845477862803803

- **soh:** ✅
  - initial: 100.80760884947753
  - final: 71.95205157786484
  - range: [np.float64(69.90890905512214), np.float64(100.80760884947753)]
  - degradation_rate: -0.20995787881329103

- **data_points:** ✅
  - mean: 299.3154761904762
  - min: 179
  - max: 371
  - below_threshold: 0

- **spikes:** ✅
  - count: 0
  - threshold: 0.5

---

## B0006

**Status:** ❌ FAILED

**Total Cycles:** 168

### Checks

- **voltage:** ✅
  - min: 2.1206980945954057
  - max: 4.222516216835943

- **current:** ✅
  - min: -2.027018156432659
  - max: 0.008808612211148337

- **temperature:** ✅
  - mean: 32.79266458937206
  - std_avg: 3.970029879900481

- **soh:** ✅
  - initial: 100.88297108833628
  - final: 58.768845403630706
  - range: [np.float64(57.18983519098024), np.float64(100.88297108833628)]
  - degradation_rate: -0.2521217331718387

- **data_points:** ✅
  - mean: 299.3154761904762
  - min: 179
  - max: 371
  - below_threshold: 0

- **spikes:** ❌
  - count: 51
  - threshold: 0.5

### Warnings

- ⚠️  High spike rate: 51/168 cycles

---

## B0007

**Status:** ❌ FAILED

**Total Cycles:** 168

### Checks

- **voltage:** ❌
  - min: 1.7370300333706354
  - max: 4.2333254357000865

- **current:** ✅
  - min: -2.0060375207298797
  - max: 0.005071881446587334

- **temperature:** ✅
  - mean: 32.367750973956205
  - std_avg: 3.9350843993136784

- **soh:** ✅
  - initial: 100.4535179156392
  - final: 76.09264518290345
  - range: [np.float64(74.39278959915893), np.float64(100.4535179156392)]
  - degradation_rate: -0.17367625250683863

- **data_points:** ✅
  - mean: 299.3154761904762
  - min: 179
  - max: 371
  - below_threshold: 0

- **spikes:** ❌
  - count: 139
  - threshold: 0.5

### Warnings

- ⚠️  Voltage outside expected range: [1.737, 4.233]
- ⚠️  High spike rate: 139/168 cycles

---

