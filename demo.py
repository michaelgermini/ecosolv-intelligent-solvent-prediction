#!/usr/bin/env python3
"""
Demo script for EcoSolvE platform
This script demonstrates the key features without running the full Streamlit app
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import (
    calculate_ecosolv_score,
    parse_chemical_formula,
    estimate_molecule_properties,
    predict_solubility,
    analyze_environmental_impact,
    generate_solubility_report
)
from config import SOLVENT_PROPERTIES, ENVIRONMENTAL_WEIGHTS

def demo_solubility_prediction():
    """Demonstrate solubility prediction"""
    print("🧪 Solubility Prediction Demo")
    print("=" * 40)
    
    # Test with benzene
    formula = "C6H6"
    print(f"Analyzing molecule: {formula}")
    
    # Parse formula
    elements = parse_chemical_formula(formula)
    print(f"Elements: {elements}")
    
    # Estimate properties
    properties = estimate_molecule_properties(formula)
    print(f"Molecular weight: {properties['molecular_weight']} g/mol")
    print(f"Polarity: {properties['polarity']:.3f}")
    print(f"Hansen parameters: dD={properties['hansen_dD']:.1f}, dP={properties['hansen_dP']:.1f}, dH={properties['hansen_dH']:.1f}")
    
    # Predict solubility in different solvents
    print("\nSolubility predictions:")
    for solvent_name, solvent_props in SOLVENT_PROPERTIES.items():
        solubility = predict_solubility(properties, solvent_props)
        print(f"  {solvent_name}: {solubility:.3f}")
    
    print()

def demo_green_optimization():
    """Demonstrate green optimization"""
    print("🌱 Green Optimization Demo")
    print("=" * 40)
    
    # Sample solvent data
    solvents = {
        "Water": {"solubility": 0.85, "toxicity": 0.1, "biodegradability": 0.95, "flammability": 0.0},
        "Ethanol": {"solubility": 0.78, "toxicity": 0.3, "biodegradability": 0.8, "flammability": 0.7},
        "Acetone": {"solubility": 0.82, "toxicity": 0.4, "biodegradability": 0.6, "flammability": 0.8},
        "Hexane": {"solubility": 0.45, "toxicity": 0.6, "biodegradability": 0.3, "flammability": 0.9}
    }
    
    print("EcoSolv Scores:")
    scores = []
    for solvent, data in solvents.items():
        score = calculate_ecosolv_score(
            data["solubility"],
            data["toxicity"],
            data["biodegradability"],
            data["flammability"]
        )
        scores.append((solvent, score))
        print(f"  {solvent}: {score:.1f}/100")
    
    # Find best solvent
    best_solvent = max(scores, key=lambda x: x[1])
    print(f"\n🥇 Best solvent: {best_solvent[0]} ({best_solvent[1]:.1f}/100)")
    
    # Environmental analysis
    print(f"\nEnvironmental analysis for {best_solvent[0]}:")
    analysis = analyze_environmental_impact(solvents[best_solvent[0]])
    print(f"  Impact level: {analysis['impact_level']}")
    print(f"  Recommendation: {analysis['recommendation']}")
    if analysis['warnings']:
        print(f"  Warnings: {', '.join(analysis['warnings'])}")
    
    print()

def demo_learning_system():
    """Demonstrate learning system"""
    print("🎓 Learning System Demo")
    print("=" * 40)
    
    # Simulate user progress
    user_data = {
        "score": 175,
        "badges": ["Green Chemist"],
        "completed_modules": ["molecular_interactions", "solubility_principles"]
    }
    
    from utils import create_learning_progress
    progress = create_learning_progress(user_data)
    
    print(f"Current level: {progress['current_level']}")
    print(f"Score: {progress['current_score']} points")
    print(f"Progress: {progress['progress_percentage']}% to next level")
    print(f"Badges earned: {progress['badges_earned']}")
    print(f"Modules completed: {progress['modules_completed']}")
    print(f"Achievement rate: {progress['achievement_rate']}%")
    
    print("\nRecommendations:")
    for rec in progress['recommendations']:
        print(f"  • {rec}")
    
    print()

def demo_3d_visualization():
    """Demonstrate 3D visualization capabilities"""
    print("📊 3D Visualization Demo")
    print("=" * 40)
    
    from utils import generate_3d_coordinates
    
    # Generate coordinates for different molecules
    molecules = ["benzene", "ethanol", "water"]
    
    for molecule in molecules:
        coords = generate_3d_coordinates(molecule)
        print(f"{molecule.capitalize()}:")
        print(f"  Atoms: {len(coords['x'])}")
        print(f"  X range: {min(coords['x']):.2f} to {max(coords['x']):.2f}")
        print(f"  Y range: {min(coords['y']):.2f} to {max(coords['y']):.2f}")
        print(f"  Z range: {min(coords['z']):.2f} to {max(coords['z']):.2f}")
        print(f"  Colors: {set(coords['colors'])}")
        print()

def demo_energy_kpis():
    """Demonstrate energy KPIs"""
    print("⚡ Energy KPIs Demo")
    print("=" * 40)
    
    from utils import calculate_energy_efficiency
    
    # Sample energy data
    current_consumption = 85.5  # kWh
    target_consumption = 70.0   # kWh
    
    efficiency = calculate_energy_efficiency(current_consumption, target_consumption)
    
    print(f"Current consumption: {efficiency['consumption_rate']} kWh")
    print(f"Target consumption: {efficiency['target_rate']} kWh")
    print(f"Efficiency: {efficiency['efficiency_percentage']}%")
    print(f"Energy savings: {efficiency['energy_savings']} kWh")
    print(f"Savings percentage: {efficiency['savings_percentage']}%")
    
    # KPI categories
    kpis = {
        "Vue d'ensemble": 85,
        "Chauffage": 78,
        "Électricité": 92,
        "Photovoltaïque": 67
    }
    
    print("\nKPI Summary:")
    for category, value in kpis.items():
        status = "🟢" if value >= 80 else "🟡" if value >= 60 else "🔴"
        print(f"  {status} {category}: {value}%")
    
    print()

def main():
    """Run all demos"""
    print("🌍 EcoSolvE Platform Demo")
    print("=" * 50)
    print("This demo showcases the key features of the EcoSolvE platform")
    print("without running the full Streamlit application.\n")
    
    try:
        demo_solubility_prediction()
        demo_green_optimization()
        demo_learning_system()
        demo_3d_visualization()
        demo_energy_kpis()
        
        print("✅ All demos completed successfully!")
        print("\n🚀 To run the full application:")
        print("   Windows: Double-click run_app.bat")
        print("   Other OS: python run_app.py")
        print("   Or: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
