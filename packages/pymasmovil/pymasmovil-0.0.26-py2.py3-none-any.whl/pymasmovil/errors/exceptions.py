class MissingLoginCredentialsError(Exception):
    """Raised when login credentials are missing"""

    message = """
    Autenthication failed.
    The required configuration setting {} was not found in your environment.
    To authenticate follow the instructions explained in the README:
    https://gitlab.com/coopdevs/pymasmovil#login
    """

    def __init__(self, missing_credential):
        self.message = self.message.format(missing_credential)
        super().__init__(self.message)


class AutenthicationError(Exception):
    """Raised when login to MM API failed"""

    message = """
    Autenthication to MM API failed. We may be using wrong login
    credentials or because there is a problem in the MM server side.
    """

    def __init__(self):
        super().__init__(self.message)


class AccountRequiredParamsError(Exception):
    """Raised when trying to create an account without some required paramether"""

    message = "Missing or empty attributes required to create an account: {}"

    def __init__(self, missing_argument_list):
        self.message = self.message.format(", ".join(missing_argument_list))
        super().__init__(self.message)


class NewLineRequestRequiredParamsError(Exception):
    """Exception raised when some compulsary attributes for the portability process
    are missing in the OTRS request."""

    message = "Missing or empty attributes required for the requested {}: {}"

    def __init__(self, is_portability, missing_argument_list):
        request_type = (
            "portability" if is_portability else "new phone number registration"
        )

        self.message = self.message.format(
            request_type, ", ".join(missing_argument_list)
        )
        super().__init__(self.message)


class OrderItemNotFoundByICC(Exception):
    """Raised when no OrderItem is found with the given ICC"""

    message = "No order item with ICC: {} can be found in the account with id: {}"

    def __init__(self, ICC, account_id):
        self.message = self.message.format(ICC, account_id)
        super().__init__(self.message)


class OrderItemNotFoundByPhone(Exception):
    """Raised when no OrderItem is found with the given ICC"""

    message = "No order item with phone: {} can be found in the account with id: {}"

    def __init__(self, phone, account_id):
        self.message = self.message.format(phone, account_id)
        super().__init__(self.message)


class InvalidTargetConsumption(Exception):
    """Raised when the consumption limit to apply to a shared bond is not available"""

    message = (
        "Consumption limit {} cannot be applied.\n"
        "Please see available values: [10, 25, 50, 75, 100]"
    )

    def __init__(self, input_value):
        self.message = self.message.format(input_value)
        super().__init__(self.message)


class WrongFormattedDate(Exception):
    """Raised when input string dates are not formatted in the expected date format"""

    message = "Date {} with unrecognizable format. Expected format is {}"

    def __init__(self, str_date, expected_format):
        self.message = self.message.format(str_date, expected_format)
        super().__init__(self.message)


class UnknownMMError(Exception):
    """Raised when the MM API returns an error with an unknown structure"""

    def __init__(self, MM_response_body):
        self.message = MM_response_body
        super().__init__(self.message)
