# Auditoría de claims — paquete BMB (2026-10-01)

Estado del repositorio auditado: HEAD `c8cd5df` (rama de trabajo `fedeg/exciting-bell-c6pdtp`, idéntica a `main`).
Documentos auditados: `submission_bmb/BMB_MANUSCRIPT.md`, `submission_bmb/BMB_ABSTRACT.md`, `submission_bmb/BMB_COVER_LETTER.md`.
Evidencia de referencia: `results_canonical/` y, para trazar cifras hasta su origen, `outputs/` e `IDENTIFIABILITY_AUDIT_REPORT.md`.

Etiquetas: **[H]** hecho verificado contra un fichero del repositorio · **[I]** inferencia · **[Hip]** hipótesis no verificada · **[R]** recomendación · **[P]** pendiente.

---

## 1. Conclusión

Las cifras del manuscrito son correctas y los claims centrales están bien acotados. No he encontrado ningún número que no coincida con los CSV congelados, y los tres claims de pronóstico (mejora dentro de la familia, skill negativo frente a persistencia y SARIMA, skill positivo frente a seasonal naive hasta h=7) se reproducen exactamente.

Los defectos están en lo que el texto **no dice** o atribuye de forma imprecisa, no en lo que afirma. Hay tres que conviene corregir antes de enviar: (A) σ está pegado a su cota inferior en todas las soluciones del conjunto admisible, y eso condiciona la envolvente de R0 sin que el manuscrito lo declare; (B) las cifras de dispersión de β, γ y d proceden de 5 semillas, pero se presentan como de «multiseed y perfil»; (C) el comparador entero está limitado por las cotas en 5 de 5 semillas, y el brazo de sensibilidad de γ que el texto menciona no se ejecutó, mientras que el Abstract y la Discusión atribuyen la mejora a «la diferenciación fraccionaria».

Ninguna de las correcciones exige recalcular resultados. Todas son de redacción o de declaración de limitaciones, y entran en el trabajo permitido por `PROJECT_CANON.md`.

---

## 2. Qué se ha hecho y qué no

**Hecho.** Se recalcularon las 144 habilidades (12 horizontes × 2 métricas × 3 baselines × 2 modelos) a partir de los errores y coinciden con `table_skill_by_horizon.csv` (diferencia máxima 7·10⁻¹⁶). Se comprobó que las 22 cifras de la sección 3.1–3.2 del manuscrito están en los CSV congelados. Se contrastó cada claim de `claim_support_table.csv` con el texto. Se rastrearon las cifras de identificabilidad hasta `outputs/` y se verificó que no hay cambios en `src/`, `scripts/`, `tests/`, `outputs/`, `results_canonical/` ni `data/` entre `13015847` y HEAD (62 commits, todos de documentación y procedencia).

**No hecho.**

- No he re-ejecutado el pipeline (calibración con evolución diferencial, rolling origin). La auditoría verifica trazabilidad texto→CSV y coherencia interna, no reproducibilidad computacional.
- No he leído `PRE_SUBMISSION_CLAIM_AUDIT.md` (para no anclarme en él) ni `bd4b744`.
- No he verificado contra los textos originales qué dicen los artículos citados. Las citas de la Discusión (Chishtie 2026, Alzahrani 2024, Kalizhanova 2024, Kharazmi 2021) quedan como **[P]**.

---

## 3. Estado de cada claim

| Claim | Estado | Comentario |
|---|---|---|
| C01 Fraccionario < entero | **Verificado, con reservas** | Cierto en los 12 horizontes (RMSE y MAE) y en el open-loop. Ver hallazgo C sobre cotas y atribución. |
| C02 Persistencia | **Verificado** | Skill negativo en 24 de 24 (horizonte × métrica). |
| C03 SARIMA | **Verificado** | Skill negativo en 24 de 24. |
| C04 Seasonal naive h=1..7 | **Verificado, con reserva** | Correcto, pero el margen en h=7 es de 2,7 %. Ver hallazgo D. |
| C05 Mejora operativa general | **Verificado como no soportado** | El manuscrito no lo afirma. |
| C06 α<1 no prueba memoria | **Verificado** | Redacción conforme. |
| C07 R0 1,1542–1,1892 | **Verificado, con reservas** | Cifras exactas; la envolvente depende de σ en cota (hallazgo A) y de la rejilla de perfil. |
| C08 DFE inestable 25/25 | **Verificado, redundante** | Es consecuencia de R0>1 (hallazgo F). |
| C09 β, γ, d débilmente identificables | **Verificado, con defecto de atribución** | Hallazgo B. |
| C10 48 % control óptimo | **Verificado** | El manuscrito lo excluye explícitamente. |
| C11 Sin inferencia estadística | **Verificado** | §2.12 es coherente con L11. |

