from .python_templates import python_templates
from .javascript_templates import javascript_templates
from .rust_templates import rust_templates
from .java_templates import java_templates
from .go_templates import go_templates

class TemplateManager:
    def __init__(self):
        self.templates = {
            'python': python_templates,
            'javascript': javascript_templates,
            'rust': rust_templates,
            'java': java_templates,
            'go': go_templates
        }

    def get_template(self, language, theme):
        language_templates = self.templates.get(language, {})
        return language_templates.get(theme, self.generic_template)

    def generic_template(self, project_name, project_description, custom_prompt=None):
        return [
            {
                'name': 'main.txt',
                'content': f"Project: {project_name}\nDescription: {project_description}\n\nThis is a generic template."
            }
        ]
