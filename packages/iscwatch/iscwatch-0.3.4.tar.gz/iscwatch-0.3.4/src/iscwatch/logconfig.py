"""Define the default logging configuration for the application."""
logging_config = {
    "version": 1,
    "formatters": {
        "defaultFormatter": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "defaultFormatter",
            "stream": "ext://sys.stderr",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["consoleHandler"]},
}
