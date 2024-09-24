def rust_cli_template(project_name, project_description, custom_prompt=None):
    return [
        {
            'name': 'src/main.rs',
            'content': f'''
// {project_name}
// {project_description}

fn main() {{
    println!("Welcome to {project_name}!");
    println!("{project_description}");
}}
'''
        },
        {
            'name': 'Cargo.toml',
            'content': f'''
[package]
name = "{project_name.lower().replace(' ', '-')}"
version = "0.1.0"
edition = "2021"

[dependencies]
'''
        }
    ]

# Add more Rust templates for different themes here...

rust_templates = {
    'cli': rust_cli_template,
    # Add more theme-specific templates here...
}

