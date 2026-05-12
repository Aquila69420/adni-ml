# ADML Refactoring Roadmap
**Publication-Ready Code Quality** | 6-8 Week Sprint

---

## Overview
This document provides a week-by-week breakdown for transforming the ADML codebase from research notebooks to publication-ready, reproducible software.

**Total Effort**: ~200-250 developer hours | **Critical Path**: 6 weeks

---

## Week 1: Foundation & Configuration

### Goal
Establish reproducible environment and extract all hardcoded values.

### Tasks

#### Task 1.1: Pin Dependencies 🔴
**Priority**: BLOCKING | **Time**: 2-3 hours

```bash
# Step 1: Generate current environment
pip freeze > requirements-current.txt

# Step 2: Create production requirements (remove development tools)
# requirements.txt should contain:
# - Core: scikit-learn==1.5.0, torch==2.1.0, pandas==2.0.3, numpy==1.24.3
# - Data: nilearn==0.10.1, nibabel==5.1.0, pydicom==2.4.0, dicom2nifti==2.3.5
# - MATLAB interop: matlab.engine (system-dependent)

# Step 3: Pin everything with == (not >=)
# Step 4: Test fresh install
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
python scripts/test_imports.py  # Verify all imports work
```

**Deliverable**: `requirements.txt` with all versions pinned

---

#### Task 1.2: Create Configuration System 🔴
**Priority**: BLOCKING | **Time**: 4-5 hours

**Step 1**: Create `config.yaml`
```yaml
# config.yaml - Central configuration file
data:
  paths:
    raw_data: "./data/raw"
    processed_data: "./data/processed"
    models: "./weights"
    results: "./results"
    logs: "./logs"
  
  file_structure:
    final_data_csv: "final_data.csv"
    huw_data_csv: "huw_whole_df.csv"
    mri_dir: "mri"
    pet_dir: "pet_csf"
    
  preprocessing:
    train_test_split: 0.8
    remove_outliers: true
    outlier_method: "iqr"  # or "zscore"
    outlier_threshold: 3.0
    imputation_method: "mean"  # or "median", "knn"
    normalize: true
    normalize_method: "standard"  # StandardScaler

biomarkers:
  atl_framework:
    # A: Amyloid
    amyloid:
      marker: "ABETA_bl"
      threshold: 880  # pg/mL
      direction: "less_than"  # values < 880 are A+
      reference: "Buckley et al. (2023)"
      doi: "10.1002/alz.xxx"
    
    # T: Tau (phosphorylated tau)
    tau:
      marker: "PTAU_bl"
      computed_ratio: "PTAU_bl / ABETA_bl"
      threshold: 0.028
      direction: "greater_than"
      reference: "Same as above"
    
    # N: Neurodegeneration
    neurodegeneration:
      marker: "TAU_bl"
      computed_ratio: "TAU_bl / ABETA_bl"
      threshold: 0.33
      direction: "greater_than"
      reference: "TBD - check paper"

models:
  random_seed: 42  # CRITICAL: Use everywhere
  
  feature_selection:
    method: "mrmr"  # mRMRe - Minimum Redundancy Maximum Relevance
    k_features: 25
    reference: "Peng et al. (2005)"
  
  svm:
    kernel: "sigmoid"
    C: 1.0
    gamma: 0.001
    probability: true
    class_weight: "balanced"
    random_state: 42
  
  gaussian_process:
    kernel: "rbf + white"
    normalize_y: true
    alpha: 1e-6
    random_state: 42
  
  pytorch:
    learning_rate: 0.001
    batch_size: 32
    epochs: 100
    early_stopping_patience: 10
    dropout: 0.5
    random_state: 42

evaluation:
  metrics:
    - accuracy
    - precision
    - recall
    - f1
    - roc_auc
    - matthews_corrcoef
  
  cross_validation:
    method: "stratified_k_fold"
    n_splits: 5
    shuffle: true
    random_state: 42

logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file_format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
```

**Step 2**: Create `src/config.py`
```python
# src/config.py
import yaml
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class Config:
    """Load and access configuration from YAML."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Loaded config from {self.config_path}")
        return config
    
    def get(self, key_path: str, default=None) -> Any:
        """Get nested config value using dot notation.
        
        Example:
            config.get('models.svm.kernel')  # Returns 'sigmoid'
        """
        keys = key_path.split('.')
        value = self.data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        
        return value
    
    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access."""
        return self.data[key]

# Global config instance
_config = None

def get_config(config_path: str = "config.yaml") -> Config:
    """Get or create global config instance."""
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config
```

