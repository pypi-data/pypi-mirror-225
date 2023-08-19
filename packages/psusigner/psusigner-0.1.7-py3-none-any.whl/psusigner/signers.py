from endesive import pdf, signer

import datetime
import hashlib
import base64
import io


import requests
import jwt


from . import psuhsm
from . import psucms
from . import exception


class PSUSigner:
    def __init__(
        self,
        code,
        secret,
        agent_key,
        jwt_secret=None,
        api_url=None,
    ):
        self.jwt_secret = jwt_secret
        self.agent_key = agent_key
        self.code = code
        self.secret = secret
        self.api_url = api_url
        self.hsm = None

        if jwt_secret:
            self.hsm = psuhsm.JWTSecretPSUHSM(
                code=code,
                secret=secret,
                jwt_secret=jwt_secret,
                agent_key=agent_key,
                api_url=api_url,
            )
        else:
            self.hsm = psuhsm.SecretPSUHSM(
                code=code, secret=secret, agent_key=agent_key, api_url=api_url
            )

        # function stuff
        self.original_signer = signer.sign
        signer.sign = self.sign_cms
        self.logs_api_url = f"{self.api_url}/sign/logs"

    def sign_byte(self, datau, dct, **kwargs):
        self.hsm.set_sign_parameters(**kwargs)
        datas = psucms.sign(datau, dct, None, None, [], "sha256", self.hsm)

        output = io.BytesIO()

        output.write(datau)
        output.write(datas)
        output.seek(0)

        return output

    def sign_file(self, input_name, dct, output_name, **kwargs):
        datau = b""
        with open(input_name, "rb") as fp:
            datau = fp.read()

        if not datau:
            raise exception.PSUSignException("No Input Data")

        self.hsm.set_sign_parameters(**kwargs)
        datas = psucms.sign(datau, dct, None, None, [], "sha256", self.hsm)

        with open(output_name, "wb") as fp:
            fp.write(datau)
            fp.write(datas)

    def search(self, **kwargs):
        """
        https://ds-dev.psu.ac.th/api/v1/sign/logs?ref1=ref1&ref2=ref2&max=10&offset=0&sort=actionDateTime&order=desc

        params

        certEntryCode: c1
        ref1: ref1 (exact match)
        ref2: ref2 (partial match)
        fromActionDateTime: 2023-06-05T11:00:00 (must apply when filter by action datetime)
        toActionDateTime: 2023-06-05T12:00:00 (optional when filter by action datetime)
        max: 10 (maximum result)
        offset: 0 (result offset for pagination)
        sort: actionDateTime [id, ref1, ref2, actionDateTime]
        order: desc [asc, desc]
        """
        headers = {"X-Agent-Key": self.agent_key}
        response = requests.get(self.logs_api_url, headers=headers, params=kwargs)
        return response.json()

    def sign_cms(
        self,
        datau,
        key,
        cert,
        othercerts,
        hashalgo,
        attrs=True,
        signed_value=None,
        hsm=None,
        pss=False,
        timestampurl=None,
        timestampcredentials=None,
        timestamp_req_options=None,
        ocspurl=None,
        ocspissuer=None,
    ):
        # print(
        #     datau,
        #     key,
        #     cert,
        #     othercerts,
        #     hashalgo,
        #     attrs,
        #     signed_value,
        #     hsm,
        #     pss,
        #     timestampurl,
        #     timestampcredentials,
        #     timestamp_req_options,
        #     ocspurl,
        #     ocspissuer,
        # )

        if hsm and isinstance(hsm, psuhsm.PSUHSM):
            if signed_value is None:
                signed_value = getattr(hashlib, hashalgo)(datau).digest()

            return hsm.sign(None, signed_value, "HA256")

        return self.original_signer(
            datau,
            key,
            cert,
            othercerts,
            hashalgo,
            attrs,
            signed_value,
            hsm,
            pss,
            timestampurl,
            timestampcredentials,
            timestamp_req_options,
            ocspurl,
            ocspissuer,
        )
