import json
import logging
import os
import time
from urllib.parse import urlparse
from urllib.parse import urlunparse

import requests
from jupyter_server.base.handlers import APIHandler
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from vdk.plugin.control_api_auth.auth_config import InMemAuthConfiguration
from vdk.plugin.control_api_auth.auth_request_values import AuthRequestValues
from vdk.plugin.control_api_auth.autorization_code_auth import generate_pkce_codes
from vdk.plugin.control_api_auth.base_auth import BaseAuth

log = logging.getLogger(__name__)


class OAuth2Handler(APIHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: do this properly using jupyter configuration
        # see https://jupyter-server.readthedocs.io/en/latest/operators/configuring-extensions.html
        # https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html
        self._authorization_url = os.environ.get("OAUTH2_AUTHORIZATION_URL")
        self._access_token_url = os.environ.get("OAUTH2_ACCESS_TOKEN_URL")
        self._client_id = os.environ.get("OAUTH2_CLIENT_ID", "")
        # No client secret. We use only native app workflow with PKCE (RFC 7636)

        # TODO: remove after debugging is finished
        self._authorization_url = (
            "https://console.cloud.vmware.com/csp/gateway/discovery"
        )
        self._access_token_url = (
            "https://console.cloud.vmware.com/csp/gateway/am/api/auth/authorize"
        )
        self._client_id = "r5FW5u5QVsbowS4kVaGtA0BZZc2xIk8hquf"

    @staticmethod
    def _fix_localhost(uri: str):
        parsed_uri = urlparse(uri)

        if parsed_uri.hostname == "localhost":
            netloc = parsed_uri.netloc.replace("localhost", "127.0.0.1")
            modified_uri = parsed_uri._replace(netloc=netloc, query="")
            return urlunparse(modified_uri)
        else:
            modified_uri = parsed_uri._replace(query="")
            return urlunparse(modified_uri)

    def get(self):
        # TODO: this is duplicating a lot of the code in vdk-control-api-auth
        # https://github.com/vmware/versatile-data-kit/tree/main/projects/vdk-plugins/vdk-control-api-auth
        # But that module is written with focus on CLI usage a bit making it harder to reuse
        # and it needs to be refactored first.

        redirect_uri = self.request.full_url()
        redirect_uri = self._fix_localhost(redirect_uri)
        log.info(f"redirect uri is {redirect_uri}")
        # redirect_uri = "http://127.0.0.1:8888/vdk-jupyterlab-extension/login"

        if self.get_argument("code", None):
            log.info("Authorization code received. Will generate access token using authorization code.")
            tokens = self._exchange_auth_code_for_access_token(redirect_uri)
            log.info(f"Got tokens data: {tokens}")  # TODO: remove this
            self._persist_tokens_data(tokens)

            initial_url = self.get_argument("state", "")
            if initial_url:
                log.info(f"Redirecting back to initial url {initial_url}")
                self.redirect(initial_url, permanent=True)
        else:
            full_authorization_url = self._prepare_authorization_code_request_url(
                redirect_uri
            )
            self.finish(full_authorization_url)

    def _persist_tokens_data(self, tokens):
        auth = BaseAuth(conf=InMemAuthConfiguration())
        auth.update_oauth2_authorization_url(self._access_token_url)
        auth.update_client_id(self._client_id)
        auth.update_access_token(tokens.get(AuthRequestValues.ACCESS_TOKEN_KEY.value))
        auth.update_access_token_expiration_time(
            time.time() + int(tokens[AuthRequestValues.EXPIRATION_TIME_KEY.value])
        )
        if AuthRequestValues.REFRESH_TOKEN_GRANT_TYPE in tokens:
            auth.update_refresh_token(
                tokens.get(AuthRequestValues.REFRESH_TOKEN_GRANT_TYPE)
            )

    def _prepare_authorization_code_request_url(self, redirect_uri):
        (code_verifier, code_challenge, code_challenge_method) = generate_pkce_codes()
        self.application.settings["code_verifier"] = code_verifier
        oauth = OAuth2Session(client_id=self._client_id, redirect_uri=redirect_uri)
        full_authorization_url = oauth.authorization_url(
            self._authorization_url,
            state=self.get_argument("initial_url", ""),
            prompt=AuthRequestValues.LOGIN_PROMPT.value,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
        )[0]
        return full_authorization_url

    def _exchange_auth_code_for_access_token(self, redirect_uri) -> dict:
        code = self.get_argument("code")
        headers = {
            AuthRequestValues.CONTENT_TYPE_HEADER.value: AuthRequestValues.CONTENT_TYPE_URLENCODED.value,
        }
        code_verifier = self.application.settings["code_verifier"]

        data = (
                f"code={code}&"
                + f"grant_type=authorization_code&"
                + f"code_verifier={code_verifier}&"
                  f"redirect_uri={redirect_uri}"
        )
        basic_auth = HTTPBasicAuth(self._client_id, "")
        try:
            # TODO : this should be async io
            response = requests.post(
                self._access_token_url, data=data, headers=headers, auth=basic_auth
            )
            if response.status_code >= 400:
                log.error(
                    f"Request to {self._access_token_url} with data {data} returned {response.status_code}\n"
                    rf"Reason: {response.reason}\dn"
                    f"Response content: {response.content}\n"
                    f"Response headers: {response.headers}"
                )

            json_data = json.loads(response.text)
            return json_data
        except Exception as e:
            log.exception(e)
