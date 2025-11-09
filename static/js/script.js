document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const exerciseOptions = document.querySelectorAll('.exercise-item');
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const setsInput = document.getElementById('sets');
    const repsInput = document.getElementById('reps');
    const currentExercise = document.getElementById('current-exercise');
    const currentSet = document.getElementById('current-set');
    const currentReps = document.getElementById('current-reps');
    
    // Variables
    let selectedExercise = null;
    let workoutRunning = false;
    let statusCheckInterval = null;
    let postureCheckInterval = null;
    
    // Select exercise
    exerciseOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            exerciseOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add selected class to clicked option
            this.classList.add('selected');
            selectedExercise = this.getAttribute('data-exercise');
            
            // Visual feedback
            console.log('Selected exercise:', selectedExercise);
        });
    });
    
    // Start workout
    startBtn.addEventListener('click', function() {
        if (!selectedExercise) {
            alert('Please select an exercise first!');
            return;
        }
        
        const sets = parseInt(setsInput.value);
        const reps = parseInt(repsInput.value);
        
        if (isNaN(sets) || sets < 1 || isNaN(reps) || reps < 1) {
            alert('Please enter valid numbers for sets and repetitions.');
            return;
        }
        
        // Start the exercise via API
        fetch('/start_exercise', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                exercise_type: selectedExercise,
                sets: sets,
                reps: reps
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                workoutRunning = true;
                startBtn.disabled = true;
                stopBtn.disabled = false;
                
                // Update UI
                currentExercise.textContent = selectedExercise.replace('_', ' ').toUpperCase();
                currentSet.textContent = `1 / ${sets}`;
                currentReps.textContent = `0 / ${reps}`;
                
                // Start status polling
                statusCheckInterval = setInterval(checkStatus, 1000);
            } else {
                alert('Failed to start exercise: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while starting the exercise.');
        });
    });
    
    // Stop workout
    stopBtn.addEventListener('click', function() {
        fetch('/stop_exercise', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resetWorkoutUI();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Voice Coach toggle button
    const voiceCoachBtn = document.getElementById('voice-coach-btn');
    const aiCoachStatus = document.getElementById('ai-coach-status');
    
    if (voiceCoachBtn) {
        // Check AI coach status on load
        fetch('/ai_coach_status')
            .then(response => response.json())
            .then(data => {
                if (data.available) {
                    aiCoachStatus.style.display = 'flex';
                    voiceCoachBtn.setAttribute('data-enabled', data.voice_enabled ? 'true' : 'false');
                    voiceCoachBtn.textContent = `Voice Coach: ${data.voice_enabled ? 'ON' : 'OFF'}`;
                } else {
                    voiceCoachBtn.style.display = 'none';
                }
            })
            .catch(error => console.error('Error checking AI coach status:', error));
        
        voiceCoachBtn.addEventListener('click', function() {
            const currentlyEnabled = this.getAttribute('data-enabled') === 'true';
            const newState = !currentlyEnabled;
            
            fetch('/toggle_voice_coach', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ enable: newState })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.setAttribute('data-enabled', data.voice_enabled ? 'true' : 'false');
                    this.textContent = `Voice Coach: ${data.voice_enabled ? 'ON' : 'OFF'}`;
                    console.log(`Voice coaching ${data.voice_enabled ? 'enabled' : 'disabled'}`);
                }
            })
            .catch(error => {
                console.error('Error toggling voice coach:', error);
            });
        });
    }

    // Test Posture button
    const testPostureBtn = document.getElementById('test-posture-btn');
    const postureStreakEl = document.getElementById('posture-streak');
    let testMode = false;

    testPostureBtn.addEventListener('click', function() {
        // Toggle test posture mode
        testMode = !testMode;
        const mode = testMode ? 'test_posture' : 'workout';

        // Use selectedExercise if available, default to hammer_curl
        const exercise_type = selectedExercise || 'hammer_curl';

        fetch('/set_test_posture', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: mode, exercise_type: exercise_type })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                testPostureBtn.textContent = testMode ? 'Stop Test' : 'Test Posture';
                // Poll posture status when in test mode
                if (testMode) {
                    postureCheckInterval = setInterval(checkPostureStatus, 1000);
                } else {
                    if (postureCheckInterval) { clearInterval(postureCheckInterval); postureCheckInterval = null; }
                    postureStreakEl.textContent = '0';
                }
            } else {
                alert('Failed to toggle test posture: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(err => { console.error(err); alert('Error toggling test posture'); });
    });

    function checkPostureStatus() {
        fetch('/test_posture_status')
        .then(r => r.json())
        .then(data => {
            if (!data || data.mode === 'none') return;
            postureStreakEl.textContent = data.correct_reps_streak || 0;
            if (data.ready_to_start) {
                // Stop polling and show message
                if (postureCheckInterval) { clearInterval(postureCheckInterval); postureCheckInterval = null; }
                alert('Posture validated — you\'re ready to start!');
                testMode = false;
                testPostureBtn.textContent = 'Test Posture';
            }
        })
        .catch(err => console.error('Error fetching posture status', err));
    }
    
    // Function to check status
    function checkStatus() {
        fetch('/get_status')
        .then(response => response.json())
        .then(data => {
            if (!data.exercise_running && workoutRunning) {
                // Workout has ended
                resetWorkoutUI();
                return;
            }
            
            // Update status display
            currentSet.textContent = `${data.current_set} / ${data.total_sets}`;
            currentReps.textContent = `${data.current_reps} / ${data.rep_goal}`;
        })
        .catch(error => {
            console.error('Error checking status:', error);
        });
    }
    
    // Reset UI after workout ends
    function resetWorkoutUI() {
        workoutRunning = false;
        startBtn.disabled = false;
        stopBtn.disabled = true;
        
        if (statusCheckInterval) {
            clearInterval(statusCheckInterval);
            statusCheckInterval = null;
        }
        
        currentExercise.textContent = 'None';
        currentSet.textContent = '0 / 0';
        currentReps.textContent = '0 / 0';
    }
});
