"""
Unit tests for EcoSolvE configuration module.
Tests cover configuration loading, validation, and default values.
"""

import pytest
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    SOLVENT_PROPERTIES,
    EDUCATION_CONFIG,
    get_config,
    validate_config
)


class TestSolventsData:
    """Test solvents data configuration."""
    
    def test_solvents_data_structure(self):
        """Test that solvents data has correct structure."""
        assert isinstance(SOLVENT_PROPERTIES, dict)
        assert len(SOLVENT_PROPERTIES) > 0
        
        # Check each solvent has required fields
        for solvent_name, solvent_data in SOLVENT_PROPERTIES.items():
            assert isinstance(solvent_name, str)
            assert isinstance(solvent_data, dict)
            
            # Required fields
            required_fields = ['molecular_weight', 'density', 'boiling_point']
            for field in required_fields:
                assert field in solvent_data
    
    def test_solvents_data_values(self):
        """Test that solvents data has reasonable values."""
        for solvent_name, solvent_data in SOLVENT_PROPERTIES.items():
            # Check molecular weight is positive
            assert solvent_data['molecular_weight'] > 0
            
            # Check density is positive
            assert solvent_data['density'] > 0
            
            # Check boiling point is reasonable (between -200 and 500°C)
            assert -200 < solvent_data['boiling_point'] < 500
    
    def test_solvents_data_properties(self):
        """Test that solvent properties are valid."""
        for solvent_name, solvent_data in SOLVENT_PROPERTIES.items():
            # Check dielectric constant is positive
            assert solvent_data['dielectric_constant'] > 0
            
            # Check safety class is a string
            assert isinstance(solvent_data['safety_class'], str)
            
            # Check environmental impact is a string
            assert isinstance(solvent_data['environmental_impact'], str)


class TestEducationalContent:
    """Test educational content configuration."""
    
    def test_educational_content_structure(self):
        """Test that educational content has correct structure."""
        assert isinstance(EDUCATION_CONFIG, dict)
        assert len(EDUCATION_CONFIG) > 0
        
        # Check modules exist
        assert 'modules' in EDUCATION_CONFIG
        assert 'badges' in EDUCATION_CONFIG
        
        modules = EDUCATION_CONFIG['modules']
        assert isinstance(modules, list)
        assert len(modules) > 0
    
    def test_educational_content_values(self):
        """Test that educational content has valid values."""
        modules = EDUCATION_CONFIG['modules']
        
        for module_data in modules:
            # Required fields
            required_fields = ['id', 'title', 'description', 'difficulty', 'points', 'content']
            for field in required_fields:
                assert field in module_data
            
            # Title should be a string
            assert isinstance(module_data['title'], str)
            assert len(module_data['title']) > 0
            
            # Description should be a string
            assert isinstance(module_data['description'], str)
            assert len(module_data['description']) > 0
            
            # Content should be a list
            assert isinstance(module_data['content'], list)
            assert len(module_data['content']) > 0
            
            # Difficulty should be a valid level
            valid_difficulties = ['Beginner', 'Intermediate', 'Advanced']
            assert module_data['difficulty'] in valid_difficulties
            
            # Points should be positive
            assert module_data['points'] > 0
    
    def test_educational_content_modules(self):
        """Test that all expected modules are present."""
        expected_modules = [
            'molecular_interactions',
            'solubility_principles',
            'green_chemistry'
        ]
        
        modules = EDUCATION_CONFIG['modules']
        module_ids = [module['id'] for module in modules]
        
        for expected_module in expected_modules:
            assert expected_module in module_ids


class TestBadges:
    """Test badges configuration."""
    
    def test_badges_structure(self):
        """Test that badges have correct structure."""
        badges = EDUCATION_CONFIG['badges']
        assert isinstance(badges, dict)
        assert len(badges) > 0
        
        # Check each badge has required fields
        for badge_name, badge_data in badges.items():
            assert isinstance(badge_name, str)
            assert isinstance(badge_data, dict)
            
            # Required fields
            required_fields = ['name', 'description', 'requirements']
            for field in required_fields:
                assert field in badge_data
    
    def test_badges_values(self):
        """Test that badges have valid values."""
        badges = EDUCATION_CONFIG['badges']
        
        for badge_name, badge_data in badges.items():
            # Name should be a string
            assert isinstance(badge_data['name'], str)
            assert len(badge_data['name']) > 0
            
            # Description should be a string
            assert isinstance(badge_data['description'], str)
            assert len(badge_data['description']) > 0
            
            # Requirements should be a list
            assert isinstance(badge_data['requirements'], list)
            assert len(badge_data['requirements']) > 0
    
    def test_badges_unique_names(self):
        """Test that badge names are unique."""
        badges = EDUCATION_CONFIG['badges']
        badge_names = [badge_data['name'] for badge_data in badges.values()]
        assert len(badge_names) == len(set(badge_names))
    
    def test_expected_badges_present(self):
        """Test that expected badges are present."""
        expected_badges = [
            'Green Chemist',
            'Solubility Master',
            'Eco Warrior'
        ]
        
        badges = EDUCATION_CONFIG['badges']
        actual_badge_names = [badge_data['name'] for badge_data in badges.values()]
        for expected_badge in expected_badges:
            assert expected_badge in actual_badge_names


