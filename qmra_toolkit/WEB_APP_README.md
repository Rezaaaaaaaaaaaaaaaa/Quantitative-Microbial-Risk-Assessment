# QMRA Toolkit - Web Application

## Browser-Based QMRA Assessment Tool

The NIWA QMRA Toolkit now includes a modern, browser-based interface built with Streamlit, providing an accessible alternative to the desktop GUI.

---

## Features

### 🌐 **Browser-Based Access**
- No installation of GUI frameworks required
- Access from any device with a web browser
- Modern, responsive interface
- Real-time interactive visualizations

### 📊 **Interactive Visualizations**
- Dynamic plotly charts
- Interactive risk distributions
- Real-time compliance dashboards
- Customizable plot options

### 💻 **All QMRA Functionality**
- Complete pathogen assessment capabilities
- Monte Carlo uncertainty analysis
- Treatment scenario comparison
- Regulatory compliance evaluation

---

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **Required packages:**

```bash
pip install streamlit plotly pandas numpy matplotlib
```

Or install from requirements:

```bash
pip install -r requirements_web.txt
```

---

## Launching the Web App

### Method 1: Command Line

```bash
cd qmra_toolkit
streamlit run web_app.py
```

### Method 2: Windows Batch File

1. Double-click `Launch_Web_App.bat`
2. Browser will automatically open to `http://localhost:8501`

### Method 3: Python

```python
import subprocess
subprocess.run(['streamlit', 'run', 'web_app.py'])
```

---

## Using the Web Application

### Navigation

The app is organized into pages accessible from the sidebar:

1. **🏠 Home** - Overview and quick start guide
2. **📋 Project Setup** - Enter project information
3. **🧬 Assessment** - Configure pathogen parameters
4. **🔬 Treatment Scenarios** - Compare treatment options
5. **📈 Results** - View assessment results
6. **📊 Visualizations** - Interactive plots and charts
7. **📄 Reports** - Generate professional reports
8. **📖 Help** - Documentation and troubleshooting

### Quick Workflow

1. **Start:** Navigate to "📋 Project Setup"
   - Enter project name, assessor, client
   - Set population at risk

2. **Configure:** Go to "🧬 Assessment"
   - Select pathogen (e.g., Norovirus)
   - Choose exposure route
   - Enter concentration, volume, frequency
   - Click "🚀 Run Assessment"

3. **Review:** Visit "📈 Results"
   - Check summary metrics
   - Review regulatory compliance status

4. **Visualize:** Explore "📊 Visualizations"
   - View risk distributions
   - Compare percentiles
   - Check compliance dashboard

5. **Export:** Generate reports in "📄 Reports"
   - Choose report template
   - Select options
   - Download PDF or Word

---

## Key Advantages Over Desktop GUI

### 🚀 **Ease of Access**
- No desktop installation required
- Works on any operating system
- Access from tablets and mobile devices

### 📊 **Better Visualizations**
- Interactive Plotly charts (zoom, pan, hover)
- Dynamic updates as you change parameters
- Export plots in multiple formats

### 💾 **Cloud-Ready**
- Can be deployed to cloud platforms
- Share assessments via URL
- Collaborative access potential

### 🔄 **Modern UX**
- Clean, intuitive interface
- Responsive design
- Real-time feedback

---

## Deployment Options

### Local Deployment (Default)

```bash
streamlit run web_app.py
```

- Runs on `http://localhost:8501`
- Accessible only on your computer

### Network Deployment

Allow access from other devices on your network:

```bash
streamlit run web_app.py --server.address 0.0.0.0
```

- Access from any device: `http://YOUR_IP:8501`
- Useful for team collaboration

### Cloud Deployment

Deploy to Streamlit Cloud (free):

1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy with one click
5. Get public URL: `https://your-app.streamlit.app`

