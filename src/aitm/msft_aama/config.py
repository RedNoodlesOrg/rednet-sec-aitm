from __future__ import annotations

BASE_URL = "https://account.activedirectory.windowsazure.com"

INITIALIZE_MOBILE_APP_URL = f"{BASE_URL}/securityinfo/InitializeMobileAppRegistration"
ADD_SECURITY_INFO_URL = f"{BASE_URL}/securityinfo/AddSecurityInfo"
VERIFY_SECURITY_INFO_URL = f"{BASE_URL}/securityinfo/VerifySecurityInfo"
AUTHORIZE_MOBILE_APP_URL = f"{BASE_URL}/securityinfo/Authorize"

AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
CLIENT_ID = "19db86c3-b2b9-44cc-b339-36da233a3be2"
REDIRECT_URI = "https://mysignins.microsoft.com"
TENANT_TOKEN_URL = "https://login.microsoftonline.com/{tid}/oauth2/v2.0/token"

HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://mysignins.microsoft.com/",
    "Origin": "https://mysignins.microsoft.com",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}

AUTH_SCOPES = [
    "openid",
    "profile",
    "email",
]

ACCESS_SCOPES = [
    "https://webshell.suite.office.com/.default openid",
    "19db86c3-b2b9-44cc-b339-36da233a3be2/.default openid",
    "https://graph.microsoft.com/.default openid",
    "0000000c-0000-0000-c000-000000000000/.default openid",
]
