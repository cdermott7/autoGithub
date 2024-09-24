import unittest
from unittest.mock import patch, MagicMock
from src.project_generator.generator import ProjectGenerator

class TestProjectGenerator(unittest.TestCase):
    def setUp(self):
        self.config = {
            'languages': ['python', 'javascript', 'rust', 'java', 'go'],
            'max_files_per_project': 5,
            'max_lines_per_file': 100,
            'themes': ['web_development', 'data_science', 'game_development', 'machine_learning', 'iot', 'blockchain', 'cybersecurity'],
            'custom_prompts': {
                'project_name': 'Generate a name for a {theme} project with {custom_prompt}',
                'project_description': 'Describe a {language} project named {project_name} for {theme} with {custom_prompt}',
                'file_content': 'Write {language} code for {filename} in a {theme} project described as: {project_description} with {custom_prompt}'
            }
        }
        self.generator = ProjectGenerator(self.config, 'fake_api_key')

    @patch('src.project_generator.generator.openai')
    def test_generate_project(self, mock_openai):
        mock_openai.Completion.create.return_value.choices = [MagicMock(text="Test Project")]
        project = self.generator.generate_project()
        
        self.assertIn('name', project)
        self.assertIn('description', project)
        self.assertIn('language', project)
        self.assertIn('theme', project)
        self.assertIn('files', project)
        self.assertIsInstance(project['files'], list)
        self.assertLessEqual(len(project['files']), self.config['max_files_per_project'])
        self.assertIn(project['language'], self.config['languages'])
        self.assertIn(project['theme'], self.config['themes'])

    @patch('src.project_generator.generator.openai')
    def test_generate_project_with_custom_options(self, mock_openai):
        mock_openai.Completion.create.return_value.choices = [MagicMock(text="Custom Test Project")]
        project = self.generator.generate_project(language='python', theme='web_development', custom_prompt='using Flask and SQLAlchemy')
        
        self.assertEqual(project['language'], 'python')
        self.assertEqual(project['theme'], 'web_development')
        self.assertTrue(any('Flask' in file['content'] for file in project['files']))
        self.assertTrue(any('SQLAlchemy' in file['content'] for file in project['files']))

    @patch('src.project_generator.generator.openai')
    def test_error_handling(self, mock_openai):
        mock_openai.Completion.create.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            self.generator.generate_project()
