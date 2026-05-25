import argparse
import sys
import traceback
from pathlib import Path


if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import DEFAULT_SHEET, INPUT_PATH, MAX_EMAILS_PER_DOCUMENT, OUTPUT_PATH
from src.exceptions import MailValidatorError
from src.excel_processor import process_excel


def parse_sheet(value: str) -> int | str:
    return int(value) if value.isdigit() else value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida correos desde un archivo Excel.")
    parser.add_argument("--input", type=Path, default=INPUT_PATH, help="Ruta del Excel de entrada.")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH, help="Ruta del Excel de salida.")
    parser.add_argument(
        "--max-correos",
        type=int,
        default=MAX_EMAILS_PER_DOCUMENT,
        help="Maximo de correos validos agrupados por documento.",
    )
    parser.add_argument(
        "--sheet",
        type=parse_sheet,
        default=DEFAULT_SHEET,
        help="Hoja de entrada. Puede ser indice numerico o nombre de hoja.",
    )
    parser.add_argument("--verbose", action="store_true", help="Muestra mas detalles del proceso.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.max_correos <= 0:
        print("Error: --max-correos debe ser mayor que cero.")
        return 1

    try:
        result = process_excel(
            input_path=args.input,
            output_path=args.output,
            max_emails_per_document=args.max_correos,
            sheet_name=args.sheet,
            logger=print,
        )
    except MailValidatorError as error:
        print(f"Error: {error}")
        if args.verbose:
            traceback.print_exc()
        return 1
    except Exception:
        print("Error inesperado durante el procesamiento.")
        if args.verbose:
            traceback.print_exc()
        return 1

    for warning in result.warnings:
        print(f"Advertencia: {warning}")

    if args.verbose:
        print(f"Total de registros leidos: {result.total_records_read}")
        print(f"Total de registros procesados: {result.total_records_processed}")
        print(f"Total de correos validos: {result.total_valid_emails}")

    print("Proceso terminado correctamente.")
    print(f"Archivo generado: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
