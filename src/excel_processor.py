from pathlib import Path

import pandas as pd

from src.cleaners import clean_document, clean_email, normalize_column_name
from src.config import EXPECTED_COLUMNS, INPUT_PATH, MAX_EMAILS_PER_DOCUMENT, OUTPUT_PATH
from src.risk_rules import evaluate_email


def read_input_excel(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontro el archivo de entrada: {input_path}")

    dataframe = pd.read_excel(input_path, dtype=str)
    dataframe.columns = [normalize_column_name(column) for column in dataframe.columns]

    missing_columns = [column for column in EXPECTED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        raise ValueError(
            "Faltan columnas obligatorias: "
            f"{', '.join(missing_columns)}. Columnas encontradas: {list(dataframe.columns)}"
        )

    dataframe = dataframe[list(EXPECTED_COLUMNS)].copy()
    dataframe["DOCUMENTO"] = dataframe["DOCUMENTO"].apply(clean_document)
    dataframe["CORREO"] = dataframe["CORREO"].apply(clean_email)

    return dataframe[(dataframe["DOCUMENTO"] != "") & (dataframe["CORREO"] != "")]


def build_validation_dataframe(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for _, row in input_dataframe.iterrows():
        evaluation = evaluate_email(row["CORREO"])
        rows.append(
            {
                "DOCUMENTO": row["DOCUMENTO"],
                "CORREO_ORIGINAL": row["CORREO"],
                **evaluation,
            }
        )

    return pd.DataFrame(rows)


def build_grouped_valid_emails(
    validation_dataframe: pd.DataFrame,
    max_emails_per_document: int = MAX_EMAILS_PER_DOCUMENT,
) -> pd.DataFrame:
    columns = ["DOCUMENTO", *[f"CORREO {index}" for index in range(1, max_emails_per_document + 1)]]

    if validation_dataframe.empty:
        return pd.DataFrame(columns=columns)

    valid_emails = validation_dataframe[validation_dataframe["VALIDACION"] == "VALIDO"].copy()
    valid_emails = valid_emails.drop_duplicates(subset=["DOCUMENTO", "CORREO_LIMPIO"])

    grouped_rows = []
    for document, group in valid_emails.groupby("DOCUMENTO"):
        emails = group["CORREO_LIMPIO"].tolist()[:max_emails_per_document]
        grouped_rows.append(
            {
                "DOCUMENTO": document,
                **{
                    f"CORREO {index + 1}": emails[index] if index < len(emails) else ""
                    for index in range(max_emails_per_document)
                },
            }
        )

    return pd.DataFrame(grouped_rows, columns=columns)


def build_summary_dataframe(validation_dataframe: pd.DataFrame) -> pd.DataFrame:
    if validation_dataframe.empty:
        counters = {
            "Total procesados": 0,
            "Total validos": 0,
            "Total riesgo medio": 0,
            "Total alto riesgo": 0,
            "Total no validos": 0,
            "Total dominios sin MX": 0,
            "Total dominios temporales": 0,
            "Total dominios posiblemente mal escritos": 0,
        }
    else:
        counters = {
            "Total procesados": len(validation_dataframe),
            "Total validos": (validation_dataframe["VALIDACION"] == "VALIDO").sum(),
            "Total riesgo medio": (validation_dataframe["VALIDACION"] == "RIESGO MEDIO").sum(),
            "Total alto riesgo": (
                validation_dataframe["VALIDACION"] == "ALTO RIESGO DE REBOTE"
            ).sum(),
            "Total no validos": (validation_dataframe["VALIDACION"] == "NO VALIDO").sum(),
            "Total dominios sin MX": (
                (validation_dataframe["FORMATO_VALIDO"] == "SI")
                & (validation_dataframe["MX_VALIDO"] == "NO")
            ).sum(),
            "Total dominios temporales": (validation_dataframe["DOMINIO_TEMPORAL"] == "SI").sum(),
            "Total dominios posiblemente mal escritos": (
                validation_dataframe["DOMINIO_SUGERIDO"].fillna("") != ""
            ).sum(),
        }

    return pd.DataFrame(
        [{"INDICADOR": indicator, "VALOR": int(value)} for indicator, value in counters.items()]
    )


def write_output_excel(
    validation_dataframe: pd.DataFrame,
    grouped_dataframe: pd.DataFrame,
    summary_dataframe: pd.DataFrame,
    output_path: Path = OUTPUT_PATH,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        validation_dataframe.to_excel(writer, sheet_name="Validacion", index=False)
        grouped_dataframe.to_excel(writer, sheet_name="Correos_Agrupados", index=False)
        summary_dataframe.to_excel(writer, sheet_name="Resumen", index=False)


def process_excel(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> Path:
    input_dataframe = read_input_excel(input_path)
    validation_dataframe = build_validation_dataframe(input_dataframe)
    grouped_dataframe = build_grouped_valid_emails(validation_dataframe)
    summary_dataframe = build_summary_dataframe(validation_dataframe)

    write_output_excel(validation_dataframe, grouped_dataframe, summary_dataframe, output_path)
    return output_path
