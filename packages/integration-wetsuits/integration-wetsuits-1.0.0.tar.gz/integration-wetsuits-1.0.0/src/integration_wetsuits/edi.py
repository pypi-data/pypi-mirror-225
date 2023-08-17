"""EDI Helpers"""
import re
from validx import exc, Validator

from .edi_dict import edifact_regexes


class ValidationError(Exception):
    """Validation error class for EDI class"""


class Edi:
    """EDI Helper class"""

    edifact_regexes = edifact_regexes

    def __init__(self, message):
        self.decripted_message = {"header": {}, "lines": []}
        self.message = message

    def __parse_header(self, keys: list = None):
        if keys is None:
            keys = []
        for key, value in self.edifact_regexes["header"].items():
            if not keys or key in keys:
                column_match = re.findall(value["pattern"], self.message)
                if len(column_match) > 0:
                    self.decripted_message["header"][key] = column_match[0]

    def __parse_lines(self, keys: list = None):
        if keys is None:
            keys = []

        # Removes headers from message
        message = re.sub(r"(?s)^(?!LIN)(.*?)(?=LIN|\Z)", "", self.message)
        matches = re.finditer(r"(.*?)(?=LIN|\Z)", message, re.MULTILINE)
        for match in matches:
            line_object = {}
            for key, value in self.edifact_regexes["lines"].items():
                if not keys or key in keys:
                    if column_match := re.findall(value["pattern"], match.group(0)):
                        line_object[key] = column_match[0]
            if line_object:
                self.decripted_message["lines"].append(line_object)

    def __generate_validator(self, header_keys: list = None, line_keys: list = None):
        """Creates validator object used for Validx"""
        header_schema = {
            hkey: hvalue["validator"]
            for hkey, hvalue in self.edifact_regexes["header"].items()
            if not header_keys or hkey in header_keys
        }

        line_schema = {
            lkey: lvalue["validator"]
            for lkey, lvalue in self.edifact_regexes["lines"].items()
            if not line_keys or lkey in line_keys
        }

        return {
            "__class__": "Dict",
            "schema": {
                "header": {"__class__": "Dict", "schema": header_schema},
                "lines": {
                    "__class__": "List",
                    "item": {"__class__": "Dict", "schema": line_schema},
                },
            },
        }

    def __validate_results(self, validator_json: dict = None):
        """Validate output edi message"""
        if validator_json is None:
            validator_json = {}

        errors = []
        search_params = Validator.load(validator_json)
        try:
            search_params(self.decripted_message)
        except exc.ValidationError as err:
            err.sort()
            errors.extend(iter(err))
        if errors:
            raise ValidationError(
                "Parsed EDI message does not pass validation, check original message.",
                errors,
            )

    def parse_all(self):
        """Parses EDI messages"""
        self.__parse_header()
        self.__parse_lines()
        self.__validate_results(self.__generate_validator())
        return self.decripted_message

    def parse_specific(self, header_keys: list = None, line_keys: list = None):
        """Parses EDI messages"""
        self.__parse_header(header_keys)
        self.__parse_lines(line_keys)
        self.__validate_results(self.__generate_validator(header_keys, line_keys))
        return self.decripted_message
