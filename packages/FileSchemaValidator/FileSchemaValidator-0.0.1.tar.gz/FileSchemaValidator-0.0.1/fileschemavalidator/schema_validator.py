

class SchemaValidator():
    """
    Base class for schema validation.
    """

    def __init__(self, schemafile):
        """
        Initializes the SchemaValidator class.

        Args:
            schemafile (list): List of dictionaries representing column schema.
        """
        self.schemafile = schemafile
    
    @property
    def schemafile(self):
        """
        Accessor for the schema list.

        Returns:
            list: List of dictionaries representing column schema.
        """
        return self._schemafile

    @schemafile.setter
    def schemafile(self, schema):
        """
        Sets the schema list and validates its information.

        Args:
            schema (list): List of dictionaries representing column schema.

        Raises:
            ValueError: If the schema is not a valid list or if schema information is invalid.
        """
        if not isinstance(schema, list):
            raise ValueError("Schema must be a list.")
        
        valid_types = ["int", "string", "float", "timestamp", "date", "boolean"]
        valid_modes = ["REQUIRED", "NULLABLE"]

        for column_info in schema:
            if not isinstance(column_info, dict):
                raise ValueError("Schema must be a list of dictionaries.")
            if "name" not in column_info or "type" not in column_info or "mode" not in column_info:
                raise ValueError("Schema must contain 'name', 'type', and 'mode' keys for each column.")
            if column_info["mode"] not in valid_modes:
                raise ValueError("Invalid mode value in schema. Use 'REQUIRED' or 'OPTIONAL'.")
            if column_info["type"] not in valid_types:
                raise ValueError(f"Invalid data type in schema. Use {','.join(valid_types)}")
    
        self._schemafile = schema