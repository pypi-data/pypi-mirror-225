# PSU Signer
Quick development for applying PSU digital signature using (Endensive)[https://github.com/m32/endesive].

## Documents
https://documenter.getpostman.com/view/644041/2s93eU1tyD

## Installation
```
pip install psusigner
```

## Example

```python
import datetime
from psusigner import PSUSigner


def main():
    fname = "file.pdf"
    date = datetime.datetime.utcnow()
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "sigflags": 3,
        "contact": "user@psu.ac.th",
        "location": "Hat Yai, Thailand",
        "signingdate": date.encode(),
        "reason": "Test",
        "attrs": False,
    }

    print("Secret Sign")
    signer = PSUSigner(
        code="c1",
        secret="",
        agent_key="",
        api_url="https://ds-dev.psu.ac.th/api/v1", # change it to use production url or remove it for using default api url
    )

    outname = fname.replace(".pdf", "-signed-cms-psuhsm.pdf")

    signer.sign_file(fname, dct, outname)

    print("JWT Sign")
    signer = PSUSigner(
        code="c1",
        secret="",
        agent_key="",
        jwt_secret="",
        api_url="https://ds-dev.psu.ac.th/api/v1",  # change it to use production url or remove it for using default api url

    )

    outname = fname.replace(".pdf", "-signed-cms-psuhsm-jwt.pdf")

    signer.sign_file(fname, dct, outname)

    search_response = signer.search(certEntryCode="c1")
    print("search output:", search_response)


main()
```
