import unittest
from unittest.mock import patch, MagicMock
from src.github_interface.github_api import GitHubAPI
from src.github_interface.repo_manager import RepoManager

class TestGitHubAPI(unittest.TestCase):
    def setUp(self):
        self.github_api = GitHubAPI('fake_token', 'fake_username')

    @patch('src.github_interface.github_api.Github')
    def test_create_repo(self, mock_github):
        mock_user = MagicMock()
        mock_user.create_repo.return_value = MagicMock(name='test_repo')
        mock_github.return_value.get_user.return_value = mock_user

        repo = self.github_api.create_repo('test_repo')
        self.assertIsNotNone(repo)
        mock_user.create_repo.assert_called_once_with('test_repo', private=False)

    @patch('src.github_interface.github_api.Github')
    def test_create_branch(self, mock_github):
        mock_repo = MagicMock()
        mock_branch = MagicMock()
        mock_branch.commit.sha = 'test_sha'
        mock_repo.get_branch.return_value = mock_branch
        
        self.github_api.create_branch(mock_repo, 'new_branch')
        
        mock_repo.get_branch.assert_called_once_with('master')
        mock_repo.create_git_ref.assert_called_once_with('refs/heads/new_branch', 'test_sha')

class TestRepoManager(unittest.TestCase):
    def setUp(self):
        self.mock_github_api = MagicMock()
        self.repo_manager = RepoManager(self.mock_github_api, 'autogithub_')

    def test_create_repo(self):
        self.mock_github_api.create_repo.return_value = MagicMock(name='autogithub_test_project')
        repo_name = self.repo_manager.create_repo('test_project')
        self.assertEqual(repo_name, 'autogithub_test_project')
        self.mock_github_api.create_repo.assert_called_once_with('autogithub_test_project')

    def test_push_project(self):
        mock_repo = MagicMock()
        self.mock_github_api.get_repo.return_value = mock_repo
        files = [
            {'name': 'file1.py', 'content': 'content1'},
            {'name': 'file2.py', 'content': 'content2'}
        ]
        self.repo_manager.push_project('autogithub_test_project', files)
        self.mock_github_api.get_repo.assert_called_once_with('autogithub_test_project')
        self.mock_github_api.create_branch.assert_called_once()
        self.assertEqual(self.mock_github_api.create_file.call_count, 2)
        self.mock_github_api.create_pull_request.assert_called_once()

    def test_update_project(self):
        mock_repo = MagicMock()
        self.mock_github_api.get_repo.return_value = mock_repo
        files = [
            {'name': 'file1.py', 'content': 'updated_content1'},
            {'name': 'file2.py', 'content': 'updated_content2'}
        ]
        mock_repo.get_contents.side_effect = [MagicMock(sha='sha1'), MagicMock(sha='sha2')]
        
        self.repo_manager.update_project('autogithub_test_project', files)
        
        self.mock_github_api.get_repo.assert_called_once_with('autogithub_test_project')
        self.mock_github_api.create_branch.assert_called_once()
        self.assertEqual(self.mock_github_api.update_file.call_count, 2)
        self.mock_github_api.create_pull_request.assert_called_once()
