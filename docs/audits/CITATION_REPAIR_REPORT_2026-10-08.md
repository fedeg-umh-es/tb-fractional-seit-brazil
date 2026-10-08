# Informe de reparación de referencias y citas (2026-10-08)

Alcance: corrección documental de `submission_bmb/BMB_MANUSCRIPT.md` y de los ficheros que repiten sus frases. No se ha modificado ningún dato, modelo, métrica, tabla, figura ni resultado.

**Veredicto: `PARTIAL_WITH_BLOCKERS`.** El texto completo de Chishtie et al. (2026) no se ha podido leer, y el informe no puede dar un veredicto superior mientras una cita usada dependa de un resumen no contrastado con el cuerpo del artículo (véase §C).

Etiquetas: **[H]** hecho verificado en la fuente indicada · **[I]** inferencia · **[P]** pendiente.

---

## A. Resumen de cambios

La rama partía de `origin/main`, que ya traía corregidas cuatro de las seis entradas con error (Raue, Meshkat, Area, Rocha). Quedaban por corregir Cramer y las frases cuya cita no respaldaba lo afirmado.

| Archivo | Problema original | Corrección |
|---|---|---|
| `submission_bmb/BMB_MANUSCRIPT.md` | Título de Cramer 2022 con «in the US». | «…in the United States». |
| ídem, Introducción | «A close fit… (Moran; Bracher)»: Bracher no trata ese punto y Moran no afirma lo que se le atribuía. | Se conserva el significado como enunciado propio de los autores, sin cita; la cita a Moran queda sobre lo que su resumen describe (datos incompletos e inexactos, cambios de comportamiento). |
| ídem, Introducción | Chishtie, Alzahrani y Kalizhanova caracterizados con más fuerza que sus fuentes («rolling-origin»; «forecasts… ARIMA»; «temporal validation»). | Reescrita separando en Chishtie la comparación fraccionario/entero de la validación rolling-origin; Alzahrani como comparación de ajuste y de sentido distinto al de este estudio; Kalizhanova con ventanas distintas y una sola partición. |
| ídem, Introducción | Meshkat citado como respaldo de la no identificabilidad práctica. | Retirado de esa frase (trata identificabilidad estructural). |
| ídem, Discusión | «Restricting evaluation… (Bracher; Cramer)»: resultado propio con citas. | Citas retiradas; frase aparte con Cramer (dos tercios de 27 modelos mejoraron un baseline ingenuo). |
| ídem, Discusión | «…must be evaluated separately (Moran; Cramer)». | Citas retiradas; Moran pasa a una frase aparte sobre las dificultades del pronóstico epidémico. |
| ídem, Discusión | Meshkat y Raue sin distinguir identificabilidad estructural y práctica. | Frase que atribuye a cada uno lo suyo y declara que el análisis de este estudio es de identificabilidad práctica. |
| ídem, Discusión | Estabilidad de cantidades derivadas sin Roosa y Chowell; Meshkat citado para ello. | Se añade Roosa y Chowell (2019); se retira Meshkat de esa lista. |
| ídem, Referencias | Bracher quedaba sin ninguna cita válida. | Eliminado de la lista (20 → 19 entradas) y renumerada; el orden alfabético se mantiene (Rocha antes de Roosa). |
| `manuscript_draft/INTRODUCTION_DRAFT.md`, `DISCUSSION_DRAFT.md` | Mismas frases con las mismas citas erróneas. | Mismo texto que el manuscrito. |
| `manuscript_draft/INTRODUCTION_TRACEABILITY.md`, `DISCUSSION_TRACEABILITY.md` | Fuentes y afirmaciones respaldadas contradictorias con el manuscrito reparado. | Actualizados con el nivel de evidencia. |
| `literature_verification/LITERATURE_VERIFICATION_MATRIX.md` | Area: cita correcta pero campo DOI con el DOI de otro artículo; Cramer con «in the US»; fichas de Moran, Bracher, Cramer, Area, Meshkat y Raue con afirmaciones que sus fuentes no sostienen; fichas de Chishtie, Alzahrani y Kalizhanova imprecisas. | Corregidos los campos afectados; Bracher pasa a «NOT CITED». |
| `manuscript_package/REFERENCE_AUDIT.md` | Recuento 20, fila de Bracher, ubicaciones obsoletas (p. ej. Alzahrani «Discussion»). | Recuento 19, inventario regenerado, descripción de los tres vecinos Gate 2 ajustada. |
| `submission_bmb/BMB_PACKAGING_TRACEABILITY.md` | Título largo anterior; recuento de palabras 18. | Título corto aprobado; 12 palabras. |
| `submission_bmb/BMB_MANUSCRIPT.md`, `BMB_COVER_LETTER.md`, `BMB_TITLE_OPTIONS.md` | Título largo. | Título corto, incorporado por cherry-pick de e3d3af7, 5a44717 y bea7188. |
| `docs/audits/CITATION_VERIFICATION_2026-10-01.md`, `CLAIM_AUDIT_2026-10-01.md` | No existían en `main`. | Copiados sin cambios desde la rama exciting-bell. |

