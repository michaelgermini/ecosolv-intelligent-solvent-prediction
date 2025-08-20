"""
Utility functions for EcoSolvE platform
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from datetime import datetime
import json

def calculate_ecosolv_score(
    solubility: float,
    toxicity: float,
    biodegradability: float,
    flammability: float,
    cost: float = 0.5
) -> float:
    """
    Calculate EcoSolv score based on multiple criteria
    
    Args:
        solubility: Solubility score (0-1)
        toxicity: Toxicity score (0-1, lower is better)
        biodegradability: Biodegradability score (0-1, higher is better)
        flammability: Flammability score (0-1, lower is better)
        cost: Cost score (0-1, lower is better)
    
    Returns:
        EcoSolv score (0-100)
    """
    # Weights for different criteria
    weights = {
        'solubility': 0.25,
        'toxicity': 0.25,
        'biodegradability': 0.20,
        'flammability': 0.20,
        'cost': 0.10
    }
    
    # Calculate weighted score
    score = (
        solubility * weights['solubility'] +
        (1 - toxicity) * weights['toxicity'] +
        biodegradability * weights['biodegradability'] +
        (1 - flammability) * weights['flammability'] +
        (1 - cost) * weights['cost']
    )
    
    return round(score * 100, 1)

def parse_chemical_formula(formula: str) -> Dict[str, int]:
    """
    Parse chemical formula and return element counts
    
    Args:
        formula: Chemical formula (e.g., "C6H6", "CH3COOH")
    
    Returns:
        Dictionary with element counts
    """
    # Regular expression to match elements and their counts
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formula)
    
    elements = {}
    for element, count in matches:
        count = int(count) if count else 1
        elements[element] = elements.get(element, 0) + count
    
    return elements

def calculate_molecular_weight(elements: Dict[str, int]) -> float:
    """
    Calculate molecular weight from element counts
    
    Args:
        elements: Dictionary with element counts
    
    Returns:
        Molecular weight in g/mol
    """
    # Atomic weights (simplified)
    atomic_weights = {
        'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
        'F': 18.998, 'P': 30.974, 'S': 32.065, 'Cl': 35.453,
        'Br': 79.904, 'I': 126.904
    }
    
    total_weight = 0
    for element, count in elements.items():
        if element in atomic_weights:
            total_weight += atomic_weights[element] * count
        else:
            # Unknown element, estimate based on periodic table
            total_weight += 50 * count  # Rough estimate
    
    return round(total_weight, 2)

def predict_solubility(
    molecule_properties: Dict[str, float],
    solvent_properties: Dict[str, float]
) -> float:
    """
    Predict solubility based on molecular and solvent properties
    
    Args:
        molecule_properties: Properties of the molecule
        solvent_properties: Properties of the solvent
    
    Returns:
        Predicted solubility score (0-1)
    """
    # Simplified solubility prediction based on Hansen parameters
    # In a real implementation, this would use ML models
    
    # Extract Hansen parameters
    mol_dD = molecule_properties.get('hansen_dD', 15.0)
    mol_dP = molecule_properties.get('hansen_dP', 8.0)
    mol_dH = molecule_properties.get('hansen_dH', 15.0)
    
    sol_dD = solvent_properties.get('hansen_dD', 15.0)
    sol_dP = solvent_properties.get('hansen_dP', 8.0)
    sol_dH = solvent_properties.get('hansen_dH', 15.0)
    
    # Calculate Hansen distance
    distance = np.sqrt(
        (mol_dD - sol_dD)**2 + 
        (mol_dP - sol_dP)**2 + 
        (mol_dH - sol_dH)**2
    )
    
    # Convert distance to solubility score (inverse relationship)
    solubility = max(0, 1 - distance / 20)
    
    return round(solubility, 3)

def estimate_molecule_properties(formula: str) -> Dict[str, float]:
    """
    Estimate molecular properties from chemical formula
    
    Args:
        formula: Chemical formula
    
    Returns:
        Dictionary with estimated properties
    """
    elements = parse_chemical_formula(formula)
    mol_weight = calculate_molecular_weight(elements)
    
    # Estimate properties based on composition
    c_count = elements.get('C', 0)
    h_count = elements.get('H', 0)
    o_count = elements.get('O', 0)
    n_count = elements.get('N', 0)
    
    # Estimate polarity based on functional groups
    polarity = 0.0
    if o_count > 0:
        polarity += 0.3 * o_count
    if n_count > 0:
        polarity += 0.2 * n_count
    if c_count > 0 and h_count > 0:
        polarity -= 0.1 * (c_count + h_count)
    
    polarity = max(0, min(1, polarity))
    
    # Estimate Hansen parameters
    hansen_dD = 15.0 + 2.0 * (c_count / max(1, len(elements)))
    hansen_dP = 8.0 + 5.0 * polarity
    hansen_dH = 15.0 + 10.0 * polarity
    
    return {
        'molecular_weight': mol_weight,
        'polarity': polarity,
        'hansen_dD': hansen_dD,
        'hansen_dP': hansen_dP,
        'hansen_dH': hansen_dH,
        'carbon_count': c_count,
        'hydrogen_count': h_count,
        'oxygen_count': o_count,
        'nitrogen_count': n_count
    }

def analyze_environmental_impact(
    solvent_data: Dict[str, float]
) -> Dict[str, str]:
    """
    Analyze environmental impact of a solvent
    
    Args:
        solvent_data: Solvent properties
    
    Returns:
        Environmental impact analysis
    """
    toxicity = solvent_data.get('toxicity', 0.5)
    biodegradability = solvent_data.get('biodegradability', 0.5)
    flammability = solvent_data.get('flammability', 0.5)
    
    # Determine impact level
    if toxicity < 0.3 and biodegradability > 0.7 and flammability < 0.3:
        impact_level = "Low"
        recommendation = "Excellent choice for green chemistry"
    elif toxicity < 0.5 and biodegradability > 0.5 and flammability < 0.5:
        impact_level = "Medium"
        recommendation = "Acceptable with proper handling"
    else:
        impact_level = "High"
        recommendation = "Consider greener alternatives"
    
    # Safety warnings
    warnings = []
    if toxicity > 0.7:
        warnings.append("High toxicity - use with extreme caution")
    if flammability > 0.8:
        warnings.append("Highly flammable - ensure proper ventilation")
    if biodegradability < 0.3:
        warnings.append("Poor biodegradability - environmental concern")
    
    return {
        'impact_level': impact_level,
        'recommendation': recommendation,
        'warnings': warnings,
        'risk_score': round((toxicity + flammability + (1 - biodegradability)) / 3, 2)
    }

def generate_solubility_report(
    molecule_name: str,
    solubility_results: Dict[str, float],
    solvent_data: Dict[str, Dict[str, float]]
) -> Dict[str, any]:
    """
    Generate comprehensive solubility report
    
    Args:
        molecule_name: Name of the molecule
        solubility_results: Solubility scores for different solvents
        solvent_data: Properties of solvents
    
    Returns:
        Comprehensive report
    """
    # Find best and worst solvents
    sorted_solvents = sorted(solubility_results.items(), key=lambda x: x[1], reverse=True)
    best_solvent = sorted_solvents[0]
    worst_solvent = sorted_solvents[-1]
    
    # Calculate average solubility
    avg_solubility = np.mean(list(solubility_results.values()))
    
    # Environmental analysis for best solvent
    best_solvent_data = solvent_data.get(best_solvent[0], {})
    env_analysis = analyze_environmental_impact(best_solvent_data)
    
    # Generate recommendations
    recommendations = []
    if best_solvent[1] > 0.8:
        recommendations.append(f"Excellent solubility in {best_solvent[0]}")
    elif best_solvent[1] > 0.6:
        recommendations.append(f"Good solubility in {best_solvent[0]}")
    else:
        recommendations.append(f"Moderate solubility in {best_solvent[0]}")
    
    if env_analysis['impact_level'] == 'Low':
        recommendations.append("Environmentally friendly choice")
    elif env_analysis['impact_level'] == 'High':
        recommendations.append("Consider greener alternatives")
    
    return {
        'molecule': molecule_name,
        'best_solvent': {
            'name': best_solvent[0],
            'solubility': best_solvent[1],
            'environmental_impact': env_analysis
        },
        'worst_solvent': {
            'name': worst_solvent[0],
            'solubility': worst_solvent[1]
        },
        'average_solubility': round(avg_solubility, 3),
        'recommendations': recommendations,
        'warnings': env_analysis['warnings'],
        'timestamp': datetime.now().isoformat()
    }

def create_learning_progress(user_data: Dict[str, any]) -> Dict[str, any]:
    """
    Create learning progress summary
    
    Args:
        user_data: User progress data
    
    Returns:
        Progress summary
    """
    score = user_data.get('score', 0)
    badges = user_data.get('badges', [])
    completed_modules = user_data.get('completed_modules', [])
    
    # Calculate level
    level = (score // 100) + 1
    
    # Determine next milestone
    next_milestone = ((level) * 100) - score
    
    # Progress percentage
    progress_percentage = (score % 100) / 100 * 100
    
    # Learning recommendations
    recommendations = []
    if score < 100:
        recommendations.append("Complete beginner modules to earn your first badge")
    elif score < 300:
        recommendations.append("Try intermediate modules to advance your knowledge")
    else:
        recommendations.append("Take on advanced challenges to become an expert")
    
    return {
        'current_level': level,
        'current_score': score,
        'progress_percentage': round(progress_percentage, 1),
        'next_milestone': next_milestone,
        'badges_earned': len(badges),
        'modules_completed': len(completed_modules),
        'recommendations': recommendations,
        'achievement_rate': round(len(badges) / max(1, len(completed_modules)) * 100, 1)
    }

def validate_molecular_file(file_content: bytes, file_type: str) -> Tuple[bool, str]:
    """
    Validate uploaded molecular file
    
    Args:
        file_content: File content as bytes
        file_type: File extension
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        content = file_content.decode('utf-8')
        
        if file_type.lower() == '.mol':
            # Check for MOL file format
            lines = content.split('\n')
            if len(lines) < 4:
                return False, "Invalid MOL file: insufficient lines"
            
            # Check header
            if not lines[0].strip():
                return False, "Invalid MOL file: missing title"
            
            # Check counts line
            counts_line = lines[3]
            if len(counts_line) < 39:
                return False, "Invalid MOL file: malformed counts line"
            
            return True, "Valid MOL file"
        
        elif file_type.lower() == '.sdf':
            # Check for SDF file format
            if '$$$$' not in content:
                return False, "Invalid SDF file: missing end marker"
            
            return True, "Valid SDF file"
        
        else:
            return False, f"Unsupported file type: {file_type}"
    
    except UnicodeDecodeError:
        return False, "File encoding error"
    except Exception as e:
        return False, f"File validation error: {str(e)}"

