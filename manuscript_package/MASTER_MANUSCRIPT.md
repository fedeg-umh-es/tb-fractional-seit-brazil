# [TITLE PLACEHOLDER: Fractional-Order SEIT Tuberculosis Modeling in Brazil: An Independent Reimplementation and Forecasting Benchmark Audit]

**Author**: fedeg (Repository Owner / Scientific Lead)  
**Status**: MASTER_MANUSCRIPT_ASSEMBLED (Frozen Draft)  
**Evidence Base**: `results_canonical/` (`FROZEN_WITH_DOCUMENTED_LIMITATIONS`)  

---

## Abstract

Assessing the forecasting utility of fractional-order compartmental models requires distinguishing within-family improvement from performance against external forecasting baselines. This study presents an independent, reproducible reimplementation and methodological audit of a Caputo fractional-order SEIT (Susceptible–Exposed–Infectious–Treated) tuberculosis model applied to national monthly surveillance data from Brazil (2001–2022) with monthly notifications represented as incidence flow rather than infectious-state prevalence. Under both a 24-month long open-loop stress test and a 13-origin expanding rolling-origin evaluation across 12 monthly lead horizons, the fractional SEIT model consistently achieved lower forecast error than an independently re-estimated integer-order SEIT comparator. However, this within-family improvement did not translate into positive observed forecast skill against external statistical benchmarks: both persistence (random walk) and SARIMA yielded lower forecast errors across all twelve lead horizons ($H_{\text{relax}} = 0$). Positive observed skill relative to seasonal naive was confined to lead times $h = 1$ through $h = 7\text{ months}$ ($H_{\text{relax}} = 7$), serving as a baseline-specific empirical descriptor. On the mechanistic axis, calibration revealed pronounced practical non-identifiability for individual kinetic rate parameters ($\beta$, $\gamma$, and $d$), precluding their interpretation as precise biological rates despite stable trajectory predictions. Conversely, derived dynamical properties were functionally robust across the 25-member near-equivalent admissible set ($\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$), defining a narrow practical-identifiability envelope for the basic reproduction number ($R_0 \in [1.1542, 1.1892]$) and uniform local instability of the Disease-Free Equilibrium under Matignon's criterion ($25/25$ unstable). In this evaluation, fractional differentiation provided a consistent within-family improvement, external statistical baselines exposed the limits of interpreting that improvement as forecasting skill, and weak individual parameter identifiability coexisted with robust derived threshold and stability properties across the predefined admissible set.

---

## 1. Introduction

Mechanistic compartmental models are used to represent transmission processes, latent states, and intervention dynamics in infectious-disease systems. In diseases with protracted latency and complex clinical progression, such as tuberculosis—which remains a persistent public health challenge in Brazil (World Health Organization, 2022; Pelissari et al., 2020)—mathematical models often aim to serve dual purposes: providing mechanistic insight into unobserved infection states and generating forward projections of reported surveillance data. However, evaluating the predictive capability of such models requires distinguishing between internal mathematical goodness-of-fit on historical data and genuine out-of-sample forecasting skill. A close calibration fit to historical surveillance records does not ensure that a compartmental model will reliably forecast future trajectory changes when subjected to strict temporal evaluation (Moran et al., 2016; Bracher et al., 2021).

Fractional-order formulations extend compartmental models by replacing integer-order derivatives with non-local operators that introduce power-law temporal dependence (Diethelm, 2013; Area et al., 2015). Such formulations provide a flexible mathematical representation of departures from exponential dynamics, but improvement relative to an integer-order counterpart remains a within-family comparison. While showing that a fractional-order model achieves lower error than its integer-order counterpart establishes within-family structural flexibility, it does not determine whether the formulation provides practical forecasting value over standard, purpose-built statistical or naive forecasting baselines.

