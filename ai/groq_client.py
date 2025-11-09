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
        
        base_prompt = """You are an elite personal trainer with expertise in biomechanics and injury prevention. 
Analyze real-time posture data and provide IMMEDIATE, SPECIFIC voice coaching.

COACHING STRATEGY:
1. If WARNING present → Address it FIRST (safety critical)
2. If at starting position → Cue next movement phase
3. If mid-movement → Check form quality
4. If completing rep → Give brief encouragement OR correction

VOICE RULES:
- Maximum 15 words
- Use action verbs (push, squeeze, drive, engage)
- Be SPECIFIC with body parts
- Mix corrections with motivation
- Vary your responses - don't be repetitive"""

        exercise_prompts = {
            "squat": base_prompt + """

**SQUAT BIOMECHANICS:**
DANGER ZONES (priority corrections):
- Knee angle < 70° → Risk: knee joint stress → "Don't go too deep, protect your knees"
- Knees past toes → Risk: ACL strain → "Knees back, sit into heels"
- Torso lean > 45° → Risk: lower back → "Chest up, core tight"

FORM OPTIMIZATION:
- Starting (angle 150-170°): Cue "Breathe in, push hips back"
- Descent (angle 90-150°): Check "Control the drop, knees out"  
- Bottom (angle 70-90°): Cue "Drive through heels"
- Ascent (angle 90-150°): Encourage "Squeeze glutes, power up"

PERFECT FORM INDICATORS:
- Knee angle 85-95° at bottom
- Even tempo
- Controlled breathing""",

            "push_up": base_prompt + """

**PUSH-UP BIOMECHANICS:**
DANGER ZONES (priority corrections):
- Hips sagging → Risk: lower back → "Engage core, hips level"
- Elbows > 70° flare → Risk: shoulder → "Elbows in, forty-five degrees"
- Incomplete range → Ineffective → "Lower more, chest to floor"

FORM OPTIMIZATION:
- Top position: Cue "Brace core, shoulders over hands"
- Descent: Check "Slow and controlled, elbows track back"
- Bottom: Cue "Chest almost touches"
- Ascent: Encourage "Press hard, full extension"

PERFECT FORM INDICATORS:
- Straight body line
- Elbow angle 70-90° at bottom
- Shoulder stability""",

            "hammer_curl": base_prompt + """

**HAMMER CURL BIOMECHANICS:**
DANGER ZONES (priority corrections):
- Elbow drift forward → Risk: momentum/ineffective → "Pin elbows to sides"
- Shoulder shrug → Risk: trap dominance → "Shoulders down and back"
- Swinging → Risk: back strain → "Stop swinging, control the weight"

FORM OPTIMIZATION:
- Starting: Cue "Arms fully extended, shoulders stable"
- Curl up: Check "Squeeze biceps, slow and controlled"
- Peak: Cue "Hold and squeeze"
- Lower: Encourage "Resist on the way down"

PERFECT FORM INDICATORS:
- Elbows stationary
- Smooth tempo
- Full range both directions"""
        }
        
        return exercise_prompts.get(exercise_type, base_prompt)
    
    def _format_posture_data(self, exercise_type, posture_data, context):
        """Format posture data into readable message"""
        
        # Determine feedback type and urgency
        priority = context.get('feedback_priority', 'normal') if context else 'normal'
        
        message_parts = [f"**Current Exercise: {exercise_type.upper()}**\n"]
        
        # Add urgency context
        if priority == "urgent":
            message_parts.append("⚠️ SAFETY ISSUE DETECTED - Address immediately!\n")
        elif priority == "milestone":
            message_parts.append("🎯 New rep started - Encourage and check form\n")
        elif priority == "technique":
            message_parts.append("💡 Movement phase changed - Provide technique cue\n")
        
        # Add progress context
        if context:
            if 'rep' in context:
                message_parts.append(f"Rep: {context['rep']}/{context.get('goal_reps', '?')}")
            if 'set' in context:
                message_parts.append(f"Set: {context['set']}/{context.get('goal_sets', '?')}")
            message_parts.append("\n")
        
        # Add detailed posture data based on exercise type
        if exercise_type == "squat":
            message_parts.append(f"**Posture Data:**\n")
            angle = posture_data.get('angle', 0)
            message_parts.append(f"- Knee angle: {angle:.1f}°")
            message_parts.append(f"- Stage: {posture_data.get('stage', 'Unknown')}")
            
            # Add interpretation hints
            if angle < 70:
                message_parts.append(f"- (Too deep - risk zone)")
            elif 85 <= angle <= 95:
                message_parts.append(f"- (Perfect depth)")
            elif angle > 170:
                message_parts.append(f"- (Standing/ready)")
            
            if 'warning' in posture_data and posture_data['warning']:
                message_parts.append(f"- ⚠️ {posture_data['warning']}")
        
        elif exercise_type == "push_up":
            message_parts.append(f"**Posture Data:**\n")
            angle = posture_data.get('angle', 0)
            message_parts.append(f"- Elbow angle: {angle:.1f}°")
            message_parts.append(f"- Stage: {posture_data.get('stage', 'Unknown')}")
            
            # Add interpretation hints
            if angle < 70:
                message_parts.append(f"- (Not low enough)")
            elif 70 <= angle <= 90:
                message_parts.append(f"- (Good depth)")
            elif angle > 160:
                message_parts.append(f"- (Top position)")
            
            if 'warning' in posture_data and posture_data['warning']:
                message_parts.append(f"- ⚠️ {posture_data['warning']}")
        
        elif exercise_type == "hammer_curl":
            message_parts.append(f"**Posture Data:**\n")
            angle_r = posture_data.get('angle_right', 0)
            angle_l = posture_data.get('angle_left', 0)
            message_parts.append(f"- Right arm angle: {angle_r:.1f}°")
            message_parts.append(f"- Left arm angle: {angle_l:.1f}°")
            message_parts.append(f"- Right stage: {posture_data.get('stage_right', 'Unknown')}")
            message_parts.append(f"- Left stage: {posture_data.get('stage_left', 'Unknown')}")
            
            # Check for imbalance
            if abs(angle_r - angle_l) > 20:
                message_parts.append(f"- (Imbalanced - {abs(angle_r - angle_l):.0f}° difference)")
            
            if 'warning_right' in posture_data and posture_data['warning_right']:
                message_parts.append(f"- ⚠️ Right: {posture_data['warning_right']}")
            if 'warning_left' in posture_data and posture_data['warning_left']:
                message_parts.append(f"- ⚠️ Left: {posture_data['warning_left']}")
        
        message_parts.append("\n**Provide brief coaching tip (max 15 words):**")
        
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
    
    def get_breathing_cue(self, exercise_type, stage):
        """Get exercise-specific breathing cues"""
        breathing_cues = {
            "squat": {
                "Descent": "Breathe in as you lower",
                "Ascent": "Exhale, drive up",
                "Starting Position": "Take a breath, brace your core"
            },
            "push_up": {
                "Down": "Inhale going down",
                "Up": "Exhale, press up",
                "Initial": "Breathe steady, brace core"
            },
            "hammer_curl": {
                "Down": "Inhale, control the descent",
                "Up": "Exhale, squeeze biceps",
                "Starting Position": "Breathe naturally, stay controlled"
            }
        }
        
        exercise_cues = breathing_cues.get(exercise_type, {})
        return exercise_cues.get(stage, "Breathe steady, stay controlled")
    
    def generate_workout_report(self, workout_data):
        """
        Generate a comprehensive workout report using LLM
        
        Args:
            workout_data: Dictionary with workout session data
                {
                    'exercise_type': str,
                    'sets_completed': int,
                    'total_reps': int,
                    'duration_seconds': int,
                    'avg_angle': float,
                    'warnings_count': int,
                    'perfect_form_percentage': float (optional)
                }
        
        Returns:
            dict: Structured report with text summary and recommendations
        """
        try:
            report_prompt = f"""Analyze this workout session and provide a brief performance report.

**Workout Summary:**
- Exercise: {workout_data['exercise_type'].upper()}
- Sets completed: {workout_data.get('sets_completed', 0)}
- Total reps: {workout_data.get('total_reps', 0)}
- Duration: {workout_data.get('duration_seconds', 0)} seconds
- Form warnings: {workout_data.get('warnings_count', 0)}

Provide:
1. One sentence performance summary
2. One key strength
3. One area for improvement
4. One specific tip for next session

Keep total response under 100 words, clear and motivating."""

            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional fitness coach providing post-workout analysis."},
                    {"role": "user", "content": report_prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=300
            )
            
            report_text = response.choices[0].message.content.strip()
            logger.info(f"Generated workout report for {workout_data['exercise_type']}")
            
            return {
                'success': True,
                'report': report_text,
                'workout_data': workout_data
            }
            
        except Exception as e:
            logger.error(f"Error generating workout report: {e}")
            return {
                'success': False,
                'report': f"Great work on your {workout_data['exercise_type']} session! Keep training consistently.",
                'error': str(e)
            }

