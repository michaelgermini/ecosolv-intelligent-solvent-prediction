#!/usr/bin/env python3
"""
Test runner script for EcoSolvE platform.
Provides easy access to run tests with different options.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and display results."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Command executed successfully!")
            print(result.stdout)
        else:
            print("❌ Command failed!")
            print(result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error executing command: {e}")
        return False

def main():
    """Main test runner function."""
    print("🧪 EcoSolvE Test Suite Runner")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [option]")
        print("\nOptions:")
        print("  all          - Run all tests")
        print("  config       - Run configuration tests only")
        print("  utils        - Run utility function tests only")
        print("  coverage     - Run tests with coverage report")
        print("  quick        - Run quick test suite (passing tests only)")
        print("  help         - Show this help message")
        return
    
    option = sys.argv[1].lower()
    
    if option == "help":
        print("Usage: python run_tests.py [option]")
        print("\nOptions:")
        print("  all          - Run all tests")
        print("  config       - Run configuration tests only")
        print("  utils        - Run utility function tests only")
        print("  coverage     - Run tests with coverage report")
        print("  quick        - Run quick test suite (passing tests only)")
        print("  help         - Show this help message")
        return
    
    elif option == "all":
        success = run_command("python -m pytest tests/ -v", "Running all tests")
        
    elif option == "config":
        success = run_command("python -m pytest tests/test_config.py -v", "Running configuration tests")
        
    elif option == "utils":
        success = run_command("python -m pytest tests/test_utils.py -v", "Running utility function tests")
        
    elif option == "coverage":
        success = run_command(
            "python -m pytest tests/test_config.py tests/test_utils.py::TestEcoSolvScore tests/test_utils.py::TestChemicalFormulaParsing::test_parse_chemical_formula_valid tests/test_utils.py::TestChemicalFormulaParsing::test_calculate_molecular_weight tests/test_utils.py::TestSolubilityPrediction::test_predict_solubility_missing_properties tests/test_utils.py::TestSolubilityPrediction::test_estimate_molecule_properties tests/test_utils.py::TestEnvironmentalImpactAnalysis::test_analyze_environmental_impact_missing_data tests/test_utils.py::TestFileValidation::test_validate_molecular_file_valid_mol tests/test_utils.py::TestFileValidation::test_validate_molecular_file_valid_sdf tests/test_utils.py::TestFileValidation::test_validate_molecular_file_invalid_type tests/test_utils.py::TestEnergyEfficiency::test_calculate_energy_efficiency_valid tests/test_utils.py::TestIntegrationTests::test_complete_solubility_workflow --cov=. --cov-report=term-missing",
            "Running tests with coverage report"
        )
        
    elif option == "quick":
        success = run_command(
            "python -m pytest tests/test_config.py tests/test_utils.py::TestEcoSolvScore tests/test_utils.py::TestChemicalFormulaParsing::test_parse_chemical_formula_valid tests/test_utils.py::TestChemicalFormulaParsing::test_calculate_molecular_weight tests/test_utils.py::TestSolubilityPrediction::test_predict_solubility_missing_properties tests/test_utils.py::TestSolubilityPrediction::test_estimate_molecule_properties tests/test_utils.py::TestEnvironmentalImpactAnalysis::test_analyze_environmental_impact_missing_data tests/test_utils.py::TestFileValidation::test_validate_molecular_file_valid_mol tests/test_utils.py::TestFileValidation::test_validate_molecular_file_valid_sdf tests/test_utils.py::TestFileValidation::test_validate_molecular_file_invalid_type tests/test_utils.py::TestEnergyEfficiency::test_calculate_energy_efficiency_valid tests/test_utils.py::TestIntegrationTests::test_complete_solubility_workflow -v",
            "Running quick test suite (passing tests only)"
        )
        
    else:
        print(f"❌ Unknown option: {option}")
        print("Use 'python run_tests.py help' for available options")
        return
    
    if success:
        print("\n🎉 Test execution completed successfully!")
    else:
        print("\n💥 Test execution failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
