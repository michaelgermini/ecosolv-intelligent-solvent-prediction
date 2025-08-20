"""
Unit tests for EcoSolvE utility functions.
Tests cover chemical formula parsing, solubility prediction, environmental analysis, and more.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    parse_chemical_formula,
    calculate_molecular_weight,
    predict_solubility,
    analyze_environmental_impact,
    generate_solubility_report,
    create_learning_progress,
    validate_molecular_file,
    generate_3d_coordinates,
    calculate_ecosolv_score,
    estimate_molecule_properties
)


class TestChemicalFormulaParsing:
    """Test chemical formula parsing and molecular weight calculation."""
    
    def test_parse_chemical_formula_valid(self):
        """Test parsing of valid chemical formulas."""
        # Test simple formulas
        assert parse_chemical_formula("H2O") == {"H": 2, "O": 1}
        assert parse_chemical_formula("CO2") == {"C": 1, "O": 2}
        assert parse_chemical_formula("CH4") == {"C": 1, "H": 4}
        
        # Test complex formulas
        assert parse_chemical_formula("C6H6") == {"C": 6, "H": 6}
        assert parse_chemical_formula("CH3COOH") == {"C": 2, "H": 4, "O": 2}
        
    def test_parse_chemical_formula_invalid(self):
        """Test parsing of invalid chemical formulas."""
        with pytest.raises(ValueError):
            parse_chemical_formula("")
        
        with pytest.raises(ValueError):
            parse_chemical_formula("Invalid")
            
        with pytest.raises(ValueError):
            parse_chemical_formula("H2O3X")
    
    def test_calculate_molecular_weight(self):
        """Test molecular weight calculations."""
        # Test simple molecules
        elements = parse_chemical_formula("H2O")
        assert abs(calculate_molecular_weight(elements) - 18.015) < 0.1
        
        elements = parse_chemical_formula("CO2")
        assert abs(calculate_molecular_weight(elements) - 44.01) < 0.1
        
        elements = parse_chemical_formula("CH4")
        assert abs(calculate_molecular_weight(elements) - 16.04) < 0.1
        
        # Test benzene
        elements = parse_chemical_formula("C6H6")
        assert abs(calculate_molecular_weight(elements) - 78.11) < 0.1


class TestSolubilityPrediction:
    """Test solubility prediction functionality."""
    
    def test_predict_solubility_valid_input(self):
        """Test solubility prediction with valid inputs."""
        molecule_properties = {
            'hansen_dD': 15.0,
            'hansen_dP': 8.0,
            'hansen_dH': 15.0
        }
        solvent_properties = {
            'hansen_dD': 15.5,
            'hansen_dP': 16.0,
            'hansen_dH': 42.3
        }
        
        result = predict_solubility(molecule_properties, solvent_properties)
        
        assert isinstance(result, float)
        assert 0 <= result <= 1
    
    def test_predict_solubility_missing_properties(self):
        """Test solubility prediction with missing properties."""
        molecule_properties = {}
        solvent_properties = {}
        
        result = predict_solubility(molecule_properties, solvent_properties)
        
        assert isinstance(result, float)
        assert 0 <= result <= 1
    
    def test_estimate_molecule_properties(self):
        """Test molecule properties estimation."""
        result = estimate_molecule_properties("C6H6")
        
        assert isinstance(result, dict)
        assert 'molecular_weight' in result
        assert 'polarity' in result
        assert 'hansen_dD' in result
        assert 'hansen_dP' in result
        assert 'hansen_dH' in result
        
        # Check that molecular weight is reasonable
        assert result['molecular_weight'] > 0
        assert result['polarity'] >= 0 and result['polarity'] <= 1


class TestEnvironmentalImpactAnalysis:
    """Test environmental impact analysis functionality."""
    
    def test_analyze_environmental_impact_valid(self):
        """Test environmental impact analysis with valid inputs."""
        solvent_data = {
            'toxicity': 0.3,
            'biodegradability': 0.8,
            'flammability': 0.2
        }
        
        result = analyze_environmental_impact(solvent_data)
        
        assert isinstance(result, dict)
        assert 'toxicity_level' in result
        assert 'biodegradability_level' in result
        assert 'flammability_level' in result
    
    def test_analyze_environmental_impact_missing_data(self):
        """Test environmental impact analysis with missing data."""
        solvent_data = {}
        
        result = analyze_environmental_impact(solvent_data)
        
        assert isinstance(result, dict)
        # Should handle missing data gracefully


class TestEcoSolvScore:
    """Test EcoSolv score calculation."""
    
    def test_calculate_ecosolv_score_valid(self):
        """Test EcoSolv score calculation with valid inputs."""
        score = calculate_ecosolv_score(
            solubility=0.8,
            toxicity=0.2,
            biodegradability=0.9,
            flammability=0.1,
            cost=0.3
        )
        
        assert isinstance(score, float)
        assert 0 <= score <= 100
    
    def test_calculate_ecosolv_score_edge_cases(self):
        """Test EcoSolv score calculation edge cases."""
        # Perfect score
        score = calculate_ecosolv_score(1.0, 0.0, 1.0, 0.0, 0.0)
        assert score > 90
        
        # Poor score
        score = calculate_ecosolv_score(0.0, 1.0, 0.0, 1.0, 1.0)
        assert score < 50


class TestReportGeneration:
    """Test report generation functionality."""
    
    def test_generate_solubility_report_valid_data(self):
        """Test solubility report generation with valid data."""
        solubility_data = {"water": 25.5, "ethanol": 45.2}
        environmental_data = pd.DataFrame({
            "Solvent": ["water", "ethanol"],
            "EcoSolv_Score": [85, 72],
            "Toxicity": ["Low", "Medium"],
            "Biodegradability": ["High", "High"]
        })
        
        report = generate_solubility_report("C6H6", solubility_data, environmental_data)
        
        assert isinstance(report, dict)
        assert "summary" in report
        assert "recommendations" in report
        assert "detailed_analysis" in report
        assert "chemical_formula" in report
        assert report["chemical_formula"] == "C6H6"
    
    def test_generate_solubility_report_empty_data(self):
        """Test solubility report generation with empty data."""
        with pytest.raises(ValueError):
            generate_solubility_report("C6H6", {}, pd.DataFrame())


class TestLearningProgress:
    """Test learning progress management."""
    
    def test_create_learning_progress_new_user(self):
        """Test learning progress creation for new user."""
        user_data = {
            "user_id": "test_user_123",
            "current_level": 1,
            "total_points": 0,
            "completed_modules": []
        }
        
        result = create_learning_progress(user_data)
        
        assert isinstance(result, dict)
        assert "user_id" in result
        assert "current_level" in result
        assert "total_points" in result
        assert "completed_modules" in result


class TestFileValidation:
    """Test file upload validation."""
    
    def test_validate_molecular_file_valid_mol(self):
        """Test validation of valid .mol file."""
        mock_content = b"Mock MOL file content"
        
        result = validate_molecular_file(mock_content, "mol")
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)
    
    def test_validate_molecular_file_valid_sdf(self):
        """Test validation of valid .sdf file."""
        mock_content = b"Mock SDF file content"
        
        result = validate_molecular_file(mock_content, "sdf")
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)
    
    def test_validate_molecular_file_invalid_type(self):
        """Test validation of file with invalid type."""
        mock_content = b"Mock content"
        
        result = validate_molecular_file(mock_content, "txt")
        
        assert isinstance(result, tuple)
        assert result[0] is False
        assert "type" in result[1].lower()
    
    def test_validate_molecular_file_empty_file(self):
        """Test validation of empty file."""
        mock_content = b""
        
        result = validate_molecular_file(mock_content, "mol")
        
        assert isinstance(result, tuple)
        assert result[0] is False
        assert "empty" in result[1].lower()


class Test3DCoordinateGeneration:
    """Test 3D coordinate generation for molecular visualization."""
    
    def test_generate_3d_coordinates_valid_formula(self):
        """Test 3D coordinate generation for valid chemical formula."""
        coordinates = generate_3d_coordinates("C6H6")
        
        assert isinstance(coordinates, dict)
        assert "atoms" in coordinates
        assert "bonds" in coordinates
        assert "positions" in coordinates
        
        # Check that we have the right number of atoms
        assert len(coordinates["atoms"]) == 12  # 6 C + 6 H
        
        # Check that positions are 3D coordinates
        for pos in coordinates["positions"]:
            assert len(pos) == 3
            assert all(isinstance(x, (int, float)) for x in pos)
    
    def test_generate_3d_coordinates_simple_molecule(self):
        """Test 3D coordinate generation for simple molecule."""
        coordinates = generate_3d_coordinates("H2O")
        
        assert len(coordinates["atoms"]) == 3  # 2 H + 1 O
        assert len(coordinates["positions"]) == 3
    
    def test_generate_3d_coordinates_invalid_formula(self):
        """Test 3D coordinate generation with invalid formula."""
        with pytest.raises(ValueError):
            generate_3d_coordinates("Invalid")


class TestEnergyEfficiency:
    """Test energy efficiency calculations."""
    
    def test_calculate_energy_efficiency_valid(self):
        """Test energy efficiency calculation with valid inputs."""
        # This would test the calculate_energy_efficiency function
        # if it exists and is properly implemented
        pass


class TestIntegrationTests:
    """Integration tests for complete workflows."""
    
    def test_complete_solubility_workflow(self):
        """Test complete solubility prediction workflow."""
        # Parse formula
        formula = "C6H6"
        parsed = parse_chemical_formula(formula)
        assert parsed == {"C": 6, "H": 6}
        
        # Calculate molecular weight
        mw = calculate_molecular_weight(parsed)
        assert abs(mw - 78.11) < 0.1
        
        # Estimate properties
        properties = estimate_molecule_properties(formula)
        assert isinstance(properties, dict)
        assert 'molecular_weight' in properties
        
        # Predict solubility
        molecule_properties = {
            'hansen_dD': properties['hansen_dD'],
            'hansen_dP': properties['hansen_dP'],
            'hansen_dH': properties['hansen_dH']
        }
        solvent_properties = {
            'hansen_dD': 15.5,
            'hansen_dP': 16.0,
            'hansen_dH': 42.3
        }
        solubility = predict_solubility(molecule_properties, solvent_properties)
        assert 0 <= solubility <= 1
        
        # Analyze environmental impact
        env_impact = analyze_environmental_impact(solvent_properties)
        assert isinstance(env_impact, dict)
    
    def test_complete_learning_workflow(self):
        """Test complete learning progress workflow."""
        user_data = {
            "user_id": "integration_test_user",
            "current_level": 1,
            "total_points": 0,
            "completed_modules": []
        }
        
        # Create learning progress
        result = create_learning_progress(user_data)
        assert isinstance(result, dict)
        assert result["user_id"] == "integration_test_user"


if __name__ == "__main__":
    pytest.main([__file__])
