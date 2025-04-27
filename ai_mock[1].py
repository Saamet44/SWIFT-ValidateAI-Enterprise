def validate_message(message):
    if "TransactionReference" not in message:
        return {"error": "Missing TransactionReference"}
    if "Amount" not in message:
        return {"error": "Missing Amount"}
    return {"status": "Valid"}