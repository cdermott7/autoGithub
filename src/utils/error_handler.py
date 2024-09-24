import traceback
from src.utils.logger import main_logger

class AutoGitHubError(Exception):
    """Base class for AutoGitHub exceptions"""
    pass

class ConfigurationError(AutoGitHubError):
    """Raised when there's an issue with the configuration"""
    pass

class ProjectGenerationError(AutoGitHubError):
    """Raised when there's an error generating a project"""
    pass

class GitHubAPIError(AutoGitHubError):
    """Raised when there's an error interacting with the GitHub API"""
    pass

def handle_error(error, context=""):
    """
    Central error handling function.
    Logs the error and returns a user-friendly error message.
    """
    error_type = type(error).__name__
    error_message = str(error)
    stack_trace = traceback.format_exc()

    main_logger.error(f"Error in {context}: {error_type} - {error_message}")
    main_logger.debug(f"Stack trace:\n{stack_trace}")

    if isinstance(error, ConfigurationError):
        return "There was an issue with the configuration. Please check your settings and try again."
    elif isinstance(error, ProjectGenerationError):
        return "An error occurred while generating the project. Please try again or check the logs for more information."
    elif isinstance(error, GitHubAPIError):
        return "There was an error communicating with GitHub. Please check your token and network connection."
    else:
        return "An unexpected error occurred. Please check the logs for more information."
