# 🌍 EcoSolvE — Intelligent Solvent Prediction and Optimization Platform

## 🎯 Vision

Build a platform that helps researchers, students, and the pharmaceutical industry to predict molecule solubility, choose greener solvents, and learn chemistry interactively through AI.

## 🚀 Live Demo

**Try the application online:** [EcoSolvE Demo](https://ecosolv-intelligent-solvent-prediction.streamlit.app/)

*The application is now live and ready to use!*

## 🔑 Main Features

### 1. Solubility Prediction (SolvPredict)
- **Input options:**
  - Chemical formula (text)
  - .mol / .sdf file upload
- **AI-powered analysis** calculates solubility in different solvents (ethanol, acetone, water, organic solvents)
- **Results displayed** as interactive tables and graphs

### 2. Green Optimization (GreenChem Optimizer)
The AI ranks possible solvents based on:
- ✅ Dissolution efficiency
- 🌱 Environmental impact (toxicity, biodegradability)
- 🧑‍🔬 Human safety (health risks, flammability)

The system automatically suggests greener alternative solvents and provides an **EcoSolv Score (0–100)**.

### 3. Interactive Learning (EduChem AI)
- Educational mode with 3D molecular animations
- Step-by-step explanations of solubility principles
- Interactive quizzes for students
- Gamification with badges ("Green Chemist", "Solubility Master")

### 4. 3D Dashboard
- Advanced molecular visualization
- Real-time data monitoring
- Energy KPIs and environmental metrics

## 👩‍💻 Target Users

1. **Pharma researchers** → Speed up R&D, reduce toxic solvent usage
2. **Chemical industry** → Comply with environmental regulations and cut costs
3. **Students** → Learn chemistry in a fun and interactive way

## 🛠️ Tech Stack

- **Backend ML**: Python (PyTorch / TensorFlow) + ChemProp / FastProp models
- **Database**: BigSolDB + collaborative extension
- **Frontend**: Streamlit + Plotly for visualization
- **3D Molecular Viewer**: Plotly 3D (molecule + solvent interactions)
- **Public API**: Ready for integration into external software

## 🚀 Expected Impact

- Reduction in toxic solvent usage
- Faster drug development pipelines
- Better training of future chemists through educational interface

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/michaelgermini/ecosolv-intelligent-solvent-prediction.git
   cd ecosolv-intelligent-solvent-prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎮 Usage Guide

### SolvPredict
1. Navigate to "SolvPredict" in the sidebar
2. Choose input method (chemical formula or file upload)
3. Enter chemical formula (e.g., C6H6, CH3COOH) or upload .mol/.sdf file
4. Click "Predict Solubility" to get results
5. View interactive charts and tables showing solubility in different solvents

### GreenChem Optimizer
1. Navigate to "GreenChem Optimizer" in the sidebar
2. Select solvents to compare from the dropdown
3. View ranked results based on EcoSolv scores
4. Analyze environmental impact metrics
5. Get recommendations for greener alternatives

### EduChem AI
1. Navigate to "EduChem AI" in the sidebar
2. Track your learning progress and earn badges
3. Complete learning modules for points
4. Take interactive quizzes to test knowledge
5. Earn badges like "Green Chemist" and "Solubility Master"

### 3D Dashboard
1. Navigate to "3D Dashboard" in the sidebar
2. View energy KPIs and efficiency metrics
3. Explore 3D molecular visualizations
4. Monitor real-time data streams
5. Use interactive controls for molecular viewing

## 🔧 Configuration

The application uses sample data for demonstration purposes. To integrate with real ML models:

1. **Replace sample data** in `SOLVENTS_DATA` with actual predictions
2. **Add molecular structure analysis** using simplified algorithms
3. **Connect to databases** for solvent property lookup
4. **Implement ML models** for solubility prediction

## 📊 Data Sources

The platform is designed to work with:
- **Chemical databases**: PubChem, ChEMBL, ZINC
- **Solvent properties**: Hansen solubility parameters
- **Environmental data**: EPA databases, GreenScreen
- **Safety data**: GHS classification, MSDS information

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team: **michael@germini.info**
- Check the documentation

## 👨‍💻 Contact

**Developer:** Michael Germini  
**Email:** michael@germini.info  
**GitHub:** [@michaelgermini](https://github.com/michaelgermini)

Feel free to reach out for:
- Feature requests
- Bug reports
- Collaboration opportunities
- Questions about the platform

## 🔮 Future Roadmap

- [ ] Integration with real ML models
- [ ] Advanced 3D molecular visualization
- [ ] Mobile app development
- [ ] API endpoints for external integration
- [ ] Collaborative features for research teams
- [ ] Advanced gamification elements
- [ ] Integration with laboratory equipment

---

**EcoSolvE** - Bridging research, industry, and education for a greener chemical future! 🌱