---

## 4. Hallazgos, por prioridad

### A. σ está en su cota inferior en todo el conjunto admisible — prioridad alta

**[H]** El espacio de búsqueda de σ es [0,01; 0,50] mes⁻¹. En las 5 semillas fraccionarias σ vale 0,01002–0,01015 (entre 0,2 % y 1,5 % sobre la cota); en las 5 enteras, 0,01000–0,01017. En los 20 puntos de perfil que entran en la banda ≤1 %, σ está entre 0,01001 y 0,01020. Es decir, **las 25 soluciones del conjunto admisible tienen σ pegado a la cota**. Fuentes: `outputs/calibration/{fractional,integer}_multiseed.csv`, `outputs/identifiability/profile_objective.csv`.

**[H]** `docs/METHOD_DECISION_LOG.md` (D019) y `docs/EXTERNAL_PARAMETER_CONTRACT.md` exigen que la limitación estructural de σ se declare «dondequiera que σ o una expresión de R0 que contenga σ se interprete». El manuscrito solo dice en §2.3 que la estructura de un único compartimento expuesto es «una simplificación epidemiológica», y no repite el caveat en los apartados de R0 (§3.3, §4, Abstract, Conclusión).

**[I]** Con σ prácticamente constante, el factor σ/(σ+μ) es casi constante (≈0,90) y R0 ≈ 0,90·β/(γ+μ+d). La estabilidad de R0 queda reducida al cociente β/(γ+μ+d), que es lo que β y γ preservan al covariar. La estrechez de la envolvente es real, pero no es independiente de que σ esté fijado por la cota, y R0 es una cantidad condicional a esa estructura.

**[R]** Añadir en §3.3 y en la Discusión: «In all 25 admissible solutions σ lay within 2% of its lower search bound (0.0100–0.0102 month⁻¹); the R0 envelope is therefore conditional on that boundary value and on the single-compartment latent structure, and is not an estimate of R0 for tuberculosis in Brazil.»

### B. Las cifras de dispersión de β, γ y d proceden de 5 semillas — prioridad alta

**[H]** El manuscrito (§3.3) escribe que «across multiseed optimization and one-dimensional profile-objective evaluations» la RMSE de calibración varió entre 605,049 y 610,388 (CV 0,35 %), β por un factor ≈5,4 (CV 58,0 %), γ ≈5,3 (CV 59,9 %) y d en más de dos órdenes de magnitud (CV 82,2 %). Esos valores son exactamente los de las **5 semillas** (`fractional_multiseed.csv`; `parameter_robustness.csv`). El rango de RMSE 605,049–610,388 es el de las semillas, no el del conjunto de perfil.

**[H]** Para los 25 miembros del conjunto admisible las cifras son otras: β 5,94×, γ 5,72×, d 210× (`outputs/identifiability/near_equivalent_solution_bands.csv`, banda ≤1 %). El mismo desliz está en `claim_support_table.csv` (C09, «across near-equivalent solutions») y en `KNOWN_LIMITATIONS.md` (L02).

**[I]** Los CV de 58–82 % se calculan sobre 5 valores. Es válido como descriptor, pero el texto debe decir n=5.

**[H]** Además, el perfil de γ no muestra subida de RMSE dentro de la rejilla probada [0,053; 0,203], y la rejilla nunca llega al 40 % exterior de cada rango (`IDENTIFIABILITY_AUDIT_REPORT.md` §5 y §10). **[I]** Por tanto 5,72× es una cota inferior de la dispersión de γ impuesta por la rejilla, no por los datos.

