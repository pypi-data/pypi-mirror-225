# coding: utf-8

"""
    imandra-http-server

    Query Imandra via HTTP. See also https://github.com/aestheticIntegration/bs-imandra-client for a sample client implementation and OCaml API types.  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import unittest
import datetime

import imandra_http_api_client
from imandra_http_api_client.models.response_error import ResponseError  # noqa: E501
from imandra_http_api_client.rest import ApiException

class TestResponseError(unittest.TestCase):
    """ResponseError unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ResponseError
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ResponseError`
        """
        model = imandra_http_api_client.models.response_error.ResponseError()  # noqa: E501
        if include_optional :
            return ResponseError(
                error = '', 
                stdout = '', 
                stderr = ''
            )
        else :
            return ResponseError(
                error = '',
        )
        """

    def testResponseError(self):
        """Test ResponseError"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
