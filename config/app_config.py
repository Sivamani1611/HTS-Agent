"""
HTS AI Agent Pro - Configuration Settings
Modern configuration management for the enhanced application
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    hts_db_path: str = "data/hts.db"
    query_history_db: str = "data/query_history.db"
    vector_store_path: str = "data/vector_store"
    backup_enabled: bool = True
    backup_interval_hours: int = 24

@dataclass
class UIConfig:
    """UI configuration settings"""
    theme: str = "modern"
    primary_color: str = "#667eea"
    secondary_color: str = "#764ba2"
    accent_color: str = "#f093fb"
    success_color: str = "#28a745"
    error_color: str = "#dc3545"
    warning_color: str = "#ffc107"
    font_family: str = "Inter, sans-serif"
    enable_animations: bool = True
    enable_dark_mode: bool = False
    sidebar_default_state: str = "collapsed"

@dataclass
class PerformanceConfig:
    """Performance configuration settings"""
    cache_enabled: bool = True
    cache_size_mb: int = 100
    batch_processing_max_records: int = 1000
    query_timeout_seconds: int = 30
    embedding_batch_size: int = 64
    max_concurrent_requests: int = 10

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    enable_authentication: bool = False
    session_timeout_minutes: int = 60
    max_login_attempts: int = 5
    enable_audit_logging: bool = True
    sensitive_data_encryption: bool = True

@dataclass
class ExportConfig:
    """Export configuration settings"""
    default_format: str = "excel"
    max_export_records: int = 10000
    include_charts_in_pdf: bool = True
    excel_sheet_protection: bool = False
    watermark_exports: bool = True

@dataclass
class AnalyticsConfig:
    """Analytics configuration settings"""
    enable_usage_tracking: bool = True
    enable_performance_monitoring: bool = True
    retention_days: int = 365
    enable_predictive_insights: bool = True
    real_time_updates: bool = True

class AppConfig:
    """Main application configuration class"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Load configuration from environment variables and defaults"""
        
        # Database configuration
        self.database = DatabaseConfig(
            hts_db_path=os.getenv("HTS_DB_PATH", "data/hts.db"),
            query_history_db=os.getenv("QUERY_HISTORY_DB", "data/query_history.db"),
            vector_store_path=os.getenv("VECTOR_STORE_PATH", "data/vector_store"),
            backup_enabled=os.getenv("BACKUP_ENABLED", "true").lower() == "true",
            backup_interval_hours=int(os.getenv("BACKUP_INTERVAL_HOURS", "24"))
        )
        
        # UI configuration
        self.ui = UIConfig(
            theme=os.getenv("UI_THEME", "modern"),
            primary_color=os.getenv("PRIMARY_COLOR", "#667eea"),
            secondary_color=os.getenv("SECONDARY_COLOR", "#764ba2"),
            enable_animations=os.getenv("ENABLE_ANIMATIONS", "true").lower() == "true",
            enable_dark_mode=os.getenv("ENABLE_DARK_MODE", "false").lower() == "true"
        )
        
        # Performance configuration
        self.performance = PerformanceConfig(
            cache_enabled=os.getenv("CACHE_ENABLED", "true").lower() == "true",
            cache_size_mb=int(os.getenv("CACHE_SIZE_MB", "100")),
            batch_processing_max_records=int(os.getenv("BATCH_MAX_RECORDS", "1000")),
            query_timeout_seconds=int(os.getenv("QUERY_TIMEOUT", "30"))
        )
        
        # Security configuration
        self.security = SecurityConfig(
            enable_authentication=os.getenv("ENABLE_AUTH", "false").lower() == "true",
            session_timeout_minutes=int(os.getenv("SESSION_TIMEOUT", "60")),
            enable_audit_logging=os.getenv("ENABLE_AUDIT", "true").lower() == "true"
        )
        
        # Export configuration
        self.export = ExportConfig(
            default_format=os.getenv("DEFAULT_EXPORT_FORMAT", "excel"),
            max_export_records=int(os.getenv("MAX_EXPORT_RECORDS", "10000")),
            include_charts_in_pdf=os.getenv("INCLUDE_CHARTS_PDF", "true").lower() == "true"
        )
        
        # Analytics configuration
        self.analytics = AnalyticsConfig(
            enable_usage_tracking=os.getenv("ENABLE_USAGE_TRACKING", "true").lower() == "true",
            retention_days=int(os.getenv("ANALYTICS_RETENTION_DAYS", "365")),
            real_time_updates=os.getenv("REAL_TIME_UPDATES", "true").lower() == "true"
        )
        
        # Model configuration
        self.model_cache_dir = os.getenv("MODEL_CACHE_DIR", "models")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        
        # API configuration
        self.api_host = os.getenv("API_HOST", "localhost")
        self.api_port = int(os.getenv("API_PORT", "8501"))
        self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """Get Streamlit-specific configuration"""
        return {
            "page_title": "HTS AI Agent Pro",
            "page_icon": "🚀",
            "layout": "wide",
            "initial_sidebar_state": self.ui.sidebar_default_state,
            "menu_items": {
                'Get Help': 'https://htsagent.com/help',
                'Report a bug': 'https://htsagent.com/bugs',
                'About': 'HTS AI Agent Pro v2.0 - Advanced Trade Intelligence Platform'
            }
        }
    
    def get_color_scheme(self) -> Dict[str, str]:
        """Get the current color scheme"""
        if self.ui.enable_dark_mode:
            return {
                "primary": "#8b5cf6",
                "secondary": "#a855f7",
                "background": "#1f2937",
                "surface": "#374151",
                "text": "#f9fafb",
                "text_secondary": "#d1d5db"
            }
        else:
            return {
                "primary": self.ui.primary_color,
                "secondary": self.ui.secondary_color,
                "background": "#ffffff",
                "surface": "#f8f9fa",
                "text": "#212529",
                "text_secondary": "#6c757d"
            }
    
    def get_chart_theme(self) -> str:
        """Get chart theme based on UI settings"""
        return "plotly_dark" if self.ui.enable_dark_mode else "plotly_white"
    
    def validate_config(self) -> List[str]:
        """Validate configuration settings and return any issues"""
        issues = []
        
        # Check database paths
        if not os.path.exists(os.path.dirname(self.database.hts_db_path)):
            issues.append(f"Database directory does not exist: {os.path.dirname(self.database.hts_db_path)}")
        
        # Check model cache directory
        if not os.path.exists(self.model_cache_dir):
            issues.append(f"Model cache directory does not exist: {self.model_cache_dir}")
        
        # Validate performance settings
        if self.performance.batch_processing_max_records > 10000:
            issues.append("Batch processing max records exceeds recommended limit (10000)")
        
        # Validate cache size
        if self.performance.cache_size_mb > 1000:
            issues.append("Cache size exceeds recommended limit (1000MB)")
        
        return issues
    
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            "data",
            "data/vector_store",
            "data/hts_csvs",
            "data/general_notes",
            "logs",
            "exports",
            "backups",
            self.model_cache_dir
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "default",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG" if self.debug_mode else "INFO",
                    "formatter": "detailed",
                    "filename": "logs/hts_agent.log",
                    "mode": "a"
                }
            },
            "loggers": {
                "hts_agent": {
                    "level": "DEBUG" if self.debug_mode else "INFO",
                    "handlers": ["console", "file"],
                    "propagate": False
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"]
            }
        }

