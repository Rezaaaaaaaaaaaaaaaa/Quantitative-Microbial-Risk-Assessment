# Excel vs Python Implementation Gap Analysis

**Date**: November 17, 2025
**Purpose**: Ensure Python app EXACTLY replicates Excel calculations - no more, no less

---

## Excel File Calculations (from QMRA_Shellfish_191023_Nino_SUMMER.xlsx)

### 1. Parameters (Global data sheet)

| Parameter | Excel Cell | Excel Value | Source |
|-----------|-----------|-------------|---------|
| Pathogen | B3 | Norovirus | User input |
| Log10 Removal (LRV) | C6 | 2 | WWTP treatment |
| **α (alpha)** | **C9** | **0.04** | Teunis et al. 2008 |
| **β (beta)** | **C10** | **0.055** | Teunis et al. 2008 |
| **H (Harmonization)** | **C11** | **18.5** | McBride et al. 2013 |
| **P (Proportion susceptible)** | **C12** | **0.74** | McBride et al. 2013 |
| **Pr(ill\|inf)** | **C13** | **0.5** | McBride et al. 2013 |

### 2. Calculation Flow (Risk Model sheet)

**Step 1: Concentration after treatment** (Column C)
```excel
C9 = Raw_Concentration / 10^LRV
```

**Step 2: Dose calculation** (Column D)
```excel
D9 = C9 * BAF / Volume
```
Where:
- C9 = Pathogen concentration (organisms/L)
- BAF = Bioaccumulation Factor (from BAF calculation sheet)
- Volume = Volume consumed (L)

**Step 3: Fractional organism handling** (Column G)
```excel
G9 = INT(F9) + _xll.RiskBinomial(1, F9-INT(F9))
```
This splits dose into:
- Integer part: INT(dose)
- Fractional part: Binomial(1, fractional_dose)

**Step 4: Infection probability** (Column H) ✅ VERIFIED
```excel
H9 = MAX(1-EXP((GAMMALN(beta+G9)+GAMMALN(alpha+beta)-GAMMALN(alpha+beta+G9)-GAMMALN(beta))),0)
```

**Step 5: Infection status** (Column I)
```excel
I9 = _xll.RiskBinomial(1, H9)
```
Binary outcome: 0 or 1

**Step 6: Illness status** (Column J)
```excel
J9 = IF(I9=1, _xll.RiskBinomial(1, Pr(ill|inf)), 0)
```
If infected (I9=1), then Binomial(1, 0.5) for illness

**Step 7: Annual risk**
```excel
Annual_Risk = 1 - (1 - P_infection_per_exposure)^frequency_per_year
```

**Step 8: Illness probability**
```excel
P(illness) = P(infection) * Pr(ill|inf) * P(susceptible)
            = P(infection) * 0.5 * 0.74
            = P(infection) * 0.37
```

### 3. Hockey-Stick Distribution (separate sheet)

**Purpose**: Model pathogen concentration distributions

**Excel Implementation**: Uses Log-Logistic distribution with truncation

**Parameters** (need to extract from Excel):
- Minimum concentration
- Median concentration
- Maximum concentration
- Shape parameter

### 4. BAF Calculation (separate sheet)

**Purpose**: Calculate Bioaccumulation Factor for shellfish

**Excel formula** (need to extract exact formula)

### 5. Monte Carlo Settings (Settings sheet)

**@RISK Settings**:
- Iterations: 10,000
- Sampling method: Latin Hypercube (need to verify)
- Random seed: Variable or fixed?

---

## Python Implementation Status

### ✅ EXACT MATCH - No Changes Needed

1. **Beta-Binomial Formula** ([dose_response.py:269-277](Batch_Processing_App/qmra_core/dose_response.py#L269-L277))
   - Formula: EXACT match (0.00000000% difference)
   - Parameters: α=0.04, β=0.055 ✅

2. **Parameters** ([pathogen_parameters.json](Batch_Processing_App/qmra_core/data/pathogen_parameters.json))
   - Alpha: 0.04 ✅
   - Beta: 0.055 ✅
   - Reference: Teunis et al. 2008 ✅

3. **Monte Carlo Iterations**
   - Default: 10,000 ✅

### ❓ NEEDS VERIFICATION

1. **Annual Risk Formula**
   - Excel: `1 - (1 - P_inf)^frequency`
   - Python: **NEED TO VERIFY EXACT FORMULA**
   - Location: Need to check monte_carlo.py or batch_processor.py

2. **Fractional Organism Handling**
   - Excel: `INT(dose) + Binomial(1, dose-INT(dose))`
   - Python: **NEED TO VERIFY**
   - This ensures proper handling of fractional pathogens

3. **Illness Probability**
   - Excel: `P(ill|inf) = 0.5`
   - Excel: `P(susceptible) = 0.74`
   - Excel: `P(illness) = P(inf) * 0.5 * 0.74`
   - Python: Has illness_model.py but **NEED TO VERIFY EXACT VALUES**

4. **Harmonization Factor (H = 18.5)**
   - Excel: Used in Global data C11
   - Python: **NEED TO CHECK IF USED**
   - Purpose: **NEED TO UNDERSTAND**

5. **Dose Calculation**
   - Excel: `concentration * BAF / volume`
   - Python: **NEED TO VERIFY EXACT FORMULA**

6. **Treatment (LRV)**
   - Excel: `Treated_Conc = Raw_Conc / 10^LRV`
   - Python: **NEED TO VERIFY EXACT FORMULA**

### ❌ MISSING - Needs Implementation

1. **Hockey-Stick Distribution**
   - Excel: Has dedicated sheet with Log-Logistic parameters
   - Python: batch_processor has `use_hockey_pathogen=False` flag
   - Status: **NEED TO IMPLEMENT EXACT EXCEL VERSION**

2. **BAF (Bioaccumulation Factor) Calculation**
   - Excel: Has dedicated BAF calculation sheet
   - Python: **NEED TO CHECK IF IMPLEMENTED**
   - **NEED TO EXTRACT EXACT FORMULA FROM EXCEL**

---

## Action Items

### Priority 1: Verify Existing Implementations

- [ ] Check annual risk formula in Python
- [ ] Check fractional organism handling in Python
- [ ] Verify illness probability uses P(ill|inf)=0.5 and P(susceptible)=0.74
- [ ] Check dose calculation formula
- [ ] Check treatment LRV formula
- [ ] Understand purpose of Harmonization Factor H=18.5

### Priority 2: Extract Missing Excel Formulas

- [ ] Extract Hockey-Stick distribution parameters from Excel
- [ ] Extract BAF calculation formula from Excel
- [ ] Document any other Excel calculations not yet identified

### Priority 3: Implement Missing Features

- [ ] Implement Hockey-Stick distribution (exact Excel match)
- [ ] Implement BAF calculation (exact Excel match)
- [ ] Implement Harmonization Factor if used

### Priority 4: Remove Extra Features

- [ ] Identify any Python features NOT in Excel
- [ ] Remove or disable features that Excel doesn't have
- [ ] Ensure app does "no more, no less" than Excel

---

## Next Steps

1. **Read Python source code** to verify formulas
2. **Extract remaining Excel formulas** (Hockey-Stick, BAF)
3. **Create side-by-side comparison** of each calculation
4. **Implement missing features** with exact Excel formulas
5. **Run comprehensive validation** across all calculations
6. **Document final verification** that Python = Excel exactly

---

**Status**: Gap analysis in progress
**Target**: 100% Excel replication - no more, no less
