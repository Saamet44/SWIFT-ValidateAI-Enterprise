from decimal import Decimal, InvalidOperation
import re


REQUIRED_FIELDS = (
    "TransactionReference",
    "Amount",
    "Currency",
    "SenderBIC",
    "ReceiverBIC",
)

BIC_RE = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")


def validate_message(message):
    errors = []

    if not isinstance(message, dict):
        return {"status": "Invalid", "errors": ["Message body must be a JSON object."]}

    for field in REQUIRED_FIELDS:
        if not message.get(field):
            errors.append(f"Missing {field}.")

    amount = message.get("Amount")
    if amount is not None:
        _validate_amount(amount, errors)

    currency = message.get("Currency")
    if currency and not CURRENCY_RE.fullmatch(str(currency)):
        errors.append("Currency must be a three-letter ISO code such as USD or EUR.")

    for field in ("SenderBIC", "ReceiverBIC"):
        value = message.get(field)
        if value and not BIC_RE.fullmatch(str(value)):
            errors.append(f"{field} must be a valid 8 or 11 character BIC.")

    return {
        "status": "Valid" if not errors else "Invalid",
        "errors": errors,
    }


def _validate_amount(amount, errors):
    normalized = str(amount).replace(",", ".")

    try:
        parsed = Decimal(normalized)
    except (InvalidOperation, ValueError):
        errors.append("Amount must be numeric.")
        return

    if parsed <= 0:
        errors.append("Amount must be greater than zero.")
        return

    if parsed.as_tuple().exponent < -2:
        errors.append("Amount must not have more than two decimal places.")
