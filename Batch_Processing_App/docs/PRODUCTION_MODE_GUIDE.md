# Production Mode Guide

## Overview

The QMRA Toolkit now includes a **Production Mode** configuration that restricts pathogen selection to norovirus only, as recommended by David Wood to align with the contract scope and ensure all risk assessments use the validated Beta-Binomial dose-response model.

## Features

### Production Mode (Default: ON)

**✅ Enabled by default** for production deployments

**Key characteristics:**
- **Pathogen Selection:** Norovirus only
- **Dose-Response Model:** Validated Beta-Binomial (exact) with GAMMALN formula
- **Validation Status:** Fully validated against David's Excel reference
- **Contract Scope:** Aligned with project deliverables

**Benefits:**
- Ensures all assessments use the validated dose-response model
- Prevents accidental use of unvalidated pathogen parameters
- Simplifies user interface and reduces confusion
- Meets contract requirements (norovirus focus)

**When to use:**
- Production deployments for public health risk assessment
- Official reports and compliance assessments
- When WHO guideline compliance is required
- Any scenario requiring validated, defensible results

### Research Mode

**⚠️ Disabled by default** - requires explicit user activation

**Key characteristics:**
- **Pathogen Selection:** All 6 pathogens available
  - norovirus (validated Beta-Binomial)
  - campylobacter (Beta-Poisson, requires validation)
  - cryptosporidium (Exponential, requires validation)
  - e_coli (Beta-Poisson/Exponential, requires validation)
  - rotavirus (Beta-Poisson, requires validation)
  - salmonella (Beta-Poisson, requires validation)
- **Warning Messages:** Clear indication that non-norovirus pathogens need validation
- **Research Purpose:** Exploratory analysis and model development

**When to use:**
- Research and development activities
- Exploratory analyses
- Model comparison studies
- Future pathogen validation work

**⚠️ IMPORTANT:** Non-norovirus pathogens have not been validated to the same standard as norovirus and should be used with caution.

## How to Use

### Web Application

1. **Launch the application:**
   ```bash
   cd Batch_Processing_App/app
   streamlit run web_app.py
   ```

2. **Configure mode in sidebar:**
   - **Production Mode:** Check the "Production Mode (Norovirus Only)" checkbox (default: ON)
   - **Research Mode:** Uncheck the checkbox to enable all pathogens

3. **Visual indicators:**
   - **Production Mode:** Green info box showing "✅ Production Mode Active"
   - **Research Mode:** Yellow warning box showing "⚠️ Research Mode Active"

### Pathogen Selection Behavior

| Assessment Type | Production Mode | Research Mode |
|----------------|----------------|---------------|
| Spatial Assessment | norovirus only | All 6 pathogens |
| Temporal Assessment | norovirus only | All 6 pathogens |
| Treatment Comparison | norovirus only | All 6 pathogens |
| Multi-Pathogen Assessment | norovirus only* | All 6 pathogens |
| Batch Scenarios | norovirus only* | All 6 pathogens |

*Multi-pathogen assessment and batch scenarios will automatically filter to norovirus-only when production mode is enabled.

## Implementation Details

### Code Changes

**File:** `Batch_Processing_App/app/web_app.py`

**Key additions:**

1. **Production mode toggle (sidebar):**
   ```python
   production_mode = st.checkbox(
       "Production Mode (Norovirus Only)",
       value=True,
       help="Enable to use only norovirus (validated per contract scope)."
   )
   ```

2. **Available pathogens logic:**
   ```python
   if production_mode:
       available_pathogens = ["norovirus"]
   else:
       available_pathogens = ["norovirus", "campylobacter", "cryptosporidium",
                             "e_coli", "rotavirus", "salmonella"]
   ```

3. **All pathogen selection boxes updated:**
   - Spatial Assessment: `st.selectbox("Pathogen:", available_pathogens)`
   - Temporal Assessment: `st.selectbox("Pathogen:", available_pathogens)`
   - Treatment Comparison: `st.selectbox("Pathogen:", available_pathogens)`
   - Multi-Pathogen Assessment: `st.multiselect(..., available_pathogens, default=["norovirus"])`

### Default Behavior

- **Web App:** Production Mode is **ON** by default
- **Command-line scripts:** Use norovirus with Beta-Binomial by default (via `pathogen_database.py`)
- **API/Library:** Norovirus defaults to Beta-Binomial model

## Validation Status

### Norovirus (Production-Ready ✅)

**Dose-Response Model:** Beta-Binomial (exact)

**Mathematical Formula:**
```
P(infection) = 1 - exp(gammaln(β+dose) + gammaln(α+β) - gammaln(α+β+dose) - gammaln(β))
```

**Parameters:**
- α (alpha) = 0.04
- β (beta) = 0.055