**Step 3**: Update `requirements-dev.txt`
```txt
# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Code quality
black==23.3.0
flake8==6.0.0
isort==5.12.0
mypy==1.3.0

# Documentation
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0

# Configuration
pyyaml>=6.0

# Development
ipython>=8.0.0
jupyter>=1.0.0
```

**Deliverables**:
- [ ] `config.yaml` (production config)
- [ ] `src/config.py` (config loader)
- [ ] `.env.example` (environment variables template)
- [ ] Updated `requirements.txt` (pinned versions)
- [ ] New `requirements-dev.txt` (development tools)

---

#### Task 1.3: Create Logging Infrastructure 🟡
**Priority**: HIGH | **Time**: 2 hours

**Step 1**: Create `src/utils/logging.py`
```python
# src/utils/logging.py
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logging(
    log_dir: str = "./logs",
    log_level: str = "INFO",
    log_name: Optional[str] = None
) -> str:
    """Configure logging to file and console.
    
    Parameters:
    -----------
    log_dir : str
        Directory for log files
    log_level : str
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_name : Optional[str]
        Custom log file name (default: adml_YYYYMMDD_HHMMSS.log)
    
    Returns:
    --------
    str
        Path to log file
    """
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Generate log filename
    if log_name is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_name = f"adml_{timestamp}.log"
    
    log_file = log_path / log_name
    
    # Create logger
    logger = logging.getLogger("adml")
    logger.setLevel(getattr(logging, log_level))
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return str(log_file)
```

**Step 2**: Usage in code
```python
# In any module:
import logging
logger = logging.getLogger("adml")

def load_data(path: str):
    logger.info(f"Loading data from {path}")
    try:
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} rows × {len(df.columns)} columns")
        return df
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error loading {path}: {e}")
        raise
```

**Deliverable**: `src/utils/logging.py` with usage examples

---

#### Task 1.4: Update .gitignore
**Priority**: HIGH | **Time**: 1 hour

```bash
# .gitignore - Add to existing

# Data (large, environment-specific)
data/
results/
logs/
weights/
*.nii
*.nii.gz
*.dcm

# Environment
env/
venv/
.env
.env.local

# Notebooks (exploration artifacts)
.ipynb_checkpoints/
*.ipynb

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
.pytest_cache/
htmlcov/

# Temporary
*.tmp
*.temp
```

---

### Deliverables (End of Week 1)
- [x] `requirements.txt` (fully pinned)
- [x] `config.yaml` (all hardcoded values extracted)
- [x] `src/config.py` (config loader)
- [x] `src/utils/logging.py` (logging infrastructure)
- [x] `requirements-dev.txt` (dev tools)
- [x] Updated `.gitignore`

### Acceptance Tests
```bash
# Test 1: Fresh environment install
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
python -c "from src.config import get_config; cfg = get_config(); print(cfg.get('biomarkers.atl_framework.amyloid.threshold'))"
# Expected: 880

# Test 2: Logging works
python -c "
from src.utils.logging import setup_logging
log_file = setup_logging()
print(f'Log file created at: {log_file}')
"
```

---

## Week 2: Data Validation & Documentation

### Goal
Ensure data integrity and document everything.

### Tasks

#### Task 2.1: Create Data Validation Module 🔴
**Priority**: BLOCKING | **Time**: 6-7 hours

**File**: `src/preprocessing/validation.py`

