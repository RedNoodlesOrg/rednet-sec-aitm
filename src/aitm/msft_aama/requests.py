from __future__ import annotations

import json

from requests import Response, request
from requests_oauthlib import OAuth2Session

from .config import HEADERS


class PostRequest():
    """
    Represents a POST request.

    Attributes:
        headers (list): A list of dictionaries representing the headers for the request.
        method (str): The HTTP method for the request.
    """

    headers = HEADERS | {
        "Content-Type": "application/json",
        "x-rff": "pwdMngMsi,pKoe,myAccSi,dchPwdLnk,fsnAcks,iamuxfb,cepcr,ebtta,otebvpf",
        "AjaxRequest": "true",
        "Priority": "u=1",
    }

    def send(self, session: OAuth2Session, url: str, data: dict | None = None, sessionCtx: str | None = None) -> Response:
        """
        Sends the request using the provided session.

        Args:
            session (Session): The session to use for sending the request.
            url (str): The URL to send the request to.
            data (dict | None, optional): The data to include in the request body. Defaults to None.

        Returns:
            Response: The response object.

        """
        if data is None:
            data = {}
        if sessionCtx:
            self.headers["SessionCtx"] = sessionCtx
        self.headers["Authorization"] = f"Bearer {session.token["access_token"]}"
        return request("POST", url, headers=self.headers, data=json.dumps(data), cookies=session.cookies)
