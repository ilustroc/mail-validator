from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "input" / "correos.xlsx"
OUTPUT_PATH = BASE_DIR / "data" / "output" / "resultado_validacion_correos.xlsx"

EXPECTED_COLUMNS = ("DOCUMENTO", "CORREO")
MAX_EMAILS_PER_DOCUMENT = 4

KNOWN_DOMAINS = (
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com",
    "icloud.com",
    "live.com",
    "msn.com",
    "protonmail.com",
)

TEMPORARY_DOMAINS = (
    "tempmail.com",
    "10minutemail.com",
    "guerrillamail.com",
    "mailinator.com",
    "yopmail.com",
    "trashmail.com",
)

GENERIC_ACCOUNTS = (
    "info",
    "ventas",
    "soporte",
    "contacto",
    "admin",
    "administracion",
    "facturacion",
    "cobranzas",
    "atencionalcliente",
)