A parallel challenge in mechanistic modeling concerns the identifiability of epidemiological parameters. When compartmental systems are calibrated against aggregate surveillance notifications, multiple disparate combinations of kinetic rate parameters can often produce near-identical trajectory fits to the observed data—a condition known as practical non-identifiability (Tuncer & Le, 2018; Roosa & Chowell, 2019; Meshkat et al., 2014). In such settings, low calibration error and stable trajectory projections can mask severe indeterminacy in individual parameter estimates. For the present study, this motivates separating three levels of evidence: individual-parameter identifiability, predictive stability of the fitted trajectories, and robustness of derived quantities such as the basic reproduction number $R_0$.

For this study, these considerations motivate an evaluation framework that explicitly separates within-family model flexibility from external forecasting competitiveness, and individual parameter recovery from derived functional stability. Specifically, this requires testing whether a fractional model: (i) achieves lower forecast error than an independently re-estimated integer-order comparator under identical optimization protocols; (ii) achieves positive out-of-sample forecast skill across multiple lead horizons when benchmarked against external statistical and naive baselines; and (iii) yields robust derived epidemiological quantities despite potential non-identifiability in individual component parameters.

To address these questions, this study presents an independent reimplementation and methodological audit of a fractional-order SEIT (Susceptible–Exposed–Infectious–Treated) tuberculosis model applied to national monthly surveillance data from Brazil spanning 2001 through 2022. The model uses a reference-time-consistent Caputo fractional derivative formulation and incorporates a corrected observation process mapping monthly notifications to monthly incidence flow ($E \to I$) rather than the unobservable infectious stock. Using this audited framework, this study investigates three central questions:
1. Does the fractional-order SEIT formulation improve upon the corresponding integer-order SEIT model under independent parameter re-estimation?
2. Does that within-family improvement translate into positive forecasting skill against standard external statistical baselines across multiple monthly lead horizons?
3. Which mechanistic quantities remain scientifically interpretable given the practical identifiability limits of aggregate surveillance data?

These questions are evaluated across two complementary forecasting protocols—a 24-month single-origin long open-loop stress test and a 13-origin expanding-window rolling-origin evaluation across 12 monthly lead horizons—benchmarked against persistence (random walk), seasonal naive, and SARIMA models. In parallel, practical parameter identifiability, the robustness of the derived $R_0$ practical-identifiability envelope, and local stability of the Disease-Free Equilibrium under Matignon's criterion are evaluated across an admissible set of calibration-equivalent solutions.

---

## 2. Methods

### 2.1 Study design and independent-reimplementation scope

This study is an independent, reproducible reimplementation and methodological audit of a fractional-order Susceptible–Exposed–Infectious–Treated (SEIT) compartmental model applied to monthly tuberculosis surveillance data in Brazil. The original numerical scripts and exact computational configurations associated with earlier historical publications on this model are unrecoverable and unavailable. Consequently, the historical manuscript is treated as a conceptual reference rather than an empirical source of truth (`REPRODUCTION_MODE = INDEPENDENT_REIMPLEMENTATION`). Methodological specifications, parameter bounds, calibration routines, identifiability protocols, and forecasting evaluations are established from explicit, auditable procedures.

The study is designed to assess whether within-family improvements over an independently re-estimated integer-order SEIT comparator extend to external forecasting skill against standard baselines, and to identify which derived mechanistic properties remain robust when individual rate parameters are weakly identified.

Optimal-control interventions and associated historical burden-reduction estimates are outside the scope of this study and were not reimplemented.

### 2.2 Data and observation mapping

The empirical series consists of monthly tuberculosis notification counts for Brazil spanning January 2001 through December 2022 ($N = 264$ consecutive monthly observations). The dataset exhibits complete temporal continuity with zero missing months, zero duplicated dates, and zero missing values. 

The dataset is partitioned into two distinct periods:
* **Calibration window**: January 2001 to December 2020 ($N_{\text{cal}} = 240$ months).
* **Validation window**: January 2021 to December 2022 ($N_{\text{val}} = 24$ months).

