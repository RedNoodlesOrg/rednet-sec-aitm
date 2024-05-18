from __future__ import annotations

import pyotp


class OTPGenerator:
    """
    A class that generates One-Time Passwords (OTP) using a secret key.

    Args:
        secret_key (str): The secret key used for generating OTPs.

    Attributes:
        secret_key (str): The secret key used for generating OTPs.
        totp (pyotp.TOTP): The TOTP object used for OTP generation.

    Methods:
        generate_otp: Generates a new OTP.

    """

    class OTPGenerator:
        def __init__(self, secret_key):
            """
            Initializes an OTPGenerator object.

            Args:
                secret_key (str): The secret key used for generating OTPs.

            """
            self.secret_key = secret_key
            self.totp = pyotp.TOTP(secret_key)

    def generate_otp(self):
        """
        Generates a new OTP.

        Returns:
            str: The generated OTP.

        """
        return self.totp.now()
