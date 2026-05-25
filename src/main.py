import argparse
import sys
from pathlib import Path


if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import INPUT_PATH, OUTPUT_PATH
from src.excel_processor import process_excel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida correos desde un archivo Excel.")
    parser.add_argument("--input", type=Path, default=INPUT_PATH, help="Ruta del Excel de entrada.")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH, help="Ruta del Excel de salida.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        output_path = process_excel(args.input, args.output)
    except (FileNotFoundError, ValueError) as error:
        print(error)
        return 1

    print("Proceso terminado correctamente.")
    print(f"Archivo generado: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
