from .schema_validator import SchemaValidator
from datetime import datetime
import csv
import warnings


class CsvSchemaValidator(SchemaValidator):
    """
    Class for CSV schema validation.
    """

    def __init__(self, schemafile, csv_reader) -> None:
        """
        Initializes the CsvSchemaValidator class.

        Args:
            schemafile (dict): Dictionary representing column schema.
            csv_reader (csv.DictReader): Instance of the CSV reader.
        """
        super().__init__(schemafile)
        self.reader = csv_reader
        self.validate_columns_errors = None
        self.validate_columns_warnings = None
        self.validate_rows_errors = {}

    @property
    def csv_reader(self):
        """
        Accessor for the CSV reader.

        Returns:
            csv.DictReader: Instance of the CSV reader.
        """
        return self._csv_reader

    @csv_reader.setter
    def csv_reader(self, reader):
        """
        Sets the CSV reader.

        Args:
            reader (csv.DictReader): Instance of the CSV reader.

        Raises:
            ValueError: If reader is not a valid instance of csv.DictReader.
        """
        if not isinstance(reader, csv.DictReader):
            raise ValueError("csv_reader must be an instance of csv.DictReader.")
        self._csv_reader = reader
        
    def validate_columns(self):
        """
        Validates if all columns required by the schema are present in the CSV.

        Raises:
            Exception: If a required column is not found in the CSV.
            Warning: If a extra column is found on CSV.
        """
        missing_columns = set(self.schemafile.keys()) - set(self.reader.fieldnames)
        extra_columns = set(self.reader.fieldnames) - set(self.schemafile.keys())

        if missing_columns:
            self.validate_columns_errors = [f'{c} Column is required but was not found.' for c in missing_columns]
            raise Exception('\n '.join(self.validate_columns_errors))
        elif extra_columns:
            self.validate_columns_warnings = [f'{c} Column is not in the SchemaFile and will not be processed, consider removing the Column.' for c in extra_columns]
            warnings.warn('\n '.join(self.validate_columns_warnings))
        else:
            print('validate_columns completed successfully.')
            return True
        
    def required_validation(self, schema, value, column):
        if schema['is_required'] and not value:
            if not self.validate_rows_errors.get(str(self.row_counter)):
                self.validate_rows_errors[str(self.row_counter)] = [f'{column}: Value can not be null.']
            else:
                self.validate_rows_errors[str(self.row_counter)].append(f'{column}: Value can not be null.')

    def type_validation(self, schema, value, column):
        data_type = schema['type']
        try:
            if value:
                if data_type == 'int':
                    int(value)
                elif data_type == 'float':
                    float(value)
                elif data_type == 'string':
                    str(value)
                elif data_type == 'date':
                    datetime.strptime(value, schema['format'])
                elif data_type == 'timestamp':
                    datetime.strptime(value, schema['format'])
                elif data_type == 'bool':
                    if value not in [0, 1, 'true', 'false', '0', '1']:
                        if not self.validate_rows_errors.get(str(self.row_counter)):
                            self.validate_rows_errors[str(self.row_counter)] = [f'{column}: Boolean field must be True or False.']
                        else:
                            self.validate_rows_errors[str(self.row_counter)].append(f'{column}: Boolean field must be True or False.')
        except Exception as e:
            if not self.validate_rows_errors.get(str(self.row_counter)):
                self.validate_rows_errors[str(self.row_counter)] = [f'{column}: {str(e)}']
            else:
                self.validate_rows_errors[str(self.row_counter)].append(f'{column}: {str(e)}')

    def validate_rows(self):
        """
        Validates the data in the CSV rows according to the schema.

        Raises:
            ValueError: If row data does not comply with the schema.
        """
        self.row_counter=0
        for row in self.reader:
            for column in list(row.keys()):
                schema = self.schemafile.get(column)
                if schema:
                    value = row.get(column)
                    # Required Validation
                    self.required_validation(schema, value, column)
                    # Types Validation
                    self.type_validation(schema, value, column)
            self.row_counter += 1       
        
        if self.validate_rows_errors:
            raise Exception(f'{len(self.validate_rows_errors)} errors were found. Check validate_rows_errors attribute.')
        else:
            print('validateRows completed successfully.')
            return True