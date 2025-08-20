"""
Configuration file for EcoSolvE platform
"""

import os
from typing import Dict, Any

# Application settings
APP_CONFIG = {
    "name": "EcoSolvE",
    "version": "1.0.0",
    "description": "Intelligent Solvent Prediction and Optimization Platform",
    "author": "EcoSolvE Team",
    "contact": "contact@ecosolve.com"
}

# Database configuration
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "ecosolve"),
    "username": os.getenv("DB_USER", "ecosolve_user"),
    "password": os.getenv("DB_PASSWORD", ""),
}

# API configuration
API_CONFIG = {
    "base_url": os.getenv("API_BASE_URL", "https://api.ecosolve.com"),
    "timeout": int(os.getenv("API_TIMEOUT", 30)),
    "retry_attempts": int(os.getenv("API_RETRY_ATTEMPTS", 3)),
}

# ML Model configuration
ML_CONFIG = {
    "model_path": os.getenv("ML_MODEL_PATH", "./models/"),
    "solubility_model": "solubility_predictor.pkl",
    "toxicity_model": "toxicity_predictor.pkl",
    "confidence_threshold": float(os.getenv("ML_CONFIDENCE_THRESHOLD", 0.8)),
}

# Solvent properties database
SOLVENT_PROPERTIES = {
    "Water": {
        "molecular_weight": 18.015,
        "density": 1.0,
        "boiling_point": 100,
        "melting_point": 0,
        "dielectric_constant": 80.1,
        "hansen_parameters": {"dD": 15.5, "dP": 16.0, "dH": 42.3},
        "safety_class": "Non-toxic",
        "environmental_impact": "Low"
    },
    "Ethanol": {
        "molecular_weight": 46.07,
        "density": 0.789,
        "boiling_point": 78.37,
        "melting_point": -114.1,
        "dielectric_constant": 24.55,
        "hansen_parameters": {"dD": 15.8, "dP": 8.8, "dH": 19.4},
        "safety_class": "Moderate",
        "environmental_impact": "Medium"
    },
    "Acetone": {
        "molecular_weight": 58.08,
        "density": 0.791,
        "boiling_point": 56.05,
        "melting_point": -94.7,
        "dielectric_constant": 20.7,
        "hansen_parameters": {"dD": 15.5, "dP": 10.4, "dH": 7.0},
        "safety_class": "Moderate",
        "environmental_impact": "Medium"
    },
    "Methanol": {
        "molecular_weight": 32.04,
        "density": 0.792,
        "boiling_point": 64.7,
        "melting_point": -97.6,
        "dielectric_constant": 32.7,
        "hansen_parameters": {"dD": 15.1, "dP": 12.3, "dH": 22.3},
        "safety_class": "Toxic",
        "environmental_impact": "High"
    },
    "DMSO": {
        "molecular_weight": 78.13,
        "density": 1.100,
        "boiling_point": 189,
        "melting_point": 18.5,
        "dielectric_constant": 46.7,
        "hansen_parameters": {"dD": 18.4, "dP": 16.4, "dH": 10.2},
        "safety_class": "Low toxicity",
        "environmental_impact": "Medium"
    },
    "Hexane": {
        "molecular_weight": 86.18,
        "density": 0.659,
        "boiling_point": 68.7,
        "melting_point": -95.3,
        "dielectric_constant": 1.89,
        "hansen_parameters": {"dD": 14.9, "dP": 0.0, "dH": 0.0},
        "safety_class": "Flammable",
        "environmental_impact": "High"
    }
}

# Environmental impact scoring weights
ENVIRONMENTAL_WEIGHTS = {
    "toxicity": 0.3,
    "biodegradability": 0.25,
    "flammability": 0.2,
    "volatility": 0.15,
    "cost": 0.1
}

