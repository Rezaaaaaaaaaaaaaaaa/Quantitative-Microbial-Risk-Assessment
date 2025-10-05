#!/usr/bin/env python3
"""
Tests for error handling module
"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from error_handling import (
    QMRAError, DataValidationError, ModelError, ConfigurationError, ResourceError,
    format_error_message, validate_file_access, ErrorCollector, create_error_report
)


class TestQMRAErrors(unittest.TestCase):
    """Test custom QMRA exception classes."""

    def test_qmra_error_basic(self):
        """Test basic QMRAError functionality."""
        error = QMRAError("Test error message")
        self.assertEqual(str(error), "Test error message")
        self.assertIsNone(error.error_code)
        self.assertEqual(error.suggestions, [])

    def test_qmra_error_with_code_and_suggestions(self):
        """Test QMRAError with error code and suggestions."""
        suggestions = ["Try this", "Or try that"]
        error = QMRAError("Test error", error_code="ERR001", suggestions=suggestions)

        self.assertEqual(str(error), "Test error")
        self.assertEqual(error.error_code, "ERR001")
        self.assertEqual(error.suggestions, suggestions)

    def test_specific_error_types(self):
        """Test specific error type inheritance."""
        data_error = DataValidationError("Data error")
        model_error = ModelError("Model error")
        config_error = ConfigurationError("Config error")
        resource_error = ResourceError("Resource error")

        self.assertIsInstance(data_error, QMRAError)
        self.assertIsInstance(model_error, QMRAError)
        self.assertIsInstance(config_error, QMRAError)
        self.assertIsInstance(resource_error, QMRAError)


class TestErrorFormatting(unittest.TestCase):
    """Test error message formatting."""

    def test_format_qmra_error(self):
        """Test formatting of QMRAError."""
        error = QMRAError("Test error", suggestions=["Suggestion 1", "Suggestion 2"])
        formatted = format_error_message(error)

        self.assertIn("❌ Test error", formatted)
        self.assertIn("Suggestions:", formatted)
        self.assertIn("• Suggestion 1", formatted)
        self.assertIn("• Suggestion 2", formatted)

    def test_format_qmra_error_without_suggestions(self):
        """Test formatting of QMRAError without suggestions."""
        error = QMRAError("Test error")
        formatted = format_error_message(error)

        self.assertIn("❌ Test error", formatted)
        self.assertNotIn("Suggestions:", formatted)

    def test_format_file_not_found_error(self):
        """Test formatting of FileNotFoundError."""
        error = FileNotFoundError("test.txt")
        formatted = format_error_message(error)

        self.assertIn("❌ File not found:", formatted)
        self.assertIn("Suggestions:", formatted)
        self.assertIn("Check that the file path is correct", formatted)

    def test_format_memory_error(self):
        """Test formatting of MemoryError."""
        error = MemoryError()
        formatted = format_error_message(error)

        self.assertIn("❌ Insufficient memory", formatted)
        self.assertIn("Suggestions:", formatted)
        self.assertIn("Reduce the number of Monte Carlo iterations", formatted)

    def test_format_keyboard_interrupt(self):
        """Test formatting of KeyboardInterrupt."""
        error = KeyboardInterrupt()
        formatted = format_error_message(error)

        self.assertEqual(formatted, "❌ Operation interrupted by user")

    def test_format_generic_error(self):
        """Test formatting of generic exceptions."""
        error = ValueError("Invalid value")
        formatted = format_error_message(error)

        self.assertIn("❌ Unexpected error: Invalid value", formatted)
        self.assertIn("Please report this to the development team", formatted)

    def test_format_generic_error_with_context(self):
        """Test formatting of generic exceptions with context."""
        error = ValueError("Invalid value")
        formatted = format_error_message(error, context="test_function")

        self.assertIn("❌ Error in test_function: Invalid value", formatted)


class TestFileValidation(unittest.TestCase):
    """Test file access validation."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_file.write_text("test content")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_validate_existing_file_read(self):
        """Test validation of existing file for reading."""
        # Should not raise an exception
        validate_file_access(self.test_file, mode='r')

    def test_validate_nonexistent_file_read(self):
        """Test validation of nonexistent file for reading."""
        nonexistent_file = Path(self.temp_dir) / "nonexistent.txt"

        with self.assertRaises(ConfigurationError) as cm:
            validate_file_access(nonexistent_file, mode='r')

        self.assertIn("Required file not found", str(cm.exception))

    def test_validate_directory_as_file(self):
        """Test validation when path points to directory instead of file."""
        with self.assertRaises(ConfigurationError) as cm:
            validate_file_access(self.temp_dir, mode='r')

        self.assertIn("Path is not a file", str(cm.exception))

    def test_validate_write_to_existing_directory(self):
        """Test validation for writing to existing directory."""
        output_file = Path(self.temp_dir) / "output.txt"

        # Should not raise an exception
        validate_file_access(output_file, mode='w')

    def test_validate_write_to_nonexistent_directory(self):
        """Test validation for writing to nonexistent directory."""
        nonexistent_dir = Path(self.temp_dir) / "nonexistent" / "output.txt"

        with self.assertRaises(ConfigurationError) as cm:
            validate_file_access(nonexistent_dir, mode='w')

        self.assertIn("Directory does not exist", str(cm.exception))


