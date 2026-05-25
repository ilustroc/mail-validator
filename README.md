# mail-validator

`mail-validator` es una herramienta en Python para limpiar, validar y clasificar correos electronicos desde un archivo Excel.

## Objetivo

Procesar una base con documentos y correos, detectar errores frecuentes, estimar riesgo de rebote y generar un Excel final con resultados detallados, resumen ejecutivo y correos validos agrupados por documento.

## Tecnologias usadas

- Python 3.10+
- pandas
- openpyxl
- dnspython

## Estructura del proyecto

```text
mail-validator/
|-- config.example.json
|-- data/
|   |-- input/
|   |   `-- correos_modelo.xlsx
|   `-- output/
|       `-- .gitkeep
|-- docs/
|   `-- estructura_columnas.md
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- cleaners.py
|   |-- validators.py
|   |-- risk_rules.py
|   |-- excel_processor.py
|   `-- main.py
|-- tests/
|   `-- test_validators.py
|-- README.md
|-- requirements.txt
|-- .gitignore
`-- CHANGELOG.md
```

## Formato esperado del Excel

El archivo real de entrada por defecto debe ubicarse en:

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
- Agrupacion de correos validos por `DOCUMENTO`.

## Clasificacion de resultados

- `VALIDO`: formato correcto, dominio con MX y bajo riesgo.
- `RIESGO MEDIO`: correo con senales de riesgo moderadas.
- `ALTO RIESGO DE REBOTE`: correo con alto riesgo, por ejemplo dominio sin MX.
- `NO VALIDO`: correo con formato invalido.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uso basico

Coloca el archivo real como `data/input/correos.xlsx` y ejecuta:

```bash
python src/main.py
```

Cuando no se pasan argumentos, el sistema usa los valores definidos en `src/config.py`.

## Uso con argumentos

```bash
python src/main.py --input data/input/correos.xlsx --output data/output/resultado_validacion_correos.xlsx
```

Comando de prueba con el Excel modelo:

```bash
python src/main.py --input data/input/correos_modelo.xlsx --output data/output/resultado_prueba.xlsx --verbose
```

Parametros disponibles:

| Parametro | Descripcion | Valor por defecto |
| --- | --- | --- |
| `--input` | Ruta del Excel de entrada. | `data/input/correos.xlsx` |
| `--output` | Ruta del Excel de salida. | `data/output/resultado_validacion_correos.xlsx` |
| `--max-correos` | Maximo de correos validos agrupados por documento. | `4` |
| `--sheet` | Hoja de entrada, por indice o nombre. | `0` |
| `--verbose` | Muestra detalles adicionales y trazas tecnicas si ocurre un error. | Desactivado |

## Salida esperada

El resultado por defecto se genera en:

```text
data/output/resultado_validacion_correos.xlsx
```

El Excel contiene estas hojas:

- `Validacion`: detalle por correo procesado, incluyendo dominio, MX, puntaje, clasificacion y motivo.
- `Correos_Agrupados`: correos clasificados como `VALIDO`, agrupados por documento y limitados por `--max-correos`.
- `Resumen`: indicadores generales como registros leidos, registros procesados, dominios unicos, dominios sin MX, temporales, posiblemente mal escritos y fecha de procesamiento.

El archivo de salida aplica formato basico: encabezados en negrita, filtros, primera fila congelada, ancho de columnas ajustado y formato de texto para `DOCUMENTO`.

## Manejo de errores

El programa muestra errores claros si:

- El archivo de entrada no existe.
- Faltan columnas requeridas.
- El Excel esta vacio.
- No hay registros procesables.
- Ocurre un error de lectura o escritura.

Las trazas tecnicas solo se muestran cuando se usa `--verbose`.

## config.example.json

`config.example.json` es una referencia para una mejora futura donde la configuracion pueda cargarse desde JSON. Actualmente el sistema no lo usa de forma automatica; la configuracion activa esta en `src/config.py` y en los argumentos de consola.

## Seguridad

No subas datos reales a GitHub. Los archivos reales de entrada y salida estan ignorados por `.gitignore`; solo debe versionarse el archivo modelo `data/input/correos_modelo.xlsx`.

## Roadmap

- Leer configuracion desde `config.example.json` o un archivo equivalente.
- Agregar mas dominios conocidos y temporales.
- Parametrizar reglas de puntaje desde archivos externos.
- Agregar pruebas de integracion para el procesamiento completo.
- Configurar CI para ejecutar pruebas automaticamente.
