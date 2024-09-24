import unittest
from unittest.mock import patch, mock_open
from src.project_tracker.tracker import ProjectTracker
import json
from datetime import datetime, timedelta

class TestProjectTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ProjectTracker(file_path='test_history.json', days_to_track=30)

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_history(self, mock_file):
        history = self.tracker.load_history()
        self.assertEqual(history, [])
        mock_file.assert_called_once_with('test_history.json', 'r')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_history(self, mock_json_dump, mock_file):
        self.tracker.history = [{'name': 'test_project', 'language': 'python', 'theme': 'web', 'timestamp': '2023-01-01T00:00:00'}]
        self.tracker.save_history()
        mock_file.assert_called_once_with('test_history.json', 'w')
        mock_json_dump.assert_called_once_with(self.tracker.history, mock_file())

    @patch('src.project_tracker.tracker.datetime')
    def test_add_project(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1)
        self.tracker.add_project('test_project', 'python', 'web')
        self.assertEqual(len(self.tracker.history), 1)
        self.assertEqual(self.tracker.history[0]['name'], 'test_project')
        self.assertEqual(self.tracker.history[0]['language'], 'python')
        self.assertEqual(self.tracker.history[0]['theme'], 'web')
        self.assertEqual(self.tracker.history[0]['timestamp'], '2023-01-01T00:00:00')

    def test_clean_old_entries(self):
        now = datetime.now()
        self.tracker.history = [
            {'name': 'old_project', 'language': 'python', 'theme': 'web', 'timestamp': (now - timedelta(days=31)).isoformat()},
            {'name': 'new_project', 'language': 'javascript', 'theme': 'web', 'timestamp': now.isoformat()}
        ]
        self.tracker.clean_old_entries()
        self.assertEqual(len(self.tracker.history), 1)
        self.assertEqual(self.tracker.history[0]['name'], 'new_project')

    def test_is_unique(self):
        self.tracker.history = [
            {'name': 'project1', 'language': 'python', 'theme': 'web', 'timestamp': '2023-01-01T00:00:00'},
            {'name': 'project2', 'language': 'javascript', 'theme': 'data_science', 'timestamp': '2023-01-02T00:00:00'}
        ]
        self.assertTrue(self.tracker.is_unique('rust', 'blockchain'))
        self.assertFalse(self.tracker.is_unique('python', 'web'))
