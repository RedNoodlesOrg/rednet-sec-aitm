from __future__ import annotations

import json

from requests import Request, Response, Session


class _BaseRequest:
    """
    Represents a base request object.

    Attributes:
        headers (list[SupportsKeysAndGetItem[str, str | bytes]]): The headers for the request.
        method (str): The HTTP method for the request.
    """

    headers: list[dict[str, str]]
    method: str

    def send(self, session: Session, url: str, data: dict | None = None) -> Response:
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
        prepared = session.prepare_request(Request(self.method, url, headers=self.headers, data=json.dumps(data)))
        return session.send(prepared)


class PostRequest(_BaseRequest):
    """
    Represents a POST request.

    Attributes:
        headers (list): A list of dictionaries representing the headers for the request.
        method (str): The HTTP method for the request.
    """

    headers = {
        "Content-Type": "application/json",
        "x-rff": "pwdMngMsi,pKoe,myAccSi,dchPwdLnk,fsnAcks,iamuxfb,cepcr,ebtta,otebvpf",
        "AjaxRequest": "true",
        "Priority": "u=1",
    }
    method = "POST"


class OptionsRequest(_BaseRequest):
    """
    Represents an HTTP OPTIONS request.

    This class is used to send an OPTIONS request to a server. It inherits from the _BaseRequest class.

    Attributes:
        headers (list): A list of dictionaries representing the headers of the request.
        method (str): The HTTP method of the request.

    Example:
        options_request = OptionsRequest()
        options_request.send()
    """

    headers = {
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "ajaxrequest,authorization,content-type,sessionctx,x-rff",
        "Priority": "u=4",
    }
    method = "OPTIONS"
