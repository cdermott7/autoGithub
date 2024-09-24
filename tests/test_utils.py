import unittest
from src.utils.error_handler import handle_error, ConfigurationError, ProjectGenerationError, GitHubAPIError
from src.utils.security import generate_api_key, hash_api_key, sanitize_input

class TestErrorHandler(unittest.TestCase):
    def test_handle_configuration_error(self):
        error = ConfigurationError("Test configuration error")
        message = handle_error(error, "test")
        self.assertIn("configuration", message)

    def test_handle_project_generation_error(self):
        error = ProjectGenerationError("Test project generation error")
        message = handle_error(error, "test")
        self.assertIn("generating the project", message)

    def test_handle_github_api_error(self):
        error = GitHubAPIError("Test GitHub API error")
        message = handle_error(error, "test")
        self.assertIn("GitHub", message)

    def test_handle_unexpected_error(self):
        error = ValueError("Unexpected error")
        message = handle_error(error, "test")
        self.assertIn("unexpected error", message)

class TestSecurity(unittest.TestCase):
    def test_generate_api_key(self):
        key = generate_api_key()
        self.assertEqual(len(key), 43)  # Base64 encoded 32-byte key

    def test_hash_api_key(self):
        key = "test_key"
        hashed_key = hash_api_key(key)
        self.assertEqual(len(hashed_key), 64)  # SHA-256 hash

    def test_sanitize_input(self):
        input_string = "Test <script>alert('XSS')</script>"
        sanitized = sanitize_input(input_string)
        self.assertEqual(sanitized, "Test &lt;script&gt;alert('XSS')&lt;/script&gt;")

