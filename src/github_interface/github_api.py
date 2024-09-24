from github import Github
from github.GithubException import GithubException
from src.utils.logger import github_interface_logger
import hashlib
import secrets


class GitHubAPI:
    def __init__(self, token, config):
        self.github = Github(token)
        self.config = config
        #self.user = self.github.get_user(username)
        #github_interface_logger.info(f"Initialized GitHub API for user: {username}")
        github_interface_logger.info(f"Initialized GitHub API for user")


    def create_repo(self, name, private=False):
        try:
            repo = self.user.create_repo(name, private=private)
            github_interface_logger.info(f"Created repository: {name}")
            return repo
        except GithubException as e:
            github_interface_logger.error(f"Error creating repository {name}: {e}")
            return None

    def get_repo(self, name):
        try:
            repo = self.user.get_repo(name)
            github_interface_logger.info(f"Retrieved repository: {name}")
            return repo
        except GithubException as e:
            github_interface_logger.error(f"Error getting repository {name}: {e}")
            return None

    def create_file(self, repo, path, content, commit_message, branch='master'):
        try:
            repo.create_file(path, commit_message, content, branch=branch)
            github_interface_logger.info(f"Created file: {path} in repository: {repo.name}")
        except GithubException as e:
            github_interface_logger.error(f"Error creating file {path} in repository {repo.name}: {e}")

    def update_file(self, repo, path, content, commit_message, sha, branch='master'):
        try:
            repo.update_file(path, commit_message, content, sha, branch=branch)
            github_interface_logger.info(f"Updated file: {path} in repository: {repo.name}")
        except GithubException as e:
            github_interface_logger.error(f"Error updating file {path} in repository {repo.name}: {e}")

    def create_branch(self, repo, branch_name, source_branch='master'):
        try:
            source = repo.get_branch(source_branch)
            repo.create_git_ref(f"refs/heads/{branch_name}", source.commit.sha)
            github_interface_logger.info(f"Created branch: {branch_name} in repository: {repo.name}")
        except GithubException as e:
            github_interface_logger.error(f"Error creating branch {branch_name} in repository {repo.name}: {e}")

    def create_pull_request(self, repo, title, body, head, base='master'):
        try:
            pr = repo.create_pull(title=title, body=body, head=head, base=base)
            github_interface_logger.info(f"Created pull request: {title} in repository: {repo.name}")
            return pr
        except GithubException as e:
            github_interface_logger.error(f"Error creating pull request in repository {repo.name}: {e}")
            return None
            