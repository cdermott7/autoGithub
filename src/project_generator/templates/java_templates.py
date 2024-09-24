def java_console_template(project_name, project_description, custom_prompt=None):
    class_name = ''.join(word.capitalize() for word in project_name.split())
    return [
        {
            'name': f'{class_name}.java',
            'content': f'''
/**
 * {project_name}
 * {project_description}
 */
public class {class_name} {{
    public static void main(String[] args) {{
        System.out.println("Welcome to {project_name}!");
        System.out.println("{project_description}");
    }}
}}
'''
        }
    ]

# Add more Java templates for different themes here...

java_templates = {
    'console': java_console_template,
    # Add more theme-specific templates here...
}
