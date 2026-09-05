# Within-Family Error Reduction Versus External Forecasting Skill in Fractional-Order Compartmental Models: A Methodological Investigation of SEIT Tuberculosis Dynamics

**Authors**: [AUTHOR INPUT REQUIRED: final human author list and order]  
**Affiliations**: [AUTHOR INPUT REQUIRED: department, institution/university, city, country for each author]  
*Corresponding Author*: [AUTHOR INPUT REQUIRED: name and active institutional email]  
*ORCID*: [AUTHOR INPUT OPTIONAL: 16-digit ORCID identifier(s), if available]

---

## Abstract

Assessing fractional-order compartmental models for forecasting requires separating within-family improvement from performance against external baselines. We independently reimplemented and audited a Caputo fractional-order SEIT tuberculosis model using monthly Brazilian surveillance data from 2001–2022, with notifications represented as incidence flow. In a 24-month open-loop stress test and a 13-origin rolling-origin evaluation across 12 monthly lead horizons, fractional SEIT produced lower forecast error than an independently re-estimated integer-order comparator. This within-family improvement did not translate into positive observed skill against persistence or SARIMA at any evaluated horizon ($H_{\text{relax}} = 0$). Observed skill relative to seasonal naive was positive only from $h=1$ through $h=7$ ($H_{\text{relax}} = 7$), a baseline-specific empirical descriptor. As a secondary analysis, practical identifiability was weak for $\beta$, $\gamma$, and $d$, precluding their interpretation as precisely estimated epidemiological rates despite comparatively stable trajectory predictions. Across the predefined 25-member near-equivalent admissible set ($\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$), $R_0$ remained within a narrow practical-identifiability envelope (1.1542–1.1892), and the Disease-Free Equilibrium was locally unstable for all 25 solutions under Matignon's criterion. Thus, fractional differentiation improved forecast error within the SEIT family, but external baselines did not support a general forecasting advantage beyond that family. The identifiability results bound the mechanistic interpretation of the fitted model rather than constituting an independent forecasting claim.

**Keywords**: Mathematical epidemiology; Fractional-order differential equations; Practical identifiability; Forecast evaluation; Basic reproduction number; Tuberculosis.

---

## 1. Introduction

Mechanistic compartmental models are used to represent transmission processes, latent states, and intervention dynamics in infectious-disease systems. In diseases with protracted latency and complex clinical progression, such as tuberculosis—which remains a persistent public health challenge in Brazil (World Health Organization, 2022; Pelissari et al., 2020)—these models may be used both to interpret unobserved disease states and to project reported surveillance data. The two aims are not equivalent. A close fit to historical observations does not ensure that a compartmental model will forecast future trajectory changes reliably under strict temporal evaluation (Moran et al., 2016; Bracher et al., 2021).

Fractional-order formulations extend compartmental models by replacing integer-order derivatives with non-local operators that introduce power-law temporal dependence (Diethelm, 2013; Area et al., 2015). They offer additional flexibility for representing departures from exponential dynamics, but an improvement over an integer-order counterpart remains a comparison within the same mechanistic family. Lower error in that comparison does not by itself show that the additional flexibility provides forecasting value beyond standard statistical or naive alternatives.

The central evaluation question is therefore whether a within-family fractional advantage survives expansion of the benchmark set under temporal out-of-sample assessment. A mechanistic extension can improve relative fit or forecast error within its own family while remaining uncompetitive against simpler baselines designed specifically for prediction. Any forecasting claim must therefore be evaluated against both an independently re-estimated integer-order comparator and external benchmarks across multiple lead horizons.

Practical identifiability provides a secondary interpretive axis. When compartmental systems are calibrated against aggregate surveillance notifications, disparate combinations of kinetic rate parameters can produce near-identical trajectory fits—a condition known as practical non-identifiability (Tuncer & Le, 2018; Roosa & Chowell, 2019; Meshkat et al., 2014). Stable trajectories therefore need not imply precise recovery of individual biological rates. Examining parameter dispersion, predictive stability, and the robustness of derived quantities such as the basic reproduction number $R_0$ can clarify which mechanistic interpretations remain supportable without redefining the paper's primary forecasting question.

This study addresses that forecasting question through an independent reimplementation and methodological audit of a fractional-order SEIT (Susceptible–Exposed–Infectious–Treated) tuberculosis model applied to national monthly surveillance data from Brazil spanning 2001 through 2022. The model uses a reference-time-consistent Caputo fractional derivative formulation and maps monthly notifications to monthly incidence flow ($E \to I$) rather than to the unobservable infectious stock. The primary analysis asks whether lower forecast error relative to an independently re-estimated integer-order SEIT model translates into positive observed forecasting skill against persistence, seasonal naive, and SARIMA benchmarks. A secondary analysis evaluates practical parameter identifiability and the robustness of derived dynamical quantities across calibration-equivalent solutions.

The forecasting comparison uses two complementary protocols: a 24-month single-origin long open-loop stress test and a 13-origin expanding-window rolling-origin evaluation across 12 monthly lead horizons. The rolling-origin analysis supplies the external benchmark comparison under strict temporal separation, while the long open-loop simulation provides a complementary fixed-origin stress test. The secondary mechanistic analysis examines individual-parameter identifiability, predictive stability, the $R_0$ practical-identifiability envelope, and local stability of the Disease-Free Equilibrium under Matignon's criterion across a predefined admissible set.

---

## 2. Methods

### 2.1 Study design and independent-reimplementation scope

This study is an independent, reproducible reimplementation and methodological audit of a fractional-order Susceptible–Exposed–Infectious–Treated (SEIT) compartmental model applied to monthly tuberculosis surveillance data in Brazil. The original numerical scripts and exact computational configurations associated with earlier historical publications on this model are unrecoverable and unavailable. Consequently, the historical manuscript is treated as a conceptual reference rather than an empirical source of truth (`REPRODUCTION_MODE = INDEPENDENT_REIMPLEMENTATION`). Methodological specifications, parameter bounds, calibration routines, identifiability protocols, and forecasting evaluations are established from explicit, auditable procedures.

