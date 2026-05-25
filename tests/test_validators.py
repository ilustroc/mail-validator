import unittest
from datetime import datetime

import pandas as pd

from src.cleaners import clean_document, clean_email
from src.excel_processor import build_summary_dataframe_with_totals
from src.risk_rules import (
    classify_score,
    detectar_dominio_parecido,
    detect_similar_domain,
    evaluate_email,
    is_suspicious_user,
    usuario_sospechoso,
)
from src.validators import get_domain, obtener_dominio, validar_formato, validate_email_format


class ValidatorTests(unittest.TestCase):
    def test_valid_email_format(self):
        self.assertTrue(validate_email_format("nombre.apellido@gmail.com"))

    def test_invalid_email_format(self):
        self.assertFalse(validate_email_format("nombre@@gmail..com"))

    def test_clean_document(self):
        self.assertEqual(clean_document("123.0"), "00000123")
        self.assertEqual(clean_document("12.345.678"), "12345678")
        self.assertEqual(clean_document(None), "")

    def test_clean_email(self):
        self.assertEqual(clean_email(" Cliente@GMAIL.COM "), "cliente@gmail.com")
        self.assertEqual(clean_email(None), "")

    def test_get_domain(self):
        self.assertEqual(get_domain("cliente@gmail.com"), "gmail.com")
        self.assertEqual(obtener_dominio("cliente@hotmail.com"), "hotmail.com")
        self.assertEqual(get_domain("correo-invalido"), "")

    def test_similar_domain(self):
        self.assertEqual(detect_similar_domain("gmial.com"), "gmail.com")
        self.assertEqual(detectar_dominio_parecido("hotnail.com"), "hotmail.com")

    def test_suspicious_user(self):
        self.assertTrue(is_suspicious_user("xxxx"))
        self.assertTrue(usuario_sospechoso("abc"))
        self.assertFalse(usuario_sospechoso("cliente.normal"))

    def test_spanish_format_alias(self):
        self.assertTrue(validar_formato("cliente@gmail.com"))
        self.assertFalse(validar_formato("cliente@gmail"))

    def test_risk_classification_by_score(self):
        self.assertEqual(classify_score(0), "VALIDO")
        self.assertEqual(classify_score(30), "RIESGO MEDIO")
        self.assertEqual(classify_score(70), "ALTO RIESGO DE REBOTE")

    def test_evaluate_valid_email_without_network(self):
        result = evaluate_email("cliente@gmail.com", mx_checker=lambda domain: True)

        self.assertEqual(result["VALIDACION"], "VALIDO")
        self.assertEqual(result["MX_VALIDO"], "SI")

    def test_evaluate_invalid_email(self):
        result = evaluate_email("cliente@@gmail.com", mx_checker=lambda domain: True)

        self.assertEqual(result["VALIDACION"], "NO VALIDO")
        self.assertEqual(result["PUNTAJE_RIESGO"], 100)

    def test_evaluate_medium_risk_email(self):
        result = evaluate_email("abc@gmail.com", mx_checker=lambda domain: True)

        self.assertEqual(result["VALIDACION"], "RIESGO MEDIO")
        self.assertEqual(result["USUARIO_SOSPECHOSO"], "SI")

    def test_evaluate_high_risk_email(self):
        result = evaluate_email("cliente@dominio-inexistente.test", mx_checker=lambda domain: False)

        self.assertEqual(result["VALIDACION"], "ALTO RIESGO DE REBOTE")
        self.assertEqual(result["MX_VALIDO"], "NO")

    def test_build_summary_dataframe(self):
        validation_dataframe = pd.DataFrame(
            [
                {
                    "VALIDACION": "VALIDO",
                    "FORMATO_VALIDO": "SI",
                    "MX_VALIDO": "SI",
                    "DOMINIO": "gmail.com",
                    "DOMINIO_TEMPORAL": "NO",
                    "DOMINIO_SUGERIDO": "",
                },
                {
                    "VALIDACION": "ALTO RIESGO DE REBOTE",
                    "FORMATO_VALIDO": "SI",
                    "MX_VALIDO": "NO",
                    "DOMINIO": "gmial.com",
                    "DOMINIO_TEMPORAL": "NO",
                    "DOMINIO_SUGERIDO": "gmail.com",
                },
                {
                    "VALIDACION": "NO VALIDO",
                    "FORMATO_VALIDO": "NO",
                    "MX_VALIDO": "NO",
                    "DOMINIO": "",
                    "DOMINIO_TEMPORAL": "NO",
                    "DOMINIO_SUGERIDO": "",
                },
            ]
        )

        summary = build_summary_dataframe_with_totals(
            validation_dataframe,
            total_records_read=4,
            processed_at=datetime(2026, 5, 25, 15, 0, 0),
        )
        values = dict(zip(summary["INDICADOR"], summary["VALOR"]))

        self.assertEqual(values["Total de registros leidos"], 4)
        self.assertEqual(values["Total de registros procesados"], 3)
        self.assertEqual(values["Total de correos validos"], 1)
        self.assertEqual(values["Total alto riesgo de rebote"], 1)
        self.assertEqual(values["Total no validos"], 1)
        self.assertEqual(values["Total dominios unicos"], 2)
        self.assertEqual(values["Total dominios sin MX"], 1)
        self.assertEqual(values["Total dominios posiblemente mal escritos"], 1)
        self.assertEqual(values["Fecha y hora de procesamiento"], "2026-05-25 15:00:00")


if __name__ == "__main__":
    unittest.main()
