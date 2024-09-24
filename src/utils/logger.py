import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with file and console handlers."""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create file handler which logs even debug messages
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
    file_handler.setFormatter(formatter)

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create loggers
main_logger = setup_logger('main', 'logs/main.log')
project_generator_logger = setup_logger('project_generator', 'logs/project_generator.log')
github_interface_logger = setup_logger('github_interface', 'logs/github_interface.log')
scheduler_logger = setup_logger('scheduler', 'logs/scheduler.log')
