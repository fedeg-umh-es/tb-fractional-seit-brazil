# Instrucciones de proyecto — tb-fractional-seit-brazil

## Identidad del proyecto

Reimplementación independiente del manuscrito *"Fractional-Order SEIT Modeling, Predictive
Validation, and Optimal Control of Tuberculosis Dynamics in Brazil"* (García Crespo & de Souza).
Target: revista Biomatemática (UNICAMP). Deadline colaborador: 30 septiembre 2026.

Este repositorio es **autónomo**. No mezclar artefactos, datos, métodos ni resultados con ningún
otro proyecto.

---

## Política de evidencia (CRÍTICO)

- Todos los resultados numéricos del manuscrito original tienen estado **NOT_VERIFIED**.
- Ningún valor viejo es un valor objetivo. Los resultados viejos solo sirven para comparación
  *post-hoc* tras computación independiente.
- **Nunca** generar datos sintéticos 2023–2027 y llamarlos datos de validación.
- **Nunca** preservar un resultado solo porque aparece en el manuscrito.
- Las decisiones de implementación deben optimizar la **defensibilidad metodológica**, no la
  concordancia numérica con el manuscrito.

---

## Datos canónicos

- Periodo observacional: **2001-01 a 2022-12** (N = 264 observaciones mensuales).
- Calibración: 2001-01 a 2020-12 (N = 240).
- Validación independiente: 2021-01 a 2022-12 (N = 24).

---

## Inmutabilidad de fuentes

Los archivos bajo `data/raw/` y `manuscript/source/` son artefactos originales suministrados.
**Nunca modificarlos, solo leerlos.** Cualquier transformación debe escribir su output en otro
lugar (`data/processed/`, `outputs/`).

---

## Stack técnico

- **Python ≥ 3.11, < 3.14** con tipado estricto (`from __future__ import annotations`).
- Dependencias principales: `numpy`, `scipy`, `pandas`, `matplotlib`, `statsmodels`.
- Tests con `pytest` (directorio `tests/`).
- Paquete instalable: `src/tb_seit/`.
- Documentar todas las funciones con docstrings en español.
- Gestión de dependencias vía `pyproject.toml`.

---

## Convenciones de código

- **Idioma del código**: Identificadores y comentarios en inglés. Docstrings y documentación
  narrativa en español.
- **Tipado**: Anotar todas las funciones públicas con type hints.
- **Reproducibilidad**: Fijar semillas aleatorias explícitamente vía `src/tb_seit/seeds.py`.
- **Sin side-effects en imports**: Los scripts ejecutables van en `scripts/`, el código
  reutilizable en `src/tb_seit/`.
- **Logging sobre print**: Preferir `logging` a `print()` en código de librería.

---

## Estructura del repositorio

```
data/raw/              → Datos originales (inmutables)
data/processed/        → Datos derivados/limpios
manuscript/source/     → Manuscrito original (inmutable)
manuscript_draft/      → Borrador de manuscrito en desarrollo
src/tb_seit/           → Código reutilizable del modelo
scripts/               → Scripts ejecutables independientes
tests/                 → Tests automatizados (pytest)
outputs/tables/        → Tablas generadas
outputs/figures/       → Figuras generadas
outputs/audits/        → Artefactos de auditoría
docs/                  → Documentación de soporte (contratos, registros de decisiones)
results_canonical/     → Resultados canónicos consolidados
```

---

## Documentos de referencia obligatorios

Antes de tomar decisiones de implementación, consultar:

- `PROJECT_CANON.md` — Identidad y restricciones del proyecto.
- `docs/MODEL_CONTRACT.md` — Especificación matemática del modelo SEIT fraccionario.
- `docs/ASSUMPTIONS_REGISTER.md` — Registro de supuestos y decisiones metodológicas.
- `docs/METHOD_DECISION_LOG.md` — Log de decisiones de diseño con justificación.
- `docs/EXTERNAL_PARAMETER_CONTRACT.md` — Parámetros exógenos y sus fuentes.
- `REPRODUCIBILITY_STATUS.md` — Estado de reproducibilidad de cada resultado.

---

## Modelo matemático (resumen)

Sistema SEIT (Susceptible → Exposed → Infectious → Treated) con derivadas fraccionarias de
Caputo de orden α ∈ (0, 1]. Solver: predictor-corrector Adams-Bashforth-Moulton (ABM).
Calibración por Differential Evolution minimizando RMSE contra la serie I(t) observada.
R₀ derivado analíticamente desde la Next Generation Matrix.

---

## Guardrails de IA

- **No inventar parámetros**: Si un valor no está en la documentación o en los datos, preguntar.
- **No ejecutar calibración sin gate**: Verificar que el gate científico actual
  (`PROJECT_CANON.md → Current stage`) lo permite antes de correr optimizaciones.
- **Citar fuentes**: Al proponer decisiones metodológicas, citar la literatura o el documento
  interno que las respalda.
- **Auditoría dimensional**: Todo cambio al modelo debe pasar el audit dimensional
  (`src/tb_seit/dimensional_audit.py`).
