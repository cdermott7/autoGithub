import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from src.cli.cli import cli

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('src.cli.cli.ProjectGenerator')
    @patch('src.cli.cli.GitHubAPI')
    @patch('src.cli.cli.RepoManager')
    def test_generate_command(self, mock_repo_manager, mock_github_api, mock_project_generator):
        mock_project_generator.return_value.generate_project.return_value = {
            'name': 'test_project',
            'language': 'python',
            'theme': 'web',
            'description': 'Test description',
            'files': []
        }
        mock_repo_manager.return_value.create_repo.return_value = 'test_repo'

        result = self.runner.invoke(cli, ['generate', '--language', 'python', '--theme', 'web'])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Generated project: test_project', result.output)

    @patch('src.cli.cli.load_config')
    @patch('src.cli.cli.save_config')
    def test_configure_command(self, mock_save_config, mock_load_config):
        mock_load_config.return_value = {'github': {}}

        result = self.runner.invoke(cli, ['configure', '--github-username', 'testuser'])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Configuration updated successfully', result.output)
        mock_save_config.assert_called_once()

if __name__ == '__main__':
    unittest.main()
