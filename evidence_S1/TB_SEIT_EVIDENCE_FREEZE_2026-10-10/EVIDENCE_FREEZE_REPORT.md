# Reconciliación y congelación de evidencia — 10 de octubre de 2026

**Dictamen: `EVIDENCE_FREEZE_PASS`.** Las Fases 1, 2 y 3 quedan congeladas documentalmente en este paquete con las limitaciones aceptadas por el autor. Pasan 66 controles de cierre y se conservan los informes previos de 43 comprobaciones de Fase 2 y 49 de Fase 3. La auditoría verifica hashes actuales y reconstruye métricas de tablas existentes; no vuelve a ejecutar esas simulaciones ni optimizaciones.

## Qué se congela

| Eje | Evidencia vigente | Alcance |
|---|---|---|
| Observación SEIT | Integral mensual ordinaria S1 de σE; trapecios sobre E corregida | No se usa el acumulador Caputo C para incidencia |
| Fase 1 global | Fractional e integer independientes, seed 20260815, train 2001–2020 | Validación open-loop 2021–2022, un origen |
| Fase 2 temporal | 780 predicciones; 156 pares por modelo; 26 ajustes SEIT | 13 orígenes 2020-12…2021-12, h=1…12 |
| Fase 3 práctica | 21 α fijos/reoptimizados; 47 soluciones; 32 bajo 1% | Diagnósticos aproximados y conjunto finito |
| R₀ y DFE | Primario .3577675038; envolvente .3416572023–.5879257724; 32 estables | Referencia autónoma; no prueba para N(t) variable |

Los bytes originales de cada fase están en `phase1/`, `phase2/` y `phase3/`. Sus propios informes reflejan los estados de revisión de sus fechas de creación y permanecen intactos. La aceptación y la congelación actual constan en este informe y en `decisions/AUTHOR_FREEZE_DECISION.md`; no se reescribe la historia para que los informes antiguos parezcan ya aceptados.

## Fase 1: validación y sustitución

| Modelo S1 | RMSE train | MAE train | Bias train | RMSE open-loop | MAE open-loop | Bias open-loop |
|---|---:|---:|---:|---:|---:|---:|
| Fractional | 619.318751 | 484.062478 | +49.456919 | 1216.541986 | 1035.207104 | −983.953702 |
| Integer | 776.040852 | 616.145573 | +171.226633 | 1759.542092 | 1588.652631 | −1588.652631 |

Las 264 predicciones de cada modelo reproducen los cuatro registros de métricas, con 240 meses de calibración y 24 de validación. La ventaja relativa de RMSE fractional frente a integer es 30.860308% en este origen. Este resultado sigue válido como descripción open-loop; no establece superioridad frente a baselines ni significación estadística.

Se sustituye el RMSE fractional histórico 1117.960028 por 1216.541986. α primario pasa de .964011 a .502203; la estimación corregida se reutiliza sin seleccionarla entre semillas diagnósticas. A α=1 los operadores son teóricamente equivalentes, pero sus discretizaciones no producen floats idénticos: RMSE integer histórico 1759.538401 y S1 1759.542092, diferencia 0.00369134. Se conserva y documenta esa pequeña diferencia. `phase1/scientific_comparison.csv` separa ablación a parámetros fijos de reajuste global; no se mezclan para atribuir causalmente todo cambio mecanístico al operador.

## Fase 2: predicciones y cuatro comparadores

Se congelan **exactamente** `phase2/rolling_origin_predictions.csv` (780 filas), `metrics_by_horizon.csv` (60), `skill_by_horizon.csv` (168) y `horizon_summary.csv` (14). No se agrupan horizontes para fabricar una métrica global. Las 468 predicciones de persistence, seasonal naive y SARIMA se conservan exactamente; las 312 SEIT pertenecen solo a S1.

| Referencia de fractional | Skill RMSE/MAE positivo | H_relax | H_strict |
|---|---|---:|---:|
| Integer | h=1…12 | 12 | 12 |
| Persistence | Ninguno | 0 | 0 |
| Seasonal naive 12 | h=1…5 | 5 | 5 |
| SARIMA | Ninguno | 0 | 0 |

