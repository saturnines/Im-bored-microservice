import logging
from fluent import handler as fluent_handler

print("Hello from logging Service")

def configure_logging(service_name: str, fluentd_host: str = 'localhost', fluentd_port: int = 24224):

    

    # Create or get current logger
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    # check if theres a logger if not just set default logger with below configs
    if not logger.handlers:
        fluent_handler_instance = fluent_handler.FluentHandler(service_name, host=fluentd_host, port=fluentd_port)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fluent_handler_instance.setFormatter(formatter)
        logger.addHandler(fluent_handler_instance)

    return logger
