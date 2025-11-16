"""
Base agent class for the agent-based architecture.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
import logging


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(self.name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'[%(asctime)s] {self.name} - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the agent's main task.

        This method must be implemented by all concrete agents.
        """
        pass

    def log_info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

    def log_error(self, message: str):
        """Log an error message."""
        self.logger.error(message)

    def log_debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
