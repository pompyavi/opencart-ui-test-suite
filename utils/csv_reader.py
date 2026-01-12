"""
CSV Reader Module
=================

Utility for reading test data from CSV files.
Used for data-driven testing with parameterized test cases.

Features:
    - Automatic header row skipping
    - Path resolution relative to project root
    - Returns data as list of tuples for pytest parametrize

Example:
    >>> from utils.csv_reader import csv_reader
    >>> 
    >>> # In test file
    >>> @pytest.mark.parametrize('username, password, expected', csv_reader('test_data/login.csv'))
    >>> def test_login(username, password, expected):
    ...     pass
"""

import csv
import logging
from pathlib import Path
from typing import List, Tuple

_logger = logging.getLogger(__name__)


def csv_reader(path: str) -> List[Tuple[str, ...]]:
    """
    Read a CSV file and return rows as a list of tuples.
    
    Automatically skips the header row and resolves the path
    relative to the project root directory.
    
    Args:
        path: Relative path to the CSV file from project root.
              Example: 'test_data/user_registration_data.csv'
              
    Returns:
        List[Tuple[str, ...]]: List of tuples, where each tuple
        contains the values from one row.
        
    File Format:
        - First row is treated as header and skipped
        - Subsequent rows are returned as tuples
        - All values are returned as strings
        
    Example:
        >>> # CSV file (test_data/users.csv):
        >>> # username,password,role
        >>> # john,pass123,admin
        >>> # jane,pass456,user
        >>> 
        >>> data = csv_reader('test_data/users.csv')
        >>> print(data)
        [('john', 'pass123', 'admin'), ('jane', 'pass456', 'user')]
        
        >>> # Use with pytest parametrize
        >>> @pytest.mark.parametrize('username, password, role', csv_reader('test_data/users.csv'))
        >>> def test_user_login(username, password, role):
        ...     # Test implementation
        ...     pass
    """
    file_path = Path(__file__).resolve().parent.parent / path
    _logger.debug(f"Reading CSV file: {file_path}")
    
    with open(file_path, newline="", encoding="utf-8") as f:
        csv_rows = csv.reader(f)
        next(csv_rows, None)  # skip header
        rows = [tuple(row) for row in csv_rows]
    
    _logger.info(f"CSV loaded | File: {path} | Rows: {len(rows)}")
    return rows
