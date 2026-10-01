# Verificación de las citas de la Discusión (2026-10-01)

Alcance: las siete frases con cita de la Discusión de `submission_bmb/BMB_MANUSCRIPT.md` (15 referencias distintas). Como esta tarea destapó errores en la lista de referencias, se comprobaron también tres referencias de la Introducción.

Etiquetas: **[H]** hecho verificado en una fuente · **[I]** inferencia · **[P]** pendiente o no verificado.

---

## 1. Conclusión

**La Discusión no está lista para enviarse con las citas actuales.** Hay tres problemas de distinto tipo:

1. **Errores bibliográficos en 4 entradas** (Raue 2009, Meshkat 2014, Area 2015, Pelissari/Rocha 2020), más dos erratas menores. En Area, el DOI del manuscrito resuelve a otro artículo. La comprobación de referencias anterior (`REFERENCE_AUDIT.md`, «DOI audit passed») solo verificaba que cada referencia estuviera citada y listada con un DOI, no que el DOI correspondiera al artículo.
2. **Dos frases cuya cita no respalda lo que se afirma.** La primera (Bracher 2021; Cramer 2022) presenta como respaldado un resultado que es del propio estudio. La segunda (Moran 2016; Cramer 2022) apoya solo de forma tangencial. Las demás citas sostienen sus frases, algunas con matices que conviene declarar.
3. **Dos caracterizaciones de trabajos previos son más fuertes que lo que dicen las fuentes** (Alzahrani 2024 y Chishtie 2026). Conviene corregirlas aunque el manuscrito no reclame prioridad: una descripción inexacta de la literatura previa debilita justo el párrafo que defiende la contribución.

Ninguna corrección afecta a resultados. Todas son de redacción o de lista de referencias.

---

## 2. Cómo se verificó y qué límites tiene

**[H] Fuentes usadas.** Crossref para el registro bibliográfico de las 18 referencias; PubMed para los resúmenes de 13 de ellas (según PubMed; enlaces DOI en las tablas); PubMed Central para el **texto completo** de Kalizhanova 2024; la ficha del editor y el **PDF** de Alzahrani 2024. Scite requiere un plan de pago y no estuvo disponible.

**[P] Límites.**

- Para Bracher, Cramer, Moran, Kharazmi, Tuncer & Le, Roosa & Chowell, Meshkat, Raue, Gutenkunst, Simpson & Maclaren y Kao & Eisenberg, el veredicto de respaldo se basa en el **resumen**, no en el texto completo. Es suficiente para juzgar si la cita encaja con la frase, pero no para descartar matices del cuerpo del artículo.
- **Chishtie 2026** está tras suscripción (no está en PMC ni en Europe PMC como acceso abierto): solo se pudo leer el resumen.
- **Chen 2021**: solo se verificó el registro (título, autores, revista). No se leyó el contenido.
- No he leído el contenido de Area 2015 (la referencia correcta), Diethelm 2013 ni Pelissari/Rocha 2020, que son de la Introducción.

---

## 3. Registro bibliográfico

### Errores que hay que corregir

