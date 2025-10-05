"""
Error handling utilities for QMRA Toolkit

This module provides comprehensive error handling, logging, and user-friendly
error messages for the QMRA toolkit.
"""

import logging
import traceback
import sys
from functools import wraps
from typing import Callable, Any, Optional, Dict, Union
from pathlib import Path
import click

logger = logging.getLogger(__name__)


class QMRAError(Exception):
    """Base exception class for QMRA-specific errors."""
    def __init__(self, message: str, error_code: Optional[str] = None, suggestions: Optional[list] = None):
        super().__init__(message)
        self.error_code = error_code
        self.suggestions = suggestions or []


class DataValidationError(QMRAError):
    """Error in data validation."""
    pass


class ModelError(QMRAError):
    """Error in model calculations."""
    pass


class ConfigurationError(QMRAError):
    """Error in configuration or setup."""
    pass


class ResourceError(QMRAError):
    """Error related to system resources (memory, disk, etc.)."""
    pass


def format_error_message(error: Exception, context: Optional[str] = None) -> str:
    """
    Format error message for user display.

    Args:
        error: Exception that occurred
        context: Additional context about where the error occurred

    Returns:
        Formatted error message
    """
    if isinstance(error, QMRAError):
        message = f"❌ {error}"
        if error.suggestions:
            message += "\n\nSuggestions:"
            for suggestion in error.suggestions:
                message += f"\n  • {suggestion}"
        return message

    elif isinstance(error, FileNotFoundError):
        message = f"❌ File not found: {error}"
        message += "\n\nSuggestions:"
        message += "\n  • Check that the file path is correct"
        message += "\n  • Ensure the file exists and is accessible"
        return message

    elif isinstance(error, MemoryError):
        message = "❌ Insufficient memory to complete the operation"
        message += "\n\nSuggestions:"
        message += "\n  • Reduce the number of Monte Carlo iterations"
        message += "\n  • Close other applications to free memory"
        message += "\n  • Consider processing smaller datasets"
        return message

    elif isinstance(error, KeyboardInterrupt):
        return "❌ Operation interrupted by user"

    else:
        message = f"❌ Unexpected error: {error}"
        if context:
            message = f"❌ Error in {context}: {error}"
        message += "\n\nThis appears to be an unexpected error. Please report this to the development team."
        return message


def handle_cli_error(func: Callable) -> Callable:
    """
    Decorator for CLI command error handling.

    Args:
        func: CLI command function to wrap

    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except QMRAError as e:
            click.echo(format_error_message(e), err=True)
            sys.exit(1)
        except FileNotFoundError as e:
            click.echo(format_error_message(e), err=True)
            sys.exit(1)
        except ValueError as e:
            error = DataValidationError(
                f"Invalid data value: {e}",
                suggestions=["Check your input parameters", "Ensure all values are within valid ranges"]
            )
            click.echo(format_error_message(error), err=True)
            sys.exit(1)
        except MemoryError as e:
            click.echo(format_error_message(e), err=True)
            sys.exit(1)
        except KeyboardInterrupt:
            click.echo(format_error_message(KeyboardInterrupt()), err=True)
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            click.echo(format_error_message(e, func.__name__), err=True)
            sys.exit(1)

    return wrapper


def handle_gui_error(func: Callable) -> Callable:
    """
    Decorator for GUI method error handling.

    Args:
        func: GUI method to wrap

    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except QMRAError as e:
            self.show_error_dialog("QMRA Error", str(e), e.suggestions)
        except FileNotFoundError as e:
            self.show_error_dialog(
                "File Not Found",
                str(e),
                ["Check that the file path is correct", "Ensure the file exists and is accessible"]
            )
        except MemoryError:
            self.show_error_dialog(
                "Memory Error",
                "Insufficient memory to complete the operation",
                ["Reduce the number of Monte Carlo iterations", "Close other applications to free memory"]
            )
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            self.show_error_dialog(
                "Unexpected Error",
                f"An unexpected error occurred: {e}",
                ["Please report this to the development team"]
            )

    return wrapper