The study is designed to assess whether within-family improvements over an independently re-estimated integer-order SEIT comparator extend to external forecasting skill against standard baselines, and to identify which derived mechanistic properties remain robust when individual rate parameters are weakly identified.

Optimal-control interventions and associated historical burden-reduction estimates are outside the scope of this study and were not reimplemented.

### 2.2 Data and observation mapping

The empirical series consists of monthly tuberculosis notification counts for Brazil spanning January 2001 through December 2022 ($N = 264$ consecutive monthly observations). The canonical observational file is preserved in the repository as `data/raw/tb_mes.xlsx`, exactly as supplied by Amaury de Souza for this collaboration; its hash, structure, and ingestion history are recorded in `DATA_PROVENANCE.md` and the machine-readable source manifest. The repository materials do not independently document the original external download URL or acquisition route, so no specific governmental acquisition path is treated here as verified provenance. The dataset exhibits complete temporal continuity with zero missing months, zero duplicated dates, and zero missing values.

The dataset is partitioned into two distinct periods:
* **Calibration window**: January 2001 to December 2020 ($N_{\text{cal}} = 240$ months).
* **Validation window**: January 2021 to December 2022 ($N_{\text{val}} = 24$ months).

The total population series $N(t)$ serves as the denominator in the standard incidence force-of-infection term. For the calibration window (2001–2020), $N(t)$ is obtained directly from the surveillance dataset. For out-of-sample simulation, population values beyond each training endpoint were generated using a log-linear trend fitted exclusively to population observations available within the corresponding training window:
$$\ln N(t) = a_0 + a_1 t, \quad t \le t_{\text{train}}$$
No population observations beyond the relevant training endpoint were used.

The observed monthly case counts represent an incidence flow rather than the standing stock of infectious individuals $I(t)$. Equating monthly case reports directly to $I(t)$ would therefore constitute a stock-flow mis-specification. To represent the observation process, monthly reported cases are mapped to the transition flow from the exposed compartment $E$ to the infectious compartment $I$. An auxiliary fractional state accumulator $C(t)$ tracks cumulative incidence:
$$^C D_t^\alpha C(t) = \tau_0^{1-\alpha} \sigma E(t), \quad C(0) = 0$$
The model-predicted monthly reported case count for calendar month $k$ (spanning $[t_k, t_{k+1}]$ with $\Delta t = 1\text{ month}$) is given by the discrete increment of the accumulator:
$$\hat{y}_k = C(t_{k+1}) - C(t_k)$$

### 2.3 Fractional SEIT formulation

The epidemiological system comprises four primary compartments: Susceptible individuals $S(t)$, Latently infected (Exposed) individuals $E(t)$, Active infectious individuals $I(t)$, and Treated/Removed individuals $T(t)$, alongside the cumulative incidence accumulator $C(t)$.

Fractional temporal differentiation is formulated using the Caputo fractional derivative of order $\alpha \in (0, 1]$ with base point $t_0 = 0$:
$$^C D_t^\alpha X(t) = \frac{1}{\Gamma(1-\alpha)} \int_0^t (t-s)^{-\alpha} X'(s)\,ds$$

Because the Caputo derivative $^C D_t^\alpha X(t)$ possesses physical dimensions of $[\text{individuals}] \cdot [\text{time}]^{-\alpha}$, whereas standard epidemiological transition parameters $(\beta, \sigma, \gamma, d, \mu)$ are defined as per-unit-time rates ($\text{month}^{-1}$) and recruitment $\Lambda$ is defined in $\text{individuals} \cdot \text{month}^{-1}$, direct dimensional compatibility requires an explicit reference timescale $\tau_0$. Setting $\tau_0 = 1\text{ month}$ yields the dimensionally consistent vector field:
$$^C D_t^\alpha X(t) = \tau_0^{1-\alpha} F(X(t); \theta)$$
For a time discretization defined in months ($\tau_0 = 1$), the numerical scaling factor is $\tau_0^{1-\alpha} = 1.0^{1-\alpha} = 1.0$, preserving identical numerical trajectories while satisfying dimensional homogeneity across all state equations:
$$\begin{aligned}
^C D_t^\alpha S(t) &= \tau_0^{1-\alpha} \left[ \Lambda - \frac{\beta S(t) I(t)}{N(t)} - \mu S(t) \right] \\
^C D_t^\alpha E(t) &= \tau_0^{1-\alpha} \left[ \frac{\beta S(t) I(t)}{N(t)} - (\sigma + \mu) E(t) \right] \\
^C D_t^\alpha I(t) &= \tau_0^{1-\alpha} \left[ \sigma E(t) - (\gamma + \mu + d) I(t) \right] \\
^C D_t^\alpha T(t) &= \tau_0^{1-\alpha} \left[ \gamma I(t) - \mu T(t) \right] \\
^C D_t^\alpha C(t) &= \tau_0^{1-\alpha} \left[ \sigma E(t) \right]
\end{aligned}$$

The parameters and their structural roles are defined as follows:
* $\mu$: Natural all-cause mortality rate, fixed externally according to the frozen demographic contract: $\mu = \frac{1}{74 \times 12} \approx 0.001126\text{ month}^{-1}$.
* $\Lambda$: Demographic recruitment into the susceptible population, fixed by demographic closure as $\Lambda = \mu \bar{N}_{\text{cal}}$, where $\bar{N}_{\text{cal}}$ is the mean population over the calibration window (2001–2020).
* $\beta$: Transmission rate coefficient, representing effective contacts per infectious individual per month. Search bounds: $\beta \in [0.01, 1.00]\text{ month}^{-1}$.
* $\sigma$: Rate of progression from latent infection $E$ to active infectious disease $I$. Search bounds: $\sigma \in [0.01, 0.50]\text{ month}^{-1}$. The single-exponential compartment structure is recognized as an epidemiological simplification.
* $\gamma$: Removal rate from active disease $I$ into the treated compartment $T$. Search bounds: $\gamma \in [0.05, 0.30]\text{ month}^{-1}$ (frozen primary calibration range; $[0.01, 0.50]\text{ month}^{-1}$ retained as a sensitivity arm).
* $d$: Tuberculosis-attributable excess mortality hazard rate. Search bounds: $d \in [0.0001, 0.05]\text{ month}^{-1}$ (frozen primary calibration range).
* $\alpha$: Fractional derivative order. Search bounds: $\alpha \in [0.50, 1.00]$ (frozen primary calibration range; $[0.70, 1.00]$ evaluated as a sensitivity arm).

