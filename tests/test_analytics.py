import unittest
from unittest.mock import MagicMock
from src.analytics.analyzer import ProjectAnalyzer
from datetime import datetime, timedelta

class TestProjectAnalyzer(unittest.TestCase):
    def setUp(self):
        self.mock_project_tracker = MagicMock()
        self.analyzer = ProjectAnalyzer(self.mock_project_tracker)

    def test_get_language_distribution(self):
        self.mock_project_tracker.history = [
            {'language': 'python'},
            {'language': 'javascript'},
            {'language': 'python'}
        ]
        distribution = self.analyzer.get_language_distribution()
        self.assertEqual(distribution, {'python': 2, 'javascript': 1})

    def test_get_theme_distribution(self):
        self.mock_project_tracker.history = [
            {'theme': 'web'},
            {'theme': 'data_science'},
            {'theme': 'web'}
        ]
        distribution = self.analyzer.get_theme_distribution()
        self.assertEqual(distribution, {'web': 2, 'data_science': 1})

    def test_get_projects_per_day(self):
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        self.mock_project_tracker.history = [
            {'timestamp': today.isoformat()},
            {'timestamp': today.isoformat()},
            {'timestamp': yesterday.isoformat()}
        ]
        projects_per_day = self.analyzer.get_projects_per_day(days=2)
        self.assertEqual(projects_per_day[today], 2)
        self.assertEqual(projects_per_day[yesterday], 1)
