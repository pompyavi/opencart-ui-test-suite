"""
Framework Exception Module
==========================

Custom exception classes for the test automation framework.
Provides meaningful error messages for framework-specific failures.

Usage:
    Raise FrameworkException when a framework operation fails,
    such as element not found, configuration error, or timeout.

Example:
    >>> from utils.framework_exception import FrameworkException
    >>> 
    >>> if not element:
    ...     raise FrameworkException("Element not found after 30 seconds")
"""


class FrameworkException(Exception):
    """
    Base exception class for all framework-specific errors.
    
    Use this exception when operations within the framework fail,
    providing clear error messages for debugging.
    
    Attributes:
        message: Human-readable error description.
        
    Example:
        >>> try:
        ...     driver.find_element(By.ID, "missing")
        ... except NoSuchElementException:
        ...     raise FrameworkException("Login button not found on page")
        
        >>> # With detailed context
        >>> raise FrameworkException(
        ...     f"Failed to load page within {timeout}s. "
        ...     f"Current URL: {driver.current_url}"
        ... )
    """
    
    def __init__(self, message: str):
        """
        Initialize FrameworkException with an error message.
        
        Args:
            message: Descriptive error message explaining what went wrong.
        """
        self.message = message
        super().__init__(self.message)
