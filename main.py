import os
import yaml
from dotenv import load_dotenv
from src.project_generator.generator import ProjectGenerator
from src.github_interface.github_api import GitHubAPI
from src.github_interface.repo_manager import RepoManager
from src.scheduler.scheduler import Scheduler
from src.utils.logger import main_logger
from src.web_interface.app import app as web_app
from src.api.api import api as api_blueprint
from src.utils.error_handler import handle_error, ConfigurationError
from src.utils.notifier import Notifier
from src.analytics.analyzer import ProjectAnalyzer
from src.project_tracker.tracker import ProjectTracker
from src.utils.security import API_KEY, generate_api_key
import threading

def load_config():
    try:
        with open('config/config.yaml', 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        raise ConfigurationError("Config file not found. Please ensure config.yaml exists in the config directory.")
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Error parsing config file: {e}")

def run_web_interface():
    web_app.register_blueprint(api_blueprint, url_prefix='/api')
    web_app.run(host='0.0.0.0', port=5002, ssl_context='adhoc')

def main():
    notifier = None
    try:
        load_dotenv()
        config = load_config()

        github_token = os.getenv('GITHUB_TOKEN')
        print(github_token)
        openai_api_key = os.getenv('OPENAI_API_KEY')

        if not github_token or not openai_api_key:
            raise ConfigurationError("GitHub token or OpenAI API key not found in .env file")

        notifier = Notifier(config['notifier'])

        if 'API_KEY' not in os.environ:
            new_api_key = generate_api_key()
            main_logger.warning(f"API_KEY not found in .env file. Generated new API key: {new_api_key}")
            main_logger.warning("Please add this API key to your .env file for future use.")
            os.environ['API_KEY'] = new_api_key

        github_api = GitHubAPI(github_token, config['github'])
        repo_manager = RepoManager(github_api, config['github']['repo_prefix'])
        project_generator = ProjectGenerator(config['project_generator'], openai_api_key)
        project_tracker = ProjectTracker()
        project_analyzer = ProjectAnalyzer(project_tracker)

        def create_and_push_project():
            try:
                project = project_generator.generate_project()
                repo_name = repo_manager.create_repo(project['name'])
                if repo_name:
                    repo_manager.push_project(repo_name, project['files'])
                    project_tracker.add_project(project['name'], project['language'], project['theme'])
                    main_logger.info(f"Successfully created and pushed project: {project['name']} (Language: {project['language']}, Theme: {project['theme']})")
                    notifier.send_notification(
                        "New AutoGitHub Project",
                        f"A new project '{project['name']}' has been generated and pushed to GitHub.\n"
                        f"Language: {project['language']}\n"
                        f"Theme: {project['theme']}\n"
                        f"Description: {project['description']}\n"
                        f"Repository: https://github.com/{config['github']['username']}/{repo_name}"
                    )
                else:
                    raise Exception(f"Failed to create repository for project: {project['name']}")
            except Exception as e:
                error_message = handle_error(e, context="create_and_push_project")
                main_logger.error(error_message)
                notifier.send_notification("AutoGitHub Error", f"An error occurred: {error_message}")

        scheduler = Scheduler(config['scheduler']['creation_time'], config['scheduler']['timezone'])
        scheduler.schedule_daily(create_and_push_project)

        # Start the web interface in a separate thread
        web_thread = threading.Thread(target=run_web_interface)
        web_thread.start()

        main_logger.info("AutoGitHub is running. Press Ctrl+C to exit.")
        scheduler.run()
    except Exception as e:
        error_message = handle_error(e, context="main")
        main_logger.error(error_message)
        if notifier:
            try:
                notifier.send_notification("AutoGitHub Critical Error", f"A critical error occurred: {error_message}")
            except Exception as notifier_error:
                main_logger.error(f"Failed to send notification: {str(notifier_error)}")
        else:
            main_logger.error("Notifier not initialized. Unable to send notification.")

if __name__ == "__main__":
    main()