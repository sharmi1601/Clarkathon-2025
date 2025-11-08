import sqlite3
import os
from datetime import datetime, timedelta
from collections import defaultdict

class WorkoutLogger:
    def __init__(self, db_path='db/workouts.db'):
        """Initialize the workout logger with SQLite database"""
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create the workouts table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                exercise_type TEXT NOT NULL,
                sets INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                duration_seconds INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_workout(self, exercise_type, sets, reps, duration_seconds):
        """Log a completed workout to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT INTO workouts (date, exercise_type, sets, reps, duration_seconds)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, exercise_type, sets, reps, duration_seconds))
        
        conn.commit()
        workout_id = cursor.lastrowid
        conn.close()
        
        return {'id': workout_id, 'success': True}
    
    def get_recent_workouts(self, limit=5):
        """Get the most recent workouts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, exercise_type, sets, reps, duration_seconds
            FROM workouts
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        workouts = []
        for row in cursor.fetchall():
            workouts.append({
                'date': row[0],
                'exercise_type': row[1],
                'sets': row[2],
                'reps': row[3],
                'duration_seconds': row[4]
            })
        
        conn.close()
        return workouts
    
    def get_weekly_stats(self):
        """Get workout statistics for the past 7 days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate date 7 days ago
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT date, COUNT(*) as workout_count, SUM(sets * reps) as total_reps
            FROM workouts
            WHERE date >= ?
            GROUP BY date
            ORDER BY date
        ''', (week_ago,))
        
        # Initialize all days with zero
        stats = {}
        for i in range(7):
            day = datetime.now() - timedelta(days=6-i)
            day_name = day.strftime('%A')
            stats[day_name] = {'workout_count': 0, 'total_reps': 0}
        
        # Fill in actual data
        for row in cursor.fetchall():
            workout_date = datetime.strptime(row[0], '%Y-%m-%d')
            day_name = workout_date.strftime('%A')
            if day_name in stats:
                stats[day_name] = {
                    'workout_count': row[1],
                    'total_reps': row[2] if row[2] else 0
                }
        
        conn.close()
        return stats
    
    def get_exercise_distribution(self):
        """Get the distribution of exercises performed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT exercise_type, COUNT(*) as count
            FROM workouts
            GROUP BY exercise_type
            ORDER BY count DESC
        ''')
        
        distribution = {}
        for row in cursor.fetchall():
            distribution[row[0]] = row[1]
        
        conn.close()
        return distribution
    
    def get_user_stats(self):
        """Get overall user statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total workouts
        cursor.execute('SELECT COUNT(*) FROM workouts')
        total_workouts = cursor.fetchone()[0]
        
        # Total exercises (sets * reps)
        cursor.execute('SELECT SUM(sets * reps) FROM workouts')
        total_exercises = cursor.fetchone()[0] or 0
        
        # Calculate streak
        cursor.execute('''
            SELECT DISTINCT date
            FROM workouts
            ORDER BY date DESC
        ''')
        
        dates = [row[0] for row in cursor.fetchall()]
        streak_days = 0
        
        if dates:
            current_date = datetime.now().date()
            for i, date_str in enumerate(dates):
                workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                expected_date = current_date - timedelta(days=i)
                
                if workout_date == expected_date:
                    streak_days += 1
                else:
                    break
        
        conn.close()
        
        return {
            'total_workouts': total_workouts,
            'total_exercises': total_exercises,
            'streak_days': streak_days
        }
    
    def get_all_workouts(self):
        """Get all workouts from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, date, exercise_type, sets, reps, duration_seconds, created_at
            FROM workouts
            ORDER BY created_at DESC
        ''')
        
        workouts = []
        for row in cursor.fetchall():
            workouts.append({
                'id': row[0],
                'date': row[1],
                'exercise_type': row[2],
                'sets': row[3],
                'reps': row[4],
                'duration_seconds': row[5],
                'created_at': row[6]
            })
        
        conn.close()
        return workouts
    
    def delete_workout(self, workout_id):
        """Delete a specific workout"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def clear_all_data(self):
        """Clear all workout data (use with caution)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM workouts')
        
        conn.commit()
        conn.close()
        
        return {'success': True}

