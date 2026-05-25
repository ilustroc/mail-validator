import re
from functools import lru_cache

import dns.resolver


EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email_format(email: str) -> bool:
    if not email:
        return False

    invalid_rules = (
        not EMAIL_PATTERN.match(email),
        ".." in email,
        ".@" in email,
        "@." in email,
        email.startswith("."),
        email.endswith("."),
        " " in email,
        email.count("@") != 1,
    )

    return not any(invalid_rules)


def validar_formato(email: str) -> bool:
    return validate_email_format(email)


def get_user(email: str) -> str:
    return email.split("@", 1)[0] if "@" in email else ""


def get_domain(email: str) -> str:
    return email.split("@", 1)[1] if "@" in email else ""


def obtener_dominio(email: str) -> str:
    return get_domain(email)


@lru_cache(maxsize=1024)
def has_mx_record(domain: str) -> bool:
    if not domain:
        return False

    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 3

    try:
        answers = resolver.resolve(domain, "MX")
        return len(answers) > 0
    except Exception:
        return False