The total population series $N(t)$ serves as the denominator in the standard incidence force-of-infection term. For the calibration window (2001–2020), $N(t)$ is obtained directly from the surveillance dataset. For out-of-sample simulation, population values beyond each training endpoint were generated using a log-linear trend fitted exclusively to population observations available within the corresponding training window:
$$\ln N(t) = a_0 + a_1 t, \quad t \le t_{\text{train}}$$
No population observations beyond the relevant training endpoint were used.

Surveillance records from Brazil's National System for Notifiable Diseases (SINAN) report newly diagnosed active tuberculosis cases aggregated over monthly intervals. These records represent an incidence flow rather than the standing stock of infectious individuals $I(t)$. Equating monthly case reports directly to $I(t)$ constitutes a stock-flow mis-specification. To accurately represent the data-generating mechanism, monthly reported cases are mapped to the transition flow from the exposed compartment $E$ to the infectious compartment $I$. An auxiliary fractional state accumulator $C(t)$ tracks cumulative incidence:
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

Model calibration is performed by optimizing the free parameter vector $\theta = (\beta, \sigma, \gamma, d, \alpha)$ using Differential Evolution (`scipy.optimize.differential_evolution`). The algorithm configuration is pre-registered as:
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

To guarantee determinism and reproducibility, pseudorandom number generators are seeded with explicit pre-registered values:
* Canonical primary seed: `20260815`
* Diagnostic seeds: `20260816`, `20260817`, `20260818`, `20260819`

The canonical primary calibration run was tied to seed `20260815`; the diagnostic seeds were used exclusively for identifiability and robustness analyses.

### 2.5 Integer-order comparator

To evaluate the specific contribution of fractional differentiation within the SEIT family, an integer-order counterpart is defined by fixing $\alpha \equiv 1.0$.

Under the fair-comparison principle, the integer comparator's remaining parameters $\theta_{\text{int}} = (\beta, \sigma, \gamma, d)$ are re-estimated independently using the identical Differential Evolution configuration, objective function, and parameter bounds over the calibration window. The integer model is never evaluated by simply setting $\alpha = 1.0$ within the parameter vector calibrated for the fractional model.

### 2.6 Practical-identifiability analysis

Practical parameter identifiability is evaluated across the calibration dataset using a two-stage protocol:
1. **Multiseed optimization ensemble**: Optimization across the five pre-registered seeds to detect stochastic solution dispersion under identical hyperparameter settings.
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

---

## 3. Results

### 3.1 Evaluation protocols and within-family comparison

Evaluation of the fractional-order SEIT model was conducted under two distinct, unmixed empirical protocols: a 24-month continuous single-origin long open-loop stress test spanning 2021-01 through 2022-12 following calibration on 2001-01 through 2020-12 ($N_{\text{cal}} = 240$), and a multi-origin expanding-window rolling-origin evaluation incorporating 13 consecutive forecast origins (2020-12 through 2021-12) evaluated across 12 monthly lead horizons ($h = 1, \dots, 12$). The single-origin stress test evaluates multi-year continuous dynamical stability from a fixed calibration point, whereas the rolling-origin protocol provides a multi-horizon assessment of out-of-sample predictive accuracy against external statistical baselines with strict temporal separation.

Under both evaluation protocols, the fractional-order SEIT formulation achieved lower observed forecast error than the independently refitted integer-order SEIT comparator across all evaluated horizons. In the 24-month long open-loop stress test, the fractional SEIT model yielded an RMSE of $1117.960$ and MAE of $953.230$ (bias: $-851.150$), compared to an RMSE of $1759.538$ and MAE of $1588.649$ (bias: $-1588.649$) for the independently refitted integer comparator. Across the 13 rolling-origin evaluations, the fractional formulation produced lower RMSE and MAE than the integer model at every lead horizon from $h = 1$ to $h = 12$ (for example, at $h = 1$: fractional RMSE $688.858$ vs. integer $1185.796$; at $h = 6$: fractional RMSE $1138.323$ vs. integer $1770.697$; at $h = 12$: fractional RMSE $1355.984$ vs. integer $2022.492$). Because the integer comparator's parameters were re-estimated independently from scratch rather than inherited from the fractional fit, this performance margin represents a consistent within-model-family improvement.