Skill=1−error_modelo/error_referencia. H_relax es el último horizonte con skill positivo y H_strict el tramo positivo desde h=1, o cero. La comparación con seasonal naive sustituye **7 por 5**; el resto conserva su conclusión descriptiva con valores nuevos. Fractional tiene bias negativo en todos los horizontes. Los 13 α fraccionarios están próximos a la cota inferior .50.

Leakage: cada rolling origin utiliza solamente datos hasta ese origen; las ventanas posteriores incorporan los meses 2021 ya observados. No son los mismos 240 meses fijos del ajuste global. Constantes, población extrapolada e inicialización se construyen dentro de cada entrenamiento. Los objetivos futuros no entran al ajuste. Los 26 vectores y controles permanecen guardados. El ZIP verificado originalmente mantiene SHA-256 `90ac75b21112be90ac4f9eba8658ef5203334535371b35011b519c167215818b`.

Limitación SARIMA: especificación congelada (0,1,2)(1,1,1,12), procedencia de código/datos y predicciones acreditadas; faltan los coeficientes de cada ajuste histórico. No se hace refit para completar el archivo. Las comparaciones son descriptivas, sin pruebas de significación que ignoren la dependencia entre errores.

## Fase 3: identificabilidad, R₀ y DFE

La sección de α con β/σ/γ/d fijos y el perfil reoptimizado usan 21 puntos idénticos; sus columnas crudas se preservan por separado. `feasible_cost_upper_bound` es una columna auxiliar y no reemplaza costes ni soluciones. El pool incluye primaria, cuatro semillas diagnósticas y 42 perfiles; se conservan todos, incluso los tres con R₀>1. El menor coste explorado no reemplaza la primaria.

El umbral principal es **619.3187514936859 ×1.01 =625.5119390086228**, aplicado al RMSE de calibración. Da 32 soluciones y coincide la membresía con los controles h=.25. Los α reoptimizados admisibles muestreados están entre .50 y .52; .55 queda fuera. No se identifica una frontera continua entre esos puntos, unicidad, un mínimo global ni un mecanismo biológico de memoria.

Con μ=1/888, R₀=βσ/[(σ+μ)(γ+μ+d)] en la referencia Nref=S*=Λ/μ. Primario **.35776750381879896**. En las 32 soluciones exploradas admisibles, **.3416572022567021–.587925772372874**. El pool diagnóstico completo tiene 47, con R₀ .341657–1.661998 (44<1, 3>1). La envolvente no es IC ni rango exhaustivo de todas las soluciones matemáticamente admisibles.

El jacobiano epidemiológico de cuatro estados incluye ∂Tdot/∂I=γ; C no realimenta y se excluye del criterio. En referencia autónoma, el bloque E/I tiene traza negativa y determinante (σ+μ)(γ+μ+d)(1−R₀). Si R₀<1 todos sus autovalores y los dos −μ son negativos: cumplen Matignon para orden común 0<α≤1. Las 32 soluciones admisibles son estables; el pool completo presenta 44 estables y tres inestables. Se conserva la demostración y la comprobación de los 188 autovalores en el informe de conformidad de Fase 3, sin recalcular un nuevo experimento.

Con N(t) exógeno el jacobiano cambia. Los espectros congelados punto a punto son diagnósticos, no una prueba no autónoma. **No se demuestra desaparición de tuberculosis en Brasil, estabilidad global ni estabilidad del sistema con N(t) variable.** Para un espectro fijo disminuir α reduce el umbral angular de Matignon; no lo hace más exigente.

El conjunto histórico de 25 soluciones con R₀ 1.154172–1.189219 y DFE inestable se marca **obsoleto para S1**, conservando sus tablas intactas en `historical_reference/`. La inversión de clasificación dentro de dos conjuntos explorados distintos no se atribuye exclusivamente al observable: también cambian los parámetros y el diseño del pool.

## Claims, figuras y retirada documental

`CLAIM_EVIDENCE_MATRIX.csv` vincula 29 afirmaciones/limitaciones con tablas y selección de filas, código de cálculo, protocolo y figuras cuando corresponde. Incluye estados NOT_ESTABLISHED/NOT_TESTED/NOT_SUPPORTED para evitar convertir una falta de evidencia en un resultado positivo. `HISTORICAL_CLAIM_DISPOSITION.csv` reconcilia los 11 claims históricos: C04 (h=7), C07 (R₀>1) y C08 (DFE inestable) quedan sustituidos; wording de estabilidad de α y factores de dispersión antiguos no se trasladan. El control óptimo ~48% continúa fuera de alcance y sin verificar.