Initial conditions at $t = 0$ are determined analytically from the initial observed incidence flow $y_0 = y(t_0)$ and initial population $N(t_0)$, introducing zero free optimization dimensions:
$$E(0) = \frac{y_0}{\sigma}, \quad I(0) = \frac{y_0}{\gamma + \mu + d}, \quad T(0) = 0, \quad S(0) = N(t_0) - E(0) - I(0), \quad C(0) = 0$$

### 2.4 Numerical solution and calibration

The system of fractional differential equations is solved using the Diethelm–Ford–Freed predictor-corrector algorithm (Adams–Bashforth–Moulton PECE scheme for Caputo fractional initial-value problems). Numerical integration used a fixed step size of $h = 1.0\text{ month}$, selected following the pre-calibration numerical-convergence audit documented in the repository.

Model calibration is performed by optimizing the free parameter vector $\theta = (\beta, \sigma, \gamma, d, \alpha)$ using Differential Evolution (`scipy.optimize.differential_evolution`). The algorithm configuration was prespecified and documented before execution:
* Strategy: `best1bin`
* Population size: `popsize = 15`
* Mutation constant: `mutation = (0.5, 1.0)`
* Recombination probability: `recombination = 0.7`
* Relative convergence tolerance: `tol = 0.01`
* Maximum iterations: `maxiter = 1000`
* Local gradient polishing: `polish = False`

The calibration objective minimizes the Root Mean Squared Error (RMSE) between observed monthly cases and model-predicted flow across the calibration window:
$$J(\theta) = \text{RMSE}(y_{\text{obs}}, \hat{y}(\theta)) = \sqrt{\frac{1}{N_{\text{cal}}} \sum_{k=1}^{N_{\text{cal}}} (y_k - \hat{y}_k(\theta))^2}$$
Any simulation yielding non-finite numerical outputs or negative state values is assigned an objective penalty ($10^{12}$).

To guarantee determinism and reproducibility, pseudorandom number generators were assigned explicit values that were prespecified and documented before execution:
* Canonical primary seed: `20260815`
* Diagnostic seeds: `20260816`, `20260817`, `20260818`, `20260819`

The canonical primary calibration run was tied to seed `20260815`; the diagnostic seeds were used exclusively for identifiability and robustness analyses.

### 2.5 Integer-order comparator

To evaluate the specific contribution of fractional differentiation within the SEIT family, an integer-order counterpart is defined by fixing $\alpha \equiv 1.0$.

Under the fair-comparison principle, the integer comparator's remaining parameters $\theta_{\text{int}} = (\beta, \sigma, \gamma, d)$ are re-estimated independently using the identical Differential Evolution configuration, objective function, and parameter bounds over the calibration window. The integer model is never evaluated by simply setting $\alpha = 1.0$ within the parameter vector calibrated for the fractional model.

### 2.6 Practical-identifiability analysis

Practical parameter identifiability is evaluated across the calibration dataset using a two-stage protocol:
1. **Multiseed optimization ensemble**: Optimization across the five prespecified seeds to detect stochastic solution dispersion under identical hyperparameter settings.
2. **Profile-objective exploration**: One-dimensional profile objective sweeps for $\beta$, $\gamma$, $d$, and $\alpha$ over fixed grids, re-optimizing the remaining parameters at each grid point under the canonical primary seed.

To distinguish between parameter identifiability, predictive identifiability, and functional identifiability, an admissible near-equivalent solution set is constructed:
$$\Theta_{\text{admissible}} = \left\{ \theta \;\middle|\; \frac{\text{RMSE}_{\text{cal}}(\theta) - \text{RMSE}_{\text{cal}}(\theta^*_{\text{primary}})}{\text{RMSE}_{\text{cal}}(\theta^*_{\text{primary}})} \le 1.0\% \right\}$$
where $\theta^*_{\text{primary}}$ is the primary calibration optimum.

This threshold defines an empirical practical-identifiability envelope of solutions with near-identical calibration fidelity. This set is strictly an operational admissibility envelope and is not a formal statistical confidence region or Bayesian credible interval.

For each solution in the admissible set and the broader profile diagnostic pool, three levels of variation are quantified:
* Individual parameter dispersion ($\beta, \sigma, \gamma, d, \alpha$).
* Prediction trajectory dispersion over calibration and validation windows.
* Derived functional dispersion (basic reproduction number $R_0$ and equilibrium stability).

### 2.7 Basic reproduction number and local stability

The basic reproduction number $R_0$ is derived using the Next-Generation Matrix (NGM) approach formulated at the Disease-Free Equilibrium (DFE).

