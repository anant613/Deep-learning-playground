import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Callable

class TaskScheduler:
    def __init__(self, voice_speaker=None):
        self.voice_speaker = voice_speaker
        self.scheduled_tasks: Dict[str, schedule.Job] = {}
        self.running = False
        self.scheduler_thread = None
    
    def start(self):
        """Start the scheduler in a background thread"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            print("📅 Task scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=1)
        print("📅 Task scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def add_reminder(self, task_id: str, message: str, when: str):
        """Add a reminder task"""
        try:
            # Parse time format (e.g., "10:30", "15:45")
            if ":" in when:
                job = schedule.every().day.at(when).do(self._reminder_task, message)
                self.scheduled_tasks[task_id] = job
                return f"Reminder set for {when}: {message}"
            else:
                return "Please provide time in HH:MM format (e.g., 10:30)"
                
        except Exception as e:
            return f"Error setting reminder: {str(e)}"
    
    def add_daily_task(self, task_id: str, message: str, time_str: str):
        """Add a daily recurring task"""
        try:
            job = schedule.every().day.at(time_str).do(self._reminder_task, message)
            self.scheduled_tasks[task_id] = job
            return f"Daily task set for {time_str}: {message}"
            
        except Exception as e:
            return f"Error setting daily task: {str(e)}"
    
    def remove_task(self, task_id: str):
        """Remove a scheduled task"""
        if task_id in self.scheduled_tasks:
            schedule.cancel_job(self.scheduled_tasks[task_id])
            del self.scheduled_tasks[task_id]
            return f"Task {task_id} removed"
        else:
            return f"Task {task_id} not found"
    
    def list_tasks(self):
        """List all scheduled tasks"""
        if not self.scheduled_tasks:
            return "No scheduled tasks"
        
        task_list = []
        for task_id, job in self.scheduled_tasks.items():
            next_run = job.next_run.strftime("%Y-%m-%d %H:%M:%S") if job.next_run else "Not scheduled"
            task_list.append(f"{task_id}: Next run at {next_run}")
        
        return "Scheduled tasks: " + ", ".join(task_list)
    
    def _reminder_task(self, message: str):
        """Execute a reminder task"""
        print(f"⏰ Reminder: {message}")
        if self.voice_speaker:
            self.voice_speaker.speak(f"Reminder: {message}")
    
    def parse_natural_time(self, time_text: str):
        """Parse natural language time expressions"""
        time_text = time_text.lower()
        now = datetime.now()
        
        # Handle "in X minutes/hours"
        if "in" in time_text:
            if "minute" in time_text:
                minutes = int(''.join(filter(str.isdigit, time_text)))
                target_time = now + timedelta(minutes=minutes)
                return target_time.strftime("%H:%M")
            elif "hour" in time_text:
                hours = int(''.join(filter(str.isdigit, time_text)))
                target_time = now + timedelta(hours=hours)
                return target_time.strftime("%H:%M")
        
        # Handle "at X pm/am"
        if "at" in time_text:
            # Extract time part
            time_part = time_text.split("at")[1].strip()
            # Simple parsing - could be enhanced
            return time_part
        
        return None