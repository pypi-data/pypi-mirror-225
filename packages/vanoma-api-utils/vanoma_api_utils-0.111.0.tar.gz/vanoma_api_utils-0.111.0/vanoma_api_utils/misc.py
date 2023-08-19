import os
import shortuuid  # type: ignore
from typing import Dict
from babel import numbers
from .constants import ERROR_CODE


def resolve_environment() -> str:
    return os.environ.get("ENVIRONMENT", "testing")


def resolve_debug() -> bool:
    return resolve_environment() != "production"


def create_api_error(error_code: ERROR_CODE, error_message: str) -> Dict[str, str]:
    return {"error_code": error_code.value, "error_message": error_message}


def get_shortuuid() -> str:
    return shortuuid.uuid()


def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1]


def format_currency(amount: float, currency: str, currency_digits: bool = False) -> str:
    return numbers.format_currency(
        amount, currency, "¤ #,###", currency_digits=currency_digits
    )


def resolve_vanoma_website_url(website: str, path: str) -> str:
    if website == "SHOP":
        domain = "vanoma.shop"
    elif website == "STORE":
        domain = "vanoma.store"
    elif website == "ADMIN":
        domain = "admin.vanoma.com"
    elif website == "SUPPLIER":
        domain = "supplier.vanoma.com"
    elif website == "INFLUENCER":
        domain = "influencer.vanoma.com"
    else:
        raise Exception(f"Unknown website: {website}")

    if resolve_environment() == "production":
        return f"https://{domain}{path}"

    return f"https://{resolve_environment()}.{domain}{path}"