**Validation:**
- ✅ Verified against David Wood's Excel (betaBinomial.xlsx)
- ✅ Exact match to reference values (100% accuracy)
- ✅ Validated against Bell Island QMRA (McBride 2017)
- ✅ Referenced to Teunis et al. (2008)

**Verification Results:**
| Dose | Beta-Binomial (Our Implementation) | Reference (David's Excel) | Match |
|------|-----------------------------------|---------------------------|-------|
| 1 | 0.421053 | 0.421053 | ✅ EXACT |
| 10 | 0.480735 | 0.480735 | ✅ EXACT |
| 100 | 0.527157 | 0.527157 | ✅ EXACT |

### Other Pathogens (Research Mode ⚠️)

**Status:** Available for research but require additional validation

| Pathogen | Model Type | Status | Notes |
|----------|-----------|--------|-------|
| Campylobacter | Beta-Poisson | ⚠️ Not validated | Parameters from literature, needs verification |
| Cryptosporidium | Exponential | ⚠️ Not validated | Based on Haas et al. (1996) |
| E. coli O157:H7 | Beta-Poisson/Exponential | ⚠️ Not validated | Multiple model options |
| Rotavirus | Beta-Poisson | ⚠️ Not validated | Ward et al. (1986) parameters |
| Salmonella | Beta-Poisson | ⚠️ Not validated | Haas et al. (1999) parameters |

**Recommendation from David Wood:**
> "I recommend that you simplify the model to do one thing and do one thing well, as agreed in the contract, which is estimating norovirus risk. The other pathogens are nice to have but outside scope of the contract and we will have to do quite a bit of work to get those right, so forget about them for now."

## Deployment Recommendations

### Production Deployment

For production use (official risk assessments, compliance reporting):

1. **Default Configuration:** Keep Production Mode ON
2. **User Training:** Inform users that only norovirus is validated
3. **Documentation:** Include disclaimer about pathogen validation status
4. **Quality Assurance:** Verify all outputs use Beta-Binomial for norovirus

### Research Deployment

For research and development:

1. **Enable Research Mode:** Allow users to toggle in sidebar
2. **Clear Warnings:** Ensure warning messages are visible
3. **Documentation:** Document validation status of all pathogens
4. **Peer Review:** Subject non-norovirus results to additional scrutiny

## Frequently Asked Questions

### Why is Production Mode the default?

**Answer:** Following David Wood's recommendation to focus on norovirus (contract scope) and ensure all assessments use the validated Beta-Binomial dose-response model. This prevents accidental use of unvalidated pathogen parameters.

### Can I still use other pathogens?

**Answer:** Yes, disable Production Mode in the sidebar to access Research Mode with all 6 pathogens. However, non-norovirus pathogens require additional validation before use in official assessments.

### What's wrong with Beta-Poisson for norovirus?

**Answer:** Beta-Poisson is an **approximation** that is only valid when β >> 1. For norovirus, β = 0.055 << 1, making the approximation invalid. Beta-Poisson underestimates norovirus infection risk by **2-4× at relevant doses**. The exact Beta-Binomial model must be used instead.

### How do I validate other pathogens?

**Answer:** Contact David Wood to discuss validation requirements. Generally requires:
1. Literature review for dose-response parameters
2. Validation against experimental data
3. Comparison with established Excel models
4. Peer review of implementation
5. Documentation of assumptions and limitations

### Can I change the default mode?

**Answer:** Yes, modify line 393 in `web_app.py`:
```python
production_mode = st.checkbox(
    "Production Mode (Norovirus Only)",
    value=True,  # Change to False for research mode default
    ...
)
```

**⚠️ NOT RECOMMENDED** for production deployments.

## References

1. **Teunis et al. (2008)** - "Norwalk virus: How infectious is it?" - Norovirus dose-response parameters
2. **McBride (2017)** - Bell Island QMRA, Appendix B (Equation 5, page 34) - Beta-Binomial implementation
3. **David Wood's betaBinomial.xlsx** - Reference validation data
4. **WHO (2016)** - Quantitative Microbial Risk Assessment guidelines

## Change Log

### Version 1.0 (November 12, 2025)
- Initial implementation of Production Mode
- Default: Production Mode ON (norovirus only)
- Research Mode available with explicit user activation
- All pathogen selection dropdowns updated
- Informational messages added to sidebar
- Documentation updated

## Contact

For questions about Production Mode or pathogen validation:

**Technical Lead:** David Wood (NIWA)
**Developer:** Reza Moghaddam (NIWA)
**Documentation:** See CRITICAL_ASSESSMENT_REPORT.md for technical details

---

**Last Updated:** November 12, 2025
**Version:** 1.0
**Status:** Production Ready ✅