# Educational content configuration
EDUCATION_CONFIG = {
    "modules": [
        {
            "id": "molecular_interactions",
            "title": "Molecular Interactions",
            "description": "Learn how molecules interact with different solvents",
            "difficulty": "Beginner",
            "points": 50,
            "content": [
                "Polar vs Non-polar molecules",
                "Hydrogen bonding",
                "Van der Waals forces",
                "Ionic interactions"
            ]
        },
        {
            "id": "solubility_principles",
            "title": "Solubility Principles",
            "description": "Understand the science behind solubility",
            "difficulty": "Intermediate",
            "points": 75,
            "content": [
                "Like dissolves like principle",
                "Hansen solubility parameters",
                "Temperature effects",
                "Pressure effects"
            ]
        },
        {
            "id": "green_chemistry",
            "title": "Green Chemistry",
            "description": "Explore environmentally friendly chemical practices",
            "difficulty": "Advanced",
            "points": 100,
            "content": [
                "12 Principles of Green Chemistry",
                "Solvent selection criteria",
                "Life cycle assessment",
                "Sustainable alternatives"
            ]
        }
    ],
    "badges": {
        "green_chemist": {
            "name": "Green Chemist",
            "description": "Master of environmentally friendly chemistry",
            "requirements": ["Complete Green Chemistry module", "Score 80+ on quiz"]
        },
        "solubility_master": {
            "name": "Solubility Master",
            "description": "Expert in solubility prediction and analysis",
            "requirements": ["Complete Solubility Principles module", "Predict 10+ molecules correctly"]
        },
        "eco_warrior": {
            "name": "Eco Warrior",
            "description": "Champion of sustainable chemistry practices",
            "requirements": ["Earn 500+ points", "Complete all modules"]
        }
    }
}

# Visualization settings
VISUALIZATION_CONFIG = {
    "default_colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
    "chart_height": 600,
    "chart_width": 800,
    "molecular_viewer": {
        "atom_radius": 0.5,
        "bond_width": 0.1,
        "background_color": "#ffffff",
        "camera_distance": 10
    }
}

# Logging configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": os.getenv("LOG_FILE", "ecosolve.log"),
    "max_size": int(os.getenv("LOG_MAX_SIZE", 10485760)),  # 10MB
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", 5))
}

# Security configuration
SECURITY_CONFIG = {
    "secret_key": os.getenv("SECRET_KEY", "your-secret-key-here"),
    "session_timeout": int(os.getenv("SESSION_TIMEOUT", 3600)),  # 1 hour
    "max_file_size": int(os.getenv("MAX_FILE_SIZE", 10485760)),  # 10MB
    "allowed_file_types": [".mol", ".sdf", ".pdb", ".xyz"]
}

# Performance configuration
PERFORMANCE_CONFIG = {
    "cache_timeout": int(os.getenv("CACHE_TIMEOUT", 300)),  # 5 minutes
    "max_concurrent_requests": int(os.getenv("MAX_CONCURRENT_REQUESTS", 10)),
    "request_timeout": int(os.getenv("REQUEST_TIMEOUT", 30)),
    "enable_caching": os.getenv("ENABLE_CACHING", "true").lower() == "true"
}

def get_config() -> Dict[str, Any]:
    """Get complete configuration dictionary"""
    return {
        "app": APP_CONFIG,
        "database": DATABASE_CONFIG,
        "api": API_CONFIG,
        "ml": ML_CONFIG,
        "solvents": SOLVENT_PROPERTIES,
        "environmental_weights": ENVIRONMENTAL_WEIGHTS,
        "education": EDUCATION_CONFIG,
        "visualization": VISUALIZATION_CONFIG,
        "logging": LOGGING_CONFIG,
        "security": SECURITY_CONFIG,
        "performance": PERFORMANCE_CONFIG
    }

def validate_config() -> bool:
    """Validate configuration settings"""
    try:
        config = get_config()
        
        # Check required fields
        required_fields = [
            "app.name",
            "app.version",
            "database.host",
            "database.database",
            "security.secret_key"
        ]
        
        for field in required_fields:
            keys = field.split(".")
            value = config
            for key in keys:
                value = value[key]
            if not value:
                raise ValueError(f"Missing required configuration: {field}")
        
        return True
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    # Test configuration
    if validate_config():
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration validation failed")
