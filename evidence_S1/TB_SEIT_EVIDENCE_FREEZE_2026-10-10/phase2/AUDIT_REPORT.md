# Fase 2 — rolling-origin con observación ordinaria

**COMPLETED_PHASE_2_PENDING_AUTHOR_REVIEW.** 780 predicciones finales, soporte común de 156 pares por modelo, 26 ajustes independientes exitosos y todos los controles numéricos/leakage/integridad pasados. No se actualizaron manuscrito ni PR #3; compilación y cierre S1 siguen pendientes de revisión humana.

Commit `b3ad21bb059eb5357742693a4d5072107dc0df63`; worktree `/Users/fede/Documents/Codex/2026-10-08/files-pasted-by-the-user-diagn/work/tb-global-refit-phase1`; rama `codex/observation-operator-global-refit-phase1-20261008`.

## Decisión fijada antes de ejecutar

`PROTOCOL_DECISION.md` mantiene alpha fractional [0.50,1.00] para todos los orígenes e integer alpha=1. Un ajuste por modelo/origen, exclusivamente semilla 20260815. DE original best1bin/popsize15/mutation(0.5,1)/CR0.7/tol0.01/maxiter1000/polishFalse, mismos límites cinéticos que Fase 1. Solver h=1 mes, sin selección por forecasting. Los resultados negativos se conservan y la interpretación es descriptiva, sin pruebas de significación.

## Gate previo sin reajustes

Se verificaron los hashes y artefactos de Fase 1, sus 4 pruebas originales y la reproducción de sus métricas/predicciones. Se compararon h=1,0.5,0.25 con los vectores verdaderos de Fase 1. Fractional alpha≈0.502203: máximo cambio mensual de 9.301783 casos/0.1156% en calibración y 0.008594 casos/≈0.000106% en validación. Los RMSE apenas varían: 619.318751→619.313494 y 1216.541986→1216.540388. Integer también pasa.

Tolerancia declarada antes de ejecutar: máximo cambio relativo mensual y cambios relativos de RMSE/MAE <=1%; cambio de bias <=1% de la media observada; reducción de discrepancia al refinar. Es una comprobación empírica de resolución a tres pasos, no una demostración matemática de la cota absoluta del error continuo. El observable usa trapecios sobre E corregida; se verificó de manera independiente con los espaciamientos reales de t, incidencia constante y lineal, e invariancia de los estados. No se añadió C ordinaria al solver fraccionario.

Siete pruebas del protocolo rolling-origin pasaron antes del ajuste: no interferencia de datos futuros en entrenamiento/población, soporte común, rechazo de pares/fechas inválidos y distinción entre H_relax y H_strict con signos no contiguos.

## Baselines y protocolo temporal

13 orígenes 2020-12…2021-12, horizontes 1…12, entrenamiento expanding-window desde 2001-01 hasta cada origen. El objetivo DE recibe exclusivamente los casos de entrenamiento; Lambda, población futura e inicialización se construyen con datos <=origen. Las observaciones objetivo se obtienen después de completar ambos ajustes y forecasts del origen. Se conservaron todos los vectores, constantes, estados iniciales y hashes de entrenamiento en `fit_states.csv` y `leakage_checks.csv`.

Se reutilizaron exactamente las 468 predicciones históricas de persistence, seasonal_naive_12 y SARIMA. Se verificaron mismo soporte, fechas, train_end/n_train, observaciones, estado finito/ok y procedencia en el commit congelado. Las fórmulas persistence/seasonal naive coinciden exactamente con los valores disponibles al origen. SARIMA usa la especificación original (0,1,2)(1,1,1,12), seleccionada solo en 2001–2020 y ajustada por origen según el script original. Sus coeficientes por origen no están guardados; la acreditación de su protocolo se apoya en código/datos inmutables, fechas registradas, orden congelado y manifest original. No se hizo fitting SARIMA ni selección nueva de modelos. Los floats guardados de baselines se preservan exactamente en la entrega.