Tres decisiones editoriales que conviene que revises:

1. **Bracher se elimina de la lista.** No se citaba en ninguna otra frase y el manuscrito no usa puntuaciones de intervalo. Si prefieres conservarlo por algún otro motivo, habría que justificar una cita nueva.
2. **Meshkat se retira de dos sitios** (definición de no identificabilidad práctica en la Introducción y lista de estabilidad de cantidades derivadas). Se mantiene en la frase donde se contrasta lo estructural con lo práctico.
3. **Las cifras de Chishtie (22,1 % y 6,2 %) no se incluyen.** El resumen no define la métrica de «mejora de precisión predictiva», y sin el texto completo no es posible citarla sin riesgo.

---

## B. Auditoría de citas

### B.1 Las seis entradas con error

| Entrada | Estado final | Verificación |
|---|---|---|
| Raue et al. (2009) | Correcta: título «…partially observed dynamical models by exploiting the profile likelihood», *Bioinformatics* 25(15):1923–1929. | **[H]** Crossref 2026-10-08. Ya estaba corregida en `main`; no se reescribió. |
| Meshkat, Kuo y DiStefano (2014) | Correcta: «…and COMBOS: a novel web implementation», *PLoS ONE* 9(10):e110261. | **[H]** Crossref 2026-10-08. Ya corregida en `main`. |
| Area et al. (2015) | Correcta: «On a fractional order Ebola epidemic model», *Adv Differ Equ* 2015:278, DOI 10.1186/s13662-015-0613-5. | **[H]** Crossref 2026-10-08. Ya corregida en `main`; el DOI antiguo seguía en la matriz y se corrigió. |
| Rocha et al. (2020) | Correcta: diez autores, primer autor Rocha MS, título original en portugués; cita en texto «Rocha et al., 2020»; ordenada antes de Roosa. | **[H]** Crossref 2026-10-08. Ya corregida en `main`. No se añadió traducción del título. |
| Cramer et al. (2022) | Corregida: «…COVID-19 mortality in the United States», *PNAS* 119(15):e2113561119. | **[H]** Crossref 2026-10-08. Esta sí faltaba. |
| Roosa y Chowell (2019) | Correcta: «…infectious disease transmission models», *Theor Biol Med Model* 16:1. | **[H]** Crossref 2026-10-08. Ya estaba correcta en `main`. |

### B.2 Resto de la lista

**[H]** Crossref (2026-10-08, con User-Agent con correo) confirma autores, iniciales, año, título, revista, volumen y páginas o número de artículo de las 19 entradas con DOI, y que cada DOI resuelve al artículo citado. Excepciones: Diethelm figura con fecha en línea 2012 y fecha de impresión 2013 (volumen 71(4), la cita es correcta); Roosa, 2019 en impresión; Alzahrani no tiene autores depositados en Crossref, y se verificaron en la ficha del editor (seis autores, mismo orden que el manuscrito, revista, volumen y páginas). La entrada del IBGE y la de la OMS (ISBN) no tienen DOI y no se han contrastado.

