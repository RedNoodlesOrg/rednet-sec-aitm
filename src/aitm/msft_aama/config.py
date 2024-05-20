from __future__ import annotations

BASE_URL = "https://account.activedirectory.windowsazure.com"

INITIALIZE_MOBILE_APP_URL = f"{BASE_URL}/securityinfo/InitializeMobileAppRegistration"
ADD_SECURITY_INFO_URL = f"{BASE_URL}/securityinfo/AddSecurityInfo"
VERIFY_SECURITY_INFO_URL = f"{BASE_URL}/securityinfo/VerifySecurityInfo"

HEADERS = {
    "Host": "account.activedirectory.windowsazure.com",
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
