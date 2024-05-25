from __future__ import annotations

INITIALIZE_MOBILE_APP_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "RegistrationType": {"type": "number"},
        "QrCode": {"type": "string"},
        "ActivationCode": {},
        "SameDeviceUrl": {"type": "string"},
        "AccountName": {"type": "string"},
        "SecretKey": {"type": "string"},
    },
    "required": [
        "SecretKey",
    ],
}

ADD_SECURITY_INFO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "Type": {"type": "number"},
        "VerificationState": {"type": "number"},
        "VerificationContext": {"type": "string"},
        "ErrorCode": {"type": "number"},
    },
    "required": ["Type", "VerificationState", "VerificationContext", "ErrorCode"],
}

VERIFY_SECURITY_INFO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "Type": {"type": "number"},
        "VerificationState": {"type": "number"},
        "DataUpdates": {
            "type": "object",
            "properties": {"DefaultMethodOptions": {"type": "number"}, "DefaultMethod": {"type": "number"}},
            "required": ["DefaultMethodOptions", "DefaultMethod"],
        },
        "ErrorCode": {"type": "number"},
    },
    "required": ["Type", "VerificationState", "ErrorCode"],
}

AUTHORIZE_MOBILE_APP_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "isAuthorized": {"type": "boolean"},
        "requireMfa": {"type": "boolean"},
        "promptForLogin": {"type": "boolean"},
        "hasMfaClaim": {"type": "boolean"},
        "authContextTags": {"type": "array", "items": {}},
        "requiresProofUpCodeParam": {"type": "boolean"},
        "isMyStarEnabled": {"type": "boolean"},
        "requireNgcMfa": {"type": "boolean"},
        "sessionCtx": {"type": "string"},
    },
    "required": [
        "isAuthorized",
        "sessionCtx",
    ],
}