### 3.2 External baseline evaluation and turning point

The error reduction achieved by the fractional SEIT formulation over its integer-order counterpart did not translate into positive forecasting skill when evaluated against external statistical benchmarks. When evaluated against the persistence (random walk) and SARIMA baselines, the fractional SEIT model exhibited negative observed forecast skill across all 12 evaluated lead horizons for both RMSE and MAE ($H_{\text{relax}} = 0$, $H_{\text{strict-from-h1}} = 0$). In descriptive sample terms across the 13 rolling origins, both persistence and SARIMA achieved lower forecast errors than the fractional SEIT model at every horizon:
* At $h = 1\text{ month}$: fractional RMSE was $688.858$, compared to $389.702$ for persistence and $535.547$ for SARIMA.
* At $h = 6\text{ months}$: fractional RMSE was $1138.323$, compared to $845.856$ for persistence and $1022.421$ for SARIMA.
* At $h = 12\text{ months}$: fractional RMSE was $1355.984$, compared to $1152.958$ for persistence and $1283.583$ for SARIMA.

Thus, the consistent within-family error reduction did not translate into positive observed skill against persistence or SARIMA at any evaluated horizon.

In contrast to persistence and SARIMA, the fractional SEIT model achieved positive observed forecast skill relative to the seasonal naive baseline ($\text{lag } 12$) at short horizons, transitioning to negative skill at longer lead times. Observed RMSE and MAE skill relative to seasonal naive were positive from $h = 1$ through $h = 7\text{ months}$ and negative from $h = 8$ through $h = 12\text{ months}$, corresponding to empirical horizon descriptors of $H_{\text{relax}} = 7$ and $H_{\text{strict-from-h1}} = 7$ for both error metrics (for example, at $h = 1$: fractional RMSE $688.858$ vs. seasonal naive $1090.638$; at $h = 7$: fractional RMSE $1203.452$ vs. seasonal naive $1237.408$; at $h = 8$: fractional RMSE $1351.227$ vs. seasonal naive $1258.413$). This seven-month positive-skill window functions strictly as an empirical descriptor of performance against this specific seasonal benchmark on the evaluated series, and does not represent an intrinsic epidemiological predictability limit or extend to the other external baselines.

### 3.3 Practical identifiability, derived functional stability, and equilibrium dynamics

Systematic practical-identifiability analysis on the calibration dataset revealed pronounced non-identifiability for individual kinetic rate parameters $\beta$, $\gamma$, and $d$, despite near-identical calibration fidelity. In both multiseed optimization and one-dimensional profile-objective evaluations, solutions achieving calibration RMSE within a tight coefficient of variation ($\text{CV} \approx 0.35\%$, spanning $605.049$ to $610.388$) exhibited substantial parameter dispersion: effective contact rate $\beta$ varied by a factor of $\approx 5.4$ ($\text{CV} \approx 58.0\%$), removal rate $\gamma$ varied by a factor of $\approx 5.3$ ($\text{CV} \approx 59.9\%$), and tuberculosis-induced mortality hazard $d$ varied across two orders of magnitude ($> 100\times$, $\text{CV} \approx 82.2\%$). Conversely, fractional order $\alpha$ exhibited a sharply peaked profile objective with minimal dispersion across optimization seeds ($\text{CV} \approx 0.08\%$, range $0.9620$–$0.9640$). Because widely disparate combinations of $\beta$, $\gamma$, and $d$ yield near-equivalent calibration fits, individual rate parameter estimates cannot be interpreted as precise epidemiological quantities.

