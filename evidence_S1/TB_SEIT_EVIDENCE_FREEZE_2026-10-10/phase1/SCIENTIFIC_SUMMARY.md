# Fase 1 — reajuste global SEIT con observación ordinaria

**Estado: COMPLETED_PHASE_1_PENDING_AUTHOR_DECISION.** Ambas optimizaciones terminaron con `success=True`, sin fallo numérico final ni discrepancia de integridad. No se ejecutó ninguna fase 2.

Repositorio: `fedeg-umh-es/tb-fractional-seit-brazil`.
Commit: `b3ad21bb059eb5357742693a4d5072107dc0df63`.
Rama NUEVA: `codex/observation-operator-global-refit-phase1-20261008`.
Worktree NUEVO: `/Users/fede/Documents/Codex/2026-10-08/files-pasted-by-the-user-diagn/work/tb-global-refit-phase1`.
Ejecutor y pruebas: ZIP aportado por el autor, extraído únicamente a la nueva carpeta no versionada `audits/observation_operator_refit_phase1_2026-10-08/`.

## Gates y método

- Las cuatro pruebas de `test_global_refit.py` pasaron.
- El preflight independiente reprodujo los ocho RMSE originales/ordinarios de la ablación del 8 de octubre con discrepancia máxima menor de 5×10⁻⁷ respecto a los valores redondeados del ejecutor; tolerancia obligatoria 0.001. Ambos modelos pasaron. El ejecutor volvió a verificar el preflight antes de ajustar.
- Operador: integral ordinaria mensual de σE sobre E corregida, mediante trapecios compuestos. Paso original h=1 mes. Dinámica SEIT y acumulador del solver originales sin cambios.
- Ajustes independientes, exclusivamente semilla primaria 20260815. Integer fija α=1 y se optimiza por separado; no reutiliza el vector fractional.
- DE original: best1bin, popsize=15, mutation=(0.5,1.0), recombination=0.7, tol=0.01, maxiter=1000, polish=False, presupuesto y reglas sin cambios.
- Límites: β [0.01,1.0], σ [0.01,0.5], γ [0.05,0.30], d [0.0001,0.05], α fractional [0.5,1.0].
- Calibración 2001-01…2020-12, n=240; validación continua open-loop 2021-01…2022-12, n=24. La función objetivo solo usa observaciones de calibración. La población futura se extrapola a partir de entrenamiento. Se conserva μ=1/(74×12), Λ y la inicialización canónica. Los valores de validación solo se consultan para el preflight autorizado y la evaluación final, nunca para la función objetivo ni para selección/ajuste.
- Python 3.12.14, numpy 2.5.3, scipy 1.18.1; dependencias completas del repositorio instaladas en el entorno aislado y registradas en `requirements_frozen.txt`.

La única modificación al ejecutor extraído es una comprobación inmediata de `result.success` y de que el objetivo sea finito e inferior a la penalización. El ZIP original imprimía un fallo de optimización, pero habría continuado con el siguiente modelo. Esta protección aplica la prohibición expresa del autor de continuar tras un fallo; no cambia el algoritmo, límites, semilla o resultados exitosos. `executor_safety_guard.diff` y `package_provenance.json` conservan el cambio y los hashes originales/ejecutados.

## Resultados del reajuste

| Modelo | Ventana | RMSE | MAE | Bias |
|---|---|---|---|---|
| fractional | calibration | 619.318751 | 484.062478 | 49.456919 |
| fractional | validation_open_loop | 1216.541986 | 1035.207104 | -983.953702 |
| integer | calibration | 776.040852 | 616.145573 | 171.226633 |
| integer | validation_open_loop | 1759.542092 | 1588.652631 | -1588.652631 |


Parámetros y diagnósticos:

| Modelo | β | σ | γ | d | α | Iteraciones | Evaluaciones |
|---|---|---|---|---|---|---|---|
| fractional | 0.120037828368 | 0.010004327169 | 0.261346737225 | 0.039100009587 | 0.502202999398 | 36 | 2775 |
| integer | 0.061166334009 | 0.010173423242 | 0.053248877140 | 0.000213340718 | 1.000000000000 | 52 | 3180 |


Fractional: `success=True`, 36 generaciones, 2775 evaluaciones. Integer: `success=True`, 52 generaciones, 3180 evaluaciones. El criterio de parada de DE se satisfizo; esto no demuestra que los vectores sean el mínimo global ni que estén identificados de forma única.

El vector integer coincide numéricamente con el antiguo vector global, pero se obtuvo mediante su propia ejecución independiente de DE. Esta coincidencia no implica reutilización: el operador entero solo difiere del original por una pequeña discrepancia de discretización.

