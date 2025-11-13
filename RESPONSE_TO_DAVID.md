# Email Response to David

---

**To:** David Wood
**From:** Reza Moghaddam
**Subject:** Re: QMRA Code Review - Beta-Binomial Implementation
**Date:** November 13, 2025

---

Hi David,

Thank you for your email and the betaBinomial.xlsx spreadsheet. Good news - I've reviewed the code and **the Beta-Binomial model is already correctly implemented**.

## Verification Results

The code uses the exact GAMMALN formula you expected and produces **identical results** to your Excel:

| Dose | Our Code | Your Excel | Match |
|------|----------|------------|-------|
| 1    | 0.421053 | 0.421053   | ✅ |
| 10   | 0.480735 | 0.480735   | ✅ |
| 100  | 0.527157 | 0.527157   | ✅ |

Norovirus automatically defaults to Beta-Binomial model. The Monte Carlo structure follows standard QMRA approach (iterations = uncertainty scenarios, annual risk = 1-(1-P)^n).

Following your recommendation, I've also implemented **Production Mode** - now defaults to norovirus-only with other pathogens requiring explicit opt-in.

## Next Steps

I'd like to schedule a **30 min call** to:
- Walk through the implementation together
- Validate relative risks against your Excel model
- Confirm everything matches your expectations

**Available:** Thu-Fri this week, 9am-5pm NZDT

Can you share your Excel QMRA model for comparison?

Best regards,
Reza

**Mobile:** [Your phone] | **Email:** reza.moghaddam@niwa.co.nz