At the DFE, the population is uninfected: $S^* = \bar{N}$, $E^* = 0$, $I^* = 0$, $T^* = 0$, with $N^* = \bar{N}$. The infected subsystem comprises states $x = [E, I]^T$. Decomposing the linearized dynamics into new infection rates ($\mathcal{F}$) and transition/removal rates ($\mathcal{V}$):
$$\mathcal{F} = \begin{bmatrix} 0 & \beta \\ 0 & 0 \end{bmatrix}, \quad \mathcal{V} = \begin{bmatrix} \sigma + \mu & 0 \\ -\sigma & \gamma + \mu + d \end{bmatrix}$$
The next-generation matrix $K = \mathcal{F}\mathcal{V}^{-1}$ is:
$$K = \begin{bmatrix} \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu + d)} & \frac{\beta}{\gamma + \mu + d} \\ 0 & 0 \end{bmatrix}$$
The basic reproduction number is the spectral radius $\rho(K)$:
$$R_0 = \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu + d)}$$
Under the uniform reference-time scaling $\tau_0^{1-\alpha}$, the common scaling factors in $\mathcal{F}_\alpha = \tau_0^{1-\alpha}\mathcal{F}$ and $\mathcal{V}_\alpha = \tau_0^{1-\alpha}\mathcal{V}$ cancel algebraically in $K_\alpha = \mathcal{F}_\alpha \mathcal{V}_\alpha^{-1} = \mathcal{F}\mathcal{V}^{-1}$, rendering the threshold expression $R_0$ mathematically invariant to $\alpha$ for all $\alpha \in (0, 1]$.

Local asymptotic stability of the DFE under fractional dynamics is evaluated via Matignon's stability theorem. The DFE is locally asymptotically stable if and only if all eigenvalues $\lambda_i$ of the system Jacobian evaluated at the DFE satisfy:
$$|\arg(\lambda_i)| > \alpha \frac{\pi}{2}$$
For each parameter vector in the admissible set, the Jacobian eigenvalues are computed analytically and evaluated using that solution's specific fitted fractional order $\alpha$.

### 2.8 Long open-loop stress test

To evaluate long-horizon dynamical stability under fixed parameterization, a single-origin open-loop simulation test is conducted:
* Calibration: The model is fitted strictly on data from 2001-01 through 2020-12 ($N_{\text{cal}} = 240$).
* Validation: Using the parameters estimated at $t_{\text{cal}} = \text{2020-12}$, the simulation continues forward in open loop across the 24-month validation window (2021-01 through 2022-12) without state reinitialization, data assimilation, or parameter updating.

This protocol provides a stress test of multi-year dynamic trajectory stability from a single origin, but does not substitute for multi-origin rolling forecast evaluation.

### 2.9 Rolling-origin forecasting evaluation

Out-of-sample forecasting performance is systematically assessed using an expanding-window rolling-origin evaluation protocol.

The evaluation incorporates 13 consecutive monthly forecast origins:
$$\mathcal{T}_{\text{origins}} = \{ \text{2020-12}, \text{2021-01}, \text{2021-02}, \dots, \text{2021-12} \}$$
From each origin $t_{\text{orig}}$, forecasts are generated across 12 monthly lead times:
$$h \in \{1, 2, \dots, 12\}\text{ months}$$
This generates a fully-crossed evaluation grid of $13 \text{ origins} \times 12 \text{ horizons} = 156$ forecast target points, ensuring that all evaluation targets fall within the 2021–2022 observational window.

For each origin $t_{\text{orig}}$:
1. The training dataset is restricted strictly to observations with date $\le t_{\text{orig}}$.
2. The population projection trend is re-estimated using only historical demographic data up to $t_{\text{orig}}$.
3. The demographic closure constant $\Lambda$ is recalculated as $\mu \bar{N}_{\text{train}}(t_{\text{orig}})$.
4. The fractional SEIT and integer SEIT models are each recalibrated via Differential Evolution using canonical primary seed `20260815` (13 fits per model family, 26 total SEIT fits).
5. All 12 forward horizon predictions ($h = 1, \dots, 12$) are generated from that single recalibrated parameter state integrated forward in open loop.

Strict temporal partitioning guarantees zero information leakage from future observations into training, calibration, demographic extrapolation, or baseline estimation.

### 2.10 External forecasting baselines

To provide rigorous external benchmarks beyond the SEIT model family, three statistical and naive baselines are implemented:

1. **Persistence (Random Walk)**:
   Assumes the future incidence flow equals the most recent observed monthly value:
   $$\hat{y}_{t_{\text{orig}}+h} = y_{t_{\text{orig}}}$$

2. **Seasonal Naive ($\text{lag } 12$)**:
   Projects the observation from the same calendar month of the preceding year:
   $$\hat{y}_{t_{\text{orig}}+h} = y_{t_{\text{orig}}+h-12}$$
   Because $h \le 12$, the target $t_{\text{orig}}+h-12 \le t_{\text{orig}}$ always lies within the observed history at that origin.

3. **SARIMA (Seasonal Autoregressive Integrated Moving Average)**:
   The model order $(p, d, q) \times (P, D, Q)_{12}$ was selected a priori by conducting an AIC-minimization grid search across 36 candidate models on the fixed 2001–2020 calibration dataset ($p \in \{0, 1, 2\}$, $d = 1$, $q \in \{0, 1, 2\}$, $P \in \{0, 1\}$, $D = 1$, $Q \in \{0, 1\}$, $s = 12$). The resulting model order, $\text{SARIMA}(0, 1, 2)(1, 1, 1)_{12}$, was frozen prior to forecasting evaluation. At each rolling origin $t_{\text{orig}}$, the SARIMA coefficients are re-estimated on the expanding historical window (date $\le t_{\text{orig}}$) using the frozen structural order.

### 2.11 Forecast metrics, relative skill, and horizon descriptors

Forecast accuracy is evaluated for each lead time $h \in \{1, \dots, 12\}$ across the $N_{\text{orig}} = 13$ origins using Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and mean bias:
$$\text{RMSE}(h) = \sqrt{\frac{1}{N_{\text{orig}}} \sum_{i=1}^{N_{\text{orig}}} \left( y_{i,h} - \hat{y}_{i,h} \right)^2}$$
$$\text{MAE}(h) = \frac{1}{N_{\text{orig}}} \sum_{i=1}^{N_{\text{orig}}} \left| y_{i,h} - \hat{y}_{i,h} \right|$$
$$\text{Bias}(h) = \frac{1}{N_{\text{orig}}} \sum_{i=1}^{N_{\text{orig}}} \left( \hat{y}_{i,h} - y_{i,h} \right)$$
where $y_{i,h}$ is the observed tuberculosis notification count at origin $i$ plus horizon $h$, and $\hat{y}_{i,h}$ is the corresponding model forecast.

