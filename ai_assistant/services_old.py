"""
Original AI Service Layer - Groq Integration
Enhanced with proper error handling and Groq API
Preserved for reference - use enhanced_services.py instead
"""
import json
import time
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from .models import AIRequest

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass


class AIService:
    """
    AI Service for product and store generation
    Supports both Groq API and mock mode with automatic fallback
    """
    
    def __init__(self):
        self.mock_mode = settings.AI_MOCK_MODE
        self.client = None
        
        # Try to initialize Groq client if not in mock mode
        if not self.mock_mode and settings.GROQ_API_KEY:
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info("Groq client initialized successfully")
            except ImportError as e:
                logger.warning(f"Groq package not available: {e}. Falling back to mock mode.")
                self.mock_mode = True
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}. Falling back to mock mode.")
                self.mock_mode = True
        else:
            logger.info("Running in mock mode (no API key or AI_MOCK_MODE=True)")
            self.mock_mode = True
