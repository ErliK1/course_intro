from rest_framework.exceptions import ValidationError


class ACIValidationError(ValidationError):
    def __init__(self, detail, code):
        super(ACIValidationError, self).__init__(detail, code)