Relative forecasting skill of model $M$ with respect to benchmark baseline $B$ at horizon $h$ is defined as:
$$\text{Skill}_{\text{RMSE}}(M, B, h) = 1 - \frac{\text{RMSE}_M(h)}{\text{RMSE}_B(h)}$$
$$\text{Skill}_{\text{MAE}}(M, B, h) = 1 - \frac{\text{MAE}_M(h)}{\text{MAE}_B(h)}$$
Positive skill ($\text{Skill} > 0$) denotes that model $M$ achieves lower error than baseline $B$, whereas negative skill ($\text{Skill} < 0$) indicates that the baseline has lower error for that metric and horizon.

To summarize performance horizons without implying universal predictability limits, two descriptive horizon indices are defined:
* $H_{\text{relax}}$: The maximum horizon $h \in \{1, \dots, 12\}$ at which model $M$ achieves positive skill ($\text{Skill} > 0$) relative to baseline $B$.
* $H_{\text{strict-from-h1}}$: The maximum horizon $h$ such that $\text{Skill}(h') > 0$ for all consecutive horizons $h' \in \{1, 2, \dots, h\}$ beginning at $h = 1$.

These indices function strictly as empirical summary descriptors of this specific 13-origin evaluation set.

### 2.12 Statistical interpretation boundary

The comparative forecasting evaluations reported in this study are descriptive sample metrics across the 13 evaluated rolling origins.

The dependence structure of the rolling-origin forecast errors and horizon-specific loss differentials was not formally characterised in the prespecified evaluation protocol. Accordingly, no post-hoc predictive-accuracy tests were added to the present analysis. Any future inferential assessment would require an explicit horizon-specific, dependence-aware protocol defined before testing.

Accordingly, forecasting comparisons are presented without claims of formal statistical significance or inferential superiority. Methodological findings strictly distinguish between empirical sample performance across the evaluated origins and generalizable claims regarding forecasting efficacy.

### 2.13 Use of large language models and AI-assisted tools

Large Language Model (LLM) and related AI tools were used under direct human oversight for drafting assistance, language editing, reference-format checks, structural review, and code-execution scripting. They were not treated as authors or scientific decision-makers and were not used as a source of empirical data or canonical numerical results. All AI-assisted text and code suggestions were reviewed against the repository evidence and accepted, modified, or rejected by the human researchers, who retain full responsibility for the scientific content and final manuscript.

---

## 3. Results

### 3.1 Within-family comparison across evaluation protocols

The fractional-order SEIT formulation achieved lower observed forecast error than the independently refitted integer-order SEIT comparator under both evaluation protocols and at every evaluated rolling-origin lead horizon. In the 24-month long open-loop stress test, the fractional SEIT model yielded an RMSE of $1117.960$ and MAE of $953.230$ (bias: $-851.150$), compared with an RMSE of $1759.538$ and MAE of $1588.649$ (bias: $-1588.649$) for the independently refitted integer comparator. Across the 13 rolling-origin evaluations, the fractional formulation produced lower RMSE and MAE than the integer model from $h = 1$ through $h = 12$; for example, RMSE was $688.858$ versus $1185.796$ at $h = 1$, $1138.323$ versus $1770.697$ at $h = 6$, and $1355.984$ versus $2022.492$ at $h = 12$. Because the integer comparator's parameters were re-estimated independently rather than inherited from the fractional fit, these differences establish a consistent within-model-family improvement.

These comparisons were obtained under two distinct empirical protocols. The single-origin stress test spans 2021-01 through 2022-12 after calibration on 2001-01 through 2020-12 ($N_{\text{cal}} = 240$) and evaluates continuous multi-year open-loop behavior from a fixed calibration point. The expanding-window rolling-origin evaluation uses 13 consecutive forecast origins (2020-12 through 2021-12) and 12 monthly lead horizons ($h = 1, \dots, 12$), providing the multi-horizon out-of-sample framework used for comparison with external statistical baselines under strict temporal separation.

### 3.2 External baseline evaluation and turning point

The within-family error reduction did not translate into positive observed forecasting skill against persistence or SARIMA. For both RMSE and MAE, observed skill relative to persistence and SARIMA was negative at all 12 evaluated lead horizons ($H_{\text{relax}} = 0$, $H_{\text{strict-from-h1}} = 0$). Across the 13 rolling origins, both external baselines had lower descriptive sample forecast errors than the fractional SEIT model at every horizon. At $h = 1$, fractional RMSE was $688.858$, compared with $389.702$ for persistence and $535.547$ for SARIMA; at $h = 6$, the corresponding values were $1138.323$, $845.856$, and $1022.421$; and at $h = 12$, they were $1355.984$, $1152.958$, and $1283.583$, respectively. Thus, the favorable fractional-versus-integer comparison did not establish positive observed skill beyond the model family for either of these external benchmarks.

A bounded exception occurred relative to the seasonal naive baseline ($\text{lag }12$). Observed RMSE and MAE skill were positive from $h = 1$ through $h = 7$ and negative from $h = 8$ through $h = 12$, giving empirical descriptors of $H_{\text{relax}} = 7$ and $H_{\text{strict-from-h1}} = 7$ for both metrics. For example, fractional RMSE was $688.858$ versus seasonal-naive RMSE $1090.638$ at $h = 1$, $1203.452$ versus $1237.408$ at $h = 7$, and $1351.227$ versus $1258.413$ at $h = 8$. This positive-skill window is specific to the seasonal-naive comparison on the evaluated series; it is not an intrinsic epidemiological predictability limit and does not extend to persistence or SARIMA.

### 3.3 Secondary mechanistic axis: practical identifiability and derived stability

Practical-identifiability analysis revealed pronounced non-identifiability of the individual kinetic rate parameters $\beta$, $\gamma$, and $d$ despite near-equivalent calibration fidelity. Across multiseed optimization and one-dimensional profile-objective evaluations, calibration RMSE varied only narrowly ($\text{CV} \approx 0.35\%$, range $605.049$ to $610.388$), whereas $\beta$ varied by a factor of $\approx 5.4$ ($\text{CV} \approx 58.0\%$), $\gamma$ by a factor of $\approx 5.3$ ($\text{CV} \approx 59.9\%$), and $d$ by more than two orders of magnitude ($\text{CV} \approx 82.2\%$). By contrast, the fractional order $\alpha$ exhibited a sharply peaked profile objective and minimal dispersion across optimization seeds ($\text{CV} \approx 0.08\%$, range $0.9620$–$0.9640$). The wide dispersion of $\beta$, $\gamma$, and $d$ among near-equivalent fits precludes interpreting their fitted values as precise epidemiological rates.

Weak individual-parameter identifiability coexisted with comparatively stable predictions and a narrow practical-identifiability envelope for the derived basic reproduction number $R_0$. Across the multiseed ensemble, model-predicted monthly incidence trajectories had mean coefficients of variation of $0.19\%$ during calibration and $0.58\%$ during out-of-sample validation. Within the predefined near-equivalent admissible set ($n = 25$, calibration RMSE degradation $\le 1.0\%$ relative to the primary optimum), $R_0 = \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu + d)}$ ranged from $1.1542$ to $1.1892$ (median $1.1735$, interquartile range $1.1682$–$1.1770$). This range is a practical-identifiability envelope over calibration-equivalent solutions, not a statistical confidence interval or Bayesian credible interval, and it does not extend to the broader 33-member diagnostic pool that includes deliberately poor-fit probes.