class TestErrorCollector(unittest.TestCase):
    """Test error collector functionality."""

    def setUp(self):
        self.collector = ErrorCollector()

    def test_empty_collector(self):
        """Test empty error collector."""
        self.assertFalse(self.collector.has_errors())
        self.assertFalse(self.collector.has_warnings())
        self.assertEqual(self.collector.get_summary(), "✅ No errors or warnings")

    def test_add_error(self):
        """Test adding errors to collector."""
        error = ValueError("Test error")
        self.collector.add_error(error, context="test_context")

        self.assertTrue(self.collector.has_errors())
        self.assertFalse(self.collector.has_warnings())

        summary = self.collector.get_summary()
        self.assertIn("❌ 1 error(s) occurred:", summary)
        self.assertIn("Test error in test_context", summary)

    def test_add_warning(self):
        """Test adding warnings to collector."""
        self.collector.add_warning("Test warning", context="test_context")

        self.assertFalse(self.collector.has_errors())
        self.assertTrue(self.collector.has_warnings())

        summary = self.collector.get_summary()
        self.assertIn("⚠️  1 warning(s):", summary)
        self.assertIn("Test warning in test_context", summary)

    def test_multiple_errors_and_warnings(self):
        """Test multiple errors and warnings."""
        self.collector.add_error(ValueError("Error 1"))
        self.collector.add_error(TypeError("Error 2"), context="context2")
        self.collector.add_warning("Warning 1")
        self.collector.add_warning("Warning 2", context="warn_context")

        self.assertTrue(self.collector.has_errors())
        self.assertTrue(self.collector.has_warnings())

        summary = self.collector.get_summary()
        self.assertIn("❌ 2 error(s) occurred:", summary)
        self.assertIn("⚠️  2 warning(s):", summary)
        self.assertIn("Error 1", summary)
        self.assertIn("Error 2 in context2", summary)
        self.assertIn("Warning 1", summary)
        self.assertIn("Warning 2 in warn_context", summary)

    def test_clear_collector(self):
        """Test clearing error collector."""
        self.collector.add_error(ValueError("Test error"))
        self.collector.add_warning("Test warning")

        self.assertTrue(self.collector.has_errors())
        self.assertTrue(self.collector.has_warnings())

        self.collector.clear()

        self.assertFalse(self.collector.has_errors())
        self.assertFalse(self.collector.has_warnings())
        self.assertEqual(self.collector.get_summary(), "✅ No errors or warnings")


class TestErrorReport(unittest.TestCase):
    """Test error report generation."""

    def test_create_error_report(self):
        """Test creating detailed error report."""
        error = ValueError("Test error message")
        context = {
            "function": "test_function",
            "parameters": {"param1": "value1", "param2": 42},
            "timestamp": "2024-01-01T12:00:00Z"
        }

        report = create_error_report(error, context)

        self.assertIn("QMRA Toolkit Error Report", report)
        self.assertIn("Error Type: ValueError", report)
        self.assertIn("Error Message: Test error message", report)
        self.assertIn("Context Information:", report)
        self.assertIn("function: test_function", report)
        self.assertIn("parameters: {'param1': 'value1', 'param2': 42}", report)
        self.assertIn("Stack Trace:", report)

    def test_create_error_report_no_context(self):
        """Test creating error report without context."""
        error = ValueError("Test error")
        report = create_error_report(error, {})

        self.assertIn("QMRA Toolkit Error Report", report)
        self.assertIn("Error Type: ValueError", report)
        self.assertIn("Error Message: Test error", report)
        self.assertNotIn("Context Information:", report)


class TestMemoryValidation(unittest.TestCase):
    """Test memory validation functionality."""

    @patch('sys.modules')
    def test_memory_validation_without_psutil(self, mock_modules):
        """Test memory validation when psutil is not available."""
        # Mock psutil not being available
        def mock_import(name, *args, **kwargs):
            if name == 'psutil':
                raise ImportError("No module named 'psutil'")
            return __import__(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=mock_import):
            from error_handling import validate_memory_requirements
            # Should not raise an exception when psutil is not available
            validate_memory_requirements(1024**3, safety_factor=2.0)

    def test_memory_validation_concept(self):
        """Test memory validation concept without external dependencies."""
        from error_handling import ResourceError

        # Test that we can create ResourceError with appropriate message
        error = ResourceError(
            "Insufficient memory: need 2.0 GB, available 1.0 GB",
            suggestions=["Reduce Monte Carlo iterations", "Close other applications"]
        )

        self.assertIn("Insufficient memory", str(error))
        self.assertEqual(len(error.suggestions), 2)


if __name__ == '__main__':
    unittest.main()