**[R]** Reescribir: «Across the five multiseed solutions (n = 5), calibration RMSE ranged from 605.049 to 610.388 (CV 0.35%) while β varied by a factor of 5.4, γ by 5.3 and d by more than 100. Within the 25-member admissible set the ranges were 5.9, 5.7 and 210; the γ range is limited by the profile grid rather than by the objective.»

### C. Comparador entero limitado por cotas; brazo de γ no ejecutado; atribución causal — prioridad media-alta

**[H]** En las 5 semillas del comparador entero, γ queda entre 0,0504 y 0,0576 (cota inferior 0,05) y σ en la cota (arriba). `BASE_MODEL_REIMPLEMENTATION_REPORT.md` §8 lo registra como «patrón notable», y en §9 atribuye la deriva del entero a «a near-lower-bound gamma producing an overly persistent decline». El entero infrapredice los 24 meses de validación (`validation_residual_signs.csv`: 0 de 24 positivos; por eso MAE = |sesgo| = 1588,649).

**[H]** La RMSE de calibración es 605,05 (fraccionario) frente a 776,06 (entero) (`calibration_metrics.csv`). **El manuscrito no reporta la calibración del entero**, que es lo que sostiene la afirmación de «comparación justa».

**[H]** §2.3 dice que γ ∈ [0,01; 0,50] se conserva «as a sensitivity arm». `docs/METHOD_DECISION_LOG.md` D017 lo declara «mandatory sensitivity-analysis comparison arm». **En `outputs/sensitivity/` solo existe el brazo de α**, y no hay script para el de γ. Para α el texto dice «evaluated»; para γ dice «retained». La diferencia es correcta, pero un lector entenderá que existe.

**[H]** El Abstract del manuscrito dice «fractional differentiation improved forecast error within the SEIT family» y la Discusión «Caputo fractional-order differentiation consistently reduced observed forecast error». `BMB_ABSTRACT.md` dice «Fractional differentiation provided within-family error reduction».

**[I]** La evidencia respalda que *el modelo fraccionario ajustado* tiene menor error que *el modelo entero ajustado bajo las mismas cotas*. No respalda atribuir la diferencia al operador de derivación, porque el entero está acotado por γ y σ y no se ha explorado qué pasa al relajar γ. Con α≈0,962, cercano a 1, el efecto atribuible al operador es especialmente difícil de aislar.

**[R]** (1) Sustituir la atribución al operador por «the fractional formulation attained lower observed error than the independently refitted integer comparator under the frozen primary bounds». (2) Reportar la RMSE de calibración de ambos modelos y decir que en el entero γ y σ están en sus cotas. (3) Cambiar «retained as a sensitivity arm» por «not executed in this study».

**[P]** Decisión de autor, no mía: ejecutar el brazo de γ activaría la política de reapertura solo si se quiere mantener la atribución al operador. Con la redacción de (1) no hace falta. Mi recomendación es no ejecutarlo y declarar la limitación.

### D. H_relax = 7 tiene un margen de 2,7 % — prioridad media

**[H]** En h=7 el skill RMSE frente a seasonal naive es +0,0274 y el MAE +0,0275. En h=8 pasa a −0,074. El manuscrito lo presenta correctamente como descriptor.

**[I, indicativo]** La RMSE de validación a 24 meses varía entre −4,7 % y +4,4 % respecto de la semilla primaria al cambiar de semilla (1065,3–1167,6 frente a 1118,0). Son medidas distintas de las de h=7 del rolling origin, por lo que no es una comparación directa, pero el orden de magnitud sugiere que el límite exacto en h=7 está dentro del ruido del optimizador. Cada origen usa una única semilla (`rolling_origin_predictions.csv`, 13 orígenes).

**[R]** Mantener «h=1..7» (es lo que dicen los datos), pero añadir el margen y la salvedad de semilla única, y evitar titulares como «siete meses» (ya prohibido por `claim_support_table.csv`, C04).

### E. La ventana de evaluación sigue a una caída y un rebote de la serie — prioridad media

**[H]** Totales anuales de la serie (calculados de `outputs/calibration/` y `outputs/validation/`): 2019 = 96 184; 2020 = 86 414 (−10,2 %); 2021 = 91 776 (+6,2 %); 2022 = 101 806 (+10,9 %). El sesgo medio es negativo en todos los horizontes para los cinco métodos, incluidos persistencia, seasonal naive y SARIMA (`table_forecasting_by_horizon.csv`).

