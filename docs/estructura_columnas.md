# Estructura de columnas

El archivo de entrada debe ser un Excel con una hoja que contenga las columnas siguientes:

| Columna | Descripcion | Obligatoria |
| --- | --- | --- |
| DOCUMENTO | DNI o documento del cliente | Si |
| CORREO | Correo electronico a validar | Si |

Notas:

- Los nombres de columnas se normalizan a mayusculas.
- `DOCUMENTO` se limpia para conservar solo digitos y se completa a 8 caracteres.
- `CORREO` se limpia quitando espacios al inicio/final y convirtiendo a minusculas.