Weak individual parameter identifiability coexisted with high predictive stability and a narrow practical-identifiability envelope for the derived basic reproduction number $R_0$. Across the multiseed ensemble, model-predicted monthly incidence trajectories displayed a mean coefficient of variation of only $0.19\%$ during calibration and $0.58\%$ across out-of-sample validation. Within the predefined near-equivalent admissible solution set ($n = 25$ solutions with calibration RMSE degradation $\le 1.0\%$ relative to the primary optimum), the derived composite functional $R_0 = \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu + d)}$ remained strictly bounded above unity, with a minimum of $1.1542$, first quartile ($Q_1$) of $1.1682$, median of $1.1735$, third quartile ($Q_3$) of $1.1770$, and maximum of $1.1892$ (interquartile range: $1.1682$–$1.1770$). This variation defines a practical-identifiability envelope across calibration-equivalent parameter sets, and does not represent a statistical confidence interval or Bayesian credible interval. This admissible envelope is distinct from the broader 33-member profile diagnostic pool, which includes deliberately exploratory, poor-fit probe points.

Under the reference-time-consistent Caputo fractional formulation and Matignon's stability theorem, the Disease-Free Equilibrium (DFE) was locally asymptotically unstable across all 25 solutions in the near-equivalent admissible set ($25/25$ unstable, $0$ stable, $0$ ambiguous). Linearization of the fractional system at the DFE using each solution's calibrated parameters and specific fitted fractional order $\alpha$ yielded at least one eigenvalue satisfying $|\arg(\lambda_i)| \le \alpha \pi / 2$, dynamically consistent with $R_0 > 1$. This instability classification is strictly a mathematical property of the fitted dynamical model across the admissible solution set, and does not constitute an empirical assertion regarding real-world tuberculosis transmission dynamics in Brazil. Furthermore, this result is restricted to the near-equivalent admissible set (two high-error diagnostic probe solutions in the broader 33-member pool exhibited $R_0 < 1$ with stable DFE) and does not imply operational forecasting efficacy.

---

## 4. Discussion

The primary scientific finding of this independent reimplementation is an empirical divergence between within-family structural improvement and external forecasting skill. Incorporating Caputo fractional-order differentiation consistently reduced forecast error relative to an independently re-estimated integer-order SEIT comparator across both long-horizon open-loop simulation and multi-horizon rolling-origin cross-validation. However, this within-family advantage did not translate into positive observed forecast skill when evaluated against standard statistical baselines: both persistence (random walk) and SARIMA achieved lower forecast errors than the fractional SEIT formulation across all twelve evaluated monthly lead horizons. In this evaluation, restricting comparison to variants within the same compartmental family would have produced a substantially more favorable assessment of predictive performance than comparison against external statistical baselines (Bracher et al., 2021; Cramer et al., 2022).

The negative skill observed against persistence and SARIMA provides an essential methodological baseline for epidemiological forecasting. In practical surveillance contexts, the relevant question is rarely whether a fractional compartmental model improves upon its integer-order counterpart, but whether its mechanistic structure provides predictive value beyond standard statistical alternatives. The finding that fractional SEIT outperforms integer SEIT while trailing persistence and SARIMA shows that lower error relative to the integer-order SEIT comparator is not sufficient evidence of competitive out-of-sample forecasting performance. While statistical time-series models do not encode compartmental transmission mechanisms, their operational forecast accuracy highlights the need to treat within-family mathematical improvements and operational forecasting utility as distinct scientific questions (Moran et al., 2016; Cramer et al., 2022). This separation is pertinent to the broader fractional epidemic modeling literature, where model comparisons have predominantly relied on within-family or in-sample metrics without evaluation against external statistical baselines (Chen et al., 2021; Kharazmi et al., 2021).

