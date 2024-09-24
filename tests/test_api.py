import unittest
from unittest.mock import patch, MagicMock
from src.api.api import api
from flask import Flask

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(api)
        self.client = self.app.test_client()

    @patch('src.api.api.ProjectGenerator')
    @patch('src.api.api.GitHubAPI')
    @patch('src.api.api.RepoManager')
    @patch('src.api.api.ProjectTracker')
    def test_generate_project(self, mock_tracker, mock_repo_manager, mock_github_api, mock_project_generator):
        mock_project_generator.return_value.generate_project.return_value = {
            'name': 'test_project',
            'language': 'python',
            'theme': 'web',
            'description': 'Test description',
            'files': []
        }
        mock_repo_manager.return_value.create_repo.return_value = 'test_repo'

        response = self.client.post('/generate', json={
            'language': 'python',
            'theme': 'web',
            'custom_prompt': 'Test prompt'
        }, headers={'X-API-Key': 'test_key'})

        self.assertEqual(response.status_code, 201)
        self.assertIn('test_project', response.get_json()['project']['name'])

    @patch('src.api.api.ProjectTracker')
    def test_get_projects(self, mock_tracker):
        mock_tracker.return_value.history = [
            {'name': 'project1', 'language': 'python', 'theme': 'web'},
            {'name': 'project2', 'language': 'javascript', 'theme': 'data_science'}
        ]

        response = self.client.get('/projects', headers={'X-API-Key': 'test_key'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['projects']), 2)