class TestLearningModules:
    """Test learning modules configuration."""
    
    def test_learning_modules_structure(self):
        """Test that learning modules have correct structure."""
        modules = EDUCATION_CONFIG['modules']
        assert isinstance(modules, list)
        assert len(modules) > 0
        
        # Check each module has required fields
        for module_data in modules:
            assert isinstance(module_data, dict)
            
            # Required fields
            required_fields = ['id', 'title', 'description', 'difficulty', 'points', 'content']
            for field in required_fields:
                assert field in module_data
    
    def test_learning_modules_values(self):
        """Test that learning modules have valid values."""
        modules = EDUCATION_CONFIG['modules']
        
        for module_data in modules:
            # Title should be a string
            assert isinstance(module_data['title'], str)
            assert len(module_data['title']) > 0
            
            # Description should be a string
            assert isinstance(module_data['description'], str)
            assert len(module_data['description']) > 0
            
            # Points should be a positive integer
            assert isinstance(module_data['points'], int)
            assert module_data['points'] > 0
            
            # Content should be a list
            assert isinstance(module_data['content'], list)
    
    def test_learning_modules_points_range(self):
        """Test that learning module points are in reasonable range."""
        modules = EDUCATION_CONFIG['modules']
        
        for module_data in modules:
            points = module_data['points']
            
            # Points should be between 10 and 100
            assert 10 <= points <= 100
    
    def test_learning_modules_content(self):
        """Test that learning module content is valid."""
        modules = EDUCATION_CONFIG['modules']
        
        for module_data in modules:
            content = module_data['content']
            
            # Content should be a list of strings
            assert isinstance(content, list)
            assert len(content) > 0
            
            for item in content:
                assert isinstance(item, str)
                assert len(item) > 0


class TestConfigurationIntegration:
    """Integration tests for configuration modules."""
    
    def test_configuration_consistency(self):
        """Test that configuration modules are consistent."""
        # Check that education config has both modules and badges
        assert 'modules' in EDUCATION_CONFIG
        assert 'badges' in EDUCATION_CONFIG
        
        # Should have modules
        assert len(EDUCATION_CONFIG['modules']) > 0
        
        # Should have badges
        assert len(EDUCATION_CONFIG['badges']) > 0
    
    def test_configuration_completeness(self):
        """Test that configuration is complete."""
        # Should have solvents data
        assert len(SOLVENT_PROPERTIES) >= 5  # At least 5 solvents
        
        # Should have educational modules
        assert len(EDUCATION_CONFIG['modules']) >= 3  # At least 3 modules
        
        # Should have badges
        assert len(EDUCATION_CONFIG['badges']) >= 3  # At least 3 badges
    
    def test_configuration_data_types(self):
        """Test that all configuration data has correct types."""
        # Test solvents data types
        for solvent_data in SOLVENT_PROPERTIES.values():
            assert isinstance(solvent_data['molecular_weight'], (int, float))
            assert isinstance(solvent_data['density'], (int, float))
            assert isinstance(solvent_data['boiling_point'], (int, float))
            assert isinstance(solvent_data['dielectric_constant'], (int, float))
            assert isinstance(solvent_data['safety_class'], str)
            assert isinstance(solvent_data['environmental_impact'], str)
        
        # Test educational content types
        for module_data in EDUCATION_CONFIG['modules']:
            assert isinstance(module_data['title'], str)
            assert isinstance(module_data['description'], str)
            assert isinstance(module_data['content'], list)
            assert isinstance(module_data['difficulty'], str)
            assert isinstance(module_data['points'], int)
        
        # Test badges types
        for badge_data in EDUCATION_CONFIG['badges'].values():
            assert isinstance(badge_data['name'], str)
            assert isinstance(badge_data['description'], str)
            assert isinstance(badge_data['requirements'], list)
    
    def test_get_config_function(self):
        """Test the get_config function."""
        config = get_config()
        
        # Should return a dictionary
        assert isinstance(config, dict)
        
        # Should have all required sections
        required_sections = ['app', 'database', 'api', 'ml', 'solvents', 'education']
        for section in required_sections:
            assert section in config
    
    def test_validate_config_function(self):
        """Test the validate_config function."""
        # Should return True for valid configuration
        assert validate_config() is True


if __name__ == "__main__":
    pytest.main([__file__])