**[H]** Comprobación mecánica del texto: 19 entradas, todas citadas, ninguna cita sin entrada, orden alfabético coherente.

### B.3 Afirmaciones revisadas y nivel de evidencia

Nivel: **TC** texto completo · **RES** resumen · **REG** solo registro bibliográfico · **PREV** contrastado en la auditoría del 2026-10-01 o tomado del encargo, no releído hoy. Scite requiere plan de pago y no estuvo disponible; se usaron Crossref, Consensus, la ficha del editor y Europe PMC.

| Afirmación del manuscrito | Fuente | Nivel | Estado |
|---|---|---|---|
| Pronosticar epidemias exige lidiar con datos incompletos e inexactos y cambios de comportamiento (Introducción y Discusión) | Moran 2016 | RES (Consensus) | Respaldada en ese alcance. No se atribuye a Moran ningún protocolo de validación. |
| Dos tercios de 27 modelos de mortalidad por COVID-19 en EE. UU. fueron más precisos que un baseline ingenuo | Cramer 2022 | RES (Crossref) | Respaldada. El resumen dice exactamente «Two-thirds of the models evaluated showed better accuracy than a naïve baseline model». |
| «Restricting evaluation to the mechanistic family…» | — | — | Resultado de este estudio, sin cita. |
| Modelo fraccionario más preciso que los enteros en dos olas de COVID-19 en Canadá; validación rolling-origin a 7, 14 y 21 días, descrita aparte | Chishtie 2026 | RES (Consensus) | **Respaldada solo a nivel de resumen.** Ver §C. |
| SEIR fraccionario con mejor ajuste que ARIMA en gripe de Arabia Saudí; comparación de ajuste, no de pronóstico; sentido distinto al de este estudio | Alzahrani 2024 | TC (PREV) + ficha del editor hoy | Respaldada. No se reproducen sus cifras (MAE idéntico en su Tabla 4, que parece un error de la tabla). |
| SARIMA más preciso que SIR básico en TB de Kazajistán; ventanas distintas y una sola partición | Kalizhanova 2024 | TC (pasajes hoy en Europe PMC: ventanas 2014–2018/2019 y 2014–2017/2018–2019; conclusión de superioridad) | Respaldada. No se han releído hoy las cifras de R₀ ni las métricas, y el manuscrito no las usa. |
| Fórmulas fraccionarias con operadores no locales y dependencia temporal de tipo ley de potencias | Diethelm 2013; Area 2015 | Area: TC (PDF abierto, hoy). Diethelm: REG | Respaldada para Area (modelo SEIR fraccionario del Ébola, orden fraccionario como índice de memoria, núcleo (t−s)^−α). Ver nota sobre Caputo abajo. |
| Identificabilidad estructural: combinaciones identificables de parámetros | Meshkat 2014 | RES (Consensus) | Respaldada. El resumen no menciona R₀ ni identificabilidad práctica, y el manuscrito ya no se lo atribuye. |
| Perfil de verosimilitud para detectar no identificabilidades estructurales (parámetros funcionalmente relacionados) y prácticas | Raue 2009 | RES (Crossref) | Respaldada. |
| Estabilidad de cantidades derivadas pese a la débil identificabilidad individual | Simpson y Maclaren 2024; Gutenkunst 2007; Kao y Eisenberg 2018; Roosa y Chowell 2019 | PREV (resúmenes, 2026-10-01 y encargo) | Respaldada a nivel de resumen; no releída hoy. |
| Parámetros individuales no interpretables como cantidades precisas | Tuncer y Le 2018; Roosa y Chowell 2019 | PREV (resumen) | Sin cambios; no releída hoy. |
| Identificabilidad y predictibilidad fraccionario/entero examinadas directamente | Kharazmi 2021 | PREV (resumen) | Sin cambios, como se pedía. |
| Marco más amplio de modelos epidémicos fraccionarios | Chen 2021 | REG | Sin cambios, como se pedía. Solo registro. |
| Angstmann, Henry y McGann (2016), carta de presentación | *Bull Math Biol* 78:468–499, «A Fractional Order Recovery SIR Model from a Stochastic Process» | REG (Crossref) + RES (Consensus) | **Existe y el título de la carta coincide.** El resumen critica los modelos con derivadas fraccionarias introducidas «ad hoc» y deriva el modelo de un proceso estocástico, lo que es coherente con la descripción de la carta. No se añade al manuscrito ni a la lista de referencias. |

