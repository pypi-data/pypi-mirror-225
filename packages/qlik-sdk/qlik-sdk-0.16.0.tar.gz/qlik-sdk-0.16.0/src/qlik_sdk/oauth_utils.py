import base64
import hashlib
import os
import random
import re
import string
from typing import Dict, List
from urllib.parse import urlencode

from .config import Config


def _generate_code_verifier() -> str:
    """
    method for generating random alphanumeric string, only to be used in the PKCE flow
    """
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
    return code_verifier


def _generate_code_challenge() -> List[str]:
    """
    Create a code challenge
    returns [code_challenge, code_verifier]
    """
    code_verifier = _generate_code_verifier()
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")
    return code_challenge, code_verifier


def _generate_authorization_url(
    config: Config, state: str = None, code_challenge: bool = False
) -> Dict[str, str]:
    if state is None:
        state = _generate_random_string(7)

    authorize_path = f"{config.host.strip('/')}/oauth/authorize"
    query_params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_url,
        "scope": " ".join(config.scope),
        "state": state,
    }
    code_verifier = None
    if code_challenge is True:
        code_challenge, code_verifier = _generate_code_challenge()
        query_params["code_challenge"] = code_challenge
        query_params["code_challenge_method"] = "S256"

    url = authorize_path + "?" + urlencode(query_params)
    return {"url": url, "code_verifier": code_verifier, "state": state}


def _generate_random_string(string_length: int = 7):
    return "".join(
        random.choices(string.ascii_lowercase + string.digits, k=string_length)
    )
