import click
import yaml
from src.project_generator.generator import ProjectGenerator
from src.github_interface.github_api import GitHubAPI
from src.github_interface.repo_manager import RepoManager
from src.utils.error_handler import handle_error, ConfigurationError
from src.utils.security import generate_api_key, hash_api_key
from dotenv import load_dotenv
import openai
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

@click.group()
def cli():
    """AutoGitHub CLI for manual project generation and configuration."""
    pass

@cli.command()
@click.option('--language', type=click.Choice(['python', 'javascript', 'rust', 'java', 'go']), help='Programming language for the project')
@click.option('--theme', type=click.Choice(['web_development', 'data_science', 'game_development', 'machine_learning', 'iot', 'blockchain', 'cybersecurity']), help='Theme of the project')
@click.option('--custom-prompt', help='Custom prompt for project generation')
def generate(language, theme, custom_prompt):
    """Generate a new project manually."""
    try:
        load_dotenv()
        config = load_config()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        github_token = os.getenv('GITHUB_TOKEN')

        if not openai_api_key or not github_token:
            raise ConfigurationError("OpenAI API key or GitHub token not found in .env file")

        project_generator = ProjectGenerator(config['project_generator'], openai_api_key)
        github_api = GitHubAPI(github_token, config['github']['username'])
        repo_manager = RepoManager(github_api, config['github']['repo_prefix'])

        if language:
            project_generator.languages = [language]
        if theme:
            project_generator.themes = [theme]

        project = project_generator.generate_project(language=language, theme=theme, custom_prompt=custom_prompt)
        click.echo(f"Generated project: {project['name']} ({project['language']}, theme: {project['theme']})")
        click.echo(f"Description: {project['description']}")

        if click.confirm('Do you want to push this project to GitHub?'):
            repo_name = repo_manager.create_repo(project['name'])
            if repo_name:
                repo_manager.push_project(repo_name, project['files'])
                click.echo(f"Successfully pushed project to GitHub: {repo_name}")
            else:
                click.echo("Failed to create GitHub repository")
        else:
            click.echo("Project not pushed to GitHub")

    except Exception as e:
        error_message = handle_error(e, context="CLI project generation")
        click.echo(f"Error: {error_message}")

@cli.command()
@click.option('--github-token', help='GitHub personal access token')
@click.option('--openai-api-key', help='OpenAI API key')
@click.option('--github-username', help='GitHub username')
@click.option('--repo-prefix', help='Prefix for generated repositories')
def configure(github_token, openai_api_key, github_username, repo_prefix):
    """Update configuration settings."""
    try:
        config = load_config()

        if github_token:
            os.environ['GITHUB_TOKEN'] = github_token
        if openai_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
        if github_username:
            config['github']['username'] = github_username
        if repo_prefix:
            config['github']['repo_prefix'] = repo_prefix

        save_config(config)
        click.echo("Configuration updated successfully")
    except Exception as e:
        error_message = handle_error(e, context="CLI configuration")
        click.echo(f"Error: {error_message}")

@cli.command()
def generate_api_key():
    """Generate a new API key for AutoGitHub."""
    try:
        new_api_key = ProjectGenerator.generate_api_key()  # Assuming this is the correct function call
        hashed_key = ProjectGenerator.hash_api_key(new_api_key)  # Assuming this is the correct function call
        
        # Update .env file
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as file:
                lines = file.readlines()
            with open(env_path, 'w') as file:
                api_key_updated = False
                for line in lines:
                    if line.startswith('API_KEY='):
                        file.write(f'API_KEY={new_api_key}\n')
                        api_key_updated = True
                    else:
                        file.write(line)
                if not api_key_updated:
                    file.write(f'API_KEY={new_api_key}\n')
        else:
            with open(env_path, 'w') as file:
                file.write(f'API_KEY={new_api_key}\n')
        
        click.echo(f"New API key generated: {new_api_key}")
        click.echo("This key has been added to your .env file.")
        click.echo("Please keep this key secure and do not share it.")
        click.echo(f"Hashed API key (for reference): {hashed_key}")
    except Exception as e:
        error_message = handle_error(e, context="API key generation")
        click.echo(f"Error: {error_message}")


def load_config():
    try:
        with open('config/config.yaml', 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        raise ConfigurationError("Config file not found. Please ensure config.yaml exists in the config directory.")
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Error parsing config file: {e}")

def save_config(config):
    with open('config/config.yaml', 'w') as config_file:
        yaml.dump(config, config_file)

if __name__ == '__main__':
    cli()