The observation of positive forecast skill relative to seasonal naive ($\text{lag } 12$) for lead horizons $h = 1$ through $h = 7\text{ months}$ represents a bounded, benchmark-specific exception. This result illustrates that evaluations of predictive skill are sensitive to baseline choice and forecast horizon. However, this seven-month window ($H_{\text{relax}} = 7$, $H_{\text{strict-from-h1}} = 7$) functions strictly as an empirical sample descriptor of performance against this specific naive benchmark on the Brazilian surveillance series. It does not denote an intrinsic biological predictability limit, nor does it rescue a broader claim of operational forecasting efficacy given the negative skill observed against persistence and SARIMA across the entire twelve-month horizon.

On the mechanistic axis, calibration revealed that high predictive trajectory stability can coexist with severe practical non-identifiability of individual kinetic rate parameters. While model-predicted monthly case trajectories were nearly identical across optimization seeds and profile explorations, individual parameters $\beta$, $\gamma$, and $d$ varied across wide ranges ($\approx 5.4$-fold for $\beta$, $\approx 5.3$-fold for $\gamma$, and over two orders of magnitude for $d$) among near-equivalent calibration fits. Consequently, low calibration RMSE and stable forecasts do not imply unique parameter recovery, and individual rate estimates cannot be interpreted as precise epidemiological quantities (Tuncer & Le, 2018; Roosa & Chowell, 2019). Furthermore, although the estimated fractional order $\alpha$ exhibited tight numerical stability across calibration seeds ($\text{CV} \approx 0.08\%$), values of $\alpha < 1$ reflect the numerical behavior of the fitted power-law kernel and cannot be interpreted as empirical evidence of biological or epidemiological memory without independent mechanistic verification.

In sharp contrast to the instability of individual rate parameters, the derived basic reproduction number $R_0 = \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu + d)}$ was functionally identifiable, remaining tightly constrained between $1.1542$ and $1.1892$ (median $1.1735$, interquartile range $1.1682$–$1.1770$) across the 25-member near-equivalent admissible set. This pattern is consistent with compensating variation among individual parameters that preserves the composite transmission-to-removal functional defining $R_0$ (Meshkat et al., 2014; Raue et al., 2009). This range constitutes an empirical practical-identifiability envelope over calibration-equivalent fits, and must not be conflated with a statistical confidence interval or Bayesian credible interval. Moreover, this robustness is property of the predefined admissible solution set ($\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$) and does not generalize to the broader 33-solution diagnostic exploration, which includes deliberately exploratory, poor-fit probe points.

The coexistence of parameter non-identifiability with robust predictions and derived functional quantities is consistent with established principles in mathematical biology. The concept that mechanistic models can yield informative predictions despite poorly identified parameters has been formally examined across compartmental and growth models (Simpson & Maclaren, 2024; Gutenkunst et al., 2007), and the possibility that composite epidemiological quantities such as $R_0$ remain identifiable when individual component parameters do not has been documented in both structural and practical identifiability analyses (Meshkat et al., 2014; Kao & Eisenberg, 2018). Accordingly, the identifiability findings of this study are presented as an applied empirical demonstration of these principles in a specific fractional-order SEIT evaluation, rather than as methodological contributions in their own right.

