# Error Handling Module

Error handling utilities for QMRA Toolkit

This module provides comprehensive error handling, logging, and user-friendly
error messages for the QMRA toolkit.

## Classes

### ConfigurationError

Error in configuration or setup.

### DataValidationError

Error in data validation.

### ErrorCollector

Collect and manage multiple errors during batch operations.

### ModelError

Error in model calculations.

### QMRAError

Base exception class for QMRA-specific errors.

### ResourceError

Error related to system resources (memory, disk, etc.).

## Functions

### create_error_report(error: Exception, context: Dict[str, Any]) -> str

Create a detailed error report for debugging.

Args:
    error: Exception that occurred
    context: Dictionary with context information

Returns:
    Formatted error report

### format_error_message(error: Exception, context: Optional[str] = None) -> str

Format error message for user display.

Args:
    error: Exception that occurred
    context: Additional context about where the error occurred

Returns:
    Formatted error message

### handle_cli_error(func: Callable) -> Callable

Decorator for CLI command error handling.

Args:
    func: CLI command function to wrap

Returns:
    Wrapped function with error handling

### handle_gui_error(func: Callable) -> Callable

Decorator for GUI method error handling.

Args:
    func: GUI method to wrap

Returns:
    Wrapped function with error handling

### setup_error_logging(log_file: Union[str, pathlib.Path, NoneType] = None, log_level: str = 'INFO') -> None

Set up comprehensive error logging.

Args:
    log_file: Optional log file path
    log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### validate_file_access(file_path: Union[str, pathlib.Path], mode: str = 'r') -> None

Validate file access before operations.

Args:
    file_path: Path to file
    mode: File access mode ('r', 'w', etc.)

Raises:
    ConfigurationError: If file access is not possible

### validate_memory_requirements(data_size: int, safety_factor: float = 2.0) -> None

Check if there's sufficient memory for an operation.

Args:
    data_size: Estimated memory requirement in bytes
    safety_factor: Safety factor for memory estimation

Raises:
    ResourceError: If insufficient memory is available

