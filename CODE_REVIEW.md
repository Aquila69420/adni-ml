# ADML Code Review & System Design Assessment
**For Publication Preparation** | Generated May 2026

---

## Executive Summary

The ADML codebase demonstrates solid research foundations with a complete end-to-end pipeline (preprocessing → training → evaluation). However, **it is not publication-ready** from a reproducibility and DevOps perspective. Critical issues center on:

1. **Hardcoded paths & configuration** (breaks across environments)
2. **Unversioned dependencies** (will fail in 6 months)
3. **Code duplication** (maintenance nightmare)
4. **Missing tests & validation** (can't guarantee correctness)
5. **Zero documentation** (README is empty)

**Estimate**: 6-8 weeks of focused refactoring to meet publication standards.

---

## 1. CRITICAL ISSUES (Blocking Publication)

### 1.1 Dependency Management 🔴
**Problem**: No pinned versions in `requirements.txt`

**Current State**:
```
pip freeze > requirements.txt  # ← NEVER RUN
# File likely contains:
scikit-learn
torch
pandas
numpy
# ... no versions!
```

**Impact**:
- Code will break when libraries update breaking APIs
- Different installs get different versions
- CI/CD pipelines will fail unpredictably

**Solution**:
- Run `pip freeze > requirements-lock.txt` immediately
- Test against locked versions
- Create `requirements-dev.txt` (dev tools: pytest, black, flake8)
- Document Python version requirement (3.9+)

**Acceptance Criteria**:
```bash
# Reproducible installs
python -m venv env
source env/bin/activate
pip install -r requirements.txt
# Should produce identical environment across machines
```

---

### 1.2 Hardcoded Paths & Configurations 🔴
**Problem**: Settings scattered across code, impossible to run in different environments

**Examples Found**:
```python
# train.ipynb
data_dir = 'data'  # ← Will break if notebook moved
df = pd.read_csv(os.path.join(data_dir, 'final_data.csv'))

# classification.ipynb
df['A+'] = df['ABETA_bl'].apply(lambda x: 1 if x < 880 else 0)  # Magic number!
df['T+'] = df['ptau_ab_ratio'].apply(lambda x: 1 if x > 0.028 else 0)
df['N+'] = df['tau_ab_ratio'].apply(lambda x: 1 if x > 0.33 else 0)

# train.ipynb
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=40)
# vs classification.ipynb
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=40)
# vs some other place
train_test_split(..., random_state=42)  # INCONSISTENT!
```

**Impact**:
- Can't run on different machines (paths break)
- Can't reproduce biomarker thresholds (where do 880, 0.028, 0.33 come from?)
- Random seeds inconsistent → non-reproducible results
- Can't swap datasets/models without code edits

**Solution**: Create `config.yaml` at repo root

```yaml
# config.yaml
data:
  input_dir: "./data"
  output_dir: "./results"
  splits:
    train: 0.8
    test: 0.2
    seed: 42

biomarkers:
  abeta_threshold: 880  # Citation: [Paper Name, 2023]
  ptau_ab_ratio_threshold: 0.028
  tau_ab_ratio_threshold: 0.33

models:
  svm:
    kernel: "sigmoid"
    C: 1.0
    gamma: 0.001
  feature_selection:
    method: "mrmr"
    k_features: 25

preprocessing:
  normalize: true
  remove_outliers: true
  imputation_method: "mean"
```

**Loading in Python**:
```python
import yaml
from pathlib import Path

def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()
data_dir = Path(config['data']['input_dir'])
abeta_threshold = config['biomarkers']['abeta_threshold']
```

**Acceptance Criteria**:
- No hardcoded paths (use `config.yaml`)
- All magic numbers documented with citations
- Unified random seed across codebase
- Tests pass with config from different directory

---

### 1.3 Magic Numbers Without Documentation 🔴
**Problem**: Biomarker thresholds have no source attribution

**Current Code**:
```python
# From classification.ipynb - but WHY these values?
df['A+'] = df['ABETA_bl'].apply(lambda x: 1 if x < 880 else 0)
df['T+'] = df['ptau_ab_ratio'].apply(lambda x: 1 if x > 0.028 else 0)
df['N+'] = df['tau_ab_ratio'].apply(lambda x: 1 if x > 0.33 else 0)
```

**Solution**: Document in `docs/BIOMARKER_THRESHOLDS.md`

```markdown
# Biomarker Thresholds (ATN Framework)

## Amyloid (A+)
- **Threshold**: Aβ42 < 880 pg/mL
- **Source**: Buckley et al. (2023) "CSF biomarkers of Alzheimer's disease concord with amyloid-β PET..."
- **Reference**: [Link to paper section]
- **Rationale**: Established cutoff from BioFINDER and ADNI cohorts

## Tau (T+)
- **Threshold**: pTau/Aβ ratio > 0.028
- **Source**: [Same paper], Table 2
- **Rationale**: Distinguishes tau pathology from amyloid alone

## Neurodegeneration (N+)
- **Threshold**: Tau/Aβ ratio > 0.33
- **Source**: [Reference needed]
- **Rationale**: [Add justification]
```

**Acceptance Criteria**:
- Every threshold has citation
- Sensitivity/specificity documented
- Alternative thresholds discussed

---

### 1.4 Missing Data Validation 🔴
**Problem**: No validation that data is in expected format

**Evidence from Code**:
```python
# Raw DICOM patching (error handling via monkey-patching)
if not hasattr(dcm, 'RepetitionTime'):
    dcm.RepetitionTime = 100  # ← What does this mean? Why 100?

# No checks for:
# - Missing values in critical columns
# - Data type mismatches
# - Outliers/impossible values
# - Cross-dataset consistency
```

**Solution**: Create `src/validation.py`

```python
def validate_data_schema(df: pd.DataFrame, config: dict) -> bool:
    """Validate dataframe matches expected schema."""
    required_cols = config['data']['required_columns']
    
    # Check columns exist
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    # Check types
    for col, dtype in config['data']['column_types'].items():
        if df[col].dtype != dtype:
            raise TypeError(f"{col} should be {dtype}, got {df[col].dtype}")
    
    # Check value ranges
    for col, (min_val, max_val) in config['data']['column_ranges'].items():
        if (df[col] < min_val).any() or (df[col] > max_val).any():
            raise ValueError(f"{col} outside expected range [{min_val}, {max_val}]")
    
    return True
```

**Acceptance Criteria**:
- Data validation runs before any processing
- Missing value strategy documented
- All transformations logged

---

## 2. MAJOR ISSUES (Strongly Recommend Fixing)

### 2.1 Code Duplication 🟡

**Found 3+ implementations of identical logic**:

1. **StandardScaler + Feature Selection** appears in:
   - `train.ipynb`
   - `classification.ipynb`
   - `torch_classification.ipynb`

2. **Evaluation metrics** computed separately:
   - Accuracy, precision, recall, F1, MCC
   - Confusion matrix plotting
   - ROC curves

3. **Train/test split** pattern:
   - `train_test_split(..., train_size=0.8, random_state=40)`
   - `train_test_split(..., train_size=0.8, random_state=42)`

**Solution**: Extract to `src/models/evaluation.py`

```python
# src/models/evaluation.py
def compute_classification_metrics(y_true, y_pred, y_scores=None):
    """Compute comprehensive classification metrics."""
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
        'mcc': matthews_corrcoef(y_true, y_pred),
        'confusion_matrix': confusion_matrix(y_true, y_pred),
    }
    if y_scores is not None:
        metrics['roc_auc'] = roc_auc_score(y_true, y_scores)
    return metrics
```

**Acceptance Criteria**:
- DRY principle: Each function/utility appears exactly once
- 100% code coverage for core modules
- Imports from `src` modules, not notebooks

---

### 2.2 No Unified Pipeline 🟡
**Problem**: Separate notebooks for each stage, hard to run end-to-end

**Current Flow**:
```
dicom_to_nifti.m → normalise.m → preprocess_nifti.py → modality_pet.py → 
  ↓
train.ipynb / torch_classification.ipynb / classification.ipynb
  ↓
statistical_signifance.py (TYPO in filename!)
```

**Solution**: Create `scripts/run_pipeline.py`

```python
#!/usr/bin/env python
"""Unified pipeline runner."""

import argparse
from src.pipeline import Pipeline
from src.config import load_config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml')
    parser.add_argument('--stage', choices=['preprocess', 'train', 'evaluate', 'all'])
    parser.add_argument('--data-dir', default=None)
    args = parser.parse_args()
    
    config = load_config(args.config)
    if args.data_dir:
        config['data']['input_dir'] = args.data_dir
    
    pipeline = Pipeline(config)
    
    if args.stage in ['preprocess', 'all']:
        pipeline.preprocess()
    
    if args.stage in ['train', 'all']:
        pipeline.train()
    
    if args.stage in ['evaluate', 'all']:
        pipeline.evaluate()

if __name__ == '__main__':
    main()
```

**Usage**:
```bash
python scripts/run_pipeline.py --stage all --config config.yaml
```

---

### 2.3 No Logging/Error Handling 🟡
**Problem**: Can't debug failures, trace execution

**Solution**: Add logging infrastructure

```python
# src/utils/logging.py
import logging
from datetime import datetime

def setup_logging(log_dir='./logs', level=logging.INFO):
    """Configure logging to file and console."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"{log_dir}/adml_{timestamp}.log"
    
    handler_file = logging.FileHandler(log_file)
    handler_console = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    for handler in [handler_file, handler_console]:
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
    
    logging.root.setLevel(level)
    return log_file

# Usage in code:
import logging
logger = logging.getLogger(__name__)

def load_data(path):
    try:
        logger.info(f"Loading data from {path}")
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        return df
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {path}")
        raise
```

---

## 3. IMPORTANT IMPROVEMENTS (Professional Quality)

### 3.1 Documentation 🔵
**Current state**: README.md is empty

**Required docs**:
1. **README.md** (comprehensive setup + usage)
2. **docs/METHODOLOGY.md** (paper summary + equations)
3. **docs/DATA_DICTIONARY.md** (all features explained)
4. **docs/API.md** (function documentation)
5. **CONTRIBUTING.md** (how to submit PRs)

**README.md template**:
```markdown
# ADML: Alzheimer's Disease Multimodal Learning

[![Tests](https://github.com/Aquila69420/adni-ml/workflows/tests/badge.svg)]()

## Overview
Brief description of the research contribution and key findings.

## Installation

### Requirements
- Python 3.9+
- MATLAB (for preprocessing)
- 16GB RAM recommended

### Quick Start
\`\`\`bash
git clone https://github.com/Aquila69420/adni-ml.git
cd adni-ml
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
\`\`\`

## Usage

### 1. Prepare Data
\`\`\`bash
# Download ADNI data (manual step)
# Place in data/ directory

# Run preprocessing
python scripts/run_pipeline.py --stage preprocess
\`\`\`

### 2. Train Models
\`\`\`bash
python scripts/run_pipeline.py --stage train --config config.yaml
\`\`\`

### 3. Evaluate
\`\`\`bash
python scripts/run_pipeline.py --stage evaluate
\`\`\`

## Results
Report key metrics, comparisons with baselines.

## Citation
```bibtex
@article{khanna2026adml,
  title={ADML: ...,
  author={Khanna, D. and ...},
  year={2026}
}
\`\`\`

## License
MIT License - see [LICENSE](LICENSE)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)
```

---

### 3.2 Testing Framework 🔵
**Zero tests currently. Add**:

```python
# tests/test_preprocessing.py
import pytest
import pandas as pd
from src.preprocessing import compute_biomarkers

def test_compute_biomarkers():
    """Test biomarker calculation."""
    df = pd.DataFrame({
        'TAU_bl': [4.6, 5.8],
        'PTAU_bl': [2.3, 3.5],
        'ABETA_bl': [731.8, 780.3],
    })
    
    result = compute_biomarkers(df)
    
    assert 'A+' in result.columns
    assert result.loc[0, 'A+'] == 1  # 731.8 < 880
    assert result.loc[1, 'A+'] == 1  # 780.3 < 880

# tests/test_models.py
def test_svm_classifier():
    """Test SVM model training."""
    X = np.random.randn(100, 25)
    y = np.random.randint(0, 2, 100)
    
    model = SVMClassifier(config)
    model.fit(X, y)
    
    predictions = model.predict(X[:10])
    assert len(predictions) == 10
    assert all(p in [0, 1] for p in predictions)
```

**Run tests**:
```bash
pytest tests/ -v --cov=src
```

---

### 3.3 Type Hints & Documentation 🔵
**Current**: No type hints

**Add throughout**:
```python
from typing import Tuple, Optional, Dict
import pandas as pd
import numpy as np

def compute_biomarkers(
    df: pd.DataFrame,
    config: Dict[str, float]
) -> pd.DataFrame:
    """
    Compute ATN biomarker status from CSF measurements.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Must contain columns: TAU_bl, PTAU_bl, ABETA_bl
    config : Dict[str, float]
        Thresholds: abeta_threshold, ptau_ab_ratio_threshold, tau_ab_ratio_threshold
    
    Returns:
    --------
    pd.DataFrame
        Original df with new columns: A+, T+, N+ (binary)
    
    Raises:
    -------
    ValueError
        If required columns missing or config incomplete
    
    Examples:
    ---------
    >>> df = pd.read_csv('csf_data.csv')
    >>> config = {'abeta_threshold': 880, ...}
    >>> df_biomarkers = compute_biomarkers(df, config)
    """
```

---

## 4. PROPOSED PROJECT STRUCTURE

```
adni-ml/
├── README.md ⭐ PRIORITY 1
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
│
├── config.yaml ⭐ PRIORITY 1
├── .env.example
├── .gitignore
├── .github/
│   └── workflows/
│       ├── tests.yml (pytest on push)
│       └── lint.yml (black + flake8)
│
├── src/
│   ├── __init__.py
│   ├── config.py (load config.yaml)
│   ├── logging.py
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── dicom_converter.py
│   │   ├── normalization.py
│   │   ├── biomarkers.py ⭐ consolidate logic
│   │   └── validation.py ⭐ NEW
│   ├── models/
│   │   ├── __init__.py
│   │   ├── svm_classifier.py
│   │   ├── gaussian_process.py
│   │   └── evaluation.py ⭐ consolidate metrics
│   ├── utils/
│   │   ├── __init__.py
│   │   └── data_utils.py
│   └── pipeline.py ⭐ NEW unified runner
│
├── scripts/
│   ├── run_pipeline.py ⭐ PRIORITY 2
│   └── evaluate_model.py
│
├── notebooks/ (exploratory only)
│   ├── README.md (explains each)
│   ├── 01_eda.ipynb
│   └── 02_preprocessing_exploration.ipynb
│
├── tests/
│   ├── test_preprocessing.py ⭐ PRIORITY 2
│   ├── test_models.py
│   └── fixtures/ (test data)
│
├── docs/
│   ├── METHODOLOGY.md ⭐ PRIORITY 1
│   ├── DATA_DICTIONARY.md ⭐ PRIORITY 1
│   ├── BIOMARKER_THRESHOLDS.md ⭐ PRIORITY 1
│   └── API.md
│
├── requirements.txt ⭐ PRIORITY 1 (pinned versions)
├── requirements-dev.txt (testing, linting)
│
├── setup.py (or pyproject.toml)
├── Dockerfile (optional, for reproducibility)
│
└── .gitignore
    data/
    results/
    weights/
    *.pyc
    __pycache__/
```

---

## 5. IMPLEMENTATION ROADMAP

### **Week 1-2: Foundation (BLOCKING ISSUES)**
- [ ] Pin dependencies → `pip freeze > requirements.txt`
- [ ] Create `config.yaml` with all hardcoded values
- [ ] Write `config.py` loader
- [ ] Create `.env.example` template
- [ ] Add logging infrastructure
- [ ] Update `.gitignore` (data/, results/, weights/)

**Acceptance**: Code runs in fresh environment with config

### **Week 3: Consolidation (DUPLICATION)**
- [ ] Extract biomarker logic → `src/preprocessing/biomarkers.py`
- [ ] Extract metrics → `src/models/evaluation.py`
- [ ] Create `src/models/base.py` for model interface
- [ ] Consolidate preprocessing pipeline

**Acceptance**: No duplicate functions, 100% of old notebook code covered

### **Week 4-5: Validation & Testing (ROBUSTNESS)**
- [ ] Implement `src/validation.py` with data schema checks
- [ ] Write unit tests (minimum 80% coverage)
- [ ] Add data dictionary → `docs/DATA_DICTIONARY.md`
- [ ] Document biomarker thresholds → `docs/BIOMARKER_THRESHOLDS.md`

**Acceptance**: `pytest` passes, data validation runs without errors

### **Week 6: Unified Pipeline (USABILITY)**
- [ ] Create `scripts/run_pipeline.py` (main entry point)
- [ ] Implement `src/pipeline.py` orchestrator
- [ ] Add CLI argument handling (--config, --stage, etc.)
- [ ] Create working example in README

**Acceptance**: `python scripts/run_pipeline.py --stage all` works end-to-end

### **Week 7-8: Documentation & Publication (QUALITY)**
- [ ] Write comprehensive README.md
- [ ] Add methodology documentation
- [ ] Create CONTRIBUTING.md
- [ ] Add type hints throughout
- [ ] Setup GitHub Actions (tests, linting)
- [ ] Remove/anonymize user-specific files

**Acceptance**: Ready for GitHub public release + citation

---

## 6. CRITICAL CHECKLIST FOR PUBLICATION

Before submitting to journal/GitHub:

### Code Quality
- [ ] No hardcoded paths (all in config.yaml)
- [ ] No user-specific filenames
- [ ] All magic numbers documented with citations
- [ ] Consistent random seeds (seed=42 everywhere)
- [ ] Zero DRY violations (single source of truth)
- [ ] Black formatted + flake8 compliant

### Reproducibility
- [ ] `requirements.txt` fully pinned with versions
- [ ] README has setup + usage instructions
- [ ] CI/CD tests pass on clean environment
- [ ] Results are deterministic (same output with same seed)
- [ ] Data provenance documented

### Documentation
- [ ] README.md complete (not empty!)
- [ ] Data dictionary (column descriptions)
- [ ] Biomarker thresholds cited
- [ ] Methodology documented (equations, citations)
- [ ] API documented (function docstrings)

### Testing
- [ ] Unit tests for core functions (>80% coverage)
- [ ] Data validation tests
- [ ] End-to-end pipeline test
- [ ] All tests pass

### Licensing
- [ ] LICENSE file added (MIT/Apache/GPL)
- [ ] All dependencies license-compatible
- [ ] No proprietary code

---

## 7. NEXT STEPS

### Immediate (This Week)
1. Create this checklist as GitHub Issue
2. Pin dependencies: `pip freeze > requirements.txt`
3. Create `config.yaml` template
4. Move `README.md` generation to Priority 1

### Short-term (Week 1-2)
1. Extract `config.py` loader
2. Implement logging
3. Create `docs/DATA_DICTIONARY.md`

### Medium-term (Week 3-6)
1. Refactor notebooks → modules
2. Implement unified pipeline
3. Add tests

### Long-term (Week 7-8)
1. Documentation pass
2. GitHub Actions setup
3. Clean up for publication

---

## Questions for Clarification

1. **Data ownership**: Can the data be shared publicly, or is it proprietary?
2. **License**: Preferred license (MIT, Apache 2.0, GPL)?
3. **Timeline**: When is publication target?
4. **Scope**: Should MATLAB preprocessing be converted to Python, or documented as external?
5. **Validation**: Are there validation datasets outside ADNI we should test on?

---

## Resources

- [Python Packaging Guide](https://python-poetry.org/)
- [Pre-commit hooks](https://pre-commit.com/)
- [GitHub Actions](https://github.com/features/actions)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Reproducible Research Best Practices](https://the-turing-way.netlify.app/)

---

**Document Status**: Draft | **Last Updated**: May 2026