| Referencia | En el manuscrito | Registro verificado (Crossref, PubMed) |
|---|---|---|
| **Raue 2009** ([DOI](https://doi.org/10.1093/bioinformatics/btp358)) | Título: «…identifiability analysis of **partial differential equation models in systems biology**» | «Structural and practical identifiability analysis of **partially observed dynamical models by exploiting the profile likelihood**». *Bioinformatics* 25(15):1923–1929. El DOI y las páginas son correctos. |
| **Meshkat 2014** ([DOI](https://doi.org/10.1371/journal.pone.0110261)) | Tercer autor «Sullivant»; título «On finding identifiable parameter combinations in nonlinear dynamic systems» | Meshkat N, Kuo CE-Z, **DiStefano J**. «On finding **and using** identifiable parameter combinations in nonlinear dynamic **systems biology models and COMBOS: a novel web implementation**». *PLoS ONE* 9(10):e110261. El DOI es correcto. |
| **Area 2015** | Título «On a fractional order epidemic model with Caputo derivative»; *Applied Mathematics Letters* 40, 23–27; DOI 10.1016/j.aml.2014.09.006 | **Ese DOI es de otro artículo**: Mortici, Rassias y Jung, «The inhomogeneous Euler equation and its Hyers–Ulam stability», *Appl Math Lett* 40:23–28. La referencia correcta es Area I, Batarfi H, Losada J, Nieto JJ, Shammakh W, Torres Á. «On a fractional order **Ebola** epidemic model». *Advances in Difference Equations* 2015, 278. DOI [10.1186/s13662-015-0613-5](https://doi.org/10.1186/s13662-015-0613-5). |
| **Pelissari 2020** ([DOI](https://doi.org/10.5123/S1679-49742020000100009)) | Autores: Pelissari, Rocha, «Bartholomeu», Sanchez, Duarte, Arakaki-Sanchez, Diaz-Quijano; cita «Pelissari et al., 2020» | Primera autora **Rocha MS**; autores: Rocha, Bartholomay, Cavalcante, Medeiros, Codenotti, Pelissari, Andrade, Silva, Arakaki-Sanchez, Pinheiro. Título original en portugués. La cita en el texto debe ser **«Rocha et al., 2020»**. |

### Erratas menores

- **Cramer 2022:** el título dice «in the **United States**», no «in the US».
- **Roosa & Chowell 2019:** el título termina en «…infectious disease transmission **models**».

### Verificadas sin discrepancias

Alzahrani 2024 (autores comprobados en la ficha del editor), Bracher 2021, Chen 2021, Chishtie 2026 (el artículo existe: *Epidemics* 54:100887), Gutenkunst 2007, Kalizhanova 2024, Kao & Eisenberg 2018, Kharazmi 2021, Moran 2016, Simpson & Maclaren 2024, Tuncer & Le 2018, Diethelm 2013. Autores, revista, año, volumen y páginas coinciden con el registro.

**[H]** Las seis entradas con error están en la lista de referencias de `submission_bmb/BMB_MANUSCRIPT.md` y, con la cita completa errónea, en `literature_verification/LITERATURE_VERIFICATION_MATRIX.md` (Pelissari, Cramer, Area, Roosa, Meshkat y Raue). `manuscript_package/REFERENCE_AUDIT.md` solo guarda autor, año y DOI. `manuscript_draft/references.bib` contiene una única entrada (IBGE) y no es la fuente de la lista. Los borradores de `manuscript_draft/` y los ficheros de trazabilidad citan «Pelissari et al., 2020».

---

## 4. ¿Respalda cada cita lo que se afirma?

| Frase de la Discusión | Cita | Veredicto | Razón |
|---|---|---|---|
| «Restricting evaluation to the mechanistic family would have produced a substantially more favorable assessment…» | Bracher 2021; Cramer 2022 | **No respaldada** (Bracher) · **parcial** (Cramer) | La frase es un resultado de este estudio. Bracher ([DOI](https://doi.org/10.1371/journal.pcbi.1008618)) trata de la puntuación de intervalo ponderada para pronósticos probabilísticos y no habla de la elección de baselines. Cramer ([DOI](https://doi.org/10.1073/pnas.2113561119)) informa de que dos tercios de 27 modelos mejoraron un baseline ingenuo: respalda comparar con baselines, no esta frase. |
| «…must be evaluated separately» | Moran 2016; Cramer 2022 | **Débil** | Moran ([DOI](https://doi.org/10.1093/infdis/jiw375)) es una revisión sobre por qué el pronóstico epidémico es más difícil que el meteorológico (comportamiento humano, datos incompletos). No trata del diseño de la evaluación. |
| «Fractional and integer-order models have been compared under rolling-origin out-of-sample forecasting» | Chishtie 2026 | **No verificable más allá del resumen** | El resumen ([DOI](https://doi.org/10.1016/j.epidem.2026.100887)) informa de una mejora de «precisión predictiva» del modelo fraccionario frente a modelos enteros (22,1 % y 6,2 % en dos olas de COVID-19 en Canadá) y, por separado, de «rolling-origin cross-validation» a 7, 14 y 21 días. No dice que la comparación fraccionario/entero se hiciera con rolling origin. Requiere el texto completo. |
| «Fractional SEIR forecasts have been compared with ARIMA forecasts in influenza» | Alzahrani 2024 | **Parcial** | Ver §5. |
| «TB-specific work has shown that SARIMA can outperform a mechanistic SIR model under temporal validation» | Kalizhanova 2024 | **Respaldada, con matices** | Texto completo leído. SARIMA entrenado con 2014–2018 y evaluado en 2019; SIR entrenado con 2014–2017 y evaluado en 2018–2019. Los autores concluyen que SARIMA tiene «clear superiority» en RMSE, MAE, MAPE y R². Matices: es un SIR básico con parámetros constantes (R₀ ≈ 0,26–0,30), una sola partición entrenamiento/prueba y **ventanas de evaluación distintas** para los dos modelos. |
| «Fractional/integer predictability and identifiability have been examined directly» | Kharazmi 2021 | **Respaldada** (resumen) | Analiza modelos de orden entero y fraccionario con redes PINN, con identificabilidad estructural y práctica e incertidumbre del pronóstico ([DOI](https://doi.org/10.1038/s43588-021-00158-0)). |
| «…within the broader fractional epidemic-modeling literature reviewed by Chen et al.» | Chen 2021 | **Respaldada** (solo registro) | Título y revista coinciden. No se leyó el contenido. |
| «…should not be interpreted as precise epidemiological quantities» | Tuncer & Le 2018; Roosa & Chowell 2019 | **Respaldada** | Tuncer & Le ([DOI](https://doi.org/10.1016/j.mbs.2018.02.004)) concluyen que ninguno de los modelos simples (SIR, SEIR, SITR) es prácticamente identificable a partir de la incidencia acumulada, que es el tipo de dato de este estudio. Roosa & Chowell ([DOI](https://doi.org/10.1186/s12976-018-0097-6)): los problemas de identificabilidad son más probables en modelos más complejos. |
| «…compensating parameter variation that preserves a composite functional» | Meshkat 2014; Raue 2009 | **Parcial** | Meshkat ([DOI](https://doi.org/10.1371/journal.pone.0110261)) trata la identificabilidad **estructural** y las combinaciones identificables; este estudio es de identificabilidad **práctica**. Raue ([DOI](https://doi.org/10.1093/bioinformatics/btp358)) respalda el uso del perfil de verosimilitud y de parámetros «funcionalmente relacionados». |
| «…useful predictions or composite quantities can remain stable despite poorly identified parameters» | Simpson & Maclaren 2024; Gutenkunst 2007; Meshkat 2014; Kao & Eisenberg 2018 | **Respaldada** | Gutenkunst ([DOI](https://doi.org/10.1371/journal.pcbi.0030189)): el ajuste colectivo da predicciones bien acotadas aunque los parámetros individuales estén mal acotados. Kao & Eisenberg ([DOI](https://doi.org/10.1016/j.epidem.2018.05.010)): R₀ se estimó con éxito en todo el rango de parámetros no identificables. Simpson & Maclaren ([DOI](https://doi.org/10.1007/s11538-024-01294-0)): predicciones con modelos mal identificados. **Roosa & Chowell** también lo apoya de forma directa (R₀ robusto a los problemas de identificabilidad individuales) y no se cita en esa frase. |

---

## 5. Alzahrani 2024 con más detalle

**[H]** Leí el PDF del artículo. Datos: casos semanales de gripe en Arabia Saudí, 305 semanas (2017–2022). La comparación de la Tabla 4 es la RMSE y el MAE de los dos modelos. El texto dice que el SEIR fraccionario «fits the observed data better than the ARIMA model» y habla de «degrees of fit». ARIMA(2,0,1) produce además una proyección de 30 semanas, pero **no se describe una evaluación sobre observaciones reservadas ni un rolling origin**.

**[H]** La Tabla 4 da un **MAE idéntico (4,26814) para los dos modelos** y RMSE de 0,3625 (fraccionario) frente a 2,788 (ARIMA). Un MAE igual a cinco decimales en dos modelos distintos, con RMSE muy distintos, es incoherente; parece un error de la tabla del propio artículo.

**[I]** El manuscrito dice «fractional SEIR forecasts have been compared with ARIMA forecasts». Lo que respalda la fuente es una comparación de ajuste, no de pronóstico fuera de muestra. Además, **ese artículo concluye lo contrario** que el nuestro (el fraccionario supera a ARIMA). Un revisor puede preguntar por qué los resultados difieren, y la Discusión no lo menciona.

---

## 6. Redacciones propuestas (para `BMB_MANUSCRIPT.md`)

**Frase 1** (quitar las citas, porque el resultado es de este estudio, y apoyar solo el principio general):
> Restricting evaluation to the mechanistic family would therefore have produced a substantially more favorable assessment of predictive performance than the broader benchmark set. Comparison with a naive baseline is a standard component of forecast evaluation; in a large multi-model evaluation of COVID-19 mortality forecasts, only two thirds of 27 models were more accurate than such a baseline (Cramer et al., 2022).

**Frase 2:**
> … show why within-family mathematical improvement and forecasting utility must be evaluated separately. Epidemic forecasting must also contend with incomplete data and changing human behavior (Moran et al., 2016).

**Frase 3** (precisión sobre los trabajos previos; la parte de Chishtie debe comprobarse con el texto completo antes de enviar):
> Fractional and integer-order models have been compared on COVID-19 data, with rolling-origin validation reported for the fractional model (Chishtie et al., 2026); a fractional SEIR model was reported to give lower RMSE than ARIMA for influenza in Saudi Arabia, without a described out-of-sample protocol and in the opposite direction to the present results (Alzahrani et al., 2024); and a basic SIR model was outperformed by SARIMA on held-out tuberculosis data from Kazakhstan under a single train–test split (Kalizhanova et al., 2024).

**Frase 6** (precisar el tipo de identificabilidad):
> This pattern is compatible with compensating parameter variation that preserves a composite functional even when its components are weakly identified (for structural analogues, Meshkat et al., 2014; for profile-based detection, Raue et al., 2009).

**Frase 7:** añadir Roosa & Chowell (2019) a las citas.

**Lista de referencias:** sustituir las entradas de Raue, Meshkat, Area y Pelissari (que pasa a «Rocha et al., 2020» y se reordena alfabéticamente), y corregir las erratas de Cramer y Roosa, según las tablas del §3. En la Introducción, la frase «A close fit … (Moran et al., 2016; Bracher et al., 2021)» tiene el mismo problema que las frases 1 y 2: Bracher trata de métricas de evaluación y no respalda la afirmación sobre la fiabilidad de pronóstico de los ajustes cercanos.

---

## 7. Pendiente

- **[P]** Leer el texto completo de **Chishtie 2026** (acceso por la universidad) y confirmar si la comparación fraccionario/entero se hizo con rolling origin. Hasta entonces la frase 3 debe quedar con la redacción prudente.
- **[P]** Verificar con el texto completo las citas que solo se han contrastado con el resumen, si algún coautor o revisor las discute.
- **[P]** Comprobar que **Area et al. (2015)**, el artículo correcto sobre el modelo fraccionario del Ébola, respalda la frase de la Introducción donde se cita.
- **[P]** Sincronizar con las correcciones la lista de `BMB_MANUSCRIPT.md`, `LITERATURE_VERIFICATION_MATRIX.md`, `REFERENCE_AUDIT.md` (la fila de Pelissari) y los borradores. Si el paquete LaTeX necesita un `.bib` completo, hay que crearlo ya con las entradas corregidas.
