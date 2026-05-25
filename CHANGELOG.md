# Changelog

## 0.2.0 - 2026-05-25

- Agrega argumentos de consola para entrada, salida, hoja, maximo de correos y modo verbose.
- Mejora el manejo de errores con mensajes claros y trazas tecnicas solo en verbose.
- Amplia la hoja `Resumen` con mas indicadores y fecha de procesamiento.
- Agrega formato basico al Excel de salida.
- Agrega `config.example.json` como referencia para configuracion futura.
- Amplia pruebas unitarias de limpieza, validacion, riesgo y resumen.

## 0.1.0 - 2026-05-25

- Reorganizacion inicial del proyecto.
- Unificacion de validacion de formato, MX y riesgo de rebote.
- Generacion de salida Excel con hojas `Validacion`, `Correos_Agrupados` y `Resumen`.
- Proteccion de archivos reales mediante `.gitignore`.