def validate_file_access(file_path: Union[str, Path], mode: str = 'r') -> None:
    """
    Validate file access before operations.

    Args:
        file_path: Path to file
        mode: File access mode ('r', 'w', etc.)

    Raises:
        ConfigurationError: If file access is not possible
    """
    file_path = Path(file_path)

    if mode == 'r':
        if not file_path.exists():
            raise ConfigurationError(
                f"Required file not found: {file_path}",
                suggestions=["Check the file path", "Ensure the file has been created"]
            )
        if not file_path.is_file():
            raise ConfigurationError(
                f"Path is not a file: {file_path}",
                suggestions=["Check that the path points to a file, not a directory"]
            )

    elif mode in ['w', 'a']:
        parent_dir = file_path.parent
        if not parent_dir.exists():
            raise ConfigurationError(
                f"Directory does not exist: {parent_dir}",
                suggestions=["Create the directory first", "Check the file path"]
            )
        if not parent_dir.is_dir():
            raise ConfigurationError(
                f"Parent path is not a directory: {parent_dir}",
                suggestions=["Check the file path"]
            )


def validate_memory_requirements(data_size: int, safety_factor: float = 2.0) -> None:
    """
    Check if there's sufficient memory for an operation.

    Args:
        data_size: Estimated memory requirement in bytes
        safety_factor: Safety factor for memory estimation

    Raises:
        ResourceError: If insufficient memory is available
    """
    try:
        import psutil
        available_memory = psutil.virtual_memory().available
        required_memory = data_size * safety_factor

        if required_memory > available_memory:
            raise ResourceError(
                f"Insufficient memory: need {required_memory / 1e9:.1f} GB, "
                f"available {available_memory / 1e9:.1f} GB",
                suggestions=[
                    "Reduce the number of Monte Carlo iterations",
                    "Process data in smaller chunks",
                    "Close other applications to free memory"
                ]
            )
    except ImportError:
        # psutil not available, skip memory check
        logger.warning("Memory validation skipped: psutil not available")


def setup_error_logging(log_file: Optional[Union[str, Path]] = None, log_level: str = "INFO") -> None:
    """
    Set up comprehensive error logging.

    Args:
        log_file: Optional log file path
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        logger.info(f"Error logging configured: {log_file}")


class ErrorCollector:
    """Collect and manage multiple errors during batch operations."""

    def __init__(self):
        self.errors: list = []
        self.warnings: list = []

    def add_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Add an error to the collection."""
        self.errors.append({
            'error': error,
            'context': context,
            'traceback': traceback.format_exc()
        })

    def add_warning(self, message: str, context: Optional[str] = None) -> None:
        """Add a warning to the collection."""
        self.warnings.append({
            'message': message,
            'context': context
        })

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    def get_summary(self) -> str:
        """Get a summary of all errors and warnings."""
        summary = []

        if self.errors:
            summary.append(f"❌ {len(self.errors)} error(s) occurred:")
            for i, error_info in enumerate(self.errors, 1):
                context = f" in {error_info['context']}" if error_info['context'] else ""
                summary.append(f"  {i}. {error_info['error']}{context}")

        if self.warnings:
            summary.append(f"\n⚠️  {len(self.warnings)} warning(s):")
            for i, warning_info in enumerate(self.warnings, 1):
                context = f" in {warning_info['context']}" if warning_info['context'] else ""
                summary.append(f"  {i}. {warning_info['message']}{context}")

        return "\n".join(summary) if summary else "✅ No errors or warnings"

    def clear(self) -> None:
        """Clear all errors and warnings."""
        self.errors.clear()
        self.warnings.clear()


def create_error_report(error: Exception, context: Dict[str, Any]) -> str:
    """
    Create a detailed error report for debugging.

    Args:
        error: Exception that occurred
        context: Dictionary with context information

    Returns:
        Formatted error report
    """
    report = []
    report.append("QMRA Toolkit Error Report")
    report.append("=" * 40)
    report.append(f"Error Type: {type(error).__name__}")
    report.append(f"Error Message: {error}")
    report.append("")

    if context:
        report.append("Context Information:")
        for key, value in context.items():
            report.append(f"  {key}: {value}")
        report.append("")

    report.append("Stack Trace:")
    report.append(traceback.format_exc())

    return "\n".join(report)