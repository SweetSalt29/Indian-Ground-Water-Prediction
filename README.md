# 💧 Groundwater Level Monitoring System

An AI-powered web application for monitoring, analyzing, and predicting groundwater levels across India.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## 🚀 Features

- **📈 Prediction**: Forecast groundwater levels using Random Forest Regression
- **🚨 Anomaly Detection**: Identify unusual patterns with Isolation Forest
- **📊 Interactive Visualizations**: Dynamic charts and maps with Plotly
- **🗺️ Geospatial Analysis**: Location-based monitoring and insights

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/groundwater-monitoring.git
cd groundwater-monitoring

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
groundwater-monitoring/
├── data/
│   └── groundwater_clean.csv
├── app.py
├── regression_model.pkl
├── anomaly_model.pkl
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Plotly
- **ML**: Scikit-learn (Random Forest, Isolation Forest)
- **Data**: Pandas, NumPy

## 💻 Usage

1. **Home**: View dashboard with statistics
2. **Regression**: Select location and predict future levels
3. **Anomaly Detection**: Identify districts with abnormal patterns
4. **About**: Learn more about the project

## 📊 Dataset

- **Source**: Central Ground Water Board (CGWB)
- **Period**: 2013-2023
- **Coverage**: Multiple states and districts across India

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 👨‍💻 Author

**Aaryan**
- GitHub: [@SweetSalt29]([https://github.com/yourusername](https://github.com/SweetSalt29)])
- Email: aaryantamhane29@gmail.com

---

⭐ If you find this project useful, please consider giving it a star!
