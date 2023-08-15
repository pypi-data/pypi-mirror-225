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
from imandra_http_api_client.models.eval_response import EvalResponse  # noqa: E501
from imandra_http_api_client.rest import ApiException

class TestEvalResponse(unittest.TestCase):
    """EvalResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test EvalResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `EvalResponse`
        """
        model = imandra_http_api_client.models.eval_response.EvalResponse()  # noqa: E501
        if include_optional :
            return EvalResponse(
                success = True, 
                stdout = '', 
                stderr = ''
            )
        else :
            return EvalResponse(
                success = True,
        )
        """

    def testEvalResponse(self):
        """Test EvalResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