**[I]** Los pronósticos de todos los métodos infrapredicen de forma sistemática en una ventana en la que el nivel sube. Las comparaciones de skill son condicionales a ese cambio de nivel.

**[Hip]** Que el origen sea la perturbación asociada a la COVID-19 es una hipótesis que no he contrastado, y el texto debe mantenerse descriptivo.

**[H]** Ni `KNOWN_LIMITATIONS.md` (L06 solo habla de la longitud de la ventana) ni el manuscrito mencionan este cambio de nivel.

**[R]** Añadir a las limitaciones: «The evaluation window (2021–2022) follows a 10.2% fall in annual notifications in 2020 and a rebound in 2021–2022; all methods, persistence included, showed negative mean bias at every horizon, so the comparisons are conditional on this level shift.»

### F. La inestabilidad del DFE es una consecuencia de R0 > 1 — prioridad baja

**[H]** Los márgenes angulares de Matignon en el conjunto admisible van de −1,5199 a −1,5093 rad (`dfe_stability_by_evidence_set.csv`). Con α entre 0,9608 y 0,9676 ese rango equivale a −απ/2.

**[I]** Eso indica |arg λ| ≈ 0, es decir, un autovalor real positivo. Para un sistema con R0 > 1 el jacobiano en el DFE siempre tiene un autovalor real positivo, y la inestabilidad se sigue con independencia de α. La comprobación de Matignon es una verificación de consistencia, no un resultado adicional.

**[R]** El Abstract y la Conclusión presentan «uniform local instability» como una segunda propiedad derivada robusta. Añadir una frase: «Because R0 > 1 for each solution, instability follows irrespective of α.» No altera ningún número.

### G. Limitaciones documentadas que el manuscrito no recoge — prioridad baja

**[H]** Frente a `KNOWN_LIMITATIONS.md`, el párrafo de limitaciones de la Discusión cubre L01–L04, L08 y L10–L12. Faltan **L05** (solo mencionada en §2.3), **L06** (ventana de validación de 24 meses), **L07** (13 orígenes como muestra pequeña) y **L09** (autocorrelación serial significativa de los residuos del open-loop; Ljung-Box p<0,001 en las cuatro series).

**[H]** L10 dice que la dependencia serial de los errores de pronóstico «no se ha caracterizado». Existe `outputs/forecasting/forecast_error_acf.csv` (generado el 2026-08-15, antes de la congelación), con ACF de lag 1 de hasta 0,69 (fraccionario, h=1) y 0,55 (SARIMA, persistencia, seasonal naive), marcada como «diagnostic only». L10 está desactualizada respecto de ese fichero. §2.12 del manuscrito es correcta («not formally characterised in the prespecified evaluation protocol»).

**[R]** Incluir L06, L07 y L09 en el párrafo de limitaciones. No tocar `results_canonical/KNOWN_LIMITATIONS.md` (evidencia congelada); registrar la discrepancia de L10 en una nota de erratas.

### H. A h=12 persistencia y seasonal naive son el mismo pronóstico — prioridad baja

**[H]** Los errores son idénticos a h=12 (RMSE 1152,958; MAE 1016,154). A ese horizonte los «tres baselines» son dos distintos. No afecta a ningún claim, pero conviene una nota al pie si se muestra una tabla por horizonte.

### I. Coherencia del paquete — prioridad variable

