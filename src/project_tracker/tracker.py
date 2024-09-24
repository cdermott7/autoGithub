import json
import os
from datetime import datetime, timedelta

class ProjectTracker:
    def __init__(self, file_path='project_history.json', days_to_track=30):
        self.file_path = file_path
        self.days_to_track = days_to_track
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.history, f)

    def add_project(self, project_name, language, theme):
        current_time = datetime.now().isoformat()
        self.history.append({
            'name': project_name,
            'language': language,
            'theme': theme,
            'timestamp': current_time
        })
        self.clean_old_entries()
        self.save_history()

    def clean_old_entries(self):
        cutoff_date = datetime.now() - timedelta(days=self.days_to_track)
        self.history = [
            entry for entry in self.history
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]

    def is_unique(self, language, theme):
        for entry in self.history:
            if entry['language'] == language and entry['theme'] == theme:
                return False
        return True
