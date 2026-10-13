# Auditoría de corpus: Applied Mathematics and Computation y Nonlinear Dynamics (2026-10-13)

Propósito: decidir si el tipo de contribución del manuscrito (evaluación de un modelo existente frente a un comparador de la misma familia y a referencias externas, sin algoritmo ni teoría nuevos) es admisible en cada revista, antes de cualquier reenvío tras el desk reject de BMB (`submission_final/SUBMISSION_RECORD_2026-10-12.md`).

Etiquetas: **[H]** hecho verificado · **[I]** inferencia · **[P]** pendiente.

## 1. Conclusión

- **Applied Mathematics and Computation: descartada para este manuscrito.** Con la regla fijada antes de leer, D = 0: ninguno de los 16 artículos epidemiológicos ni de los 12 de la sonda general evalúa modelos existentes sin aportar un método. Lo corrobora el alcance oficial, que dice que la revista «emphasizes papers of a computational nature focusing on new algorithms, their analysis and numerical results».
- **Nonlinear Dynamics: admisible, con un riesgo concreto.** Fuera de la epidemiología publica artículos de tipo D: al menos tres confirmados por su resumen y otros por el título. Dentro de la epidemiología, los 51 artículos son de construcción de modelos (A, B o C) y ninguno evalúa modelos existentes. El tipo de contribución está aceptado en la revista, pero no se ha visto aplicado a modelos epidémicos.

Esto no es una probabilidad de aceptación. Es un filtro sobre si el tipo de artículo aparece en el corpus reciente.

## 2. Criterio, fijado antes de leer

Cada artículo se clasifica por su contribución principal:

- **A**: algoritmo o método numérico o computacional nuevo (incluye marcos híbridos ML-mecanicistas y métodos de control).
- **B**: teoría o análisis nuevo (existencia, estabilidad, bifurcación, umbrales, soluciones exactas).
- **C**: modelo nuevo o modificado con ajuste o simulación.
- **D**: evaluación o comparación de modelos o métodos existentes sin aportar un método nuevo.

Regla por revista: D = 0 → descartar; D = 1 → dudoso; D ≥ 2 → admisible.

## 3. Método y fuentes

- **[H]** Muestra: artículos de revista publicados entre el 2025-04-01 y el 2026-10-13 en AMC (ISSN 0096-3003) y Nonlinear Dynamics (ISSN 0924-090X y 1573-269X), recuperados de Crossref con diez consultas temáticas (epidemia, tuberculosis, COVID-19, SIR, SEIR, etc.) y filtrados por título. Se excluyeron manualmente los falsos positivos de «transmission» y «disease» (engranajes, líneas eléctricas, Parkinson, Alzheimer, malware, cadenas de suministro).
- **[H]** Sonda general: en las dos revistas y el mismo periodo, títulos con «comparison», «evaluation», «assessment», «benchmark», «forecast», «validation» o «versus» en cualquier dominio, para no perder artículos de tipo D fuera de la epidemiología.
- **[H]** Resúmenes: OpenAlex y Semantic Scholar. Consensus y SciSpace no tenían los de Nonlinear Dynamics de 2025–2026; la web de Springer devuelve un desafío anti-bot y ScienceDirect un 403, y no se intentó sortearlos.
- **[H]** Alcance de AMC: página oficial de Elsevier Shop, consultada el 2026-10-13.

### Límites

- **[P]** La muestra es dirigida (consultas por relevancia en Crossref), no exhaustiva.
- **[P]** Solo 6 de 16 artículos epidemiológicos de AMC y 6 de 51 de Nonlinear Dynamics tienen el resumen leído. El resto se clasificó por el título, que basta para separar A/B/C de D en títulos como «Stability analysis and Hopf bifurcation…», pero es evidencia más débil.
- **[P]** No se ha verificado el alcance oficial de Nonlinear Dynamics (Springer redirige a una página de autenticación) ni, para ninguna de las dos revistas, la existencia de una vía de suscripción sin APC.

## 4. Resultados

| Revista | Epidemiológicos | A | B | C | D | D en la sonda general | Veredicto |
|---|--:|--:|--:|--:|--:|---|---|
| AMC | 16 | 4 | 4 | 8 | 0 | 0 (12 títulos revisados) | Descartar |
| Nonlinear Dynamics | 51 | 7 | 26 | 18 | 0 | ≥ 3 confirmados por resumen | Admisible con riesgo |