def calculate_energy_efficiency(
    energy_consumption: float,
    target_consumption: float,
    time_period: str = "hour"
) -> Dict[str, float]:
    """
    Calculate energy efficiency metrics
    
    Args:
        energy_consumption: Current energy consumption
        target_consumption: Target energy consumption
        time_period: Time period for measurement
    
    Returns:
        Efficiency metrics
    """
    efficiency = (target_consumption / max(energy_consumption, 0.001)) * 100
    savings = max(0, energy_consumption - target_consumption)
    savings_percentage = (savings / max(energy_consumption, 0.001)) * 100
    
    return {
        'efficiency_percentage': round(efficiency, 1),
        'energy_savings': round(savings, 2),
        'savings_percentage': round(savings_percentage, 1),
        'consumption_rate': round(energy_consumption, 2),
        'target_rate': round(target_consumption, 2)
    }

def generate_3d_coordinates(
    molecule_type: str,
    num_atoms: int = 50
) -> Dict[str, List[float]]:
    """
    Generate 3D coordinates for molecular visualization
    
    Args:
        molecule_type: Type of molecule
        num_atoms: Number of atoms to generate
    
    Returns:
        Dictionary with x, y, z coordinates and properties
    """
    np.random.seed(hash(molecule_type) % 2**32)
    
    # Generate coordinates based on molecule type
    if molecule_type.lower() == "benzene":
        # Ring structure
        radius = 1.4
        angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
        x = radius * np.cos(angles)
        y = radius * np.sin(angles)
        z = np.zeros(6)
        
        # Add hydrogen atoms
        h_radius = 2.1
        h_angles = angles + np.pi/6
        x = np.concatenate([x, h_radius * np.cos(h_angles)])
        y = np.concatenate([y, h_radius * np.sin(h_angles)])
        z = np.concatenate([z, np.zeros(6)])
        
        colors = ['gray'] * 6 + ['white'] * 6
        sizes = [12] * 6 + [6] * 6
        
    elif molecule_type.lower() == "ethanol":
        # Linear structure
        x = np.array([0, 0, 0, 1.5, 1.5, 1.5, 2.5, 2.5, 2.5])
        y = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        z = np.array([0, 1.1, 2.2, 0, 1.1, 2.2, 0, 1.1, 2.2])
        
        colors = ['gray', 'white', 'white', 'gray', 'white', 'white', 'red', 'white', 'white']
        sizes = [12, 6, 6, 12, 6, 6, 12, 6, 6]
        
    else:
        # Random structure
        x = np.random.randn(num_atoms)
        y = np.random.randn(num_atoms)
        z = np.random.randn(num_atoms)
        colors = np.random.choice(['red', 'blue', 'green', 'yellow', 'gray'], num_atoms)
        sizes = np.random.randint(5, 15, num_atoms)
    
    return {
        'x': x.tolist(),
        'y': y.tolist(),
        'z': z.tolist(),
        'colors': colors,
        'sizes': sizes,
        'molecule_type': molecule_type
    }

def export_results_to_json(results: Dict[str, any], filename: str) -> str:
    """
    Export results to JSON file
    
    Args:
        results: Results dictionary
        filename: Output filename
    
    Returns:
        Success message
    """
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        return f"Results exported to {filename}"
    except Exception as e:
        return f"Export failed: {str(e)}"

def import_results_from_json(filename: str) -> Dict[str, any]:
    """
    Import results from JSON file
    
    Args:
        filename: Input filename
    
    Returns:
        Results dictionary
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"Import failed: {str(e)}"}
