

class SchemaValidator():
    """
    Base class for schema validation.
    """

    def __init__(self, schemafile):
        """
        Initializes the SchemaValidator class.

        Args:
            schemafile (dict): Dictionary representing column schema.
        """
        self.schemafile = schemafile
        self.schema_errors = {}
    
    @property
    def schemafile(self):
        """
        Accessor for the schema dict.

        Returns:
            dict: Dictionary representing column schema.
        """
        return self._schemafile

    @schemafile.setter
    def schemafile(self, schema):
        """
        Sets the schema dictionary and validates its information.

        Args:
            schema (dict): Dictionary representing column schema.

        Raises:
            ValueError: If the schema is not a valid dictionary or if schema information is invalid.
        """
        if not isinstance(schema, dict):
            raise ValueError("Schema must be a dictionary.")
        
        valid_types = ["int", "string", "float", "timestamp", "date", "bool"]
        valid_modes = [0, 1]
        required_format = ['date', 'timestamp']

        for column_name, column_info in schema.items():
            if not isinstance(column_info, dict):
                raise ValueError(f"Column {column_name} must be a dictionary.")
            if "type" not in column_info or "is_required" not in column_info:
                raise ValueError(f"Column {column_name} must contain 'type' and 'is_required' keys.")
            if column_info["type"] not in valid_types:
                raise ValueError(f"Invalid data type in schema of Column {column_name}. Use True or False.")
            if column_info["is_required"] not in valid_modes:
                raise ValueError(f"Invalid 'is_required' value in schema of Column {column_name}. Use {','.join(valid_modes)}")
            if column_info["type"] in required_format and 'format' not in column_info:
                raise ValueError(f"Column of type {column_info['type']} must contain 'format' keys")
    
        self._schemafile = schema