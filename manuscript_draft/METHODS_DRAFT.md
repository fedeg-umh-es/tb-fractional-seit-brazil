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
