from datetime import datetime, timedelta

def calculate_reward(task_deadline):
    # Define the reward parameters
    on_time_bonus = 100  # Bonus points for submitting on time
    early_submission_bonus = 50  # Bonus points for submitting before the deadline

    # Convert task_deadline and submission_time to datetime objects
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    task_deadline = datetime.strptime(task_deadline, "%Y-%m-%d %H:%M:%S")
    submission_time = datetime.strptime(submission_time, "%Y-%m-%d %H:%M:%S")

    # Calculate the time difference
    time_difference = task_deadline - submission_time

    # Check if the task was submitted before or on the deadline
    if time_difference.total_seconds() >= 0:
        # On-time submission
        reward = on_time_bonus

        # Check if the task was submitted before the deadline
        if time_difference.total_seconds() > 0:
            # Early submission bonus
            reward += early_submission_bonus
    else:
        # Late submission, no bonus
        reward = 0

    return reward

