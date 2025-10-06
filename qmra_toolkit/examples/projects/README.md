# QMRA Toolkit - Example Projects

This directory contains example project files demonstrating various QMRA assessment scenarios. These examples are designed to help you learn the toolkit and understand different application contexts.

---

## Available Example Projects

### 1. 🏖️ **Beach Swimming Risk Assessment**
**File:** `beach_swimming_assessment.json`

**Scenario:** Public health risk assessment for swimming at Mission Bay Beach, Auckland during summer season.

**Key Features:**
- **Pathogen:** Norovirus
- **Exposure Route:** Primary contact (recreational swimming)
- **Population:** 50,000 summer beach visitors
- **Application:** Recreational water quality monitoring

**Learning Points:**
- Basic single-pathogen assessment
- Recreational water exposure calculations
- Seasonal risk evaluation
- Beach management decision support

**Use Case:** Local councils managing beach water quality

---

### 2. 🚰 **Municipal Drinking Water Safety**
**File:** `drinking_water_safety.json`

**Scenario:** Cryptosporidium risk assessment for Wellington municipal water supply.

**Key Features:**
- **Pathogen:** Cryptosporidium parvum
- **Exposure Route:** Drinking water consumption
- **Population:** 200,000 urban water consumers
- **Application:** Regulatory compliance assessment

**Learning Points:**
- Drinking water regulatory compliance (NZ standards)
- Chlorine-resistant pathogen assessment
- Daily exposure frequency modeling
- Treatment barrier evaluation (UV disinfection)

**Use Case:** Water utilities ensuring drinking water safety

---

### 3. 🏭 **Wastewater Treatment Upgrade Evaluation**
**File:** `wastewater_treatment_comparison.json`

**Scenario:** Multi-pathogen assessment comparing current secondary vs. proposed tertiary treatment at Christchurch WWTP.

**Key Features:**
- **Pathogens:** Norovirus, Campylobacter, Cryptosporidium (multi-pathogen)
- **Exposure Route:** Primary contact in estuary
- **Population:** 75,000 recreational users
- **Application:** Treatment optimization and cost-benefit analysis

**Learning Points:**
- Multi-pathogen assessment workflow
- Treatment scenario comparison
- Pathogen-specific log reduction values
- Cost-benefit evaluation framework
- Different LRVs for different pathogens

**Use Case:** Wastewater utilities evaluating treatment upgrades

---

### 4. 🦪 **Shellfish Harvesting Area Risk**
**File:** `shellfish_consumption_risk.json`

**Scenario:** Norovirus risk from recreational shellfish harvesting in Coromandel Peninsula.

**Key Features:**
- **Pathogen:** Norovirus (bioaccumulation in shellfish)
- **Exposure Route:** Shellfish consumption
- **Population:** 10,000 recreational harvesters
- **Application:** Food safety and harvesting area management

**Learning Points:**
- Bioaccumulation factor calculations
- Seasonal variation in risk
- Multiple management options evaluation
- Food safety regulatory framework
- Risk communication strategies

**Use Case:** Food safety authorities managing shellfish harvesting areas

---

## How to Use Example Projects

### Method 1: Desktop GUI

1. **Launch the GUI:**
   ```bash
   python launch_enhanced_gui.py
   ```

2. **Open Example:**
   - Click: **File** → **Open Project**
   - Navigate to: `qmra_toolkit/examples/projects/`
   - Select an example `.json` file
   - Click **Open**

3. **Explore the Project:**
   - Review pre-filled parameters in each tab
   - Note the pathogen, exposure route, and population settings
   - Check treatment scenarios (if applicable)

4. **Run Assessment:**
   - Navigate to **Assessment Parameters** tab
   - Click **Run Assessment** button
   - View results in **Results** tab
   - Generate plots in **Visualizations** tab

5. **Modify and Experiment:**
   - Change parameters to see how results vary
   - Try different pathogens or exposure routes
   - Adjust treatment LRVs
   - Compare scenarios

### Method 2: Web Application

1. **Launch the Web App:**
   ```bash
   streamlit run web_app.py
   ```

2. **Load Example:**
   - Click **📂 Load Project** in sidebar
   - Select example file from `examples/projects/`
   - Review loaded parameters

3. **Run Assessment:**
   - Navigate through pages to review settings
   - Go to **🧬 Assessment** page
   - Click **🚀 Run Assessment**
   - View interactive results and visualizations

### Method 3: Command Line (Advanced)

```bash
cd qmra_toolkit

# Load and run example
python src/qmra_toolkit.py --load examples/projects/beach_swimming_assessment.json --run --report

# Or use batch processing
python src/qmra_toolkit.py batch --projects examples/projects/*.json
```

---

## Understanding the JSON Structure

Each example project file contains:

### Project Information
```json
{
  "project_info": {
    "project_name": "Descriptive name",
    "assessor_name": "Your name",
    "client_name": "Organization",
    "assessment_date": "YYYY-MM-DD",
    "description": "Brief description",
    "location": "Geographic location",
    "project_type": "Category"
  }
}
```

### Population Data
```json
{
  "population": {
    "at_risk": 50000,
    "description": "Who is at risk",
    "demographics": "Age groups, vulnerabilities"
  }
}
```

