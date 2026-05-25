import re
from difflib import get_close_matches
from typing import Callable

from src.cleaners import clean_email
from src.config import GENERIC_ACCOUNTS, KNOWN_DOMAINS, TEMPORARY_DOMAINS
from src.validators import get_domain, get_user, has_mx_record, validate_email_format


MxChecker = Callable[[str], bool]


def detect_similar_domain(domain: str) -> str:
    matches = get_close_matches(domain, KNOWN_DOMAINS, n=1, cutoff=0.80)

    if matches and matches[0] != domain:
        return matches[0]

    return ""


def detectar_dominio_parecido(domain: str) -> str:
    return detect_similar_domain(domain)


def is_temporary_domain(domain: str) -> bool:
    return domain in TEMPORARY_DOMAINS


def is_generic_account(user: str) -> bool:
    normalized_user = re.sub(r"[^a-zA-Z]", "", user)
    return normalized_user in GENERIC_ACCOUNTS


def is_suspicious_user(user: str) -> bool:
    if len(user) <= 3:
        return True

    if re.search(r"(.)\1{3,}", user):
        return True

    letters_only = re.sub(r"[^a-zA-Z]", "", user)
    if len(letters_only) >= 5:
        vowels = len(re.findall(r"[aeiou]", letters_only))
        return vowels / len(letters_only) < 0.15

    return False


def usuario_sospechoso(user: str) -> bool:
    return is_suspicious_user(user)


def classify_score(score: int) -> str:
    if score >= 70:
        return "ALTO RIESGO DE REBOTE"

    if score >= 30:
        return "RIESGO MEDIO"

    return "VALIDO"


def evaluate_email(email: object, mx_checker: MxChecker = has_mx_record) -> dict[str, object]:
    clean = clean_email(email)

    if not validate_email_format(clean):
        return {
            "CORREO_LIMPIO": clean,
            "FORMATO_VALIDO": "NO",
            "USUARIO": "",
            "DOMINIO": "",
            "MX_VALIDO": "NO",
            "DOMINIO_TEMPORAL": "NO",
            "DOMINIO_SUGERIDO": "",
            "CUENTA_GENERICA": "NO",
            "USUARIO_SOSPECHOSO": "NO",
            "VALIDACION": "NO VALIDO",
            "PUNTAJE_RIESGO": 100,
            "MOTIVO": "Formato invalido",
        }

    user = get_user(clean)
    domain = get_domain(clean)
    reasons = []
    risk_score = 0

    mx_valid = mx_checker(domain)
    if not mx_valid:
        risk_score += 70
        reasons.append("Dominio sin servidor MX")

    suggested_domain = detect_similar_domain(domain)
    if suggested_domain:
        risk_score += 50
        reasons.append(f"Posible dominio mal escrito: quiza quiso decir {suggested_domain}")

    temporary_domain = is_temporary_domain(domain)
    if temporary_domain:
        risk_score += 60
        reasons.append("Dominio temporal o descartable")

    generic_account = is_generic_account(user)
    if generic_account:
        risk_score += 20
        reasons.append("Cuenta generica")

    suspicious_user = is_suspicious_user(user)
    if suspicious_user:
        risk_score += 30
        reasons.append("Usuario sospechoso o poco confiable")

    if not reasons:
        reasons.append("Formato correcto y dominio con MX")

    return {
        "CORREO_LIMPIO": clean,
        "FORMATO_VALIDO": "SI",
        "USUARIO": user,
        "DOMINIO": domain,
        "MX_VALIDO": "SI" if mx_valid else "NO",
        "DOMINIO_TEMPORAL": "SI" if temporary_domain else "NO",
        "DOMINIO_SUGERIDO": suggested_domain,
        "CUENTA_GENERICA": "SI" if generic_account else "NO",
        "USUARIO_SOSPECHOSO": "SI" if suspicious_user else "NO",
        "VALIDACION": classify_score(risk_score),
        "PUNTAJE_RIESGO": risk_score,
        "MOTIVO": " | ".join(reasons),
    }
