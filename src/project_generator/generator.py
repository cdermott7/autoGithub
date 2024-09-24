import random
import openai
from .utils import sanitize_filename
from .templates.template_manager import TemplateManager
from src.utils.logger import project_generator_logger
import hashlib
import secrets

class ProjectGenerator:
    def __init__(self, config, openai_api_key):
        self.config = config
        self.languages = config['languages']
        self.max_files = config['max_files_per_project']
        self.max_lines = config['max_lines_per_file']
        self.themes = config.get('themes', [])
        self.template_manager = TemplateManager()
        self.custom_prompts = config.get('custom_prompts', {})
        openai.api_key = openai_api_key

    def generate_project(self, language=None, theme=None, custom_prompt=None):
        try:
            language = language or random.choice(self.languages)
            theme = theme or (random.choice(self.themes) if self.themes else None)
            
            project_name = self._generate_project_name(theme, custom_prompt)
            project_description = self._generate_project_description(project_name, language, theme, custom_prompt)
            files = self._generate_files(project_name, project_description, language, theme, custom_prompt)
            
            project_generator_logger.info(f"Generated project: {project_name} ({language}, theme: {theme})")
            return {
                'name': project_name,
                'description': project_description,
                'language': language,
                'theme': theme,
                'files': files
            }
        except Exception as e:
            project_generator_logger.error(f"Error generating project: {str(e)}")
            raise

    def _generate_project_name(self, theme=None, custom_prompt=None):
        try:
            if custom_prompt and 'project_name' in self.custom_prompts:
                prompt = self.custom_prompts['project_name'].format(theme=theme, custom_prompt=custom_prompt)
            else:
                prompt = f"Generate a unique and creative name for a software project{' related to ' + theme if theme else ''}{' with the following characteristics: ' + custom_prompt if custom_prompt else ''}."
            
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=20,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return sanitize_filename(response.choices[0].text.strip())
        except openai.error.OpenAIError as e:
            project_generator_logger.error(f"OpenAI API error while generating project name: {str(e)}")
            raise
        except Exception as e:
            project_generator_logger.error(f"Unexpected error while generating project name: {str(e)}")
            raise

    def _generate_project_description(self, project_name, language, theme=None, custom_prompt=None):
        try:
            if custom_prompt and 'project_description' in self.custom_prompts:
                prompt = self.custom_prompts['project_description'].format(project_name=project_name, language=language, theme=theme, custom_prompt=custom_prompt)
            else:
                prompt = f"Write a brief description for a {language} project named '{project_name}'{' related to ' + theme if theme else ''}{' with the following characteristics: ' + custom_prompt if custom_prompt else ''}."
            
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except openai.error.OpenAIError as e:
            project_generator_logger.error(f"OpenAI API error while generating project description: {str(e)}")
            raise
        except Exception as e:
            project_generator_logger.error(f"Unexpected error while generating project description: {str(e)}")
            raise

    def _generate_files(self, project_name, project_description, language, theme, custom_prompt=None):
        template = self.template_manager.get_template(language, theme)
        files = template(project_name, project_description, custom_prompt)
        
        while len(files) < self.max_files:
            try:
                filename = self._generate_filename(language, len(files))
                content = self._generate_file_content(filename, project_name, project_description, language, theme, custom_prompt)
                files.append({'name': filename, 'content': content})
                project_generator_logger.info(f"Generated additional file: {filename}")
            except Exception as e:
                project_generator_logger.error(f"Error generating additional file: {str(e)}")
                break
        
        return files

    def _generate_filename(self, language, index):
        extension = {
            'python': 'py',
            'javascript': 'js',
            'rust': 'rs',
            'java': 'java',
            'go': 'go'
        }.get(language, language)
        return f"file_{index}.{extension}"

    def _generate_file_content(self, filename, project_name, project_description, language, theme, custom_prompt=None):
        try:
            if custom_prompt and 'file_content' in self.custom_prompts:
                prompt = self.custom_prompts['file_content'].format(filename=filename, project_name=project_name, project_description=project_description, language=language, theme=theme, custom_prompt=custom_prompt)
            else:
                prompt = f"Generate {language} code for a file named '{filename}' in a {theme} project described as: {project_description}{' with the following characteristics: ' + custom_prompt if custom_prompt else ''}"
            
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=self.max_lines * 5,
                n=1,
                stop=None,
                temperature=0.7,
            )
            content = response.choices[0].text.strip()
            
            return f"""
# {project_name}
# {project_description}
# File: {filename}
# Language: {language}
# Theme: {theme}
#
# This file was generated by AutoGitHub

{content}
"""
        except openai.error.OpenAIError as e:
            project_generator_logger.error(f"OpenAI API error while generating file content: {str(e)}")
            raise
        except Exception as e:
            project_generator_logger.error(f"Unexpected error while generating file content: {str(e)}")
            raise

    def generate_api_key():
        """Generate a new API key."""
        return secrets.token_urlsafe(32)

    def hash_api_key(api_key):
        """Hash the API key for secure storage."""
        return hashlib.sha256(api_key.encode()).hexdigest()