## Comparación científica

`original_frozen_parameters`: operador fraccionario original, parámetros antiguos.
`ordinary_frozen_parameters`: ablación ordinaria con esos parámetros congelados.
`ordinary_global_refit`: fase 1 actual, operador ordinario y parámetros reajustados.

| Modelo | Etapa | RMSE calibración | RMSE validación | Bias validación |
|---|---|---|---|---|
| fractional | original_frozen_parameters | 605.048881 | 1117.960028 | -851.149888 |
| fractional | ordinary_frozen_parameters | 1620.116037 | 1178.733666 | 932.032400 |
| fractional | ordinary_global_refit | 619.318751 | 1216.541986 | -983.953702 |
| integer | original_frozen_parameters | 776.058253 | 1759.538401 | -1588.648614 |
| integer | ordinary_frozen_parameters | 776.040852 | 1759.542092 | -1588.652631 |
| integer | ordinary_global_refit | 776.040852 | 1759.542092 | -1588.652631 |


1. Tras ajustar ambos modelos bajo una observación ordinaria común, fractional vuelve a tener menor error de calibración: RMSE −156.722100 casos (20.195% menor), MAE −132.083094 (21.437% menor) frente a integer. La inversión de ranking detectada en la ablación con θ congelado no persiste en este reajuste.
2. En validación open-loop, fractional mantiene menor error: RMSE −543.000106 (30.860% menor) y MAE −553.445527 (34.837% menor) frente a integer. Ambos sesgos son negativos; fractional subpredice en promedio 983.953702 casos/mes.
3. Frente al resultado histórico fractional con operador original, el RMSE de validación empeora de 1117.960028 a 1216.541986: +98.581958 casos, +8.818%. El reajuste ordinario mejora mucho la calibración respecto a la ablación congelada (1620.116037 → 619.318751), pero no mejora su RMSE de validación (1178.733666 → 1216.541986). La validación no se utilizó para escoger ni corregir ese resultado.
4. α pasa de 0.9640110362133341 a 0.5022029993981696, a 0.0022029993981696 del límite inferior permitido. γ, d y β también cambian sustancialmente. Esto documenta sensibilidad del vector ajustado a la definición del operador. La proximidad al límite requiere cautela interpretativa; no se amplió el límite, no se añadieron semillas ni perfiles y no se recalculó R0/estabilidad.
5. La comparación muestra que una ventaja descriptiva global dentro de la familia puede persistir tras el reajuste ordinario. No demuestra memoria epidemiológica, superioridad estadística, habilidad frente a benchmarks ni ventaja rolling-origin. Es una única ejecución primaria por modelo, con el paso original; no se evaluó robustez adicional del nuevo vector.

**Decisión pendiente: REQUIRES_AUTHOR_SCIENTIFIC_REVIEW_BEFORE_ANY_ROLLING_ORIGIN.** La fase 1 termina aquí. No se autoriza por inferencia ningún reajuste adicional ni fase 2.

## Verificación e integridad

Se verificaron las fechas, los 264 valores finitos de predicción por modelo, los splits 240/24, las observaciones contra sus CSV históricos, los residuos, la consistencia entre CSV de predicciones y métricas, los límites y la coincidencia de cada objetivo optimizado con su RMSE de calibración. Verificación: PASS.

Los 239 archivos tracked del nuevo worktree conservan sus SHA-256. Raw-data SHA-256: `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`.

Se comprobaron además los HEAD, estados Git y hashes de los 224 archivos tracked de main, de los 224 del worktree claude-science y de los 258 archivos tracked/auditoría del worktree anterior. Todos permanecen intactos. No hubo commit, push o merge.

Estado final abreviado:

```text
?? audits/
```

Todos los archivos nuevos pertenecen a `audits/observation_operator_refit_phase1_2026-10-08/`; `git_status.txt` recoge el listado completo. `results_canonical/`, datos, outputs históricos, manuscrito y paquete editorial permanecen intactos. No se ejecutó rolling-origin, no se añadieron modelos o semillas y no se preparó compilación, envío BMB ni correo a Amaury.

## Entrega

En `tb_global_refit_phase1/results_global_primary/`:

- `global_refit_parameters.csv`
- `global_refit_metrics.csv`
- `fractional_predictions.csv`
- `integer_predictions.csv`
- `phase1_report.json`

La carpeta de entrega también conserva el ejecutor, las pruebas, README original, preflight, log de ejecución, hashes, diff mínimo, verificación y comparación científica. Es una copia de la nueva auditoría, sin duplicar datos ni resultados canónicos.
