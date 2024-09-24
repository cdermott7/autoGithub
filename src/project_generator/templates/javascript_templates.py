def javascript_web_template(project_name, project_description, custom_prompt=None):
    return [
        {
            'name': 'index.js',
            'content': f'''
// {project_name}
// {project_description}

const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {{
    res.send(`
        <h1>Welcome to {project_name}</h1>
        <p>{project_description}</p>
    `);
}});

app.listen(port, () => {{
    console.log(`{project_name} is running at http://localhost:${{port}}`);
}});
'''
        },
        {
            'name': 'package.json',
            'content': f'''
{{
  "name": "{project_name.lower().replace(' ', '-')}",
  "version": "1.0.0",
  "description": "{project_description}",
  "main": "index.js",
  "scripts": {{
    "start": "node index.js"
  }},
  "dependencies": {{
    "express": "^4.17.1"
  }}
}}
'''
        }
    ]

# Add more JavaScript templates for different themes here...

javascript_templates = {
    'web_development': javascript_web_template,
    # Add more theme-specific templates here...
}
