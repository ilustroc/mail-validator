class MailValidatorError(Exception):
    """Base exception for controlled application errors."""


class InputFileNotFoundError(MailValidatorError):
    """Raised when the input file does not exist."""


class MissingColumnsError(MailValidatorError):
    """Raised when required columns are missing from the input file."""


class EmptyExcelError(MailValidatorError):
    """Raised when the input Excel has no records to process."""


class ExcelReadError(MailValidatorError):
    """Raised when the input Excel cannot be read."""


class ExcelWriteError(MailValidatorError):
    """Raised when the output Excel cannot be written."""
