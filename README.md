# AutoGitHub

AutoGitHub is an AI-powered project that automatically generates and pushes random coding projects to your GitHub account. It uses OpenAI's GPT model to create unique project ideas and code, and then uses the GitHub API to create repositories and push the generated content.

## Features

- Generates random project ideas and code using AI
- Supports multiple programming languages (Python, JavaScript, Rust, Java, Go)
- Automatically creates GitHub repositories and pushes code
- Configurable scheduling for daily project creation
- Web interface for monitoring project generation and viewing logs
- CLI for manual project generation and configuration
- API for external integrations
- Basic analytics for generated projects

## Prerequisites

- Python 3.7+
- GitHub account and personal access token
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/autogithub.git
   cd autogithub
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` file to `.env` and fill in your GitHub token, OpenAI API key, and other required information:
   ```
   cp .env.example .env
   ```

4. Edit the `config/config.yaml` file to customize your settings.

## Usage

To start AutoGitHub, run:

```
python main.py
```

### CLI Usage

For manual project generation:
```
python -m src.cli.cli generate
```

To update configuration:
```
python -m src.cli.cli configure
```

To generate a new API key:
```
python -m src.cli.cli generate-api-key
```

### Web Interface

Access the web interface at `https://localhost:5002`

### API

Make requests to `https://localhost:5000/api/` with the appropriate endpoints. Remember to include your API key in the `X-API-Key` header.

## Security

Please ensure that you keep your API keys and tokens secure. Do not share them or commit them to version control.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational purposes only. Use it responsibly and in accordance with GitHub's terms of service. The authors are not responsible for any misuse or consequences arising from the use of this software.
