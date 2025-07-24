class DynamicModelFetcher:
    """
    A utility for dynamically querying Django models based on structured payload input.

    I built this class to collect useful scripts I wrote during my work with Django REST Framework (DRF) projects, 
    especially for extracting serializer data more efficiently.

    Since I enjoy working low-level, I have a habit of writing custom utility methods to improve performance and structure.
    This class includes methods for querying over relational models based on a client-provided payload.

    The payload is a dictionary where each key represents a model name from your project. Each model key maps to another
    dictionary with two keys:
        - "instances": A list of primary key IDs to filter the model queryset.
        - "params": A list of field names to fetch from the related model (for FK, M2M, or O2O relationships).

    Example payload:
        {
            "inverter": {
                "instances": [1, 2],
                "params": ["i_current", "v_current"]  # Fields from the related model
            },
            "battery": {
                "instances": [5, 6, 7],
                "params": ["temperature", "voltage"]
            }
        }

    Different methods in this class handle different types of relationships (e.g. ForeignKey, ManyToMany, etc.),
    so the structure of the response may vary depending on which method is used.
    """
    DATA = {}

    def __init__(self, payload: dict, model_map: dict):
        self.payload = payload
        self.model_map = model_map

    def fetch_foreign_key(self, related_name: str) -> dict:
        for model_key, filter_data in self.payload.items():
            ModelKey = self.payload.get(model_key)
            if not ModelKey:
                # Skip if model not found
                continue

            # Extract primary keys and parameter names
            PKs = filter_data.get("instances", [])
            fields = filter_data.get("params", [])

            # Build list of related field values
            fields_values = [f"{related_name}__{field}" for field in fields]

            # Query and extract values from related model fields
            queryset = ModelKey.objects.filter(pk__in=PKs).values(*fields_values)

            DATA[model_key] = list(queryset)

        return DATA
