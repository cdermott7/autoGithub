from flask import Blueprint, jsonify, request
from src.project_generator.generator import ProjectGenerator
from src.github_interface.github_api import GitHubAPI
from src.github_interface.repo_manager import RepoManager
from src.utils.error_handler import handle_error, ConfigurationError
from src.project_tracker.tracker import ProjectTracker
from src.utils.security import require_api_key, sanitize_input
import yaml
import os

api = Blueprint('api', __name__)
project_tracker = ProjectTracker()

def load_config():
    with open('config/config.yaml', 'r') as config_file:
        return yaml.safe_load(config_file)

@api.route('/generate', methods=['POST'])
@require_api_key
def generate_project():
    try:
        config = load_config()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        github_token = os.getenv('GITHUB_TOKEN')

        if not openai_api_key or not github_token:
            raise ConfigurationError("OpenAI API key or GitHub token not found")

        project_generator = ProjectGenerator(config['project_generator'], openai_api_key)
        github_api = GitHubAPI(github_token, config['github']['username'])
        repo_manager = RepoManager(github_api, config['github']['repo_prefix'])

        data = request.json
        language = sanitize_input(data.get('language', ''))
        theme = sanitize_input(data.get('theme', ''))
        custom_prompt = sanitize_input(data.get('custom_prompt', ''))

        if language:
            project_generator.languages = [language]
        if theme:
            project_generator.themes = [theme]

        project = project_generator.generate_project(language=language, theme=theme, custom_prompt=custom_prompt)
        repo_name = repo_manager.create_repo(project['name'])
        
        if repo_name:
            repo_manager.push_project(repo_name, project['files'])
            project_tracker.add_project(project['name'], project['language'], project['theme'])
            return jsonify({
                "status": "success",
                "project": {
                    "name": project['name'],
                    "language": project['language'],
                    "theme": project['theme'],
                    "description": project['description'],
                    "repository": f"https://github.com/{config['github']['username']}/{repo_name}"
                }
            }), 201
        else:
            return jsonify({"status": "error", "message": "Failed to create GitHub repository"}), 500

    except Exception as e:
        error_message = handle_error(e, context="API project generation")
        return jsonify({"status": "error", "message": error_message}), 500

@api.route('/projects', methods=['GET'])
@require_api_key
def get_projects():
    try:
        projects = project_tracker.history
        return jsonify({
            "status": "success",
            "projects": projects
        }), 200
    except Exception as e:
        error_message = handle_error(e, context="API get projects")
        return jsonify({"status": "error", "message": error_message}), 500