### Pathogen Configuration
```json
{
  "pathogen": {
    "primary": "norovirus",
    "description": "Details",
    "multi_pathogen": false,
    "secondary_pathogens": []
  }
}
```

### Exposure Parameters
```json
{
  "exposure": {
    "route": "primary_contact",
    "concentration": 1000.0,
    "volume": 100.0,
    "frequency": 7
  }
}
```

### Treatment Scenarios
```json
{
  "treatment": {
    "current": {
      "type": "Secondary Treatment",
      "lrv": 1.5
    },
    "proposed": {
      "type": "Tertiary Treatment",
      "lrv": 3.5
    }
  }
}
```

---

## Modifying Examples for Your Project

1. **Copy an Example:**
   ```bash
   cp beach_swimming_assessment.json my_project.json
   ```

2. **Edit Project Info:**
   - Change project name, assessor, client
   - Update location and description

3. **Adjust Parameters:**
   - Modify concentration based on your monitoring data
   - Update population at risk
   - Change exposure frequency for your scenario

4. **Update Treatment:**
   - Reflect your actual treatment processes
   - Use appropriate LRVs for your system

5. **Save and Run:**
   - Save your modified project
   - Load in GUI or web app
   - Run assessment with your data

---

## Example Comparison Table

| Example | Pathogen | Route | Population | Complexity | Key Learning |
|---------|----------|-------|------------|------------|--------------|
| Beach Swimming | Norovirus | Primary contact | 50,000 | ⭐ Basic | Recreational water assessment |
| Drinking Water | Cryptosporidium | Drinking water | 200,000 | ⭐⭐ Intermediate | Regulatory compliance |
| WWTP Upgrade | Multi-pathogen | Primary contact | 75,000 | ⭐⭐⭐ Advanced | Multi-pathogen & cost-benefit |
| Shellfish Harvest | Norovirus | Shellfish | 10,000 | ⭐⭐⭐ Advanced | Food safety & bioaccumulation |

---

## Learning Path

### Beginner Path:
1. **Start with:** Beach Swimming Assessment
   - Simplest scenario
   - Single pathogen
   - Clear exposure route

2. **Progress to:** Drinking Water Safety
   - Regulatory context
   - Different pathogen (Cryptosporidium)
   - Daily exposure pattern

### Intermediate Path:
3. **Try:** Wastewater Treatment Comparison
   - Multi-pathogen assessment
   - Treatment scenario comparison
   - Cost considerations

### Advanced Path:
4. **Explore:** Shellfish Harvesting Risk
   - Bioaccumulation factors
   - Seasonal variations
   - Multiple management options
   - Complex decision framework

---

## Validation and Quality Assurance

All example projects have been:
- ✅ Peer-reviewed for technical accuracy
- ✅ Based on real-world monitoring data ranges
- ✅ Validated against published QMRA studies
- ✅ Aligned with NZ regulatory frameworks
- ✅ Tested in both GUI and web app interfaces

---

## Creating Your Own Examples

To contribute additional examples:

1. **Identify Unique Scenario:**
   - Different pathogen/route combination
   - Novel application context
   - Important use case

2. **Use Template:**
   ```bash
   cp beach_swimming_assessment.json my_example.json
   ```

3. **Populate with Realistic Data:**
   - Use actual monitoring data ranges
   - Reference published studies
   - Include proper documentation in notes

4. **Document Thoroughly:**
   - Add detailed description
   - Explain key assumptions
   - Provide context and references

5. **Test and Validate:**
   - Load in GUI and web app
   - Run assessment
   - Verify results are reasonable
   - Compare to literature if available

6. **Share:**
   - Add to examples directory
   - Update this README
   - Consider contributing to NIWA repository

---

## Support and Resources

### Documentation:
- **Full User Manual:** `qmra_toolkit/docs/USER_MANUAL.md`
- **Web App Guide:** `qmra_toolkit/WEB_APP_README.md`
- **Quick Start:** Help menu in GUI or web app

### Example Usage Questions:
- How to interpret results? → See USER_MANUAL.md "Understanding Results"
- How to modify parameters? → See "Modifying Examples" section above
- What concentration to use? → See Concentration Helper (📊 button in GUI)

### Technical Support:
- NIWA QMRA Team
- GitHub Issues: [Repository URL]
- Email: [Contact Information]

---

## References

Example projects based on:

1. **WHO (2011).** Guidelines for Drinking-water Quality (4th ed.)
2. **Ministry of Health (2008).** Drinking-water Standards for New Zealand 2005 (Revised 2008)
3. **Haas, C. N., Rose, J. B., & Gerba, C. P. (2014).** Quantitative Microbial Risk Assessment (2nd ed.)
4. **McBride, G. B., et al. (2013).** Discharge-related changes in bathing water quality. Water Research.
5. **Soller, J. A., et al. (2010).** Estimated human health risks from recreational exposures. Environmental Science & Technology.

---

**Happy Learning! 🚀**

Use these examples as starting points for your own QMRA assessments.

© 2025 NIWA - QMRA Assessment Toolkit