```python
# src/preprocessing/validation.py
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger("adml")

class DataValidator:
    """Validate data schema, ranges, and quality."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.validation_results = {}
    
    def validate_schema(self, df: pd.DataFrame, required_cols: List[str]) -> Tuple[bool, List[str]]:
        """Check all required columns exist."""
        missing = set(required_cols) - set(df.columns)
        
        if missing:
            logger.error(f"Missing columns: {missing}")
            return False, list(missing)
        
        logger.info(f"Schema validation passed ({len(required_cols)} columns)")
        return True, []
    
    def validate_types(self, df: pd.DataFrame, type_spec: Dict[str, str]) -> Tuple[bool, Dict]:
        """Check column data types."""
        errors = {}
        
        for col, expected_type in type_spec.items():
            if col not in df.columns:
                continue
            
            actual_type = df[col].dtype
            if actual_type != expected_type:
                errors[col] = f"Expected {expected_type}, got {actual_type}"
        
        if errors:
            logger.error(f"Type validation failed: {errors}")
            return False, errors
        
        logger.info("Type validation passed")
        return True, {}
    
    def validate_ranges(self, df: pd.DataFrame, ranges: Dict[str, Tuple[float, float]]) -> Tuple[bool, Dict]:
        """Check values are within expected ranges."""
        errors = {}
        
        for col, (min_val, max_val) in ranges.items():
            if col not in df.columns:
                continue
            
            below_min = (df[col] < min_val).sum()
            above_max = (df[col] > max_val).sum()
            
            if below_min > 0 or above_max > 0:
                errors[col] = f"Out of range: {below_min} < {min_val}, {above_max} > {max_val}"
        
        if errors:
            logger.warning(f"Range validation issues: {errors}")
            return len(errors) == 0, errors
        
        logger.info("Range validation passed")
        return True, {}
    
    def validate_missing_values(self, df: pd.DataFrame, max_missing_pct: float = 0.1) -> Tuple[bool, Dict]:
        """Check missing value percentage."""
        missing_info = {}
        
        for col in df.columns:
            missing_pct = df[col].isna().sum() / len(df)
            if missing_pct > max_missing_pct:
                missing_info[col] = missing_pct
        
        if missing_info:
            logger.warning(f"Columns with > {max_missing_pct*100}% missing: {missing_info}")
            return False, missing_info
        
        logger.info("Missing value validation passed")
        return True, {}
    
    def validate_all(self, df: pd.DataFrame, config: Dict) -> Dict:
        """Run all validations."""
        results = {
            'schema': self.validate_schema(df, config.get('required_columns', [])),
            'types': self.validate_types(df, config.get('column_types', {})),
            'ranges': self.validate_ranges(df, config.get('column_ranges', {})),
            'missing': self.validate_missing_values(df, config.get('max_missing_pct', 0.1)),
        }
        
        all_passed = all(result[0] for result in results.values())
        logger.info(f"Validation summary: {'PASSED' if all_passed else 'FAILED'}")
        
        return results
```

**Step 2**: Add validation config to `config.yaml`
```yaml
data_validation:
  required_columns:
    - TAU_bl
    - PTAU_bl
    - ABETA_bl
    - A+
    - T+
    - N+
  
  column_types:
    TAU_bl: "float64"
    PTAU_bl: "float64"
    ABETA_bl: "float64"
    A+: "int64"
    T+: "int64"
    N+: "int64"
  
  column_ranges:
    TAU_bl: [0.0, 100.0]
    PTAU_bl: [0.0, 100.0]
    ABETA_bl: [0.0, 2000.0]
  
  max_missing_pct: 0.10
```

**Deliverable**: `src/preprocessing/validation.py` + integration tests

---

#### Task 2.2: Create DATA_DICTIONARY.md 🔴
**Priority**: BLOCKING | **Time**: 4-5 hours

**File**: `docs/DATA_DICTIONARY.md`