The local asymptotic instability of the Disease-Free Equilibrium (DFE) across all 25 admissible solutions ($25/25$ unstable under Matignon's criterion) confirms that equilibrium dynamics are robustly determined across near-equivalent calibrations and dynamically consistent with $R_0 > 1$. However, this instability classification is strictly a mathematical property of the calibrated dynamical system over the admissible set. It does not constitute an independent empirical assertion that tuberculosis transmission in Brazil is necessarily persistent. Crucially, internal dynamical coherence and derived functional robustness must not be conflated with forecasting efficacy: a model may possess mathematically consistent equilibrium properties while remaining uncompetitive against simple statistical forecasting baselines.

The findings of this study are subject to several explicit methodological boundaries. First, this work is an independent reimplementation conducted in the absence of unrecoverable historical code and configurations. Second, empirical evaluations are based on a single national monthly surveillance series, bounding empirical generalization. Third, individual rate parameters remain weakly identifiable, precluding their interpretation as direct biological rates. Fourth, the 1% calibration RMSE admissibility threshold is an operational identifiability envelope rather than a formal statistical boundary. Fifth, rolling-origin forecast evaluations are descriptive sample comparisons across thirteen origins; formal inferential testing was omitted because error dependence across overlapping multi-step horizons was not prespecified. Finally, optimal-control formulations and historical burden-reduction estimates were not reimplemented and remain unverified. Within these bounds, fractional differentiation provides a consistent within-family improvement to the SEIT compartmental model, external statistical baselines delineate the boundaries of its forecasting capability, and parameter non-identifiability limits point estimation while permitting robust derived functional and stability analyses across admissible solutions.

---

## 5. Conclusion

This independent reimplementation and methodological audit established that incorporating Caputo fractional-order differentiation provides a consistent within-family improvement to the SEIT compartmental model, yielding lower forecast error than an independently re-estimated integer-order SEIT comparator across both single-origin long-horizon simulation and 13-origin rolling-origin cross-validation. However, this within-family advantage did not translate into positive observed forecast skill against standard statistical baselines: both persistence (random walk) and SARIMA achieved lower forecast errors across all twelve evaluated monthly lead horizons. Positive observed forecast skill relative to seasonal naive ($\text{lag } 12$) was confined to lead times $h = 1$ through $h = 7\text{ months}$, serving strictly as an empirical sample descriptor for that specific naive benchmark rather than general forecasting efficacy.

On the mechanistic axis, calibration demonstrated that high predictive trajectory stability coexists with substantial practical non-identifiability of individual kinetic rate parameters ($\beta$, $\gamma$, and $d$), precluding their interpretation as precise biological rates. In contrast, derived dynamical quantities were functionally robust across the predefined near-equivalent admissible set ($n = 25$ solutions with $\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$), defining a narrow practical-identifiability envelope for the basic reproduction number ($R_0 \in [1.1542, 1.1892]$) and uniform local instability of the Disease-Free Equilibrium under Matignon's criterion. In this descriptive evaluation on Brazilian national surveillance data, fractional differentiation provided a consistent within-family improvement, external statistical baselines exposed the limits of interpreting that improvement as forecasting skill, and weak individual parameter identifiability coexisted with robust derived threshold and stability properties within the predefined admissible set.

---

## References

1. **Area, I., Batarfi, H., Losada, J., Nieto, J. J., Shammakh, W., & Torres, Á.** (2015). On a fractional order epidemic model with Caputo derivative. *Applied Mathematics Letters*, 40, 23–27. [DOI: 10.1016/j.aml.2014.09.006](https://doi.org/10.1016/j.aml.2014.09.006)
2. **Bracher, J., Ray, E. L., Gneiting, T., & Reich, N. G.** (2021). Evaluating epidemic forecasts in an interval format. *PLOS Computational Biology*, 17(2), e1008618. [DOI: 10.1371/journal.pcbi.1008618](https://doi.org/10.1371/journal.pcbi.1008618)
3. **Chen, Y., Liu, F., Yu, Q., & Li, T.** (2021). Review of fractional epidemic models. *Applied Mathematical Modelling*, 97, 281–307. [DOI: 10.1016/j.apm.2021.03.044](https://doi.org/10.1016/j.apm.2021.03.044)
4. **Cramer, E. Y., Ray, E. L., Lopez, V. K., et al.** (2022). Evaluation of individual and ensemble probabilistic forecasts of COVID-19 mortality in the US. *Proceedings of the National Academy of Sciences*, 119(15), e2113561119. [DOI: 10.1073/pnas.2113561119](https://doi.org/10.1073/pnas.2113561119)
5. **Diethelm, K.** (2013). A fractional calculus based model for the simulation of an outbreak of dengue fever. *Nonlinear Dynamics*, 71(4), 613–619. [DOI: 10.1007/s11071-012-0475-2](https://doi.org/10.1007/s11071-012-0475-2)
6. **Gutenkunst, R. N., Waterfall, J. J., Casey, F. P., Brown, K. S., Myers, C. R., & Sethna, J. P.** (2007). Universally sloppy parameter sensitivities in systems biology models. *PLOS Computational Biology*, 3(10), e189. [DOI: 10.1371/journal.pcbi.0030189](https://doi.org/10.1371/journal.pcbi.0030189)
7. **Kao, Y.-H., & Eisenberg, M. C.** (2018). Practical unidentifiability of a simple vector-borne disease model: Implications for parameter estimation and intervention assessment. *Epidemics*, 25, 89–100. [DOI: 10.1016/j.epidem.2018.05.010](https://doi.org/10.1016/j.epidem.2018.05.010)
8. **Kharazmi, E., Cai, M., Zheng, X., Zhang, Z., Lin, G., & Karniadakis, G. E.** (2021). Identifiability and predictability of integer- and fractional-order epidemiological models using physics-informed neural networks. *Nature Computational Science*, 1, 744–753. [DOI: 10.1038/s43588-021-00158-0](https://doi.org/10.1038/s43588-021-00158-0)
9. **Meshkat, N., Kuo, C. E., & Sullivant, S.** (2014). On finding identifiable parameter combinations in nonlinear dynamic systems. *PLOS ONE*, 9(10), e110261. [DOI: 10.1371/journal.pone.0110261](https://doi.org/10.1371/journal.pone.0110261)
10. **Moran, K. R., Fairchild, G., Generous, N., Hickmann, K., Osthus, D., Priedhorsky, R., Hyman, J., & Del Valle, S. Y.** (2016). Epidemic forecasting is messier than weather forecasting: The role of human behavior and Internet data streams in epidemic forecast. *The Journal of Infectious Diseases*, 214(suppl_4), S404–S408. [DOI: 10.1093/infdis/jiw375](https://doi.org/10.1093/infdis/jiw375)
11. **Pelissari, D. M., Rocha, M. S., Bartholomeu, P. V. O., Sanchez, M. N., Duarte, E. C., Arakaki-Sanchez, D., & Diaz-Quijano, F. A.** (2020). Notifiable Diseases Information System (SINAN): main features of tuberculosis notification and data analysis. *Epidemiologia e Serviços de Saúde*, 29(1), e2019154. [DOI: 10.5123/S1679-49742020000100009](https://doi.org/10.5123/S1679-49742020000100009)
12. **Raue, A., Kreutz, C., Maiwald, T., Bachmann, J., Schilling, M., Klingmüller, U., & Timmer, J.** (2009). Structural and practical identifiability analysis of partial differential equation models in systems biology. *Bioinformatics*, 25(15), 1923–1929. [DOI: 10.1093/bioinformatics/btp358](https://doi.org/10.1093/bioinformatics/btp358)
13. **Roosa, S., & Chowell, G.** (2019). Assessing parameter identifiability in compartmental dynamic models using a computational approach: application to infectious disease transmission. *Theoretical Biology and Medical Modelling*, 16, 1. [DOI: 10.1186/s12976-018-0094-2](https://doi.org/10.1186/s12976-018-0094-2)
14. **Simpson, M. J., & Maclaren, O. J.** (2024). Making predictions using poorly identified mathematical models. *Bulletin of Mathematical Biology*, 86, 80. [DOI: 10.1007/s11538-024-01294-0](https://doi.org/10.1007/s11538-024-01294-0)
15. **Tuncer, N., & Le, T. T.** (2018). Structural and practical identifiability analysis of outbreak models. *Mathematical Biosciences*, 299, 1–18. [DOI: 10.1016/j.mbs.2018.02.004](https://doi.org/10.1016/j.mbs.2018.02.004)
16. **World Health Organization.** (2022). *Global Tuberculosis Report 2022*. Geneva: World Health Organization. ISBN 978-92-4-006172-9.
