"""
AI Coach Coordinator
Coordinates between posture detection, LLM analysis, and voice feedback
"""

import time
import logging
from ai.groq_client import GroqFitnessCoach
from ai.voice_feedback import speak_feedback

logger = logging.getLogger(__name__)

class AICoachCoordinator:
    def __init__(self, groq_api_key, enable_voice=True):
        """
        Initialize AI Coach system
        
        Args:
            groq_api_key: Groq API key for LLM
            enable_voice: Enable voice feedback
        """
        self.enable_voice = enable_voice
        self.last_feedback_time = 0
        self.feedback_cooldown = 8  # Seconds between feedback
        self.rep_last_feedback = -1  # Track when we last gave feedback
        
        # Initialize Groq LLM
        try:
            self.groq_coach = GroqFitnessCoach(api_key=groq_api_key)
            logger.info("✅ Groq Fitness Coach initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq: {e}")
            self.groq_coach = None
        
        logger.info(f"🎤 Voice feedback: {'Enabled' if enable_voice else 'Disabled'}")
    
    def analyze_and_coach(self, exercise_type, posture_data, context=None):
        """
        Main function: Analyze posture and provide voice coaching
        
        Args:
            exercise_type: Type of exercise
            posture_data: Current posture measurements
            context: Additional context (rep count, etc.)
        
        Returns:
            str: Feedback text (also spoken if voice enabled)
        """
        if not self.groq_coach:
            return None
        
        current_time = time.time()
        current_rep = context.get('rep', 0) if context else 0
        
        # Cooldown logic: Don't spam feedback
        if current_time - self.last_feedback_time < self.feedback_cooldown:
            return None
        
        # Only give feedback when form is wrong OR new rep starts
        has_warning = self._has_warning(posture_data)
        new_rep = current_rep != self.rep_last_feedback
        
        if not has_warning and not new_rep:
            return None
        
        try:
            # Get LLM analysis
            feedback_text = self.groq_coach.analyze_posture(
                exercise_type=exercise_type,
                posture_data=posture_data,
                context=context
            )
            
            if feedback_text:
                # Speak feedback
                if self.enable_voice:
                    speak_feedback(feedback_text, priority=has_warning)
                
                # Update tracking
                self.last_feedback_time = current_time
                self.rep_last_feedback = current_rep
                
                logger.info(f"🗣️ Feedback: {feedback_text}")
                return feedback_text
                
        except Exception as e:
            logger.error(f"Error in coach analysis: {e}")
        
        return None
    
    def give_encouragement(self, milestone_type="rep"):
        """
        Give encouraging feedback at milestones
        
        Args:
            milestone_type: Type of milestone (rep, set, workout_complete)
        """
        if not self.enable_voice or not self.groq_coach:
            return
        
        encouragements = {
            "rep": self.groq_coach.quick_encouragement(),
            "set": "Great set! Take a breath and keep going!",
            "workout_complete": "Workout complete! Excellent work today!"
        }
        
        message = encouragements.get(milestone_type, "Keep going!")
        speak_feedback(message, priority=False)
        logger.info(f"🎉 Encouragement: {message}")
    
    def _has_warning(self, posture_data):
        """Check if posture data contains warnings"""
        return (
            posture_data.get('warning') or
            posture_data.get('warning_right') or
            posture_data.get('warning_left')
        )
    
    def test_voice(self):
        """Test voice feedback system"""
        if self.enable_voice:
            speak_feedback("AI Fitness Coach initialized. Let's get started!", priority=True)
            return True
        return False

# Global coach instance
_coach = None

def initialize_coach(groq_api_key, enable_voice=True):
    """Initialize global coach instance"""
    global _coach
    try:
        _coach = AICoachCoordinator(groq_api_key=groq_api_key, enable_voice=enable_voice)
        logger.info("✅ AI Coach initialized successfully")
        return _coach
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI Coach: {e}")
        return None

def get_coach():
    """Get global coach instance"""
    return _coach

def provide_coaching(exercise_type, posture_data, context=None):
    """Convenience function to get coaching"""
    if _coach:
        return _coach.analyze_and_coach(exercise_type, posture_data, context)
    return None

