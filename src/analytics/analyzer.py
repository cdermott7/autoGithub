from collections import Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io

class ProjectAnalyzer:
    def __init__(self, project_tracker):
        self.project_tracker = project_tracker

    def get_language_distribution(self):
        languages = [project['language'] for project in self.project_tracker.history]
        return dict(Counter(languages))

    def get_theme_distribution(self):
        themes = [project['theme'] for project in self.project_tracker.history]
        return dict(Counter(themes))

    def get_projects_per_day(self, days=30):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        daily_counts = Counter()
        for project in self.project_tracker.history:
            project_date = datetime.fromisoformat(project['timestamp']).date()
            if start_date.date() <= project_date <= end_date.date():
                daily_counts[project_date] += 1
        
        return dict(daily_counts)

    def generate_language_chart(self):
        language_dist = self.get_language_distribution()
        plt.figure(figsize=(10, 6))
        plt.bar(language_dist.keys(), language_dist.values())
        plt.title('Project Language Distribution')
        plt.xlabel('Language')
        plt.ylabel('Number of Projects')
        plt.xticks(rotation=45)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        return buffer

    def generate_theme_chart(self):
        theme_dist = self.get_theme_distribution()
        plt.figure(figsize=(10, 6))
        plt.bar(theme_dist.keys(), theme_dist.values())
        plt.title('Project Theme Distribution')
        plt.xlabel('Theme')
        plt.ylabel('Number of Projects')
        plt.xticks(rotation=45)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        return buffer

    def generate_projects_per_day_chart(self, days=30):
        daily_counts = self.get_projects_per_day(days)
        plt.figure(figsize=(12, 6))
        plt.plot(list(daily_counts.keys()), list(daily_counts.values()))
        plt.title(f'Projects Generated per Day (Last {days} Days)')
        plt.xlabel('Date')
        plt.ylabel('Number of Projects')
        plt.xticks(rotation=45)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        return buffer