Within the same 25-member admissible set, the Disease-Free Equilibrium was locally asymptotically unstable for all solutions under Matignon's criterion ($25/25$ unstable, $0$ stable, $0$ ambiguous). Each calibrated solution produced at least one eigenvalue satisfying $|\arg(\lambda_i)| \le \alpha \pi / 2$, dynamically consistent with $R_0 > 1$ within that admissible set. This is a mathematical property of the fitted dynamical system rather than an empirical claim about real-world transmission in Brazil, and it does not imply operational forecasting efficacy.

---

## 4. Discussion

The primary finding of this independent reimplementation is a divergence between within-family improvement and external forecasting skill. Caputo fractional-order differentiation consistently reduced observed forecast error relative to an independently re-estimated integer-order SEIT comparator across both the long open-loop stress test and the multi-horizon rolling-origin evaluation. Yet the same fractional model showed negative observed skill relative to persistence and SARIMA at every evaluated monthly lead horizon. Restricting evaluation to the mechanistic family would therefore have produced a substantially more favorable assessment of predictive performance than the broader benchmark set (Bracher et al., 2021; Cramer et al., 2022).

This turning point changes the interpretation of the fractional-versus-integer result. Lower forecast error than an integer-order counterpart establishes improvement within the SEIT family, but it is not sufficient evidence that the added fractional flexibility provides competitive out-of-sample forecasting performance. Persistence and SARIMA do not encode compartmental transmission structure, yet their lower observed errors across all twelve lead horizons show why within-family mathematical improvement and forecasting utility must be evaluated separately (Moran et al., 2016; Cramer et al., 2022). The relevant assessment is therefore not only whether a mechanistic extension improves its parent model, but whether that improvement survives comparison with appropriate external baselines under the same temporal protocol.

The interpretation does not depend on claiming that earlier studies omitted such comparisons. Fractional and integer-order epidemic models have been compared under rolling-origin out-of-sample forecasting (Chishtie et al., 2026), fractional SEIR forecasts have been compared with ARIMA forecasts in influenza (Alzahrani et al., 2024), and TB-specific work has shown that SARIMA can outperform a mechanistic SIR model under temporal validation (Kalizhanova et al., 2024). Fractional/integer predictability and identifiability have also been examined directly (Kharazmi et al., 2021), within the broader fractional epidemic-modeling literature reviewed by Chen et al. (2021). The contribution here is therefore not a historical-priority claim. It is the empirical demonstration that a favorable fractional-versus-integer conclusion can change materially when the benchmark set is expanded beyond the model family within a common multi-horizon temporal evaluation.

The positive observed skill relative to seasonal naive ($\text{lag }12$) from $h = 1$ through $h = 7$ is a bounded exception that reinforces the importance of benchmark choice. The corresponding $H_{\text{relax}} = 7$ and $H_{\text{strict-from-h1}} = 7$ are empirical descriptors for this particular baseline and series. They do not define an intrinsic biological predictability horizon and do not support a general forecasting-advantage claim, because observed skill remained negative relative to persistence and SARIMA throughout $h = 1,\dots,12$.

The identifiability analysis provides a secondary constraint on mechanistic interpretation rather than a second novelty claim. Model-predicted trajectories were comparatively stable across calibration solutions, whereas $\beta$, $\gamma$, and $d$ varied widely among near-equivalent fits. Low calibration error and stable trajectories therefore do not imply unique recovery of these individual rates, which should not be interpreted as precise epidemiological quantities (Tuncer & Le, 2018; Roosa & Chowell, 2019). Likewise, the tight numerical stability of the fitted fractional order $\alpha$ does not establish biological or epidemiological memory. Values of $\alpha < 1$ describe the fitted fractional formulation and require independent mechanistic evidence before receiving a biological interpretation.

Some derived dynamical quantities were nevertheless robust across the predefined near-equivalent admissible set. The practical-identifiability envelope for $R_0$ was $1.1542$–$1.1892$ across the 25 admissible solutions, with median $1.1735$ and interquartile range $1.1682$–$1.1770$. This pattern is compatible with compensating parameter variation that preserves a composite functional even when its components are weakly identified (Meshkat et al., 2014; Raue et al., 2009). The range is an operational practical-identifiability envelope, not a confidence or credible interval, and it is restricted to the predefined admissible set rather than the broader diagnostic pool. All 25 admissible solutions also had a locally unstable Disease-Free Equilibrium under Matignon's criterion. That classification is a property of the fitted dynamical systems, not independent empirical evidence of persistent real-world transmission or of forecasting efficacy. These observations are consistent with established results showing that useful predictions or composite quantities can remain stable despite poorly identified individual parameters (Simpson & Maclaren, 2024; Gutenkunst et al., 2007; Meshkat et al., 2014; Kao & Eisenberg, 2018).