```markdown
# Data Dictionary

## Overview
Complete description of all variables in the ADML dataset.

## Clinical Data (CSF Biomarkers)

### TAU_bl
- **Description**: Total tau at baseline (CSF)
- **Type**: float64
- **Units**: pg/mL
- **Valid Range**: 0 - 100
- **Missing**: [X%]
- **Source**: ADNI database
- **Notes**: Baseline (bl) measurement

### PTAU_bl
- **Description**: Phosphorylated tau at baseline (CSF)
- **Type**: float64
- **Units**: pg/mL
- **Valid Range**: 0 - 100
- **Missing**: [X%]
- **Source**: ADNI database

### ABETA_bl
- **Description**: Amyloid-beta 42 at baseline (CSF)
- **Type**: float64
- **Units**: pg/mL
- **Valid Range**: 0 - 2000
- **Missing**: [X%]
- **Source**: ADNI database
- **Clinical Significance**: Lower values indicate amyloid pathology

## Derived Biomarkers (ATL Framework)

### A+ (Amyloid Status)
- **Description**: Binary indicator of amyloid pathology
- **Type**: int64 (0 or 1)
- **Calculation**: 1 if ABETA_bl < 880 else 0
- **Threshold**: 880 pg/mL
- **Reference**: Buckley et al. (2023)
- **A+ = 1**: Amyloid positive (pathology present)
- **A+ = 0**: Amyloid negative (normal)

### T+ (Tau Status)
- **Description**: Binary indicator of phosphorylated tau pathology
- **Type**: int64 (0 or 1)
- **Calculation**: 1 if (PTAU_bl / ABETA_bl) > 0.028 else 0
- **Threshold**: 0.028 (ratio)
- **Reference**: Buckley et al. (2023)
- **T+ = 1**: Tau positive (pathology present)
- **T+ = 0**: Tau negative (normal)

### N+ (Neurodegeneration Status)
- **Description**: Binary indicator of neurodegeneration
- **Type**: int64 (0 or 1)
- **Calculation**: 1 if (TAU_bl / ABETA_bl) > 0.33 else 0
- **Threshold**: 0.33 (ratio)
- **Reference**: [Citation needed]
- **N+ = 1**: Neurodegeneration present
- **N+ = 0**: Neurodegeneration absent

## PET Features (120+ ROIs)

### SUVr_[ROI_NAME]
- **Description**: Standardized Uptake Value ratio for brain region
- **Type**: float64
- **Units**: Ratio (unitless)
- **Valid Range**: Typically 0.5 - 2.5
- **Source**: FDG-PET imaging (normalized to cerebellum)
- **Processing**: 
  1. DICOM files coregistered to MNI template
  2. Normalized to cerebellar uptake
  3. Interpolated to AAL3 atlas ROIs
- **Example ROIs**:
  - `SUVr_Precuneus_L.nii`: Left precuneus
  - `SUVr_Angular_R.nii`: Right angular gyrus
  - `SUVr_Temporal_Mid_L.nii`: Left middle temporal lobe
  - [Full list of 120+ ROIs in Appendix A]

## Demographics

### [Add age, sex, cognitive score, etc.]

## Feature Engineering

### Biomarker Ratios
- `ptau_ab_ratio`: PTAU_bl / ABETA_bl
- `tau_ab_ratio`: TAU_bl / ABETA_bl

---

## Data Quality Notes

- **Total Samples**: [N]
- **Missing Values**: [Handled via imputation/removal]
- **Outliers**: [Detected and handled via IQR/Z-score]
- **Train/Test Split**: 80% / 20%
- **Stratification**: Stratified by A+T+N+ status

---

## Appendix A: Full ROI List

| ROI Index | ROI Name | Hemisphere | Lobe |
|-----------|----------|-----------|------|
| 1 | Precentral | L | Frontal |
| 2 | Precentral | R | Frontal |
| ... | ... | ... | ... |
```

**Deliverable**: Complete `docs/DATA_DICTIONARY.md`

---

#### Task 2.3: Create BIOMARKER_THRESHOLDS.md 🔴
**Priority**: BLOCKING | **Time**: 3-4 hours

**File**: `docs/BIOMARKER_THRESHOLDS.md`

```markdown
# Biomarker Thresholds & ATL Framework

## Overview
This document describes the ATN (Amyloid, Tau, Neurodegeneration) biomarker framework used in this project.

## Amyloid (A+)

### Threshold
- **Marker**: CSF Amyloid-β 42 (ABETA_bl)
- **Threshold**: 880 pg/mL
- **Criterion**: A+ when ABETA_bl < 880 pg/mL
- **Interpretation**: Lower values indicate amyloid accumulation

### Rationale
- Source: Buckley et al. (2023)
- Citation: "CSF biomarkers of Alzheimer's disease concord with amyloid-β PET and predict clinical progression"
- DOI: [10.1002/alz.xxxxx]
- Section: Table 2, ROC analysis

### Validation
- **Sensitivity**: X%
- **Specificity**: Y%
- **AUC**: Z
- **Comparison to PET**: Matches amyloid-PET status in XX% of cases

### Alternative Thresholds
| Threshold (pg/mL) | Sensitivity | Specificity | Notes |
|------------------|-------------|-----------|-------|
| 800 | X% | Y% | More conservative |
| 880 | X% | Y% | **Selected** |
| 950 | X% | Y% | More liberal |

---

## Phosphorylated Tau (T+)

### Threshold
- **Marker**: CSF Phosphorylated Tau / Amyloid-β ratio (PTAU / ABETA)
- **Threshold**: 0.028 (ratio)
- **Criterion**: T+ when (PTAU_bl / ABETA_bl) > 0.028
- **Interpretation**: Higher ratio indicates tau pathology

### Rationale
- Source: Same as A+ (Buckley et al. 2023)
- Advantages of ratio:
  - Normalizes for inter-individual variability in amyloid
  - More sensitive to tau pathology
  - Better concordance with PET tau

### Validation
- **Sensitivity**: X%
- **Specificity**: Y%
- **AUC**: Z

---

## Neurodegeneration (N+)

### Threshold
- **Marker**: CSF Total Tau / Amyloid-β ratio (TAU / ABETA)
- **Threshold**: 0.33 (ratio)
- **Criterion**: N+ when (TAU_bl / ABETA_bl) > 0.33
- **Source**: [Reference needed - check your paper]

### Validation
- **Sensitivity**: X%
- **Specificity**: Y%
- **AUC**: Z

---

## ATL Interpretation

| A+ | T+ | N+ | Status | Clinical Relevance |
|----|----|----|---------|--------------------|
| 0 | 0 | 0 | Negative | Normal cognition (expected) |
| 1 | 0 | 0 | A+TN- | Amyloid alone (increased risk) |
| 1 | 1 | 0 | A+T+N- | Amyloid + tau (mild symptomatology) |
| 1 | 1 | 1 | A+T+N+ | Full AD pathology (MCI/dementia likely) |
| [Other combinations...] | | | | |

---

## Limitations

1. **CSF biomarkers** are more invasive than plasma biomarkers
2. **Thresholds** validated in ADNI cohort; may differ in other populations
3. **Ratio approach** sensitive to ABETA measurement precision
4. **Cross-sectional** design; longitudinal progression not captured here

---

## Sensitivity Analysis

We tested threshold robustness by varying cutoffs:

### Amyloid Threshold Sensitivity
[Graph showing model performance vs threshold]

### Tau Ratio Sensitivity
[Graph showing model performance vs threshold]

**Finding**: Results are relatively robust within ±10% threshold variation.

---

## References

1. Buckley RF, Rabinovici GD, et al. (2023). CSF biomarkers of Alzheimer's disease concord with amyloid-β PET...
2. [Add other key references]
```