### 4.1 Artículos de tipo D en Nonlinear Dynamics (sonda general)

| Artículo | Por qué es D | Base |
|---|---|---|
| [Comparing the Efficiency of Finite Element Models and Reduced-order Models with Varying Parameters](https://doi.org/10.1007/s11071-025-11590-6) | Muestra que un método establecido (ROM basados en ICE) recoge la variación de parámetros de un modelo de elementos finitos; no propone un método nuevo. | resumen |
| [In-plane vibrations of slightly curved beams: two models compared](https://doi.org/10.1007/s11071-025-11691-2) | Usa un modelo de referencia para evaluar los límites de validez de un modelo existente. | resumen |
| [Dynamic substructuring system versus hybrid simulation under nonlinear dynamics and reduced-order modeling inaccuracies](https://doi.org/10.1007/s11071-026-13016-3) | Evaluación comparativa sistemática de dos esquemas existentes bajo errores de modelización. | resumen |
| [Nonlinear model order reduction of dynamical systems in process engineering: review and comparison](https://doi.org/10.1007/s11071-026-12495-8) | Revisión y comparación de ocho métodos establecidos; incluye además una extensión menor. Mixto. | resumen |
| [Assessment of chaotic features for PM10 concentrations in İstanbul](https://doi.org/10.1007/s11071-025-11328-4) | Aplica métodos existentes de análisis del caos a una serie de datos. | resumen |
| [Harnessing deep learning for chaotic time series forecasting: a performance comparison of different methods and models](https://doi.org/10.1007/s11071-025-12016-z) | Comparación de rendimiento de métodos de pronóstico. | solo título |

No se cuentan como D, aunque el título lo sugiera, los dos artículos «Evaluating applied force reduced-order models» (validación y verificación): sus resúmenes proponen un método de validación nuevo y un marco nuevo, así que son A.

### 4.2 Sonda general en AMC

Ninguno de los 12 títulos es de tipo D. Los que tenían resumen proponen un método: condiciones de contorno numéricas nuevas para problemas fraccionarios, un modelo gris fraccionario para pronóstico de ventas. «Comparative analysis of nonlinear Urysohn functional integral equations via Nyström method» no tiene resumen accesible; su título indica un estudio numérico de ecuaciones, no una evaluación de modelos.

### 4.3 Uso de datos reales y pronóstico en el corpus epidemiológico

**[H/I]** En Nonlinear Dynamics, al menos cinco artículos epidemiológicos usan datos reales (COVID-19, ébola, mpox, vacunación). Uno de ellos pronostica con datos del Reino Unido mediante un modelo híbrido mecanicista–ML nuevo ([10.1007/s11071-026-12484-x](https://doi.org/10.1007/s11071-026-12484-x)). Sin resumen, no consta si alguno compara con referencias externas fuera de muestra. En AMC, ninguno de los 6 resúmenes leídos ni de los 10 títulos restantes indica uso de datos reales.

## 5. Lectura para la decisión

- **[I] AMC repetiría la puerta que falló en BMB** (tipo de contribución), esta vez en su versión computacional: el corpus y el alcance piden un método.
- **[I] En Nonlinear Dynamics el riesgo cambia de naturaleza.** La revista publica evaluaciones de los límites de validez de modelos existentes, que es el mismo tipo de pregunta que la del manuscrito: ¿la mejora del orden fraccionario sobrevive a una comparación más amplia? Pero su corpus epidemiológico reciente es de construcción de modelos. Un editor del área podría esperar un modelo o análisis nuevo.
- **[I] Si se elige Nonlinear Dynamics**, el ajuste de énfasis (título, resumen y carta) tendría que presentar el artículo como una evaluación de los límites de validez de una extensión fraccionaria, en la línea de los artículos de la §4.1, sin cambiar la pregunta ni las afirmaciones.
- **[P]** Antes de enviar: verificar el alcance oficial de Nonlinear Dynamics y la vía sin APC, y ver si el Transfer Desk de Springer Nature la propone (permitiría transferir sin reformatear).

## 6. Tablas completas del corpus epidemiológico

Cat.: categoría asignada. Base: «resumen» si se leyó el resumen; «título» si se clasificó por el título.

### Applied Mathematics and Computation (16)

| Fecha | Título | Cat. | Base | Datos reales |
|---|---|:--:|---|---|
| 2025-08 | [A co-evolutionary model of information, behavior, and epidemics in multiplex networks: Incorporating subjective and objective factors](https://doi.org/10.1016/j.amc.2025.129406) | C | título |  |
| 2026-01 | [The numerical solution of epidemic models on moving domains using combined masses](https://doi.org/10.1016/j.amc.2025.129691) | A | resumen |  |
| 2026-01 | [Routes to extreme events in forced-transmission eco-epidemic model: A dynamical-systems perspective](https://doi.org/10.1016/j.amc.2025.129619) | B | título |  |
| 2026-01 | [Evolution of group behaviour in the ecological snowdrift game-level-headed and impatient delayed epidemic model under emergencies](https://doi.org/10.1016/j.amc.2025.129668) | C | título |  |
| 2026-01 | [Vaccination dilemmas in mitigating monkeypox outbreaks: An imitation dynamics game model approach](https://doi.org/10.1016/j.amc.2025.129641) | C | título |  |
| 2026-02 | [Optimal information spreading strategy for containing epidemic spreading on higher-order multiplex networks](https://doi.org/10.1016/j.amc.2025.129725) | C | título |  |
| 2026-02 | [Dynamics of two-strain disease transmission with negative vaccine information and vaccination on multiplex networks](https://doi.org/10.1016/j.amc.2025.129701) | C | título |  |
| 2026-03 | [Numerical investigation of the effect of macro control measures on epidemic transport via a coupled PDE crowd flow - epidemic spreading dynamics model](https://doi.org/10.1016/j.amc.2025.129789) | A | resumen |  |
| 2026-04 | [Stability analysis and Hopf bifurcation in a time-delayed fractional epidemic model](https://doi.org/10.1016/j.amc.2025.129863) | B | resumen |  |
| 2026-05 | [Exploring the effectiveness of coupled control measures on strain diversity and epidemic spread](https://doi.org/10.1016/j.amc.2025.129897) | C | título |  |
| 2026-06 | [Prosocial behavior on testing and quarantine in an epidemic disease](https://doi.org/10.1016/j.amc.2026.129949) | C | resumen |  |
| 2026-07 | [A nonstandard finite difference scheme for an SEIQR epidemiological PDE model](https://doi.org/10.1016/j.amc.2026.129953) | A | resumen |  |
| 2026-07 | [Adaptive parameter-space refinement and Markov state models for eco-epidemiological dynamics](https://doi.org/10.1016/j.amc.2026.129974) | A | resumen |  |
| 2026-09 | [Dual memory effects and epidemic thresholds in a fractional-order SEIR model](https://doi.org/10.1016/j.amc.2026.130037) | B | título |  |
| 2026-09 | [An evolutionary game model of disease-vaccination strategy in multiplex hypernetwork](https://doi.org/10.1016/j.amc.2026.130040) | C | título |  |
| 2026-10 | [Effects of media coverage on threshold dynamics of a stochastic avian-human influenza epidemic system with distributed delay and logarithmic Ornstein-Uhlenbeck process](https://doi.org/10.1016/j.amc.2026.130108) | B | título |  |

### Nonlinear Dynamics (51)

| Fecha | Título | Cat. | Base | Datos reales |
|---|---|:--:|---|---|
| 2025-04 | [Epidemic spreading in temporal multilayer networks coupling with individual behavioral changes](https://doi.org/10.1007/s11071-025-11070-x) | C | título |  |
| 2025-05 | [Effect of cross-immunity on the transmission of a two serotypes co-infected dengue model under deterministic and stochastic environments](https://doi.org/10.1007/s11071-025-11172-6) | B | título |  |
| 2025-05 | [Lineage of the SEIRS model and its critical thresholds on social networks](https://doi.org/10.1007/s11071-025-11255-4) | B | título |  |
| 2025-05 | [Dynamical behaviors of a stochastic SIRB model for cholera with general infection dynamics and Ornstein-Uhlenbeck process](https://doi.org/10.1007/s11071-025-11227-8) | B | título |  |
| 2025-05 | [Non-smooth dynamics of a tick-borne disease model with two-threshold control strategies](https://doi.org/10.1007/s11071-025-11237-6) | B | título |  |
| 2025-05 | [The impact of stochasticity on the outbreak and extinction thresholds of emerging infectious diseases: a case study of COVID-19](https://doi.org/10.1007/s11071-025-11417-4) | B | título | sí (caso COVID-19) |
| 2025-06 | [Dynamics of delayed models in ecology, epidemiology, and cytology: Existence of non-positive solutions](https://doi.org/10.1007/s11071-025-11390-y) | B | título |  |
| 2025-06 | [Dynamics of Ebola Virus Disease with awareness effects: a case study of guinea and sierra leone](https://doi.org/10.1007/s11071-025-11286-x) | C | título | sí (Guinea, Sierra Leona) |
| 2025-06 | [A Mathematical model for Epidemic dynamics with multiple vaccines, age-structured strategies, and parameter estimation](https://doi.org/10.1007/s11071-025-11332-8) | C | título | sí (estimación de parámetros) |
| 2025-06 | [Nonlinear dynamics of measles and HIV co-infection using a reaction-diffusion model and artificial neural networks](https://doi.org/10.1007/s11071-025-11432-5) | C | título |  |
| 2025-06 | [Co-evolution of information, behavior and epidemic transmission under multiple local influences in multiplex networks](https://doi.org/10.1007/s11071-025-11416-5) | C | título |  |
| 2025-06 | [Impact of competing opinions on epidemic spread: a virus transmission model with denier and vigilant groups in activity-driven networks](https://doi.org/10.1007/s11071-025-11506-4) | C | título |  |
| 2025-07 | [Dynamics of COVID-19 and tuberculosis co-infection: a mathematical model incorporating nonlinear treatment rate](https://doi.org/10.1007/s11071-025-11150-y) | C | título |  |
| 2025-07 | [Effect of behavior change pattern on disease transmission dynamics](https://doi.org/10.1007/s11071-025-11557-7) | C | título |  |
| 2025-07 | [Establishment and research of individual-based markov chain model for COVID-19 transmission in a boarding school](https://doi.org/10.1007/s11071-025-11649-4) | C | título | probable (internado) |
| 2025-08 | [Fractional diffusion induced pattern formation in an epidemic model with nonlinear incidence rate](https://doi.org/10.1007/s11071-025-11675-2) | B | título |  |
| 2025-09 | [Analysis of fractional order SVEIR infectious disease model with fear effect and secondary vaccination](https://doi.org/10.1007/s11071-025-11752-6) | C | título |  |
| 2025-09 | [A consistent SIR model on time scales with exact solution](https://doi.org/10.1007/s11071-025-11758-0) | B | resumen |  |
| 2025-09 | [Emergence of Chaos in a Coinfection Model of HIV/AIDS and Mpox with Treatment Constraints](https://doi.org/10.1007/s11071-025-11803-y) | B | título |  |
| 2026-01 | [Analysis of a generalized stochastic population diffusion epidemic model perturbed by Black–Karasinski process](https://doi.org/10.1007/s11071-025-11990-8) | B | título |  |
| 2026-01 | [Epidemic control under hidden transmission and network heterogeneity using individual-based modeling and reinforcement learning](https://doi.org/10.1007/s11071-025-11967-7) | A | título |  |
| 2026-01 | [Machine intelligent expedition with supervised Bayesian adaptive neural networks for stochastic cholera epidemic model in a periodic environment](https://doi.org/10.1007/s11071-025-12006-1) | A | título |  |
| 2026-01 | [Dynamics of a multi-trophic eco-epidemiological model incorporating fear effect, nonlinear functional response and harvesting](https://doi.org/10.1007/s11071-025-11914-6) | B | título |  |
| 2026-01 | [Analysis on an SIS epidemic model with saturated recovery and dynamic behavior changes](https://doi.org/10.1007/s11071-025-12014-1) | B | título |  |
| 2026-01 | [Epidemic spreading on heterogeneous probabilistic activity driven network model](https://doi.org/10.1007/s11071-025-12206-9) | C | título |  |
| 2026-02 | [An stochastic epidemic model with transport-related infections between two cities](https://doi.org/10.1007/s11071-025-12066-3) | B | título |  |
| 2026-02 | [Effect of fear and refuge in eco-epidemiological model with predator supported by additional food](https://doi.org/10.1007/s11071-025-12124-w) | B | resumen |  |
| 2026-02 | [A climate-based model of mosquito-borne disease dynamics with wolbachia](https://doi.org/10.1007/s11071-025-12069-0) | C | título |  |
| 2026-02 | [Modeling the transmission dynamics and optimal control analysis of Mpox infection incorporating vaccination control strategy](https://doi.org/10.1007/s11071-025-12047-6) | C | resumen | sí (Nigeria, EE. UU., Ghana) |
| 2026-03 | [The role of cooperation in epidemic control: insights from an SIRS model with evolutionary games](https://doi.org/10.1007/s11071-026-12240-1) | C | título |  |
| 2026-03 | [Turing pattern and optimal control of reaction-diffusion infectious disease systems on complex networks](https://doi.org/10.1007/s11071-025-12170-4) | B | título |  |
| 2026-03 | [Impact of heterogeneous vaccination and contact on influenza dynamics in age structure population](https://doi.org/10.1007/s11071-025-12213-w) | C | título |  |
| 2026-04 | [Threshold dynamics and traveling wave profile of a diffusive SEIRS epidemic model with nonlinear incidence](https://doi.org/10.1007/s11071-026-12477-w) | B | título |  |
| 2026-04 | [Global analysis of a non-smooth delayed SIR epidemic model with media-induced threshold policy](https://doi.org/10.1007/s11071-026-12420-z) | B | título |  |
| 2026-04 | [A hybrid mechanistic–machine learning model for SARS-CoV-2: stability, sensitivity, and forecasting insights based on UK data](https://doi.org/10.1007/s11071-026-12484-x) | A | título | sí (Reino Unido; pronóstico) |
| 2026-04 | [Opinion modulation and higher-order contact effects in dual-virus epidemic dynamics](https://doi.org/10.1007/s11071-026-12493-w) | C | título |  |
| 2026-04 | [Oscillatory dynamics driven induced by higher-order interactions and self-awareness in multiplex information–epidemic systems](https://doi.org/10.1007/s11071-026-12488-7) | B | título |  |
| 2026-05 | [Assessing gathering suppression and vaccination intervention in SIR contagion processes with higher-order interactions](https://doi.org/10.1007/s11071-026-12619-0) | C | título |  |
| 2026-05 | [Dynamics and adaptive control of a periodic multi-patch brucellosis transmission model](https://doi.org/10.1007/s11071-026-12598-2) | B | título |  |
| 2026-06 | [Dynamics analysis of a spatially extended SIS epidemic model with nonlocal disease transmission](https://doi.org/10.1007/s11071-026-12726-y) | B | resumen |  |
| 2026-06 | [Diagnosing and rescuing the identifiability crisis in nonlinear epidemic dynamics: a hybrid deep learning and fisher information approach](https://doi.org/10.1007/s11071-026-12674-7) | A | título |  |
| 2026-06 | [Jacobian-regularized network for hepatitis disease detection and fractional-order modeling for hepatitis progression with vaccination](https://doi.org/10.1007/s11071-026-12683-6) | A | título |  |
| 2026-07 | [Distributed model predictive control for agent-based epidemic networks with waterborne coupling](https://doi.org/10.1007/s11071-026-12880-3) | A | título |  |
| 2026-07 | [A dual-stochastic network epidemic model with logarithmic Ornstein-Uhlenbeck process and white noise](https://doi.org/10.1007/s11071-026-12760-w) | B | título |  |
| 2026-07 | [Stochastic shift and dynamical complexities of a disease-induced forage and piscivore fishery model](https://doi.org/10.1007/s11071-026-12870-5) | B | título |  |
| 2026-08 | [Fear-driven higher-order epidemic dynamics on heterogeneous hypergraphs](https://doi.org/10.1007/s11071-026-12918-6) | C | título |  |
| 2026-08 | [Optimal control strategies integrating higher-order diffusion-guided local intervention with sparse control for infectious disease mitigation](https://doi.org/10.1007/s11071-026-12936-4) | A | título |  |
| 2026-08 | [The influence of virus suppression and delayed immunity mediation on an HIV model with virus-to-cell and cell-to-cell infections](https://doi.org/10.1007/s11071-026-12978-8) | B | resumen |  |
| 2026-09 | [Modeling epidemic dynamics in variable environments using nonlinear perturbation methods](https://doi.org/10.1007/s11071-026-13033-2) | B | título |  |
| 2026-09 | [Stochastic reversal of deterministic selection in epidemic strain competition](https://doi.org/10.1007/s11071-026-13032-3) | B | resumen |  |
| 2026-09 | [The dynamics of vaccine-sensitive and vaccine-escape strains in an infection-age-structured epidemic model](https://doi.org/10.1007/s11071-026-13092-5) | B | título |  |
