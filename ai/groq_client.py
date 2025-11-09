"""
Groq LLM Client for Fitness Posture Analysis
Uses Groq's fast LPU-based inference for real-time feedback
"""

import os
from groq import Groq
import logging

logger = logging.getLogger(__name__)

class GroqFitnessCoach:
    def __init__(self, api_key=None):
        """Initialize Groq client with API key"""
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Fast, capable model from Groq
        
        logger.info(f"Initialized Groq Fitness Coach with model: {self.model}")
    
    def analyze_posture(self, exercise_type, posture_data, context=None):
        """
        Analyze exercise posture and provide coaching feedback
        
        Args:
            exercise_type: Type of exercise (squat, push_up, hammer_curl)
            posture_data: Dictionary with angles, landmarks, warnings
            context: Additional context (rep count, set number, etc.)
        
        Returns:
            str: Coaching feedback text
        """
        try:
            # Build system prompt based on exercise type
            system_prompt = self._get_system_prompt(exercise_type)
            
            # Build user message with posture data
            user_message = self._format_posture_data(exercise_type, posture_data, context)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=150,  # Keep responses concise for voice
                top_p=1,
                stream=False
            )
            
            feedback = response.choices[0].message.content.strip()
            logger.info(f"Generated feedback for {exercise_type}: {feedback[:50]}...")
            
            return feedback
            
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return "Keep going! Focus on your form."
    
    def _get_system_prompt(self, exercise_type):
        """Get exercise-specific system prompt"""
        
        base_prompt = """You are an expert fitness coach with deep knowledge of biomechanics and exercise form. 
Your job is to analyze real-time posture data from a user's workout and provide SHORT, ACTIONABLE, ENCOURAGING voice feedback.

Guidelines:
- Keep responses under 20 words for voice delivery
- Be specific about what to fix
- Use simple, clear language
- Stay positive and motivating
- Focus on ONE key correction at a time
- Don't repeat information already given"""

        exercise_prompts = {
            "squat": base_prompt + """

**SQUAT EXPERTISE:**
- Knee angle should be 70-170°
- Back should stay straight (torso angle < 45°)
- Knees should NOT go past toes
- Weight on heels, chest up
- Depth: thighs parallel to ground""",

            "push_up": base_prompt + """

**PUSH-UP EXPERTISE:**
- Body should form straight line (plank position)
- Elbows at 45° from body (not flaring out)
- Lower until chest near ground (elbow angle ~70°)
- Core engaged, no sagging hips
- Full range of motion""",

            "hammer_curl": base_prompt + """

**HAMMER CURL EXPERTISE:**
- Elbows stay close to sides (< 40° from body)
- No swinging or momentum
- Controlled motion up and down
- Shoulders stable, no shrugging
- Full contraction at top, full extension at bottom"""
        }
        
        return exercise_prompts.get(exercise_type, base_prompt)
    
    def _format_posture_data(self, exercise_type, posture_data, context):
        """Format posture data into readable message"""
        
        message_parts = [f"**Current Exercise: {exercise_type.upper()}**\n"]
        
        # Add context info
        if context:
            if 'rep' in context:
                message_parts.append(f"Rep: {context['rep']}/{context.get('goal_reps', '?')}")
            if 'set' in context:
                message_parts.append(f"Set: {context['set']}/{context.get('goal_sets', '?')}")
            message_parts.append("\n")
        
        # Add posture data based on exercise type
        if exercise_type == "squat":
            message_parts.append(f"**Posture Data:**\n")
            message_parts.append(f"- Knee angle: {posture_data.get('angle', 'N/A')}°")
            message_parts.append(f"- Stage: {posture_data.get('stage', 'Unknown')}")
            if 'warning' in posture_data and posture_data['warning']:
                message_parts.append(f"- ⚠️ Warning: {posture_data['warning']}")
        
        elif exercise_type == "push_up":
            message_parts.append(f"**Posture Data:**\n")
            message_parts.append(f"- Elbow angle: {posture_data.get('angle', 'N/A')}°")
            message_parts.append(f"- Stage: {posture_data.get('stage', 'Unknown')}")
            if 'warning' in posture_data and posture_data['warning']:
                message_parts.append(f"- ⚠️ Warning: {posture_data['warning']}")
        
        elif exercise_type == "hammer_curl":
            message_parts.append(f"**Posture Data:**\n")
            message_parts.append(f"- Right arm angle: {posture_data.get('angle_right', 'N/A')}°")
            message_parts.append(f"- Left arm angle: {posture_data.get('angle_left', 'N/A')}°")
            message_parts.append(f"- Right stage: {posture_data.get('stage_right', 'Unknown')}")
            message_parts.append(f"- Left stage: {posture_data.get('stage_left', 'Unknown')}")
            if 'warning_right' in posture_data and posture_data['warning_right']:
                message_parts.append(f"- ⚠️ Right: {posture_data['warning_right']}")
            if 'warning_left' in posture_data and posture_data['warning_left']:
                message_parts.append(f"- ⚠️ Left: {posture_data['warning_left']}")
        
        message_parts.append("\n**Provide brief coaching tip (max 20 words):**")
        
        return "\n".join(message_parts)
    
    def quick_encouragement(self):
        """Get a quick encouraging phrase"""
        encouragements = [
            "Great form! Keep it up!",
            "You're doing awesome!",
            "Perfect! One more!",
            "Excellent work!",
            "Strong rep! Next one!",
            "Looking good! Keep going!",
            "Nice! Control that movement!",
            "Solid form! Push through!"
        ]
        import random
        return random.choice(encouragements)