- **[H] Dos resúmenes distintos.** `BMB_ABSTRACT.md` (243 palabras, declara `DESK_REVIEW_INTEGRITY = PASS`) y el resumen de `BMB_MANUSCRIPT.md` (≈208 palabras con recuento simple) no coinciden en el texto. El del manuscrito es más cauto («comparatively stable», sin «functionally robust»). **[R]** Declarar canónico el del manuscrito y alinear el otro.
- **[H] El manuscrito no contiene ninguna referencia a figuras ni a tablas** (0 apariciones de «Figure»/«Table»), aunque `BMB_FIGURE_TABLE_PACKAGE.md` y `results_canonical/06_figures/` existen. **[P]** Pendiente de producción.
- **[H] Commit congelado.** `13015847a6f364505391d4f6e24d9c4c994669ff` existe en GitHub (no estaba en el clon porque era superficial; ya traído con `git fetch --unshallow`). Es un commit de documentación («assemble master manuscript package»; añade 4 ficheros de `manuscript_package/`). Como identifica un árbol completo, es válido como punto de congelación, y se ha verificado que `src/`, `scripts/`, `tests/`, `outputs/`, `results_canonical/` y `data/` son idénticos en HEAD. **[R]** Que la declaración diga «tree at commit …» en lugar de sugerir que el commit modificó código.
- **[H] `CANONICAL_EVIDENCE_MANIFEST.csv` no contiene hashes** y, por las comas sin entrecomillar en la columna `notes`, el CSV tiene filas con más campos que cabecera. Los 31 paths existen. Se adjunta abajo un baseline sha256 de los 18 ficheros de `results_canonical/` en HEAD.
- **[P] Carta de presentación.** Cita a Angstmann, Henry y McGann (2016) como precedente en el *Bulletin*, pero esa referencia no aparece en `REFERENCE_AUDIT.md` ni en `references.bib`. No la he verificado externamente.
- **[H] Procedencia de datos.** Los «4 configuraciones, la más cercana difiere en 99 meses» coincide con `provenance/datasus/C1_ACCESS_LOG.md` y `DATA_PROVENANCE.md` (C2–C4 difieren en los 264).

---

## 5. Qué decide el autor

1. **Aplicar las redacciones A–F** al manuscrito y al resumen (trabajo documental, sin tocar resultados).
2. **Brazo de sensibilidad de γ:** no ejecutar y declarar como no ejecutado (recomendado), o ejecutarlo bajo la política de reapertura.
3. **Qué parte de A, B y C se consulta con Amaury** antes de enviar. Esta auditoría no sustituye su revisión final.

---

## 6. Aplicación de las redacciones (2026-10-01)

Autorizada por el autor en la sesión. Ficheros modificados: `submission_bmb/BMB_MANUSCRIPT.md`, `submission_bmb/BMB_ABSTRACT.md` y `submission_bmb/BMB_COVER_LETTER.md` (una frase). No se ha modificado nada en `results_canonical/`, `outputs/`, `src/` ni `data/`.

| Hallazgo | Aplicado en |
|---|---|
| A (σ en cota) | §2.3 (viñeta de σ), §3.3, Discusión, Abstract, Conclusión, carta |
| B (n=5 frente a 25) | §3.3 (primer párrafo) |
| C (cotas, calibración del entero, brazo de γ, atribución) | §2.3 (viñeta de γ), §3.1, Abstract, Discusión (primer párrafo y limitaciones) |
| D (margen en h=7, semilla única) | Abstract, §3.2, Discusión |
| E (caída de 2020 y sesgo negativo) | §3.2, Discusión (limitaciones) |
| F (DFE se sigue de R0>1) | §2.7, §3.3, Discusión, Abstract, Conclusión |
| G (L06, L07, L09) | Discusión (limitaciones) |
| H (h=12) | §3.2 |
| I (dos resúmenes) | `BMB_ABSTRACT.md` alineado; texto idéntico al del manuscrito (228 palabras, recuento simple) |

**No aplicado, por requerir decisión o fuera de alcance:**

- ~~Referencias a figuras y tablas en el manuscrito~~: preparadas el 2026-10-01 (ver más abajo).
- Referencia de Angstmann et al. (2016) en `REFERENCE_AUDIT.md` y `references.bib`.
- Verificación de las citas de la Discusión contra los textos originales.
- Redacción de la declaración de disponibilidad de código («tree at commit …»).
- Nota de erratas para L02 y L10 de `results_canonical/KNOWN_LIMITATIONS.md` y para C09 de `claim_support_table.csv`, que son evidencia congelada y no se editan.
- Los borradores `manuscript_draft/*.md` no se han actualizado: la fuente canónica es `submission_bmb/BMB_MANUSCRIPT.md`, y los borradores han quedado desfasados respecto de ella.
- El brazo de sensibilidad de γ no se ejecuta; se declara como no ejecutado.

### Figuras, tablas y material suplementario (2026-10-01)

