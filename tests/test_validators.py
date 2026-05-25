import unittest

from src.cleaners import clean_document
from src.risk_rules import detect_similar_domain, evaluate_email, is_suspicious_user
from src.validators import validate_email_format


class ValidatorTests(unittest.TestCase):
    def test_valid_email_format(self):
        self.assertTrue(validate_email_format("nombre.apellido@gmail.com"))

    def test_invalid_email_format(self):
        self.assertFalse(validate_email_format("nombre@@gmail..com"))

    def test_clean_document(self):
        self.assertEqual(clean_document("123.0"), "00000123")
        self.assertEqual(clean_document("12.345.678"), "12345678")

    def test_similar_domain(self):
        self.assertEqual(detect_similar_domain("gmial.com"), "gmail.com")

    def test_suspicious_user(self):
        self.assertTrue(is_suspicious_user("xxxx"))

    def test_evaluate_valid_email_without_network(self):
        result = evaluate_email("cliente@gmail.com", mx_checker=lambda domain: True)

        self.assertEqual(result["VALIDACION"], "VALIDO")
        self.assertEqual(result["MX_VALIDO"], "SI")


if __name__ == "__main__":
    unittest.main()
