from raga.validators.dataset_creds_validations import DatasetCredsValidator
from raga.utils import HTTPClient

class DatasetCreds:
    def __init__(self, type: str, location: str):
        self.type = DatasetCredsValidator.validate_type(type)
        self.location = DatasetCredsValidator.validate_location(location)
        # self.reference_id = DatasetCredsValidator.validate_reference_id(reference_id)
        # self.http_client = HTTPClient("https://api.example.com")