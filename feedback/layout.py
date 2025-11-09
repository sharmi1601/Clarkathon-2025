# feedback/layout.py

from feedback.indicators import draw_squat_indicators, draw_pushup_indicators, draw_hammercurl_indicators

def layout_indicators(frame, exercise_type, exercise_data):
    if exercise_type == "squat":
        counter, angle, stage = exercise_data
        draw_squat_indicators(frame, counter, angle, stage)
    elif exercise_type == "push_up":
        counter, angle, stage = exercise_data
        draw_pushup_indicators(frame, counter, angle, stage)
    elif exercise_type == "hammer_curl":
        (counter_right, angle_right, counter_left, angle_left,
         warning_message_right, warning_message_left, progress_right, progress_left,
         stage_right, stage_left, posture_errors, correct_reps_streak, ready_to_start) = exercise_data
        # Pass through posture feedback values as optional args (indicators may ignore them)
        draw_hammercurl_indicators(frame, counter_right, angle_right, counter_left, angle_left,
                                   stage_right, stage_left, posture_errors=posture_errors,
                                   correct_reps_streak=correct_reps_streak, ready_to_start=ready_to_start)