Se insertaron en `BMB_MANUSCRIPT.md` las llamadas y los bloques de Figuras 1–3 y Tablas 1–2, y se generó `BMB_SUPPLEMENTARY_INFORMATION.md` (Figura S1, Tablas S1A–S5). El detalle, las correcciones al paquete anterior y las comprobaciones están en `submission_bmb/BMB_FIGURE_TABLE_PACKAGE.md`. Hallazgos que motivaron regenerar las figuras: resolución de 120 ppp, línea gris sin leyenda en F3 que sugería una envolvente más ancha, y una leyenda que tapaba el título del eje. Además, las leyendas de la Tabla 1 y de la Tabla S3 del paquete anterior no coincidían con el contenido real de los CSV congelados. Las figuras y tablas se regeneran con `scripts/build_bmb_figures.py` y `scripts/build_bmb_tables.py`, que abortan si un valor difiere de los resúmenes congelados.

---

## Anexo — baseline sha256 de `results_canonical/` en HEAD `c8cd5df`

Este baseline permite detectar cambios futuros en la evidencia congelada. No sustituye al «digest de digests» de otra máquina, cuyo método desconozco.

```
7dd27f038cf2ab367187d5a61a57b19f75b2fc4d7c0acc59a8450280c4b783fb  results_canonical/00_manifest/CANONICAL_EVIDENCE_MANIFEST.csv
edf23fea30b24dcb2839c5e43ed48b09905b7cecf91a122d73a78aff8ed19ff6  results_canonical/01_model_contract/table_model_contract_status.csv
8e517202cf335cc79a40d16487502ec9d78c1d549dc419cdd2b88cd743cbfd13  results_canonical/02_identifiability/table_full_profile_diagnostic.csv
92e935d7c969e3e1fb2229074243350510041561cbbc989e3d869553933b26c5  results_canonical/03_R0_stability/table_R0_stability_summary.csv
b1524b93fbf7123615689374499f876b63aba73ae419dba8d4e699e750269cff  results_canonical/04_long_open_loop/table_long_open_loop.csv
9d2e55c5b3e9349436479e591eb328dee2df9aa133d85cf0964071e0f4862eee  results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv
3683e654c24ad4e617208bb9a455ffcd74f80b45464a293a8a76fcbd1c96d950  results_canonical/05_rolling_origin/table_horizon_summary.csv
1fb3370fca4b319b5a3d87a32e4d20f8e6d264f166f606c08203e205f2160db1  results_canonical/05_rolling_origin/table_skill_by_horizon.csv
a791d0567f8e4fadc918938633ce1f73cf4fc9e7cf4bfc8cbcf5ae67fb7657a2  results_canonical/06_figures/F1_rmse_vs_horizon.png
b05310258bbbaf6a4853d0a9ca0265a4a628e93f096bb515f1dcceae2b22f5ae  results_canonical/06_figures/F2a_skill_rmse_vs_horizon.png
a9d3220c12198825943836e6755e62665d5ee8b0f97818068cb1b12bf6ad175a  results_canonical/06_figures/F2b_skill_mae_vs_horizon.png
c3d40c45f9bf53d4208895121b8b35628972a7994bf63441baa908ff336dde02  results_canonical/06_figures/F3_R0_near_equivalent_envelope.png
538372ebb7e0f097b6298c9e56dfc5ed37ddb3da8b5430b57d0959322bb9139b  results_canonical/06_figures/F4_bias_vs_horizon.png
0087f447c04d867412eca792d9d3ead52164c2e753ed5a1957c762ed1c098ed1  results_canonical/07_claim_support/claim_support_table.csv
27df73cc6cd5aec41994120246562ccd4a629a77ab04c5b4670f155d10ef5a96  results_canonical/EVIDENCE_FREEZE_REPORT.md
9b4b5fc3be3578cfa36e06a93035a34c4fb5b179603a0af28eff9191fbbf0ab9  results_canonical/KNOWN_LIMITATIONS.md
3f47f7acc147254502b9a79154b0e9668468d203e51ac154a828ad16c4d8b557  results_canonical/RESULT_SET_FREEZE.md
d97059a016bb05aeaf1a4c0fcae98a750b3a41976e03b0f76c193f9104de534c  results_canonical/RESULT_STORYBOARD.md
```
