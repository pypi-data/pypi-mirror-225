import os
import click
import requests
import json
import time
import threading
from logging import getLogger

from configparser import ConfigParser
from requests.auth import AuthBase
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

from sumatra_client.config import CONFIG, _CONFIG_PATH, urljoin

logger = getLogger("sumatra.auth")

AUTH_REDIRECT_PORTS = [20005, 20015, 20025]


class TokenNotFoundException(Exception):
    def __str__(self) -> str:
        return "No valid auth token. Run `sumatra login` first."


class TokenExpiredException(Exception):
    def __str__(self) -> str:
        return "Your auth token has expired. Run `sumatra login` to refresh."


class CognitoJwtAuth(AuthBase):
    """Authorization: JWT_TOKEN"""

    def __init__(self, tenant):
        self._jwt_token = CONFIG.jwt_token
        self._tenant = tenant

    def __eq__(self, other):
        return self._jwt_token == other._jwt_token

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        if not self._jwt_token:
            auth = CognitoAuth()
            self._jwt_token = auth.get_or_refresh_token()
        r.headers["Authorization"] = self._jwt_token
        if "x-sumatra-tenant" not in r.headers:
            r.headers["x-sumatra-tenant"] = self._tenant
        return r


class SDKKeyAuth(AuthBase):
    """x-api-key: SDK_KEY"""

    def __init__(self):
        self._sdk_key = CONFIG.sdk_key

    def __eq__(self, other):
        return self._sdk_key == other._sdk_key

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["x-api-key"] = self._sdk_key
        return r


class CallbackServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.debug(format % args)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", self.server._origin)
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')
        self.end_headers()

    def do_POST(self):
        l = int(self.headers.get("Content-Length", 0))
        response_json = json.loads(self.rfile.read(l))
        if "error" in response_json:
            raise RuntimeError(response_json.get("error"))

        refresh_token = response_json.get("refreshToken")
        id_token = response_json.get("idToken")
        access_token = response_json.get("accessToken")
        if not (refresh_token and id_token and access_token):
            logger.debug(f"Invalid request body {json.dumps(response_json)}")
            raise RuntimeError("Invalid request body from server during authentication")
        self.server.refresh_token = refresh_token
        self.server.id_token = id_token
        self.server.access_token = access_token
        self.server.expires_at = response_json.get("expiration")

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", self.server._origin)
        self.end_headers()
        self.wfile.flush()
        threading.Thread(target=self.server.shutdown, daemon=True).start()


class CallbackServer(HTTPServer):
    def __init__(self, *args, origin=None, **kwargs):
        # Because HTTPServer is an old-style class, super() can't be used.
        HTTPServer.__init__(self, *args, **kwargs)
        self.refresh_token = None
        self.id_token = None
        self.access_token = None
        self.expires_at = None
        self._origin = origin


