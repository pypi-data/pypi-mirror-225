# FileSchemaValidator

![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)
[![License](https://img.shields.io/github/license/yourusername/FileSchemaValidator)](LICENSE)

The **FileSchemaValidator** module provides a powerful and extensible solution for validating CSV files against customizable schemas in Python. This module is designed to enhance data quality and integrity by seamlessly integrating schema-based validation into your data processing workflows.

## Features

- **Dynamic Schema Definition:** Define flexible validation schemas using a list of dictionaries, specifying column names, data types, and modes (REQUIRED or NULLABLE).
- **Comprehensive Data Validation:** Validate column presence and data integrity. Supports various data types: integers, floats, strings, dates, timestamps, and booleans.
- **Data Type Validation:** Perform thorough data type checks to ensure data adherence to specified types.
- **Intuitive Integration:** Easily integrate with existing CSV processing pipelines using `csv.DictReader`.
- **Expandable Architecture:** Designed for expansion to support other file formats and validation scenarios.
- **Clear Error Reporting:** Detailed error messages pinpointing column names and error specifics for quick issue resolution.
- **Open Source and Customizable:** Contribute, customize, and extend the module to meet your unique requirements.

## Installation

Install the module using pip:

```bash
pip install FileSchemaValidator