**Deliverable**: Complete `docs/BIOMARKER_THRESHOLDS.md`

---

#### Task 2.4: Create METHODOLOGY.md 🔴
**Priority**: BLOCKING | **Time**: 5-6 hours

**File**: `docs/METHODOLOGY.md`

```markdown
# Methodology

## Overview
This document describes the complete methodology for the ADML project, including data sources, preprocessing, model architectures, and evaluation approaches.

## 1. Data Source & Cohort

### ADNI Dataset
- **Source**: Alzheimer's Disease Neuroimaging Initiative (ADNI)
- **Cohort**: [Specify which ADNI phase(s): ADNI1, ADNI2, ADNIGO, ADNI3]
- **Sample Size**: N = [XXX]
- **Age Range**: [XX-XX years]
- **Demographics**: [% male/female, age breakdown]

### Inclusion Criteria
- [List criteria]

### Exclusion Criteria
- [List criteria]

---

## 2. Data Modalities

### 2.1 CSF Biomarkers
**Collection**: Lumbar puncture at baseline
**Measures**:
- Total tau (TAU_bl)
- Phosphorylated tau (PTAU_bl)
- Amyloid-β 42 (ABETA_bl)

**Preprocessing**: 
- [Describe any harmonization/preprocessing]

### 2.2 Structural MRI
**Acquisition**: 
- Sequence: MPRAGE or T1-weighted
- Resolution: [voxel size]
- Field strength: [1.5T or 3T]

**Preprocessing**:
1. Bias field correction
2. Registration to MNI152 template
3. Segmentation (gray/white/CSF)

### 2.3 FDG-PET
**Acquisition**:
- Tracer: [18F]FDG
- Duration: [XX minutes]
- Reconstruction: [method]

**Preprocessing**:
1. Motion correction
2. Coregistration to MRI
3. Normalization to cerebellar reference region
4. ROI extraction (AAL3 atlas)

**Result**: 120+ regional standardized uptake value ratios (SUVr)

---

## 3. Biomarker Definition (ATL Framework)

[Include condensed version from BIOMARKER_THRESHOLDS.md]

---

## 4. Feature Engineering

### 4.1 Feature Selection
**Method**: mRMRe (Minimum Redundancy Maximum Relevance)
**Implementation**: mrmr Python library
**Parameters**: K = 25 features selected

**Rationale**: 
- Reduces dimensionality (120+ → 25)
- Removes redundant features
- Balances relevance and non-redundancy

### 4.2 Feature Scaling
**Method**: StandardScaler (z-score normalization)
**Formula**: $x_{scaled} = \frac{x - \mu}{\sigma}$
**Fit**: Computed on training set only
**Applied**: To both training and test sets

### 4.3 Data Split
**Train/Test Ratio**: 80% / 20%
**Stratification**: By A+T+N+ status (ensure class balance)
**Random Seed**: 42 (for reproducibility)

---

## 5. Models

### 5.1 Support Vector Machine (SVM)
**Task**: Binary classification of [outcome]
**Kernel**: Sigmoid
**Hyperparameters**:
- C = 1.0
- γ = 0.001
- class_weight = 'balanced'

**Justification**: 
- Sigmoid kernel chosen via grid search
- Hyperparameters optimized via Bayesian search (skopt)

**Reference**: Scikit-learn documentation

### 5.2 Gaussian Process
**Task**: Regression for [outcome]
**Kernel**: RBF + White noise
**Parameters**:
- α = 1e-6 (noise level)
- Normalized targets: True

**Advantages**:
- Uncertainty quantification
- Probabilistic predictions
- Small dataset suitability

### 5.3 PyTorch Neural Network
**Architecture**: [Describe layers/activation functions]
**Loss Function**: [BCE / MSE / etc.]
**Optimizer**: [Adam / SGD]
**Learning Rate**: 0.001
**Batch Size**: 32
**Epochs**: 100
**Early Stopping**: Patience = 10

---

## 6. Evaluation Metrics

### Classification Metrics
- **Accuracy**: (TP + TN) / (TP + TN + FP + FN)
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1 Score**: 2 × (Precision × Recall) / (Precision + Recall)
- **Matthews Correlation Coefficient (MCC)**: Balanced metric for imbalanced data
- **ROC-AUC**: Area under receiver operating characteristic curve

### Regression Metrics
- **Mean Squared Error (MSE)**
- **R² Score**
- **Mean Absolute Error (MAE)**

---

## 7. Statistical Testing

### Significance Tests
- [Describe any statistical tests used]

### Cross-Validation
- **Method**: Stratified 5-fold cross-validation
- **Random Seed**: 42
- **Rationale**: Ensures model stability across data subsets

---

## 8. Reproducibility

### Environment
- Python 3.9+
- Dependencies locked in requirements.txt
- Docker image available (optional)

### Random Seeds
All random operations use seed=42:
```python
np.random.seed(42)
torch.manual_seed(42)
random.seed(42)
```

### Configuration
All parameters in config.yaml

---

## 9. Limitations

1. **Cross-sectional design**: No longitudinal follow-up
2. **ADNI-specific**: May not generalize to other cohorts
3. **Lumbar puncture**: Invasive, limits population applicability
4. **PET availability**: Not all subjects have imaging
5. **Class imbalance**: [Describe if relevant]

---

## 10. Code Availability

All code available at: https://github.com/Aquila69420/adni-ml

---

## References

[Add bibliography]
```