class CognitoAuth:
    def __init__(self):
        self._redirect_uri = None
        self._code_verifier = None
        self._response = {}

    def fetch_new_tokens(self) -> None:
        self._fetch_authorization_tokens()
        tokens = self._parse_token_response(self._response)
        self._save_tokens(tokens)

    def get_or_refresh_token(self) -> str:
        tokens = self._load_tokens()
        if time.time() > tokens["expiration"]:
            try:
                tokens = self._refresh_tokens(tokens["refresh"])
            except:
                raise TokenExpiredException
        return tokens["id"]

    def _load_tokens(self) -> dict:
        fname = CONFIG.jwt_tokens_path
        logger.info(f"Loading tokens from {fname}")
        tokfile = ConfigParser()
        tokfile.read(fname)
        try:
            tokens = dict(tokfile[CONFIG.instance])
            tokens["expiration"] = int(tokens["expiration"])
            assert tokens.get("id") and tokens.get("refresh")
            return tokens
        except Exception as e:
            logger
            raise TokenNotFoundException

    def _save_tokens(self, tokens: dict) -> None:
        fname = CONFIG.jwt_tokens_path
        logger.info(f"Saving tokens to {fname}")
        tokens = dict(tokens)
        tokens = {k: str(v) for k, v in tokens.items()}
        tokfile = ConfigParser()
        tokfile.read(fname)
        tokfile[CONFIG.instance] = tokens
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(
            os.open(fname, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600), "w"
        ) as f:
            tokfile.write(f)

    # refresh id/access tokens using previously fetched refresh token
    def _refresh_tokens(self, refresh_token) -> dict:
        logger.info("Attempting to refresh expired tokens.")
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CONFIG.user_pool_client_id,
            "scope": "email profile openid aws.cognito.signin.user.admin",
        }
        logger.debug(f"POSTing to {CONFIG.cognito_token_url}: {params}")
        response = requests.post(CONFIG.cognito_token_url, data=params)
        logger.debug(f"Received: {response}")
        new_tokens = self._parse_token_response(response.json())
        new_tokens["refresh"] = refresh_token
        self._save_tokens(new_tokens)
        return new_tokens

    # open browser and allow user to authenticate using selected cognito flow
    # and store returned auth code
    def _fetch_authorization_tokens(self):
        logger.info("Launching browser-based authentication.")
        if CONFIG.server_version.startswith("v1.2"):
            self._start_callback_listener_compat()
        else:
            self._download_certs()
            self._start_callback_listener()

        auth_url = self._build_auth_url()
        try:
            click.launch(auth_url)
            self._httpd.serve_forever(poll_interval=1)
        except:
            logger.exception("failed to handle request")
        finally:
            self._response = {
                "refresh_token": self._httpd.refresh_token,
                "id_token": self._httpd.id_token,
                "access_token": self._httpd.access_token,
                "expires_at": self._httpd.expires_at,
            }
            self._httpd.server_close()
            if not (self._httpd.refresh_token and self._httpd.id_token and self._httpd.access_token):
                raise RuntimeError("Callback server failed to receive access tokens")

    def _download_certs(self):
        logger.debug("Downloading local certificates")
        os.makedirs(os.path.join(_CONFIG_PATH, "certs"), exist_ok=True)
        response = requests.get(urljoin(CONFIG.lrd_certs_url, "privkey.pem"))
        with open(os.path.join(_CONFIG_PATH, "certs", "privkey.pem"), "w") as f:
            f.write(response.text)
        response = requests.get(urljoin(CONFIG.lrd_certs_url, "fullchain.pem"))
        with open(os.path.join(_CONFIG_PATH, "certs", "fullchain.pem"), "w") as f:
            f.write(response.text)

    def _build_auth_url(self):
        return f"{CONFIG.instance_url}/log-in-ext/{self._redirect_port}"

    def _start_callback_listener_compat(self):
        logger.debug("Using 1.2.0 compatible request handler")
        for port in AUTH_REDIRECT_PORTS:
            try:
                self._httpd = CallbackServer(
                    ("localhost", int(port)), CallbackServerHandler,
                    origin=CONFIG.instance_url
                )
                self._redirect_uri = f"http://localhost:{port}"
                self._redirect_port = port
                break
            except OSError as e:
                if e.errno == 48:
                    continue
                else:
                    raise OSError(f"error during authentication: {e}")
        else:
            raise

    def _start_callback_listener(self):
        for port in AUTH_REDIRECT_PORTS:
            try:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                certfile = os.path.join(
                    _CONFIG_PATH, "certs", "fullchain.pem"
                )
                keyfile = os.path.join(
                    _CONFIG_PATH, "certs", "privkey.pem"
                )
                context.load_cert_chain(certfile, keyfile)
                self._httpd = CallbackServer(
                    ("l0.lrd.sumatra.ai", int(port)), CallbackServerHandler,
                    origin=CONFIG.instance_url
                )
                self._redirect_uri = f"http://l0.lrd.sumatra.ai:{port}"
                self._redirect_port = port
                self._httpd.socket = context.wrap_socket(
                    self._httpd.socket,
                    server_side=True,
                )
                break
            except OSError as e:
                if e.errno == 48:
                    continue
                else:
                    raise OSError(f"error during authentication: {e}")
        else:
            raise

    def _parse_token_response(self, response):
        now = int(time.time())
        expires_at = response.get("expires_at")
        expiration = now if not expires_at else int(expires_at)

        return {
            "access": response.get("access_token"),
            "id": response.get("id_token"),
            "refresh": response.get("refresh_token"),
            "expiration": expiration,
        }