El CSV histórico de claims tiene dos comas sin entrecomillar en la nota final de C09 y una en C11. Se conserva intacto y, solo para el nuevo registro de disposición, se unen sus campos sobrantes de notas; los seis primeros campos permanecen sin cambio. Es una limitación de formato histórica, sin efecto en las cifras científicas o la clasificación de este gate.

Se generan cinco figuras documentales a partir de las tablas guardadas, PNG y PDF: ajuste/open-loop, RMSE rolling, skill frente a cuatro comparadores, α fijo/perfilado y pool R₀. `FIGURE_TRACEABILITY.json` fija los insumos y el alcance de cada una. No son figuras insertadas en el manuscrito ni una redacción editorial. Las figuras históricas permanecen en la sección marcada como referencia obsoleta y no se deben reutilizar para S1.

## Protocolo y cronología

Se conserva `PROTOCOL_DECISION.md` SHA-256 **58d4bed36871f9c63cd93e4c199d5c9890f006ccaf96ede85362480dee91469b**. Registro local: creación de sus bytes exactos 2026-10-08 19:36:16.660 UTC, ejecución 19:40:16.626 UTC. Es anterior al cálculo de Fase 3, pero posterior a los resultados conocidos de Fases 1/2; adopción humana documental del 10 de octubre. No existe sellado temporal independiente de esa cronología.

`ORIGINAL_PROTOCOL_UNAVAILABLE`: decisión cerrada, sin nueva búsqueda, equivalencia ni autorización atribuida al documento desaparecido. Se conservan los 21 puntos y cuatro semillas diagnósticas como diseño ejecutado y aceptado, sin volver a ejecutar para producir resultados más favorables.

## Integridad, reproducibilidad y límites del sellado

239 hashes tracked, HEAD/rama/status de cuatro worktrees y todos los archivos fuente auditados se preservan. Git científico termina con `?? audits/`; esos archivos se conservan. No hubo commit, push, merge, cambios canónicos, manuscrito, PR ni compilación. La copia de código/datos/protocolos y el entorno guardado permiten inspección y reproducción futura, pero este gate no autoriza repetir experimentos.

Los controles de resolución existentes comparan h=1,.5,.25; su máxima diferencia mensual de Fase 3 es aproximadamente .119134%, inferior al 1%. Son controles empíricos, no una cota formal de error continuo. Fase 3 no conserva todos los estados crudos de las mallas finas: se guardan 115 controles, 114 checkpoints y código/insumos. El cierre no realiza simulaciones para completar ese archivo. Se conserva expresamente esta limitación, junto a la ausencia de un manifiesto integral de Fase 3 sellado antes de esta auditoría.

`SOURCE_PROVENANCE.json` registra procedencia y SHA-256 de cada copia. `artifact_manifest.json` cubre todos los archivos del paquete salvo a sí mismo; se entrega un hash externo del manifiesto y del ZIP. Es congelación por integridad criptográfica local a la fecha actual, no un sello prospectivo o certificado temporal externo. Cualquier cambio requiere una versión nueva y un manifiesto nuevo, sin sobrescribir esta.

Comprobación portátil de solo lectura: `python verification/verify_frozen_bundle.py RUTA_PAQUETE`. Verifica manifiesto, lista completa, predicciones/soporte y estados, sin importar solvers u optimizadores. El generador conservado `verification/freeze_evidence_20261010.py` documenta las comprobaciones aritméticas detalladas y rechaza sobrescribir una congelación existente.

## Estado de cierre

El gate de evidencia queda satisfecho con las limitaciones documentadas. Forecasting y referencia mecanística siguen separados. Queda preparada la evidencia para una instrucción posterior de reconciliación editorial; este encargo no modifica Abstract, Results, Discussion, PR #3, compilación, envío ni selección de revista. El paso del gate no constituye permiso para merge, publicación ni envío.

**Dictamen final: `EVIDENCE_FREEZE_PASS`.**
