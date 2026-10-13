# Búsqueda de destino: revistas de modelización y simulación (2026-10-13)

Continúa `JOURNAL_CORPUS_AUDIT_AMC_ND_2026-10-13.md`. Cambia el criterio: ya no se busca una revista de matemáticas, sino una que valore la validación, la comparación predictiva y los límites de los modelos mecanicistas sin exigir teoría ni algoritmo nuevos. Se mantienen dos condiciones: la pregunta científica del manuscrito no cambia, y la publicación debe poder hacerse por suscripción, sin APC obligatorio.

Etiquetas: **[H]** hecho verificado · **[I]** inferencia · **[P]** pendiente.

## 1. Decisión

**Primera candidata: Mathematics and Computers in Simulation (MATCOM).** Segunda: Simulation Modelling Practice and Theory (SIMPAT). Journal of Simulation queda descartada para este manuscrito. Las razones están en la §3.

## 2. Evidencia

### 2.1 Modelo de publicación

**[H]** La lista oficial de APC de Elsevier (`article-publishing-charge.xlsx`, «Prices as of date: 05-Oct-2026», descargada de https://legacyfileshare.elsevier.com/els_com_pricing/article-publishing-charge.xlsx) clasifica las tres revistas de Elsevier como «Hybrid Open Access». La columna de APC solo se aplica si los autores eligen acceso abierto:

| ISSN | Revista | Modelo | APC en acceso abierto opcional (EUR) |
|---|---|---|--:|
| 0378-4754 | Mathematics and Computers in Simulation | Hybrid Open Access | 2750 |
| 1569-190X | Simulation Modelling Practice and Theory | Hybrid Open Access | 2710 |
| 0096-3003 | Applied Mathematics and Computation | Hybrid Open Access | 3040 |

**[P]** Journal of Simulation (Taylor & Francis): la página de la revista devuelve 403. Que la opción sin acceso abierto no tenga cargos es información aportada por el autor, no verificada aquí.

### 2.2 Alcance oficial (Elsevier Shop, consultado el 2026-10-13)

- **[H] MATCOM:** foro de información actualizada sobre herramientas matemáticas «as they apply to the dynamics of systems, their simulation and scientific computation in general». No exige ningún tipo de contribución concreto y no menciona la epidemiología.
- **[H] SIMPAT:** acepta artículos sobre cualquier aspecto de la simulación y la modelización de sistemas, pero «must significantly contribute to modelling and simulation in general». Los artículos de aplicación deben dejar claros el desarrollo, la implementación y la validación del modelo. Menciona «methods and algorithms for validation and verification», el análisis de sensibilidad y la ingeniería biomédica, y no la epidemiología.

### 2.3 Precedentes en el corpus

- **[H, resumen leído por el autor en ScienceDirect] Zhao, Y., Wu, H., Li, M. Y. y Lou, J. (2026). Model selection and parameter identification analysis in epidemiological models. *Mathematics and Computers in Simulation*, 239, 318–339. https://doi.org/10.1016/j.matcom.2025.05.012.** Crossref confirma el registro (volumen 239, enero de 2026). El artículo aplica métodos existentes (GWMCMC y criterios de selección de modelos) a modelos de COVID-19 anidados de una y dos variantes con datos del Reino Unido. Examina la identificabilidad estructural y práctica, la robustez paramétrica y la fiabilidad de las predicciones, y pronostica con el modelo seleccionado. Clasificación: **E/M**. La contribución principal es la evaluación, con un componente de formulación (el modelo de dos cepas).
- **[H, resumen] Chen et al. (2022), *MATCOM*** ([10.1016/j.matcom.2022.02.025](https://doi.org/10.1016/j.matcom.2022.02.025)): un modelo SEIR por tramos ajustado con datos de COVID-19 de EE. UU. y evaluado con métricas de error. Es de tipo **M**, pero confirma que MATCOM publica modelos epidémicos calibrados con datos reales.
- **[H, registro] SIMPAT:** precedentes de comparación de modelos y de credibilidad de reimplementaciones, ninguno epidemiológico: [10.1016/j.simpat.2023.102868](https://doi.org/10.1016/j.simpat.2023.102868) (microsimulación de tráfico; comparación de modelos y análisis de sensibilidad) y [10.1016/j.simpat.2016.12.013](https://doi.org/10.1016/j.simpat.2016.12.013) (comparación de resultados de simulación independiente del modelo; aporta una técnica propia). Consensus no devolvió ningún artículo epidemiológico de SIMPAT.
- **[H, resumen] Journal of Simulation:** sus artículos epidemiológicos recientes son modelos híbridos de eventos discretos, agentes y dinámica de sistemas ([10.1080/17477778.2025.2610014](https://doi.org/10.1080/17477778.2025.2610014), [10.1080/17477778.2025.2488485](https://doi.org/10.1080/17477778.2025.2488485)) y un marco nuevo para comparar modelos de simulación con datos ([10.1080/17477778.2025.2486664](https://doi.org/10.1080/17477778.2025.2486664)). No aparece ninguna evaluación de pronósticos con EDO.

### 2.4 Límites

- **[P]** La búsqueda se hizo con Consensus, y su preferencia por revista reordena los resultados pero no filtra. No es un censo del corpus.
- **[P]** No se hizo el sondeo sistemático de Crossref de las tres revistas, por decisión del autor.

## 3. Lectura

- **[I] MATCOM es la única de las tres con un precedente epidemiológico cuya contribución principal es la evaluación de modelos** (Zhao et al., 2026). Su alcance no impone un tipo de contribución, publica modelos epidémicos con datos reales y tiene vía de suscripción. El riesgo que queda es de nivel, no de tipo: Zhao et al. evalúan la selección y la identificabilidad, y el manuscrito evalúa si la ventaja dentro de la familia resiste referencias externas. El editor tendrá que ver en ello una contribución suficiente.
- **[I] SIMPAT** tiene la validación en su alcance, pero exige una contribución «significativa a la modelización y simulación en general» y no se ha encontrado ningún precedente epidemiológico. Es plausible como segunda opción si MATCOM rechaza.
- **[I] Journal of Simulation** está orientada a paradigmas (eventos discretos, agentes, dinámica de sistemas) que el manuscrito no usa. Queda descartada para este manuscrito.
- **[I] Material para la carta de presentación (no para el manuscrito sin decisión expresa):** varios artículos recientes con resumen leído en Consensus afirman que el modelo fraccionario supera al entero por su RMSE de ajuste o de pronóstico, sin referencias externas. Por ejemplo, Musafir et al. (2024), *Journal of Biosafety and Biosecurity*, [10.1016/j.jobb.2024.02.003](https://doi.org/10.1016/j.jobb.2024.02.003); Abdoon et al. (2024), *Symmetry*, [10.3390/sym16091126](https://doi.org/10.3390/sym16091126); y Alsubaie et al. (2024), *Symmetry*, [10.3390/sym16070929](https://doi.org/10.3390/sym16070929). El manuscrito responde exactamente a ese patrón de afirmación, y eso puede explicar al editor por qué la evaluación importa a quien construye estos modelos. Solo se ha leído el resumen; no se han verificado los diseños.

## 4. Reserva fuera de las tres candidatas

**[H, resumen] Karami et al. (2025), *Statistical Methods in Medical Research*** ([10.1177/09622802251387451](https://doi.org/10.1177/09622802251387451)): compara la estimación bayesiana y la frecuentista en modelos compartimentales por su capacidad predictiva, con MAE, RMSE y WIS en datos simulados e históricos. Es una evaluación pura (E) de métodos existentes en epidemiología. **[P]** No se ha verificado el modelo de publicación de SMMR (Sage devuelve 403) ni si su alcance exige una contribución estadística propia. Solo se anota como reserva.
