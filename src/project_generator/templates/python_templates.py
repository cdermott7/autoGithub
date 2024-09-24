def python_web_template(project_name, project_description, custom_prompt=None):
    return [
        {
            'name': 'app.py',
            'content': f'''
# {project_name}
# {project_description}

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', project_name="{project_name}")

if __name__ == '__main__':
    app.run(debug=True)
'''
        },
        {
            'name': 'templates/index.html',
            'content': f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ project_name }}}}</title>
</head>
<body>
    <h1>Welcome to {{{{ project_name }}}}</h1>
    <p>{project_description}</p>
</body>
</html>
'''
        },
        {
            'name': 'requirements.txt',
            'content': 'flask==2.0.1\n'
        }
    ]

python_templates = {
    'web_development': python_web_template,
    # Add more theme-specific templates here...
}
