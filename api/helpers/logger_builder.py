import logging
import os

DEFAULT_LEVEL = logging.INFO
"""The default logging level."""
DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(name)s [%(filename)s:%(lineno)d] - %(message)s"
"""The default logging format."""


class LoggerBuilder:
    """
    Utility class for building and configuring loggers.

    This class provides methods to build and configure loggers with console and Azure Application Insights handlers.
    """
    name: str
    """The name of the logger."""
    _initialized_logger: bool
    """Flag to check if the logger has been initialized."""

    @classmethod
    def build(
        cls,
        name: str,
        level: str = DEFAULT_LEVEL,
        format: str = DEFAULT_FORMAT,
        extra_handlers: list[logging.Handler] = [],
    ) -> logging.Logger:
        """
        Build and configure a logger instance.

        Args:
            name (str): The name of the logger.
            level (str, optional): The logging level. Defaults to ``DEFAULT_LEVEL``.
            format (str, optional): The logging format. Defaults to ``DEFAULT_FORMAT``.
            extra_handlers (list[logging.Handler], optional): A list of additional logging handlers. Defaults to [].

        Returns:
            logging.Logger: The configured logger instance.

        Example:
            .. code-block:: python

                from helpers.logger_builder.logger_builder import LoggerBuilder
                import logging

                logger = LoggerBuilder.build(
                    name="my_logger",
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s"
                )

                logger.info("This is an info message.")
                logger.error("This is an error message.")
        """
        # Get logger instance (will create if doesn't exist)
        
        logger_instance = logging.getLogger(name)
        
        # If logger already has handlers, it was already configured, so return it
        # Check if logger was already initialized
        if not hasattr(cls, '_initialized_logger'):
            cls._initialized_logger = False

        # Case when the logger was already initialized
        if cls._initialized_logger:
            return logger_instance
        
        # Configure the logger since it doesn't have handlers yet
        cls.name = name
        logger_instance.setLevel(level)

        # Get Azure Monitor connection string (prioritize Databricks-specific env var)
        app_insights_cs = (
            os.getenv("REALE_APPLICATIONINSIGHTS_CONNECTION_STRING") or 
            os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
        )
        
        if app_insights_cs is not None:
            from azure.monitor.opentelemetry import configure_azure_monitor
            # Configure Azure Monitor (handles both telemetry and console logging)
            configure_azure_monitor(
                connection_string=app_insights_cs,
                logger_name=name,
            )
        
        # Set Console log handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(format))
        logger_instance.addHandler(console_handler)

        for extra_handler in extra_handlers:
            # Set File Handler
            extra_handler.setLevel(level)
            extra_handler.setFormatter(logging.Formatter(format))
            logger_instance.addHandler(extra_handler)

        cls._initialized_logger = True

        return logger_instance