Several features of the design bound these conclusions. The study is an independent reimplementation because the historical numerical code and complete configuration were unavailable. The empirical evaluation uses a single national monthly surveillance series; individual kinetic rates are weakly identifiable; the 1% calibration-RMSE admissibility threshold is operational rather than a formal statistical uncertainty region; and the rolling-origin comparisons are descriptive because a dependence-aware predictive-accuracy test was not prespecified. Optimal-control formulations and historical burden-reduction estimates were not reimplemented and remain outside the present evidence base.

Within these boundaries, the main methodological implication is specific: improvement within a mechanistic model family should not, by itself, be interpreted as evidence of forecasting utility. For fractional epidemic models in particular, a favorable fractional-versus-integer comparison should be accompanied by explicit temporal out-of-sample evaluation against appropriate external baselines before the additional fractional flexibility is described as operationally predictive. The identifiability results qualify the mechanistic interpretation of the fitted model, but the central contribution remains the distinction between within-family error reduction and forecasting skill beyond the model family.

---

## 5. Conclusion

This independent reimplementation tested whether lower forecast error from a fractional-order SEIT model relative to an independently re-estimated integer-order counterpart translated into forecasting skill beyond the model family. The fractional formulation produced a consistent within-family improvement across both the long open-loop stress test and the 13-origin rolling-origin evaluation, but observed skill remained negative relative to persistence and SARIMA at every evaluated horizon from $h = 1$ through $h = 12$. Positive observed skill relative to seasonal naive was limited to $h = 1$ through $h = 7$ and is therefore a benchmark-specific empirical result rather than evidence of general forecasting efficacy.

Practical identifiability constrains the mechanistic interpretation of this fitted model but does not alter the primary forecasting conclusion. Individual parameters $\beta$, $\gamma$, and $d$ were weakly identified, whereas predicted trajectories were comparatively stable and the predefined 25-member admissible set yielded a narrow $R_0$ practical-identifiability envelope of $1.1542$–$1.1892$ with uniform local DFE instability under Matignon's criterion. These derived results are bounded properties of the admissible fitted solutions, not confidence intervals, precise parameter recovery, or evidence of operational predictive skill. In this case study, within-family fractional improvement was therefore insufficient to establish a general forecasting advantage beyond the model family: the stronger external-benchmark evaluation remained unfavorable relative to persistence and SARIMA, with positive observed skill confined to the seasonal-naive comparison through $h = 7$.

---

## Declarations

### Funding
[AUTHOR INPUT REQUIRED: State funding sources and grant numbers, or confirm an explicit no-funding statement consistent with the journal requirements.]

### Competing Interests
[AUTHOR CONFIRMATION REQUIRED: Confirm that all final authors have no relevant financial or non-financial interests, or provide the required disclosures.]

### Author Contributions
[AUTHOR INPUT REQUIRED: Final contribution statement for every confirmed author. CRediT taxonomy may be used, but no contribution roles are assumed until the final author list is confirmed.]

### Ethics Approval and Consent to Participate
[AUTHOR CONFIRMATION REQUIRED: Confirm that the analysis uses only aggregate national monthly notification counts with no individual-level or identifiable patient data. If confirmed, state the applicable ethics/consent position in wording consistent with institutional and journal requirements. The repository does not independently establish the original public acquisition route for the supplied observational file.]

### Consent for Publication
Not applicable unless the final manuscript includes identifiable individual material, which the present manuscript does not.

### Data Availability
The canonical observational dataset analyzed in this study is the aggregate monthly Brazil tuberculosis series stored as `data/raw/tb_mes.xlsx`, covering January 2001 through December 2022 ($N=264$). The file is preserved unchanged as supplied by Amaury de Souza for this collaboration and is used directly by the computational pipeline. Repository provenance, including the source-file hash and structural audit, is recorded in `DATA_PROVENANCE.md` and `outputs/audits/source_manifest.csv`.

The supplied repository materials do not independently record the original governmental download URL or acquisition path; these must not be represented as independently verified unless the authors subsequently document them. During peer review, the canonical observational file and reproducible repository bundle or private repository access can be provided to editors and reviewers.

### Code Availability
The computational code implementing the numerical fractional differential equation solver, Differential Evolution calibration, profile-objective practical-identifiability analysis, equilibrium stability analysis, and rolling-origin forecasting benchmarks is tied to frozen computational commit `13015847a6f364505391d4f6e24d9c4c994669ff`. Editorial/documentation commits after this freeze do not modify canonical numerical evidence. The repository is private; a reproducible repository bundle or private access can be supplied during peer review. No public archival DOI currently exists.

### AI Assistance Disclosure
Use of Large Language Model and AI-assisted tools is documented in Methods §2.13 in accordance with the journal's current submission guidance. AI tools are not authors or scientific decision-makers; final scientific responsibility remains with the human authors.

---

## References