**Deliverable**: Complete `docs/METHODOLOGY.md`

---

### Deliverables (End of Week 2)
- [x] `src/preprocessing/validation.py` (DataValidator class)
- [x] Data validation config in `config.yaml`
- [x] `docs/DATA_DICTIONARY.md` (complete data description)
- [x] `docs/BIOMARKER_THRESHOLDS.md` (threshold documentation)
- [x] `docs/METHODOLOGY.md` (complete methodology)

### Acceptance Tests
```bash
# Test 1: Validate test data
python -c "
from src.preprocessing.validation import DataValidator
import yaml
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)
validator = DataValidator(cfg)
print('Validator initialized successfully')
"

# Test 2: Docs exist and are readable
ls -l docs/{DATA_DICTIONARY,BIOMARKER_THRESHOLDS,METHODOLOGY}.md
```

---

## [Weeks 3-8 continue in next section...]

**Continue reading for**:
- Week 3: Code Consolidation & Duplication Removal
- Week 4-5: Modularization & Pipeline Creation
- Week 6-7: Testing & Quality Assurance
- Week 8: Documentation Polish & Publication

---

## Summary Table

| Week | Focus | Deliverables | Status |
|------|-------|--------------|--------|
| 1 | Foundation | config.yaml, logging, deps | ⏳ TO DO |
| 2 | Documentation | DATA_DICT, BIOMARKERS, METHODOLOGY | ⏳ TO DO |
| 3 | Consolidation | Eliminate duplicates, common functions | ⏳ TO DO |
| 4-5 | Modularization | Unified pipeline runner | ⏳ TO DO |
| 6-7 | Testing | Unit tests, integration tests | ⏳ TO DO |
| 8 | Polish | README, CI/CD, publication prep | ⏳ TO DO |

---

*Last Updated: May 2026 | Estimated Total Effort: 200-250 developer hours*