# Feature flags for enabling/disabling functionality
FEATURE_FLAGS = {
    "ADVANCED_ANALYTICS": True,
    "BATCH_PROCESSING": True,
    "EXPORT_ENHANCED": True,
    "REAL_TIME_CHARTS": True,
    "PREDICTIVE_INSIGHTS": True,
    "GEOGRAPHIC_MAPPING": True,
    "COMPLIANCE_MONITORING": True,
    "API_INTEGRATION": False,  # Disabled by default
    "AUTHENTICATION": False,   # Disabled by default
    "AUDIT_TRAIL": True,
    "BACKUP_AUTOMATION": True,
    "PERFORMANCE_MONITORING": True
}

# Default user preferences
DEFAULT_USER_PREFERENCES = {
    "dashboard_layout": "standard",
    "chart_preferences": {
        "default_chart_type": "plotly",
        "color_scheme": "modern",
        "animation_duration": 500
    },
    "export_preferences": {
        "default_format": "excel",
        "include_charts": True,
        "include_summary": True
    },
    "notification_preferences": {
        "enable_notifications": True,
        "notification_types": ["success", "error", "warning"]
    }
}

# Application constants
APP_CONSTANTS = {
    "VERSION": "2.0.0",
    "BUILD_DATE": "2024-01-15",
    "AUTHOR": "HTS AI Agent Team",
    "LICENSE": "MIT",
    "SUPPORTED_FILE_TYPES": ["csv", "xlsx", "pdf", "json"],
    "MAX_FILE_SIZE_MB": 50,
    "SUPPORTED_EXPORT_FORMATS": ["excel", "pdf", "csv", "json"],
    "DEFAULT_PAGINATION_SIZE": 25,
    "CHART_EXPORT_DPI": 300,
    "PDF_EXPORT_QUALITY": "high"
}

# Create global config instance
config = AppConfig()

def get_config() -> AppConfig:
    """Get the global configuration instance"""
    return config

def reload_config():
    """Reload configuration from environment variables"""
    global config
    config = AppConfig()

def update_config(**kwargs):
    """Update configuration settings"""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)

def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURE_FLAGS.get(feature_name, False)

def get_user_preferences() -> Dict[str, Any]:
    """Get default user preferences"""
    return DEFAULT_USER_PREFERENCES.copy()

def get_app_constants() -> Dict[str, Any]:
    """Get application constants"""
    return APP_CONSTANTS.copy() 