1. **Alzahrani, S. M., Saadeh, R., Abdoon, M. A., Qazza, A., El Guma, F., & Berir, M.** (2024). Numerical Simulation of an Influenza Epidemic: Prediction with Fractional SEIR and the ARIMA Model. *Applied Mathematics & Information Sciences*, 18(1), 1–12. [DOI: 10.18576/amis/180101](https://doi.org/10.18576/amis/180101)
2. **Area, I., Batarfi, H., Losada, J., Nieto, J. J., Shammakh, W., & Torres, Á.** (2015). On a fractional order epidemic model with Caputo derivative. *Applied Mathematics Letters*, 40, 23–27. [DOI: 10.1016/j.aml.2014.09.006](https://doi.org/10.1016/j.aml.2014.09.006)
3. **Bracher, J., Ray, E. L., Gneiting, T., & Reich, N. G.** (2021). Evaluating epidemic forecasts in an interval format. *PLOS Computational Biology*, 17(2), e1008618. [DOI: 10.1371/journal.pcbi.1008618](https://doi.org/10.1371/journal.pcbi.1008618)
4. **Chen, Y., Liu, F., Yu, Q., & Li, T.** (2021). Review of fractional epidemic models. *Applied Mathematical Modelling*, 97, 281–307. [DOI: 10.1016/j.apm.2021.03.044](https://doi.org/10.1016/j.apm.2021.03.044)
5. **Chishtie, F. A., Drozd, J., Li, X., Benterki, A., & Valluri, S. R.** (2026). A robust compartmental modeling framework for infectious disease monitoring and analysis via fractional differential equations. *Epidemics*, 54, 100887. [DOI: 10.1016/j.epidem.2026.100887](https://doi.org/10.1016/j.epidem.2026.100887)
6. **Cramer, E. Y., Ray, E. L., Lopez, V. K., et al.** (2022). Evaluation of individual and ensemble probabilistic forecasts of COVID-19 mortality in the US. *Proceedings of the National Academy of Sciences*, 119(15), e2113561119. [DOI: 10.1073/pnas.2113561119](https://doi.org/10.1073/pnas.2113561119)
7. **Diethelm, K.** (2013). A fractional calculus based model for the simulation of an outbreak of dengue fever. *Nonlinear Dynamics*, 71(4), 613–619. [DOI: 10.1007/s11071-012-0475-2](https://doi.org/10.1007/s11071-012-0475-2)
8. **Gutenkunst, R. N., Waterfall, J. J., Casey, F. P., Brown, K. S., Myers, C. R., & Sethna, J. P.** (2007). Universally sloppy parameter sensitivities in systems biology models. *PLOS Computational Biology*, 3(10), e189. [DOI: 10.1371/journal.pcbi.0030189](https://doi.org/10.1371/journal.pcbi.0030189)
9. **Kalizhanova, A., Yerdessov, S., Sakko, Y., Tursynbayeva, A., Kadyrov, S., Gaipov, A., & Kashkynbayev, A.** (2024). Modeling tuberculosis transmission dynamics in Kazakhstan using SARIMA and SIR models. *Scientific Reports*, 14, 24824. [DOI: 10.1038/s41598-024-76721-2](https://doi.org/10.1038/s41598-024-76721-2)
10. **Kao, Y.-H., & Eisenberg, M. C.** (2018). Practical unidentifiability of a simple vector-borne disease model: Implications for parameter estimation and intervention assessment. *Epidemics*, 25, 89–100. [DOI: 10.1016/j.epidem.2018.05.010](https://doi.org/10.1016/j.epidem.2018.05.010)
11. **Kharazmi, E., Cai, M., Zheng, X., Zhang, Z., Lin, G., & Karniadakis, G. E.** (2021). Identifiability and predictability of integer- and fractional-order epidemiological models using physics-informed neural networks. *Nature Computational Science*, 1, 744–753. [DOI: 10.1038/s43588-021-00158-0](https://doi.org/10.1038/s43588-021-00158-0)
12. **Meshkat, N., Kuo, C. E., & Sullivant, S.** (2014). On finding identifiable parameter combinations in nonlinear dynamic systems. *PLOS ONE*, 9(10), e110261. [DOI: 10.1371/journal.pone.0110261](https://doi.org/10.1371/journal.pone.0110261)
13. **Moran, K. R., Fairchild, G., Generous, N., Hickmann, K., Osthus, D., Priedhorsky, R., Hyman, J., & Del Valle, S. Y.** (2016). Epidemic forecasting is messier than weather forecasting: The role of human behavior and Internet data streams in epidemic forecast. *The Journal of Infectious Diseases*, 214(suppl_4), S404–S408. [DOI: 10.1093/infdis/jiw375](https://doi.org/10.1093/infdis/jiw375)
14. **Pelissari, D. M., Rocha, M. S., Bartholomeu, P. V. O., Sanchez, M. N., Duarte, E. C., Arakaki-Sanchez, D., & Diaz-Quijano, F. A.** (2020). Notifiable Diseases Information System (SINAN): main features of tuberculosis notification and data analysis. *Epidemiologia e Serviços de Saúde*, 29(1), e2019154. [DOI: 10.5123/S1679-49742020000100009](https://doi.org/10.5123/S1679-49742020000100009)
15. **Raue, A., Kreutz, C., Maiwald, T., Bachmann, J., Schilling, M., Klingmüller, U., & Timmer, J.** (2009). Structural and practical identifiability analysis of partial differential equation models in systems biology. *Bioinformatics*, 25(15), 1923–1929. [DOI: 10.1093/bioinformatics/btp358](https://doi.org/10.1093/bioinformatics/btp358)
16. **Roosa, S., & Chowell, G.** (2019). Assessing parameter identifiability in compartmental dynamic models using a computational approach: application to infectious disease transmission. *Theoretical Biology and Medical Modelling*, 16, 1. [DOI: 10.1186/s12976-018-0097-6](https://doi.org/10.1186/s12976-018-0097-6)
17. **Simpson, M. J., & Maclaren, O. J.** (2024). Making predictions using poorly identified mathematical models. *Bulletin of Mathematical Biology*, 86, 80. [DOI: 10.1007/s11538-024-01294-0](https://doi.org/10.1007/s11538-024-01294-0)
18. **Tuncer, N., & Le, T. T.** (2018). Structural and practical identifiability analysis of outbreak models. *Mathematical Biosciences*, 299, 1–18. [DOI: 10.1016/j.mbs.2018.02.004](https://doi.org/10.1016/j.mbs.2018.02.004)
19. **World Health Organization.** (2022). *Global Tuberculosis Report 2022*. Geneva: World Health Organization. ISBN 978-92-4-006172-9.
