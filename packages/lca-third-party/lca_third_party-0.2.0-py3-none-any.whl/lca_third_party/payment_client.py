

def _validate_account_name(**kwargs):
    if not isinstance(kwargs.get("account_name"), str):
        return "'account_name' must be string"


def _validate_recipient_id(**kwargs):
    if not isinstance(kwargs.get("recipient_id"), int):
        return "'recipient_id' must be integer"


def _validate_amount(**kwargs):
    if not isinstance(kwargs.get("amount"), int):
        return "'amount' must be integer"


class PaymentClient:
    def _validate(self, **data):
        validators = [
            _validate_account_name,
            _validate_recipient_id,
            _validate_amount
        ]
        errors = []
        for validator in validators:
            error = validator(**data)
            if error is not None:
                errors.append(error)
        return errors

    def pay(self, account_name: str, recipient_id: int, amount: int) -> bool:
        """
        Makes a payment and returns the flag indicating successful operation
        and validation errors, if it was not.
        """
        errors = self._validate(
            account_name=account_name,
            recipient_id=recipient_id,
            amount=amount
        )
        if errors:
            return False, errors

        print(f"Sending {amount}: {account_name} -> {recipient_id}")
        return True, []
