# Data Audit Report: NASA_batteries

**Timestamp:** 20260203_022442

---

## B0005

**Status:** ✅ PASSED

**Total Cycles:** 168

### Checks

- **voltage:** ✅
  - min: 2.4556793246645583
  - max: 4.222920057935785
  - in_expected_range: True
  - in_tolerance: True

- **current:** ✅
  - min: -2.029098489464331
  - max: 0.0074961910680886356

- **temperature:** ✅
  - mean: 32.79131856603086
  - std_avg: 3.8845477862803803

- **soh:** ✅
  - initial: 100.80760884947753
  - final: 71.95205157786484
  - range: [69.90890905512214, 100.80760884947753]
  - degradation_rate: -0.20995787881329103

- **data_points:** ✅
  - mean: 299.3154761904762
  - min: 179
  - max: 371
  - below_threshold: 0

- **spikes:** ✅
  - count: 0
  - rate: 0.0
  - threshold: 0.5
  - mean_max_change: 0.3670435053733249
  - max_change: 0.48943918261345987

---

## B0006

**Status:** ✅ PASSED

**Total Cycles:** 168

### Checks

- **voltage:** ✅
  - min: 2.1206980945954057
  - max: 4.222516216835943
  - in_expected_range: True
  - in_tolerance: True

- **current:** ✅
  - min: -2.027018156432659
  - max: 0.008808612211148337

- **temperature:** ✅
  - mean: 32.79266458937206
  - std_avg: 3.970029879900481

- **soh:** ✅
  - initial: 100.88297108833628
  - final: 58.768845403630706
  - range: [57.18983519098024, 100.88297108833628]
  - degradation_rate: -0.25212173317183867

- **data_points:** ✅
  - mean: 299.3154761904762
  - min: 179
  - max: 371
  - below_threshold: 0

- **spikes:** ✅
  - count: 51
  - rate: 0.30357142857142855
  - threshold: 0.5
  - mean_max_change: 0.45336561287289795
  - max_change: 0.6281966581362637

### Warnings

- ⚠️  Elevated spike rate: 51/168 (30.4%) cycles

---

## B0007

**Status:** ✅ PASSED

**Total Cycles:** 168

### Checks

- **voltage:** ✅
  - min: 1.7370300333706354
  - max: 4.2333254357000865
  - in_expected_range: False
  - in_tolerance: True

- **current:** ✅
  - min: -2.0060375207298797
  - max: 0.005071881446587334

- **temperature:** ✅
  - mean: 32.367750973956205
  - std_avg: 3.9350843993136784

- **soh:** ✅
  - initial: 100.4535179156392
  - final: 76.09264518290345
  - range: [74.39278959915893, 100.4535179156392]
  - degradation_rate: -0.17367625250683863

- **data_points:** ✅
  - mean: 299.3154761904762
  - min: 179
  - max: 371
  - below_threshold: 0

- **spikes:** ❌
  - count: 139
  - rate: 0.8273809523809523
  - threshold: 0.5
  - mean_max_change: 0.6458009484193431
  - max_change: 0.9785213226488301

### Warnings

- ⚠️  Voltage slightly outside expected range: [1.737, 4.233] V (within tolerance)
- ⚠️  Elevated spike rate: 139/168 (82.7%) cycles

---

