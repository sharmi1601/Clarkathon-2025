"""
AI Coaching Module
Integrates Groq LLM with voice feedback for real-time fitness coaching
"""

from ai.coach_coordinator import initialize_coach, get_coach, provide_coaching
from ai.voice_feedback import speak_feedback, get_voice_system
from ai.groq_client import GroqFitnessCoach

__all__ = [
    'initialize_coach',
    'get_coach',
    'provide_coaching',
    'speak_feedback',
    'get_voice_system',
    'GroqFitnessCoach'
]

