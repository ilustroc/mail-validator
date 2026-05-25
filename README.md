# mail-validator

`mail-validator` es una herramienta en Python para limpiar, validar y clasificar correos electronicos desde un archivo Excel.

## Objetivo

Procesar una base con documentos y correos, detectar errores frecuentes, estimar riesgo de rebote y generar un Excel final con resultados detallados, resumen y correos validos agrupados por documento.

## Tecnologias usadas

- Python 3.10+
- pandas
- openpyxl
- dnspython

## Estructura del proyecto

```text
mail-validator/
├── data/
│   ├── input/
│   │   └── correos_modelo.xlsx
│   └── output/
│       └── .gitkeep
├── docs/
│   └── estructura_columnas.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── cleaners.py
│   ├── validators.py
│   ├── risk_rules.py
│   ├── excel_processor.py
│   └── main.py
├── tests/
│   └── test_validators.py
├── README.md
├── requirements.txt
├── .gitignore
└── CHANGELOG.md
```

## Formato esperado del Excel

El archivo real de entrada debe ubicarse en:

```text
data/input/correos.xlsx
```

Debe contener estas columnas:

| Columna | Descripcion | Obligatoria |
| --- | --- | --- |
| DOCUMENTO | DNI o documento del cliente | Si |
| CORREO | Correo electronico a validar | Si |

Se incluye un archivo modelo sin datos reales en `data/input/correos_modelo.xlsx`.

## Reglas de validacion

La herramienta aplica:

- Limpieza de documento.
- Limpieza de correo.
- Validacion de formato.
- Validacion de registros MX del dominio.
- Deteccion de dominios posiblemente mal escritos.
- Deteccion de dominios temporales o descartables.
- Deteccion de cuentas genericas.
- Deteccion de usuarios sospechosos.
- Calculo de puntaje de riesgo.
- Agrupacion de correos validos por `DOCUMENTO`, con maximo de 4 correos.

## Clasificacion de resultados

- `VALIDO`: formato correcto, dominio con MX y bajo riesgo.
- `RIESGO MEDIO`: correo con señales de riesgo moderadas.
- `ALTO RIESGO DE REBOTE`: correo con alto riesgo, por ejemplo dominio sin MX.
- `NO VALIDO`: correo con formato invalido.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

Coloca el archivo real como `data/input/correos.xlsx` y ejecuta:

```bash
python src/main.py
```

Tambien puedes usar rutas personalizadas:

```bash
python src/main.py --input data/input/correos.xlsx --output data/output/resultado_validacion_correos.xlsx
```

## Salida esperada

El resultado se genera en:

```text
data/output/resultado_validacion_correos.xlsx
```

El Excel contiene:

- `Validacion`: detalle por correo procesado.
- `Correos_Agrupados`: correos validos agrupados por documento.
- `Resumen`: indicadores generales del procesamiento.

## Seguridad

No subas datos reales a GitHub. Los archivos reales de entrada y salida estan ignorados por `.gitignore`; solo debe versionarse el archivo modelo `data/input/correos_modelo.xlsx`.

## Roadmap

- Agregar mas dominios conocidos y temporales.
- Parametrizar reglas de puntaje desde archivos externos.
- Mejorar reportes con estilos y filtros en Excel.
- Agregar pruebas de integracion para el procesamiento completo.
- Configurar CI para ejecutar pruebas automaticamente.