Las 312 predicciones SEIT finales se generaron exclusivamente con el operador ordinario. Ninguna predicción histórica fractional/integer entra en las métricas nuevas; solo se usa en las tablas de comparación histórica.

## Métricas por horizonte

RMSE, 13 forecasts por celda:

| Horizonte | Fractional | Integer | Persistence | Seasonal naive | SARIMA |
|---|---|---|---|---|---|
| 1 | 791.588 | 1185.800 | 389.702 | 1090.638 | 535.547 |
| 2 | 855.628 | 1281.075 | 494.271 | 1049.835 | 595.827 |
| 3 | 1089.172 | 1530.886 | 709.999 | 1170.540 | 725.784 |
| 4 | 1127.269 | 1574.968 | 720.287 | 1182.556 | 841.713 |
| 5 | 1233.747 | 1710.971 | 832.477 | 1278.390 | 939.654 |
| 6 | 1274.003 | 1770.702 | 845.856 | 1239.172 | 1022.421 |
| 7 | 1340.440 | 1858.590 | 964.206 | 1237.408 | 1096.024 |
| 8 | 1480.861 | 2009.191 | 1077.249 | 1258.413 | 1161.578 |
| 9 | 1499.639 | 2037.321 | 1120.357 | 1207.927 | 1213.959 |
| 10 | 1501.699 | 2041.686 | 1170.294 | 1189.946 | 1242.805 |
| 11 | 1498.888 | 2048.768 | 1175.946 | 1190.754 | 1291.796 |
| 12 | 1472.295 | 2022.497 | 1152.958 | 1152.958 | 1283.583 |


Métricas SEIT completas, bias=mean(predicted−observed):

| Horizonte | RMSE fractional | MAE fractional | Bias fractional | RMSE integer | MAE integer | Bias integer |
|---|---|---|---|---|---|---|
| 1 | 791.588 | 661.662 | -563.500 | 1185.800 | 1052.249 | -1052.249 |
| 2 | 855.628 | 740.442 | -666.709 | 1281.075 | 1164.042 | -1164.042 |
| 3 | 1089.172 | 906.178 | -880.178 | 1530.886 | 1386.161 | -1386.161 |
| 4 | 1127.269 | 955.180 | -930.164 | 1574.968 | 1444.838 | -1444.838 |
| 5 | 1233.747 | 1091.947 | -1080.366 | 1710.971 | 1603.765 | -1603.765 |
| 6 | 1274.003 | 1168.019 | -1168.019 | 1770.702 | 1700.173 | -1700.173 |
| 7 | 1340.440 | 1267.587 | -1267.587 | 1858.590 | 1808.524 | -1808.524 |
| 8 | 1480.861 | 1395.916 | -1395.916 | 2009.191 | 1945.663 | -1945.663 |
| 9 | 1499.639 | 1416.931 | -1416.931 | 2037.321 | 1975.515 | -1975.515 |
| 10 | 1501.699 | 1418.786 | -1418.786 | 2041.686 | 1986.232 | -1986.232 |
| 11 | 1498.888 | 1408.482 | -1408.482 | 2048.768 | 1984.816 | -1984.816 |
| 12 | 1472.295 | 1365.941 | -1365.941 | 2022.497 | 1951.188 | -1951.188 |


`metrics_by_horizon.csv` contiene RMSE/MAE/bias de los cinco modelos, sin agregación de horizontes. `skill_by_horizon.csv` conserva Skill_RMSE=1−RMSE_modelo/RMSE_referencia y Skill_MAE equivalente, incluidas las comparaciones internas frente a integer.

## Skill y horizontes

