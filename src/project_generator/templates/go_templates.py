def go_web_template(project_name, project_description, custom_prompt=None):
    return [
        {
            'name': 'main.go',
            'content': f'''
// {project_name}
// {project_description}

package main

import (
    "fmt"
    "net/http"
)

func main() {{
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {{
        fmt.Fprintf(w, "<h1>Welcome to %s</h1><p>%s</p>", "{project_name}", "{project_description}")
    }})

    fmt.Println("Server is running on http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}}
'''
        }
    ]

# Add more Go templates for different themes here...

go_templates = {
    'web_development': go_web_template,
    # Add more theme-specific templates here...
}
