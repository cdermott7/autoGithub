from flask import Flask, render_template, jsonify
from flask_talisman import Talisman
import os
import yaml
from src.project_tracker.tracker import ProjectTracker
from src.utils.error_handler import handle_error
from src.analytics.analyzer import ProjectAnalyzer

app = Flask(__name__)
Talisman(app, content_security_policy={
    'default-src': "'self'",
    'script-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
    'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
})

project_tracker = ProjectTracker()
project_analyzer = ProjectAnalyzer(project_tracker)

@app.route('/')
def home():
    try:
        dashboard = {
            "total_projects": len(project_tracker.history),
            "language_distribution": project_analyzer.get_language_distribution(),
            "theme_distribution": project_analyzer.get_theme_distribution(),
            "projects_per_day": project_analyzer.get_projects_per_day(),
            "recent_projects": project_tracker.history[-5:]  # Last 5 projects
        }
        return render_template('index.html', dashboard=dashboard)
    except Exception as e:
        error_message = handle_error(e, context="fetch_dashboard_data")
        return jsonify({"error": error_message}), 500

@app.route('/config')
def config():
    try:
        config = load_config()
        return jsonify(config)
    except Exception as e:
        error_message = handle_error(e, context="fetch_config")
        return jsonify({"error": error_message}), 500

@app.route('/logs')
def logs():
    try:
        log_files = os.listdir('logs')
        logs = {}
        for log_file in log_files:
            with open(os.path.join('logs', log_file), 'r') as f:
                logs[log_file] = f.readlines()[-50:]  # Get last 50 lines
        return jsonify(logs)
    except Exception as e:
        error_message = handle_error(e, context="fetch_logs")
        return jsonify({"error": error_message}), 500

@app.route('/dashboard')
def dashboard():
    try:
        language_distribution = project_analyzer.get_language_distribution()
        theme_distribution = project_analyzer.get_theme_distribution()
        projects_per_day = project_analyzer.get_projects_per_day()
        recent_projects = project_tracker.history[-5:]  # Last 5 projects
        
        # Debug statement to log the structure of each project in recent_projects
        for project in recent_projects:
            app.logger.debug(f"Project: {project.__dict__}")
        
        return jsonify({
            "total_projects": len(project_tracker.history),
            "language_distribution": language_distribution,
            "theme_distribution": theme_distribution,
            "projects_per_day": projects_per_day,
            "recent_projects": recent_projects
        })
    except Exception as e:
        error_message = handle_error(e, context="fetch_dashboard_data")
        return jsonify({"error": error_message}), 500
@app.route('/charts/language')
def language_chart():
    try:
        chart = project_analyzer.generate_language_chart()
        return chart.getvalue(), 200, {'Content-Type': 'image/png'}
    except Exception as e:
        error_message = handle_error(e, context="generate_language_chart")
        return jsonify({"error": error_message}), 500

@app.route('/charts/theme')
def theme_chart():
    try:
        chart = project_analyzer.generate_theme_chart()
        return chart.getvalue(), 200, {'Content-Type': 'image/png'}
    except Exception as e:
        error_message = handle_error(e, context="generate_theme_chart")
        return jsonify({"error": error_message}), 500

@app.route('/charts/projects_per_day')
def projects_per_day_chart():
    try:
        chart = project_analyzer.generate_projects_per_day_chart()
        return chart.getvalue(), 200, {'Content-Type': 'image/png'}
    except Exception as e:
        error_message = handle_error(e, context="generate_projects_per_day_chart")
        return jsonify({"error": error_message}), 500

def load_config():
    with open('config/config.yaml', 'r') as config_file:
        return yaml.safe_load(config_file)

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Change the port if needed