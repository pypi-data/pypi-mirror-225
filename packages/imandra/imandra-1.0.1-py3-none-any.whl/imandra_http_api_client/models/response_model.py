# coding: utf-8

"""
    imandra-http-server

    Query Imandra via HTTP. See also https://github.com/aestheticIntegration/bs-imandra-client for a sample client implementation and OCaml API types.  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr
from imandra_http_api_client.models.syntax import Syntax

class ResponseModel(BaseModel):
    """
    ResponseModel
    """
    syntax: Optional[Syntax] = None
    src: Optional[StrictStr] = Field(None, description="Source code string with a given syntax (default Iml)")
    __properties = ["syntax", "src"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ResponseModel:
        """Create an instance of ResponseModel from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ResponseModel:
        """Create an instance of ResponseModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ResponseModel.parse_obj(obj)

        _obj = ResponseModel.parse_obj({
            "syntax": obj.get("syntax"),
            "src": obj.get("src")
        })
        return _obj

