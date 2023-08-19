import datetime
import jwt
import base64
import requests

from endesive import hsm, pdf, signer

from . import exception


class PSUHSM(hsm.BaseHSM):
    def __init__(self, code, secret, agent_key, api_url=None):
        self.api_url = "https://ds.psu.ac.th/api/v1"
        if api_url:
            self.api_url = api_url

        self.sign_api_url = f"{self.api_url}/sign/withPdfSignature"
        self.log_api_url = f"{self.api_url}/sign/logs"

        self.code = code
        self.secret = secret
        self.agent_key = agent_key
        self.sign_parameters = {}

    def set_sign_parameters(self, **kwargs):
        self.sign_parameters = kwargs

    def certificate(self):
        return None, None

    def get_headers(self):
        headers = {"X-Agent-Key": self.agent_key}

        return headers

    def get_payload(self, **kwargs):
        kwargs.update(self.sign_parameters)
        return kwargs

    def sign(self, keyid, data, mech):
        headers = self.get_headers()
        payload = self.get_payload(data)

        # print("headers:", headers)
        # print("payload:", payload)
        response = requests.post(
            self.sign_api_url,
            json=payload,
            headers=headers,
        )

        if response.status_code != 200:
            raise exception.PSUSignException(response.json())

        json_data = response.json()
        status_code = json_data.get("statusCode")
        if status_code != 1:
            raise exception.PSUSignException(response.json())

        sign_data = json_data.get("signData")

        return base64.b64decode(sign_data)


class SecretPSUHSM(PSUHSM):
    def __init__(self, code, secret, agent_key, api_url=None):
        super().__init__(code, secret, agent_key, api_url)

    def get_payload(self, signed_value):
        pdf_hash = base64.b64encode(signed_value)

        data = {"code": self.code, "secret": self.secret, "pdfHash": pdf_hash.decode()}

        data.update(self.sign_parameters)
        return data


class JWTSecretPSUHSM(SecretPSUHSM):
    def __init__(self, code, secret, agent_key, jwt_secret=None, api_url=None):
        super().__init__(code, secret, agent_key, api_url)
        self.jwt_secret = jwt_secret

    def get_payload(self, signed_value):
        data = super().get_payload(signed_value)
        # print("jwt data", data)
        encoded = jwt.encode(data, self.jwt_secret, algorithm="HS256")

        data = {"payload": encoded}

        return data
