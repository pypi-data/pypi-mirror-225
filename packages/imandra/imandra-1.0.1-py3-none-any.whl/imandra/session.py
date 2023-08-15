from . import auth, instance 
import imandra_http_api_client

class HttpInstanceSession:
    def __init__(self):
        self.auth = auth.Auth()
        self.instance_ = instance.create(self.auth, None, "imandra-http-api")

        config = imandra_http_api_client.Configuration(
            host = self.instance_['new_pod']['url'],
            access_token = self.instance_['new_pod']['exchange_token'],
        )

        self.api_client = imandra_http_api_client.ApiClient(config)
        self.api_instance = imandra_http_api_client.DefaultApi(self.api_client)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        instance.delete(self.auth, self.instance_['new_pod']['id'])

    def eval(self, src):
        eval_request_src = imandra_http_api_client.EvalRequestSrc(src=src)
        return self.api_instance.eval(eval_request_src)

    def verify(self, src):
        verify_request_src = imandra_http_api_client.VerifyRequestSrc(src=src)
        return self.api_instance.verify_by_src(verify_request_src)

    def instance(self, src):
        instance_request_src = imandra_http_api_client.InstanceRequestSrc(src=src)
        return self.api_instance.instance_by_src(instance_request_src)

    def decompose(self, name):
        decompose_request = imandra_http_api_client.DecomposeRequestSrc(name=name)
        return self.api_instance.decompose(decompose_request)
        