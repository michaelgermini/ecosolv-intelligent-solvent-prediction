import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="EcoSolvE - Intelligent Solvent Prediction",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Nature Green theme */
    :root {
        --bg-primary: #0d1b2a;
        --bg-secondary: #1b263b;
        --bg-card: #2d3748;
        --bg-sidebar: #1a202c;
        --text-primary: #f7fafc;
        --text-secondary: #e2e8f0;
        --text-muted: #a0aec0;
        --accent-primary: #48bb78;
        --accent-secondary: #68d391;
        --accent-tertiary: #9ae6b4;
        --border-color: #4a5568;
        --shadow-light: rgba(0,0,0,0.3);
        --shadow-medium: rgba(0,0,0,0.5);
        --shadow-heavy: rgba(0,0,0,0.7);
    }
    
    /* Global dark theme */
    .main {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    .main .block-container {
        background-color: var(--bg-primary);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    /* Header styles */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: var(--accent-primary);
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px var(--shadow-medium);
    }
    
    /* Card styles */
    .feature-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid var(--accent-primary);
        box-shadow: 0 4px 8px var(--shadow-light);
        transition: transform 0.3s ease;
        border: 1px solid var(--border-color);
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px var(--shadow-medium);
        border-color: var(--accent-primary);
    }
    
    .feature-card h3, .feature-card h4 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Metric card styles */
    .metric-card {
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-tertiary) 100%);
        color: var(--bg-primary);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 8px var(--shadow-medium);
        transition: transform 0.3s ease;
        border: 1px solid var(--accent-primary);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px var(--shadow-heavy);
    }
    
    .metric-card h3, .metric-card h4 {
        color: var(--bg-primary);
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-card div {
        color: var(--bg-primary);
        font-weight: bold;
    }
    
    /* Eco score styles */
    .eco-score {
        font-size: 2rem;
        font-weight: bold;
        color: var(--accent-secondary);
        text-shadow: 1px 1px 2px var(--shadow-medium);
    }
    
    /* Warning styles */
    .warning {
        background: linear-gradient(135deg, #2d1b1b 0%, #3d2b2b 100%);
        border: 2px solid var(--accent-secondary);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: var(--accent-secondary);
        font-weight: 500;
    }
    
    /* Navigation button styles */
    .nav-button {
        margin: 0.5rem 0;
        border-radius: 10px;
        border: 2px solid var(--accent-primary);
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        color: var(--text-primary);
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px var(--shadow-light);
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow-medium);
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-tertiary) 100%);
        color: var(--bg-primary);
    }
    
    .active-page {
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-tertiary) 100%) !important;
        border-color: var(--accent-primary) !important;
        box-shadow: 0 2px 4px var(--shadow-medium);
        color: var(--bg-primary) !important;
    }
    
    /* Sidebar improvements */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, var(--bg-sidebar) 0%, var(--bg-secondary) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    /* Text improvements */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    p, div, span {
        color: var(--text-secondary) !important;
    }
    
    /* Streamlit element improvements */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-tertiary) 100%);
        color: var(--bg-primary);
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px var(--shadow-medium);
        background: linear-gradient(135deg, var(--accent-tertiary) 0%, var(--accent-primary) 100%);
    }
    
    /* Dataframe improvements */
    .dataframe {
        background-color: var(--bg-card);
        border-radius: 10px;
        box-shadow: 0 2px 4px var(--shadow-light);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .dataframe th {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border-color: var(--border-color);
    }
    
    .dataframe td {
        background-color: var(--bg-card);
        color: var(--text-secondary);
        border-color: var(--border-color);
    }
    
    /* Metric improvements */
    .metric-container {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }
    
    /* Badge styles */
    .badge {
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-tertiary) 100%);
        color: var(--bg-primary);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.25rem;
        box-shadow: 0 2px 4px var(--shadow-light);
    }
    
    /* Streamlit specific dark mode overrides */
    .stSelectbox, .stTextInput, .stRadio, .stCheckbox {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    .stSelectbox > div > div {
        background-color: var(--bg-card);
        color: var(--text-primary);
    }
    
    .stTextInput > div > div > input {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    .stRadio > div > div > label {
        color: var(--text-primary);
    }
    
    .stCheckbox > div > div > label {
        color: var(--text-primary);
    }
    
    /* Plotly chart dark mode */
    .js-plotly-plot {
        background-color: var(--bg-card) !important;
    }
    
    /* Expander dark mode */
    .streamlit-expanderHeader {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #1a3a1a;
        color: var(--accent-primary);
        border: 1px solid var(--accent-primary);
    }
    
    .stError {
        background-color: #3a1a1a;
        color: #f56565;
        border: 1px solid #f56565;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: var(--accent-primary);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--accent-primary);
        border-top-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []

# Get current page from session state
page = st.session_state.current_page

# Sidebar navigation
st.sidebar.markdown("## 🌍 EcoSolvE")
st.sidebar.markdown("Intelligent Solvent Prediction & Optimization")

# Navigation menu with buttons
st.sidebar.markdown("### 📋 Navigation")

# Create navigation buttons with visual indicators
col1, col2 = st.sidebar.columns([1, 4])

with col1:
    if page == "Overview":
        st.markdown("🟢")
    else:
        st.markdown("⚪")

with col2:
    if st.button("🏠 Overview", use_container_width=True, key="nav_overview"):
        st.session_state.current_page = "Overview"
        st.rerun()

col1, col2 = st.sidebar.columns([1, 4])

with col1:
    if page == "SolvPredict":
        st.markdown("🟢")
    else:
        st.markdown("⚪")

with col2:
    if st.button("🧪 SolvPredict", use_container_width=True, key="nav_solv"):
        st.session_state.current_page = "SolvPredict"
        st.rerun()

col1, col2 = st.sidebar.columns([1, 4])

with col1:
    if page == "GreenChem Optimizer":
        st.markdown("🟢")
    else:
        st.markdown("⚪")

with col2:
    if st.button("🌱 GreenChem Optimizer", use_container_width=True, key="nav_green"):
        st.session_state.current_page = "GreenChem Optimizer"
        st.rerun()

col1, col2 = st.sidebar.columns([1, 4])

with col1:
    if page == "EduChem AI":
        st.markdown("🟢")
    else:
        st.markdown("⚪")

with col2:
    if st.button("🎓 EduChem AI", use_container_width=True, key="nav_edu"):
        st.session_state.current_page = "EduChem AI"
        st.rerun()

col1, col2 = st.sidebar.columns([1, 4])

with col1:
    if page == "3D Dashboard":
        st.markdown("🟢")
    else:
        st.markdown("⚪")

with col2:
    if st.button("📊 3D Dashboard", use_container_width=True, key="nav_3d"):
        st.session_state.current_page = "3D Dashboard"
        st.rerun()

# Sample data for demonstration
SOLVENTS_DATA = {
    "Water": {"solubility": 0.85, "toxicity": 0.1, "biodegradability": 0.95, "flammability": 0.0, "eco_score": 92},
    "Ethanol": {"solubility": 0.78, "toxicity": 0.3, "biodegradability": 0.8, "flammability": 0.7, "eco_score": 75},
    "Acetone": {"solubility": 0.82, "toxicity": 0.4, "biodegradability": 0.6, "flammability": 0.8, "eco_score": 65},
    "Methanol": {"solubility": 0.75, "toxicity": 0.5, "biodegradability": 0.7, "flammability": 0.9, "eco_score": 60},
    "DMSO": {"solubility": 0.88, "toxicity": 0.2, "biodegradability": 0.4, "flammability": 0.1, "eco_score": 70},
    "Hexane": {"solubility": 0.45, "toxicity": 0.6, "biodegradability": 0.3, "flammability": 0.9, "eco_score": 40}
}

def main():
    if page == "Overview":
        show_overview()
    elif page == "SolvPredict":
        show_solv_predict()
    elif page == "GreenChem Optimizer":
        show_green_optimizer()
    elif page == "EduChem AI":
        show_edu_chem()
    elif page == "3D Dashboard":
        show_3d_dashboard()

def show_overview():
    st.markdown('<h1 class="main-header">🌍 EcoSolvE</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Intelligent Solvent Prediction and Optimization Platform</h2>', unsafe_allow_html=True)
    
    # Mission statement
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Our Mission</h3>
        <p>Empowering researchers, students, and the pharmaceutical industry to predict molecule solubility, 
        choose greener solvents, and learn chemistry interactively through AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🧪 Molecules Analyzed</h3>
            <div style="font-size: 2rem; font-weight: bold;">1,247</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🌱 Eco Score Avg</h3>
            <div style="font-size: 2rem; font-weight: bold;">78.5</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Cost Saved</h3>
            <div style="font-size: 2rem; font-weight: bold;">$45K</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>👨‍🎓 Students</h3>
            <div style="font-size: 2rem; font-weight: bold;">892</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features overview
    st.markdown("## 🔑 Main Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🧪 SolvPredict</h4>
            <p>AI-powered solubility prediction for molecules in various solvents. 
            Input chemical formulas or molecular files for instant analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🌱 GreenChem Optimizer</h4>
            <p>Rank solvents by dissolution efficiency, environmental impact, and safety. 
            Get EcoSolv scores and greener alternatives.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎓 EduChem AI</h4>
            <p>Interactive learning with 3D molecular animations, step-by-step explanations, 
            and gamified chemistry education.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>📊 3D Dashboard</h4>
            <p>Advanced visualization of molecular interactions, solvent properties, 
            and environmental impact metrics.</p>
        </div>
        """, unsafe_allow_html=True)

def show_solv_predict():
    st.markdown("## 🧪 SolvPredict - Solubility Prediction")
    
    # Input section
    st.markdown("### Input Molecule")
    
    input_method = st.radio(
        "Choose input method:",
        ["Chemical Formula", "Upload Molecular File (.mol/.sdf)"]
    )
    
    if input_method == "Chemical Formula":
        chemical_formula = st.text_input(
            "Enter chemical formula (e.g., C6H6, CH3COOH):",
            placeholder="C6H6"
        )
        
        if st.button("Predict Solubility") and chemical_formula:
            with st.spinner("Analyzing molecule..."):
                time.sleep(2)  # Simulate processing
                show_solubility_results(chemical_formula)
    
    else:
        uploaded_file = st.file_uploader(
            "Upload molecular file",
            type=['mol', 'sdf'],
            help="Supported formats: .mol, .sdf"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            if st.button("Predict Solubility"):
                with st.spinner("Analyzing molecular structure..."):
                    time.sleep(2)
                    show_solubility_results("Uploaded Molecule")

def show_solubility_results(molecule_name):
    st.markdown("### 📊 Solubility Results")
    
    # Create sample solubility data
    solvents = list(SOLVENTS_DATA.keys())
    solubilities = [SOLVENTS_DATA[solvent]["solubility"] for solvent in solvents]
    
    # Results table
    results_df = pd.DataFrame({
        "Solvent": solvents,
        "Solubility Score": solubilities,
        "Eco Score": [SOLVENTS_DATA[solvent]["eco_score"] for solvent in solvents],
        "Toxicity": [SOLVENTS_DATA[solvent]["toxicity"] for solvent in solvents],
        "Flammability": [SOLVENTS_DATA[solvent]["flammability"] for solvent in solvents]
    })
    
    st.dataframe(results_df, use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Solubility bar chart
        fig = px.bar(
            x=solvents,
            y=solubilities,
            title=f"Solubility of {molecule_name} in Different Solvents",
            labels={"x": "Solvent", "y": "Solubility Score"},
            color=solubilities,
            color_continuous_scale="viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Radar chart for best solvent
        best_solvent = solvents[np.argmax(solubilities)]
        best_data = SOLVENTS_DATA[best_solvent]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[best_data["solubility"], 1-best_data["toxicity"], 
               1-best_data["flammability"], best_data["biodegradability"]],
            theta=['Solubility', 'Safety', 'Non-flammable', 'Biodegradable'],
            fill='toself',
            name=best_solvent
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title=f"Properties of Best Solvent: {best_solvent}"
        )
        st.plotly_chart(fig, use_container_width=True)

def show_green_optimizer():
    st.markdown("## 🌱 GreenChem Optimizer")
    
    # Solvent selection
    st.markdown("### Select Solvents to Compare")
    
    selected_solvents = st.multiselect(
        "Choose solvents:",
        list(SOLVENTS_DATA.keys()),
        default=["Water", "Ethanol", "Acetone"]
    )
    
    if selected_solvents:
        # Create comparison dataframe
        comparison_data = []
        for solvent in selected_solvents:
            data = SOLVENTS_DATA[solvent]
            comparison_data.append({
                "Solvent": solvent,
                "EcoSolv Score": data["eco_score"],
                "Solubility": data["solubility"],
                "Toxicity": data["toxicity"],
                "Biodegradability": data["biodegradability"],
                "Flammability": data["flammability"]
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Sort by EcoSolv score
        comparison_df = comparison_df.sort_values("EcoSolv Score", ascending=False)
        
        st.markdown("### 🏆 Solvent Ranking")
        st.dataframe(comparison_df, use_container_width=True)
        
        # Best solvent recommendation
        best_solvent = comparison_df.iloc[0]
        st.markdown(f"""
        <div class="feature-card">
            <h3>🥇 Recommended Solvent: {best_solvent['Solvent']}</h3>
            <p><strong>EcoSolv Score:</strong> <span class="eco-score">{best_solvent['EcoSolv Score']}/100</span></p>
            <p><strong>Why this solvent?</strong> Best balance of solubility, safety, and environmental impact.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # EcoSolv scores comparison
            fig = px.bar(
                comparison_df,
                x="Solvent",
                y="EcoSolv Score",
                title="EcoSolv Scores Comparison",
                color="EcoSolv Score",
                color_continuous_scale="RdYlGn"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Multi-criteria radar chart
            fig = go.Figure()
            
            for _, row in comparison_df.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[row["Solubility"], 1-row["Toxicity"], 
                       1-row["Flammability"], row["Biodegradability"]],
                    theta=['Solubility', 'Safety', 'Non-flammable', 'Biodegradable'],
                    fill='toself',
                    name=row["Solvent"]
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                title="Multi-criteria Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Environmental impact analysis
        st.markdown("### 🌍 Environmental Impact Analysis")
        
        impact_col1, impact_col2, impact_col3 = st.columns(3)
        
        with impact_col1:
            avg_toxicity = comparison_df["Toxicity"].mean()
            st.metric("Average Toxicity", f"{avg_toxicity:.2f}", delta="-0.1")
        
        with impact_col2:
            avg_biodegradability = comparison_df["Biodegradability"].mean()
            st.metric("Average Biodegradability", f"{avg_biodegradability:.2f}", delta="+0.05")
        
        with impact_col3:
            avg_flammability = comparison_df["Flammability"].mean()
            st.metric("Average Flammability", f"{avg_flammability:.2f}", delta="-0.15")

def show_edu_chem():
    st.markdown("## 🎓 EduChem AI - Interactive Learning")
    
    # User progress
    st.markdown(f"### 👤 Your Progress")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score", f"{st.session_state.user_score} points")
    
    with col2:
        st.metric("Badges Earned", len(st.session_state.badges))
    
    with col3:
        st.metric("Level", f"Level {st.session_state.user_score // 100 + 1}")
    
    # Badges display
    if st.session_state.badges:
        st.markdown("### 🏆 Your Badges")
        badge_cols = st.columns(len(st.session_state.badges))
        for i, badge in enumerate(st.session_state.badges):
            with badge_cols[i]:
                st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
    
    # Learning modules
    st.markdown("### 📚 Learning Modules")
    
    modules = [
        {
            "title": "Molecular Interactions",
            "description": "Learn how molecules interact with different solvents",
            "difficulty": "Beginner",
            "points": 50
        },
        {
            "title": "Solubility Principles",
            "description": "Understand the science behind solubility",
            "difficulty": "Intermediate",
            "points": 75
        },
        {
            "title": "Green Chemistry",
            "description": "Explore environmentally friendly chemical practices",
            "difficulty": "Advanced",
            "points": 100
        }
    ]
    
    for i, module in enumerate(modules):
        with st.expander(f"{module['title']} - {module['difficulty']} ({module['points']} points)"):
            st.write(module['description'])
            
            if st.button(f"Start Module {i+1}"):
                st.session_state.user_score += module['points']
                if module['title'] == "Green Chemistry" and "Green Chemist" not in st.session_state.badges:
                    st.session_state.badges.append("Green Chemist")
                st.success(f"Completed! +{module['points']} points")
                st.rerun()
    
    # Interactive quiz
    st.markdown("### 🧠 Quick Quiz")
    
    quiz_question = st.selectbox(
        "Choose a question:",
        [
            "What makes a solvent 'green'?",
            "How does molecular structure affect solubility?",
            "What is the principle of 'like dissolves like'?"
        ]
    )
    
    if quiz_question == "What makes a solvent 'green'?":
        answer = st.radio(
            "Select the best answer:",
            [
                "Low toxicity and high biodegradability",
                "High flammability and low cost",
                "Strong odor and high volatility",
                "High toxicity and low biodegradability"
            ]
        )
        
        if st.button("Submit Answer"):
            if answer == "Low toxicity and high biodegradability":
                st.success("Correct! +25 points")
                st.session_state.user_score += 25
                if "Green Chemist" not in st.session_state.badges:
                    st.session_state.badges.append("Green Chemist")
            else:
                st.error("Incorrect. Try again!")
    
    elif quiz_question == "How does molecular structure affect solubility?":
        answer = st.radio(
            "Select the best answer:",
            [
                "It doesn't matter",
                "Polar molecules dissolve in polar solvents",
                "Large molecules always dissolve better",
                "Small molecules are always insoluble"
            ]
        )
        
        if st.button("Submit Answer"):
            if answer == "Polar molecules dissolve in polar solvents":
                st.success("Correct! +25 points")
                st.session_state.user_score += 25
                if "Solubility Master" not in st.session_state.badges:
                    st.session_state.badges.append("Solubility Master")
            else:
                st.error("Incorrect. Try again!")

def show_3d_dashboard():
    st.markdown("## 📊 3D Dashboard")
    
    # Energy KPIs section
    st.markdown("### ⚡ Energy KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Vue d'ensemble</h4>
            <div style="font-size: 1.5rem; font-weight: bold;">85%</div>
            <div>Efficiency</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Chauffage</h4>
            <div style="font-size: 1.5rem; font-weight: bold;">78%</div>
            <div>Optimization</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>Électricité</h4>
            <div style="font-size: 1.5rem; font-weight: bold;">92%</div>
            <div>Usage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>Photovoltaïque</h4>
            <div style="font-size: 1.5rem; font-weight: bold;">67%</div>
            <div>Generation</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 3D molecular visualization placeholder
    st.markdown("### 🧬 3D Molecular Visualization")
    
    # Create a 3D scatter plot to simulate molecular structure
    np.random.seed(42)
    n_atoms = 50
    
    # Generate random molecular coordinates
    x = np.random.randn(n_atoms)
    y = np.random.randn(n_atoms)
    z = np.random.randn(n_atoms)
    colors = np.random.choice(['red', 'blue', 'green', 'yellow'], n_atoms)
    sizes = np.random.randint(5, 15, n_atoms)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.8
        ),
        text=[f'Atom {i+1}' for i in range(n_atoms)],
        hovertemplate='<b>%{text}</b><br>' +
                      'X: %{x}<br>' +
                      'Y: %{y}<br>' +
                      'Z: %{z}<extra></extra>'
    )])
    
    fig.update_layout(
        title="3D Molecular Structure Visualization",
        scene=dict(
            xaxis_title="X (Å)",
            yaxis_title="Y (Å)",
            zaxis_title="Z (Å)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive controls
    st.markdown("### 🎮 Interactive Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rotation_speed = st.slider("Rotation Speed", 0, 10, 5)
        molecule_type = st.selectbox("Molecule Type", ["Benzene", "Ethanol", "Water", "Acetone"])
    
    with col2:
        view_mode = st.selectbox("View Mode", ["Ball and Stick", "Space Filling", "Wireframe"])
        show_bonds = st.checkbox("Show Bonds", value=True)
    
    # Real-time data simulation
    st.markdown("### 📈 Real-time Data Stream")
    
    # Generate time series data
    time_points = pd.date_range(start='2024-01-01', periods=100, freq='h')
    energy_data = np.cumsum(np.random.randn(100)) + 100
    temperature_data = 20 + 10 * np.sin(np.linspace(0, 4*np.pi, 100)) + np.random.randn(100) * 2
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Energy Consumption', 'Temperature'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Scatter(x=time_points, y=energy_data, name="Energy (kWh)", line=dict(color='blue')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=time_points, y=temperature_data, name="Temperature (°C)", line=dict(color='red')),
        row=2, col=1
    )
    
    fig.update_layout(height=600, title_text="Real-time Monitoring Dashboard")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