- Fractional vs integer, RMSE: skill positivo en [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; rango de skill [0.262956, 0.332444].
- Fractional vs integer, MAE: skill positivo en [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; rango de skill [0.282550, 0.371192].
- Fractional vs persistence, RMSE: skill positivo en ningún horizonte; rango de skill [-1.031264, -0.274623].
- Fractional vs persistence, MAE: skill positivo en ningún horizonte; rango de skill [-1.074676, -0.344227].
- Fractional vs seasonal_naive_12, RMSE: skill positivo en [1, 2, 3, 4, 5]; rango de skill [-0.276972, 0.274197].
- Fractional vs seasonal_naive_12, MAE: skill positivo en [1, 2, 3, 4, 5]; rango de skill [-0.344227, 0.357514].
- Fractional vs SARIMA, RMSE: skill positivo en ningún horizonte; rango de skill [-0.500684, -0.147020].
- Fractional vs SARIMA, MAE: skill positivo en ningún horizonte; rango de skill [-0.542935, -0.202864].

H_relax=último horizonte con skill>0, o cero. H_strict=longitud del tramo positivo desde h=1, o cero. Nuevo e histórico, claramente separados:

| Modelo | Referencia | Métrica | H relax nuevo | H strict nuevo | H relax histórico | H strict histórico |
|---|---|---|---|---|---|---|
| fractional | SARIMA | MAE | 0 | 0 | 0 | 0 |
| fractional | SARIMA | RMSE | 0 | 0 | 0 | 0 |
| fractional | integer | MAE | 12 | 12 | 12 | 12 |
| fractional | integer | RMSE | 12 | 12 | 12 | 12 |
| fractional | persistence | MAE | 0 | 0 | 0 | 0 |
| fractional | persistence | RMSE | 0 | 0 | 0 | 0 |
| fractional | seasonal_naive_12 | MAE | 5 | 5 | 7 | 7 |
| fractional | seasonal_naive_12 | RMSE | 5 | 5 | 7 | 7 |
| integer | SARIMA | MAE | 0 | 0 | 0 | 0 |
| integer | SARIMA | RMSE | 0 | 0 | 0 | 0 |
| integer | persistence | MAE | 0 | 0 | 0 | 0 |
| integer | persistence | RMSE | 0 | 0 | 0 | 0 |
| integer | seasonal_naive_12 | MAE | 0 | 0 | 0 | 0 |
| integer | seasonal_naive_12 | RMSE | 0 | 0 | 0 | 0 |


No se consideran estos horizontes límites universales de predictibilidad. No se interpreta una diferencia descriptiva como significación.

## Estado de los ajustes y controles posteriores

| Origen | Modelo | α | RMSE train | Iteraciones | Evaluaciones | success |
|---|---|---|---|---|---|---|
| 2020-12-01 | fractional | 0.502202999 | 619.319 | 36 | 2775 | True |
| 2020-12-01 | integer | 1.000000000 | 776.041 | 52 | 3180 | True |
| 2021-01-01 | fractional | 0.500210998 | 617.953 | 47 | 3600 | True |
| 2021-01-01 | integer | 1.000000000 | 787.983 | 42 | 2580 | True |
| 2021-02-01 | fractional | 0.500688507 | 616.909 | 40 | 3075 | True |
| 2021-02-01 | integer | 1.000000000 | 786.403 | 41 | 2520 | True |
| 2021-03-01 | fractional | 0.500256690 | 616.545 | 31 | 2400 | True |
| 2021-03-01 | integer | 1.000000000 | 787.333 | 42 | 2580 | True |
| 2021-04-01 | fractional | 0.500911982 | 615.529 | 32 | 2475 | True |
| 2021-04-01 | integer | 1.000000000 | 773.412 | 51 | 3120 | True |
| 2021-05-01 | fractional | 0.500787158 | 614.260 | 34 | 2625 | True |
| 2021-05-01 | integer | 1.000000000 | 769.210 | 58 | 3540 | True |
| 2021-06-01 | fractional | 0.503772894 | 613.586 | 39 | 3000 | True |
| 2021-06-01 | integer | 1.000000000 | 773.369 | 47 | 2880 | True |
| 2021-07-01 | fractional | 0.503632873 | 613.503 | 41 | 3150 | True |
| 2021-07-01 | integer | 1.000000000 | 770.912 | 54 | 3300 | True |
| 2021-08-01 | fractional | 0.500626363 | 617.360 | 41 | 3150 | True |
| 2021-08-01 | integer | 1.000000000 | 779.506 | 56 | 3420 | True |
| 2021-09-01 | fractional | 0.500021248 | 621.607 | 37 | 2850 | True |
| 2021-09-01 | integer | 1.000000000 | 784.138 | 57 | 3480 | True |
| 2021-10-01 | fractional | 0.500218688 | 622.991 | 45 | 3450 | True |
| 2021-10-01 | integer | 1.000000000 | 787.781 | 62 | 3780 | True |
| 2021-11-01 | fractional | 0.501443448 | 625.974 | 36 | 2775 | True |
| 2021-11-01 | integer | 1.000000000 | 791.429 | 68 | 4140 | True |
| 2021-12-01 | fractional | 0.501910526 | 627.466 | 38 | 2925 | True |
| 2021-12-01 | integer | 1.000000000 | 808.459 | 48 | 2940 | True |


alpha fractional está en [0.500021248, 0.503772894]; 13 de 13 ajustes quedan a <=0.01 del límite inferior. El criterio success de DE solo acredita su parada por tolerancia, no unicidad/identificabilidad/mínimo global.

También se comprobó cada nuevo vector ajustado en h=1,0.5,0.25, sin recalibración. Los 26 controles pasaron; máxima diferencia relativa mensual 0.118918% y absoluta 9.567230 casos entre h=1 y h=.25. Los signos de Skill_RMSE/MAE y, por ello, H_relax/H_strict se mantienen en los tres pasos, frente a cada referencia, según `skill_discretization_check.csv`. Los forecasts por paso se guardan únicamente como control de discretización en `origin_step_forecasts.csv`; las métricas principales usan siempre h=1.

Las penalizaciones de candidatos no válidos durante DE siguen el protocolo original; se registraron 2903 candidatos penalizados en total. Ningún ajuste final/forecast tuvo fallo numérico u optimización fallida.

## Comparación histórica y lectura científica

`historical_metrics_comparison.csv`, `historical_skill_comparison.csv` y `historical_horizon_comparison.csv` comparan el nuevo operador con las mismas filas históricas. La recomputación descriptiva de las métricas antiguas coincide con los CSV canónicos dentro de tolerancias float64; no los sobrescribe. Hay 4 cambios de signo positivo/no positivo en las comparaciones guardadas.

Los signos y horizontes anteriores describen lo observado con el modelo corregido bajo este protocolo. La comparación dentro de SEIT se distingue de cada baseline externo. La proximidad de alpha a la frontera es una advertencia de sensibilidad; no se amplió el rango ni se escogieron semillas u orígenes favorables. No se infiere memoria biológica. Las posibles afirmaciones del artículo deben revisarse frente a esta evidencia nueva, incluyendo las que resulten negativas.

**Los resultados antiguos de identificabilidad, R0 y estabilidad DFE no se trasladan al modelo corregido.** Requieren reevaluación posterior autorizada porque cambiaron observable y parámetros. Para autovalores fijos, disminuir alpha reduce el umbral Matignon alpha*pi/2; no basta para concluir estabilidad cuando también cambia el Jacobiano. No se recalcularon esos diagnósticos en esta fase.

## Integridad y cierre

Los 239 archivos tracked conservaron sus SHA-256. Se preservaron los 24 archivos existentes de Fase 1, incluidos los sin seguimiento, y los archivos/HEAD/status de main, claude-science y la auditoría anterior. `integrity_check.csv`, `final_verification.json`, inventarios de hashes y `artifact_manifest.json` documentan la entrega.

Git solo registra archivos nuevos bajo audits; no hay modificaciones tracked, commit, push o merge. No se tocó el manuscrito ni PR #3 ni se compiló o preparó correo/envío BMB. PR #3, compilación y cierre S1 permanecen bloqueados hasta revisión del autor y resolución de los claims afectados.

**La ejecución científica autorizada termina aquí.** No se inicia reevaluación secundaria, cambios editoriales ni otra fase sin decisión humana.
