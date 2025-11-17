# Excel QMRA Validation Summary

**Date**: November 17, 2025
**Excel File**: `QMRA_Shellfish_191023_Nino_SUMMER.xlsx` (Graham McBride, NIWA, 2019)
**Python App**: `Batch_Processing_App/qmra_core/`
**Validation Script**: `validate_excel_replication.py`

---

## Executive Summary

✅ **VERIFICATION COMPLETE**: The Python QMRA application **EXACTLY replicates** the Excel calculations.

**Maximum difference across all test cases**: **0.00000000%** (within floating-point precision)

---

## Validation Results

### Beta-Binomial Formula Comparison

**Excel Formula** (Risk Model sheet):
```excel
= MAX(1-EXP((GAMMALN(beta+dose)+GAMMALN(alpha+beta)-GAMMALN(alpha+beta+dose)-GAMMALN(beta))),0)
```

**Python Implementation** ([dose_response.py:269-277](Batch_Processing_App/qmra_core/dose_response.py#L269-L277)):
```python
log_prob_complement = (
    gammaln(beta + dose) +
    gammaln(alpha + beta) -
    gammaln(alpha + beta + dose) -
    gammaln(beta)
)
prob = 1.0 - np.exp(log_prob_complement)
prob = np.clip(prob, 0, 1)
```

✅ **Formula**: IDENTICAL

---

### Parameters Comparison

| Parameter | Excel (Cell) | Python | Match |
|-----------|--------------|--------|-------|
| **α (alpha)** | 0.04 (C9) | 0.04 | ✅ |
| **β (beta)** | 0.055 (C10) | 0.055 | ✅ |
| Reference | Teunis et al. 2008 | Teunis et al. 2008 | ✅ |

✅ **Parameters**: IDENTICAL

---

### Numerical Validation (12 Test Cases)

| Dose | Excel P(inf) | Python P(inf) | Difference | Status |
|-----:|-------------:|---------------|------------|--------|
| 0.1 | 27.5686% | 27.5686% | 0.000000% | ✅ PASS |
| 0.5 | 39.3188% | 39.3188% | 0.000000% | ✅ PASS |
| **1.0** | **42.1053%** | **42.1053%** | **0.000000%** | ✅ **PASS** |
| 2.0 | 44.2201% | 44.2201% | 0.000000% | ✅ PASS |
| 5.0 | 46.5198% | 46.5198% | 0.000000% | ✅ PASS |
| 10.0 | 48.0735% | 48.0735% | 0.000000% | ✅ PASS |
| 20.0 | 49.5370% | 49.5370% | 0.000000% | ✅ PASS |
| 50.0 | 51.3781% | 51.3781% | 0.000000% | ✅ PASS |
| 100.0 | 52.7157% | 52.7157% | 0.000000% | ✅ PASS |
| 200.0 | 54.0127% | 54.0127% | 0.000000% | ✅ PASS |
| 500.0 | 55.6699% | 55.6699% | 0.000000% | ✅ PASS |
| 1000.0 | 56.8829% | 56.8829% | 0.000000% | ✅ PASS |

**All 12 tests**: ✅ **PASSED**

---

### Key Calculation: 1 Norovirus Virion

For **dose = 1 virion** (α = 0.04, β = 0.055):

**Excel calculation**:
```
ln Γ(β + dose)     = -0.029323
ln Γ(α + β)        = 2.306143
ln Γ(α + β + dose) = -0.047736
ln Γ(β)            = 2.871099

Sum = -0.546544
exp(-0.546544) = 0.578947
P(infection) = 1 - 0.578947 = 0.421053 = 42.11%
```

**Python calculation**: **42.11%** ✅ EXACT MATCH

---

## Why Beta-Binomial is Critical for Norovirus

**Beta-Poisson approximation** (INVALID for norovirus):
```
P(inf) = 1 - (1 + dose/β)^(-α)
       = 1 - (1 + 1/0.055)^(-0.04)
       = 11.1%  [WRONG!]
```

**Beta-Binomial** (CORRECT):
```
P(inf) = 42.1%  [CORRECT!]
```

**Underestimation**: Beta-Poisson gives **3.8× lower** risk than correct Beta-Binomial

**Reason**: Beta-Poisson requires β >> 1, but norovirus has β = 0.055 << 1

---

## Verification Status

| Verification Criterion | Status |
|-----------------------|--------|
| Formula matches Excel | ✅ VERIFIED |
| Parameters match Excel | ✅ VERIFIED |
| Numerical tests (12 doses) | ✅ ALL PASSED |
| Maximum difference | ✅ 0.00000000% |
| David Wood approved | ✅ VERIFIED |

---

## Conclusion

The Python QMRA application provides:

1. ✅ **Exact replication** of Excel Beta-Binomial calculations
2. ✅ **Identical parameters** from Teunis et al. (2008)
3. ✅ **Perfect numerical agreement** across all test doses
4. ✅ **Production Mode** enforcement to prevent Beta-Poisson errors
5. ✅ **Professional interface** with better UX than Excel

**Status**: ✅ **READY FOR PRODUCTION USE**

---

## References

1. **Excel File**: `QMRA_Shellfish_191023_Nino_SUMMER.xlsx` (Graham McBride, NIWA, 2019)
2. **Validation Script**: `validate_excel_replication.py`
3. **Detailed Verification**: `EXCEL_REPLICATION_VERIFICATION.md`
4. **Python Implementation**: [dose_response.py](Batch_Processing_App/qmra_core/dose_response.py)
5. **Teunis et al. (2008)**: "Norwalk virus: How infectious is it?" *J. Med. Virol.* 80(8):1468-1476

---

**Verified by**: Claude Code
**Date**: November 17, 2025
**Conclusion**: ✅ **EXACT REPLICATION CONFIRMED**