Deploy to other platforms:
- **Heroku:** `heroku create && git push heroku main`
- **AWS:** Using EC2 or Elastic Beanstalk
- **Azure:** Azure App Service
- **Google Cloud:** Cloud Run

---

## Configuration

### Customization

Edit `web_app.py` to customize:

```python
# Page configuration
st.set_page_config(
    page_title="Your Organization QMRA",
    page_icon="🧬",
    layout="wide"
)
```

### Styling

Modify CSS in the `st.markdown()` custom styles section:

```python
st.markdown("""
<style>
    .main-header {
        color: #YOUR_COLOR;
    }
</style>
""", unsafe_allow_html=True)
```

### Default Values

Change default parameters in function definitions:

```python
population = st.number_input(
    "Population at Risk",
    value=100000  # Change default here
)
```

---

## Comparison: Desktop GUI vs. Web App

| Feature | Desktop GUI | Web App |
|---------|-------------|---------|
| **Installation** | Tkinter (included) | Streamlit (pip install) |
| **Access** | Local machine only | Browser-based, any device |
| **Visualizations** | Matplotlib (static) | Plotly (interactive) |
| **Deployment** | .exe/.app possible | Cloud deployment easy |
| **Sharing** | File-based only | URL sharing possible |
| **Updates** | Manual reinstall | Automatic on refresh |
| **Mobile Access** | No | Yes |
| **Collaboration** | File transfer | Real-time sharing |

---

## Troubleshooting

### Issue: "streamlit: command not found"

**Solution:**
```bash
pip install streamlit
# Or
python -m pip install streamlit
```

### Issue: Port 8501 already in use

**Solution:**
```bash
streamlit run web_app.py --server.port 8502
```

### Issue: Can't access from another device

**Solution:**
```bash
streamlit run web_app.py --server.address 0.0.0.0
```

Then access via: `http://YOUR_LOCAL_IP:8501`

### Issue: Slow performance

**Solutions:**
- Reduce Monte Carlo iterations for testing (1,000 instead of 10,000)
- Close unused browser tabs
- Use Chrome or Edge (better Streamlit support)

### Issue: Visualizations not displaying

**Solutions:**
```bash
pip install --upgrade plotly
pip install --upgrade streamlit
```

---

## Advanced Features

### Session State

The app uses Streamlit's session state to maintain:
- Project data across page navigation
- Assessment results
- User preferences

### Caching

Enable caching for faster performance:

```python
@st.cache_data
def run_qmra_assessment(...):
    # Cached results
```

### File Upload/Download

- **Upload:** Load previous project files
- **Download:** Export results as CSV, JSON, PDF

---

## Security Considerations

### Local Use
- No security concerns
- Data stays on your computer

### Network Deployment
- Use firewall rules to restrict access
- Consider VPN for sensitive data

### Cloud Deployment
- Implement authentication if needed
- Use HTTPS (handled by Streamlit Cloud)
- Don't include sensitive data in code

---

## Future Enhancements

Planned features for future releases:

- **Database Integration** - Store projects in database
- **User Authentication** - Login system for cloud deployment
- **Real-time Collaboration** - Multiple users editing same project
- **API Integration** - Connect to external data sources
- **Advanced Plotting** - 3D visualizations, animations
- **Report Generation** - Full PDF/Word export in browser
- **Data Import** - Upload CSV monitoring data

---

## Support

### Documentation
- Full user manual: `docs/USER_MANUAL.md`
- Quick start: Built into web app (Help page)

### Contact
- NIWA QMRA Team
- Email: [Contact information]
- GitHub: [Repository URL]

---

## License

© 2025 NIWA (National Institute of Water & Atmospheric Research Ltd)

This software is provided for professional QMRA assessments.

---

## Version History

- **v2.0** (Oct 2025) - Initial web app release
  - Streamlit-based interface
  - Interactive Plotly visualizations
  - Mobile-responsive design
  - Cloud deployment ready

---

**Enjoy the modern browser-based QMRA experience!** 🚀