**Nota sobre Area y «Caputo».** **[H]** En el texto completo, Area define la derivada de Riemann–Liouville como D^α, recuerda la de Caputo como ᶜD^α y escribe el sistema con un D^α sin etiquetar; resuelve con el esquema PECE de Adams–Bashforth–Moulton. El artículo no dice expresamente que el modelo use Caputo. La frase de la Introducción no menciona Caputo y se sostiene; en cambio, la ficha L3-02 de la matriz afirmaba que Area respaldaba un uso estándar de operadores de tipo Caputo, y se ha corregido.

---

## C. Pendientes justificados

- **[P] Chishtie et al. (2026): lectura íntegra.** Está tras suscripción y no hay copia abierta. Con el resumen no se puede afirmar con qué protocolo se hizo la comparación fraccionario/entero, ni qué métrica define la mejora del 22,1 % y 6,2 %. La redacción actual solo afirma lo que el resumen dice, y lo separa de la validación rolling-origin. Mientras no se lea el cuerpo, esta cita se sostiene solo a nivel de resumen. Dos detalles del resumen que el texto completo debería aclarar: los órdenes fraccionarios del artículo están en (0, 2], y el modelo tiene parámetros dependientes del tiempo.
- **[P] Rocha et al. (2020): ajuste con la frase.** El registro es correcto, pero no se ha leído el contenido. Se cita en la Introducción para «la tuberculosis sigue siendo un reto de salud pública en Brasil» junto con la OMS, y el artículo describe las características del Sinan. Puede que respalde mejor una frase sobre vigilancia que sobre carga de enfermedad. No se ha editado por no estar en el alcance; conviene decidir si se mantiene, se desplaza a la descripción de los datos o se retira.
- **[P] Resúmenes sin cuerpo.** Moran, Meshkat, Raue y Cramer se han contrastado con el resumen. Simpson y Maclaren, Gutenkunst, Kao y Eisenberg, Roosa y Chowell, Tuncer y Le, Kharazmi y Chen no se han releído en esta sesión. Si algún coautor o revisor discute alguna de ellas, hay que abrir el artículo.
- **[P] Diethelm 2013, OMS 2022 e IBGE 2013.** Solo registro (y la OMS y el IBGE ni eso: no tienen DOI en Crossref).
- **[P] Sin verificar en esta tarea:** la base de la afirmación de que Alzahrani no describe evaluación sobre observaciones reservadas procede de la lectura del PDF del 2026-10-01 (la ficha del editor solo confirma el resumen).
- **[P] Informes históricos que quedan desactualizados** (no editados, por regla): `docs/audits/CITATION_VERIFICATION_2026-10-01.md` y `CLAIM_AUDIT_2026-10-01.md` (describen las frases antes de la reparación, y la propuesta de la frase 3 incluye una afirmación de rolling-origin que no se ha adoptado); `literature_verification/LITERATURE_SEARCH_LOG.md` (cita «Pelissari et al.» y el DOI antiguo de Area); `literature_verification/MANUSCRIPT_MARKER_RESOLUTION.md` (afirma que Moran y Bracher respaldan la distinción ajuste/pronóstico); `docs/NOVELTY_AUDIT_DECISION.md` (describe a Chishtie como comparación fraccionario/entero con rolling-origin); `submission_bmb/STATE_FREEZE_2026-10-03.md` (dice que los autores de Alzahrani no estaban verificados; ahora lo están).
- **Fuera de alcance, ya anotado en `CLAIM_AUDIT_2026-10-01.md`:** discrepancia entre el resumen de `BMB_ABSTRACT.md` y el del manuscrito, ausencia de referencias a figuras y tablas en el cuerpo, y limitaciones L06, L07, L09 y L10. No se han tocado.

