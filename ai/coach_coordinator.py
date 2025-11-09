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
        self.last_warning_time = 0
        self.feedback_cooldown = 6  # Seconds between normal feedback
        self.warning_cooldown = 3  # Shorter cooldown for safety warnings
        self.rep_last_feedback = -1  # Track when we last gave feedback
        self.last_stage = None  # Track movement stage changes
        self.feedback_count = 0  # Track total feedback given
        
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
        Main function: Analyze posture and provide voice coaching with smart timing
        
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
        current_stage = posture_data.get('stage', '')
        
        # Check feedback triggers (prioritized)
        has_warning = self._has_warning(posture_data)
        new_rep = current_rep != self.rep_last_feedback
        stage_changed = current_stage != self.last_stage
        
        # Priority 1: Safety warnings (shortest cooldown)
        if has_warning:
            if current_time - self.last_warning_time < self.warning_cooldown:
                return None  # Too soon for another warning
            priority = "urgent"
        
        # Priority 2: New rep started (motivational + form check)
        elif new_rep and current_rep > 0:
            if current_time - self.last_feedback_time < self.feedback_cooldown:
                return None
            priority = "milestone"
        
        # Priority 3: Stage change (technique cues)
        elif stage_changed and self.feedback_count > 0:  # Skip first stage change
            if current_time - self.last_feedback_time < self.feedback_cooldown:
                return None
            priority = "technique"
        
        # Priority 4: Periodic check-ins
        elif current_time - self.last_feedback_time > self.feedback_cooldown * 2:
            priority = "encouragement"
        
        else:
            return None  # No feedback needed now
        
        try:
            # Enhance context with priority info
            enhanced_context = context.copy() if context else {}
            enhanced_context['feedback_priority'] = priority
            enhanced_context['stage'] = current_stage
            
            # Get LLM analysis
            feedback_text = self.groq_coach.analyze_posture(
                exercise_type=exercise_type,
                posture_data=posture_data,
                context=enhanced_context
            )
            
            if feedback_text:
                # Speak feedback with appropriate priority
                if self.enable_voice:
                    speak_feedback(feedback_text, priority=(priority == "urgent"))
                
                # Update tracking
                self.last_feedback_time = current_time
                if has_warning:
                    self.last_warning_time = current_time
                self.rep_last_feedback = current_rep
                self.last_stage = current_stage
                self.feedback_count += 1
                
                logger.info(f"🗣️ [{priority.upper()}] Feedback: {feedback_text}")
                return feedback_text
                
        except Exception as e:
            logger.error(f"Error in coach analysis: {e}")
        
        return None
    
    def give_encouragement(self, milestone_type="rep", rep_num=0, total_reps=0):
        """
        Give encouraging feedback at milestones
        
        Args:
            milestone_type: Type of milestone (rep, set, workout_complete)
            rep_num: Current rep number
            total_reps: Total reps in set
        """
        if not self.enable_voice or not self.groq_coach:
            return
        
        # Context-aware encouragements
        if milestone_type == "rep":
            if rep_num == 1:
                message = "First rep! Focus on perfect form!"
            elif rep_num == total_reps // 2:
                message = "Halfway there! Keep pushing!"
            elif rep_num >= total_reps - 2:
                message = f"Almost done! {total_reps - rep_num} more!"
            else:
                message = self.groq_coach.quick_encouragement()
        elif milestone_type == "set":
            message = "Set complete! Shake it out, breathe deep!"
        elif milestone_type == "workout_complete":
            message = "Workout complete! Outstanding effort today!"
        else:
            message = "Keep going! You've got this!"
        
        speak_feedback(message, priority=False)
        logger.info(f"🎉 Encouragement: {message}")
    
    def reset_session(self):
        """Reset tracking variables for new workout session"""
        self.last_feedback_time = 0
        self.last_warning_time = 0
        self.rep_last_feedback = -1
        self.last_stage = None
        self.feedback_count = 0
        logger.info("🔄 AI Coach session reset")
    
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

