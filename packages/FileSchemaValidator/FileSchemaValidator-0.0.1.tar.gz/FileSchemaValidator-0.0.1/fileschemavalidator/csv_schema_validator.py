from schema_validator import SchemaValidator
from datetime import datetime
import csv


class CsvSchemaValidator(SchemaValidator):
    """
    Class for CSV schema validation.
    """
    DATE_FORMAT = '%Y-%m-%d'
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, schemafile, csv_reader) -> None:
        """
        Initializes the CsvSchemaValidator class.

        Args:
            schemafile (list): List of dictionaries representing column schema.
            csv_reader (csv.DictReader): Instance of the CSV reader.
        """
        super().__init__(schemafile)
        self.reader = csv_reader
        self.values = [row for row in self.reader]

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
        """
        for c in self.schemafile:
            if c.get("name") not in self.reader.fieldnames:
                raise Exception(f'{c.get("name")} column is required but was not found.')
            else:
                print('validateColumns completed successfully.')
                return True

    def validate_rows(self):
        """
        Validates the data in the CSV rows according to the schema.

        Raises:
            ValueError: If row data does not comply with the schema.
        """
        for row in self.values:
            for column in list(row.keys()):
                schema = [schema for schema in self.schemafile if schema['name'] == column][0]
                data_type = schema.get('type')
                value = row.get(column)
                # Mode
                if schema['mode'] == 'REQUIRED':
                    if not row[column]:
                        raise Exception(f'{column} Cant be null')
                # Types
                try:
                    if data_type == 'int':
                        int(value)
                    elif data_type == 'float':
                        float(value)
                    elif data_type == 'string':
                        str(value)
                    elif data_type == 'date':
                        datetime.strptime(value, self.DATE_FORMAT)
                    elif data_type == 'timestamp':
                        datetime.strptime(value, self.TIMESTAMP_FORMAT)
                    elif data_type == 'boolean':
                        if value not in ('True', 'False', True, False):
                            raise ValueError('Boolean field must be True or False.')
                except Exception as e:
                    raise ValueError(f'Error in column "{column}": {str(e)}')                 
        
        print('validateRows completed successfully.')
        return True