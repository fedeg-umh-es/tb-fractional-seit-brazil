# Evidencia TB/SEIT Brasil — S1 — congelación 2026-10-10

Estado vigente: `EVIDENCE_FREEZE_PASS`; leer `EVIDENCE_FREEZE_REPORT.md` y `FREEZE_SUMMARY.json`.

- `phase1/`, `phase2/`, `phase3/`: copias byte idénticas de la evidencia corregida.
- `CLAIM_EVIDENCE_MATRIX.csv`: afirmaciones vigentes, no demostradas y límites; insumos de cálculo y protocolo.
- `HISTORICAL_CLAIM_DISPOSITION.csv`, `reconciled_tables/`: sustituciones y comparaciones.
- `figures/`, `FIGURE_TRACEABILITY.json`: visualizaciones documentales de tablas existentes.
- `historical_reference/`: EVIDENCIA HISTÓRICA del otro operador, conservada para comparación; **no usar como evidencia vigente S1**. Sus informes y sellos históricos no prevalecen sobre el presente registro de sustituciones.
- `repository_snapshot/`: insumos y código base del commit b3ad21b; el acumulador histórico sigue en el código base, pero los ejecutores corregidos en phase1/2/3 usan la cuadratura S1.
- `verification/`: controles previos, cierre actual, cronología y verificador portátil.
- `SOURCE_PROVENANCE.json`, `artifact_manifest.json`: procedencia y SHA-256.

Los informes/protocolos anteriores están preservados, incluidos sus estados de revisión a fecha de ejecución. La aceptación presente está en `decisions/AUTHOR_FREEZE_DECISION.md`. La búsqueda del protocolo perdido permanece cerrada.

Solo verificar: `python verification/verify_frozen_bundle.py RUTA_PAQUETE`. No ejecutar los runners científicos por este gate. No hay permiso de nuevas optimizaciones, simulaciones, editorial, merge ni envío. Las líneas de las curvas de α solo conectan los 21 puntos y no son un intervalo continuo.