---

## D. Evidencia técnica

- **Rama de trabajo:** `fix/bmb-citation-repair-2026-10-08`, creada desde `origin/main`.
- **SHA de `origin/main` al empezar:** `b3ad21b` (`b3ad21bb059eb5357742693a4d5072107dc0df63`).
- **SHA de `origin/fedeg/exciting-bell-c6pdtp`:** `bea7188` (`bea7188728ccf625c4f250d891e9c3d839ce3454`).
- **Árbol de trabajo:** limpio al empezar.
- **Commits:** `06bf137`, `be0b83a` y `15c0cf4` (cherry-picks del título, sin conflictos); `67c1275` (dos informes de auditoría copiados); `67381ed` (manuscrito); `2779ade` (borradores y trazabilidad); `be598c1` (matriz y auditoría de referencias); `1543ced` (trazabilidad del paquete). Este informe va en un commit propio.
- **No incorporado:** el paquete de figuras y tablas de la rama exciting-bell.
- **`git diff --check`:** sin errores.
- **Ficheros modificados respecto a `origin/main`:** todos pertenecen a los apartados 4 a 6, más los dos informes copiados y este informe. `git diff` de `results_canonical/`, `outputs/`, `src/`, `scripts/`, `tests/`, `data/` y `manuscript/source/` está vacío, y no se ha tocado ningún fichero de figuras o tablas.
- **Tokens numéricos del manuscrito (antes y después, sin contar la lista de referencias):** solo cambian los años de citas eliminadas (2021 ×2, 2022 ×1, 2014 ×2) y se añaden 7, 14 y 21 (horizontes de Chishtie), 27 (Cramer), 2019 (Roosa y Chowell) y dos «19» de «COVID-19». Ningún resultado, métrica ni descriptor de horizonte cambia (`H_relax` = 0 frente a persistencia y SARIMA, 7 frente a seasonal naive).
- **Título corto:** aparece exactamente una vez en el manuscrito, la carta, `BMB_PACKAGING_TRACEABILITY.md` y dos veces en `BMB_TITLE_OPTIONS.md` (título principal y constante final); el título largo no aparece en ninguno ni en el resto del repositorio.
- **Tests (pytest instalado en esta sesión):** `tests/test_canonical_freeze.py`, 15 pasan; `tests/test_manuscript_architecture.py`, 8 pasan; `tests/test_repository_integrity.py`, 7 pasan. Total 30 de 30; ninguno falla ni quedó sin ejecutar.
- **Limitación de los tests:** son tests documentales y de integridad; no validan el contenido de las citas.

---

## E. Veredicto

**`PARTIAL_WITH_BLOCKERS`**

Se cumple todo lo que depende de la rama y de la validación (procedimiento de ramas, seis entradas verificadas, ninguna cita huérfana, ningún cambio en resultados, tests en verde). No se puede declarar `DOCUMENTARY_REPAIR_COMPLETE` porque la caracterización de Chishtie et al. (2026) descansa solo en su resumen, y quedan además dos puntos abiertos sobre citas usadas: Rocha (ajuste con la frase) y las citas de identificabilidad que no se han releído hoy. El manuscrito tampoco debe considerarse listo para envío: sigue teniendo marcadores `[AUTHOR INPUT REQUIRED]` y la disponibilidad de datos pendiente de confirmación de los autores.

**Siguiente paso concreto:** conseguir el texto completo de Chishtie et al. (2026) por acceso institucional y comprobar tres cosas: con qué protocolo se comparan el modelo fraccionario y los enteros, qué métrica define la mejora del 22,1 % y 6,2 %, y si la validación rolling-origin incluye al modelo entero. Con eso se podría cerrar la frase de la Introducción y subir el veredicto, una vez decidido también lo de Rocha.
