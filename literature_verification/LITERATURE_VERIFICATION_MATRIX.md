# Literature Verification Matrix

This matrix documents the candidate literature sources evaluated to support the framing, methodology, and interpretation of the TB SEIT manuscript, mapped across topics L1–L5.

---

## Matrix of Verified Sources

### L1 — Tuberculosis Epidemiology and Surveillance in Brazil

#### L1-01
* **ID**: L1-01
* **TOPIC**: L1 — Tuberculosis epidemiology in Brazil
* **FULL_CITATION**: World Health Organization. (2022). *Global Tuberculosis Report 2022*. Geneva: World Health Organization.
* **YEAR**: 2022
* **DOI_OR_IDENTIFIER**: ISBN 978-92-4-006172-9
* **SOURCE_TYPE**: Official Global Health Report (WHO)
* **CLAIM_SUPPORTED**: Tuberculosis remains a substantial and persistent public health burden in Brazil; Brazil is designated as a high-burden country for TB and TB/HIV co-infection.
* **CLAIM_NOT_SUPPORTED**: Sub-national transmission disparities; specific monthly seasonality dynamics.
* **INTRODUCTION_LOCATION**: Paragraph 1 (I1)
* **DISCUSSION_LOCATION**: N/A (background context)
* **RECOMMENDED_USE**: Cite in Introduction Paragraph 1 to anchor the public health relevance of tuberculosis in Brazil without quoting volatile annual incidence figures.
* **STATUS**: KEEP

#### L1-02
* **ID**: L1-02
* **TOPIC**: L1 — Surveillance data and SINAN notification system
* **FULL_CITATION**: Rocha, M. S., Bartholomay, P., Cavalcante, M. V., Medeiros, F. C. de, Codenotti, S. B., Pelissari, D. M., Andrade, K. B., Silva, G. D. M. da, Arakaki-Sanchez, D., & Pinheiro, R. S. (2020). Sistema de Informação de Agravos de Notificação (Sinan): principais características da notificação e da análise de dados relacionada à tuberculose. *Epidemiologia e Serviços de Saúde*, 29(1).
* **YEAR**: 2020
* **DOI_OR_IDENTIFIER**: DOI: 10.5123/S1679-49742020000100009
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Surveillance Methodology
* **CLAIM_SUPPORTED**: The Notifiable Diseases Information System (SINAN) is the official national platform for mandatory TB notification, continuous epidemiological monitoring, and case surveillance in Brazil.
* **CLAIM_NOT_SUPPORTED**: Mathematical model forecasting performance.
* **INTRODUCTION_LOCATION**: Paragraph 1 (I1)
* **DISCUSSION_LOCATION**: N/A
* **RECOMMENDED_USE**: Cite when referring to Brazilian national surveillance records and notification data.
* **STATUS**: KEEP

---

### L2 — External-Baseline Evaluation of Mechanistic Epidemic Forecasting Models

#### L2-01
* **ID**: L2-01
* **TOPIC**: L2 — Goodness-of-fit vs. out-of-sample forecasting skill
* **FULL_CITATION**: Moran, K. R., Fairchild, G., Generous, N., Hickmann, K., Osthus, D., Priedhorsky, R., Hyman, J., & Del Valle, S. Y. (2016). Epidemic forecasting is messier than weather forecasting: The role of human behavior and Internet data streams in epidemic forecast. *The Journal of Infectious Diseases*, 214(suppl_4), S404–S408.
* **YEAR**: 2016
* **DOI_OR_IDENTIFIER**: DOI: 10.1093/infdis/jiw375
* **SOURCE_TYPE**: Peer-reviewed Methodological / Perspective Paper
* **CLAIM_SUPPORTED**: Epidemic forecasting must contend with incomplete and inaccurate data and with changes in human behavior, and is more challenging than weather forecasting (abstract level).
* **CLAIM_NOT_SUPPORTED**: Any validation protocol or the statement that goodness-of-fit does not imply out-of-sample accuracy; fractional-order compartmental formulations specifically.
* **INTRODUCTION_LOCATION**: Paragraph 1 (I1)
* **DISCUSSION_LOCATION**: Paragraph 2 (D2)
* **RECOMMENDED_USE**: Cite only for the difficulties of epidemic forecasting (incomplete data, changing behavior); the fit-versus-forecast distinction is the authors' own framing.
* **STATUS**: KEEP

#### L2-02
* **ID**: L2-02
* **TOPIC**: L2 — External baseline evaluation and benchmark standards
* **FULL_CITATION**: Bracher, J., Ray, E. L., Gneiting, T., & Reich, N. G. (2021). Evaluating epidemic forecasts in an interval format. *PLOS Computational Biology*, 17(2), e1008618.
* **YEAR**: 2021
* **DOI_OR_IDENTIFIER**: DOI: 10.1371/journal.pcbi.1008618
* **SOURCE_TYPE**: Peer-reviewed Methodological Framework
* **CLAIM_SUPPORTED**: Evaluation of quantile and interval forecasts with the weighted interval score, a proper score that generalizes the absolute error to probabilistic forecasts (abstract level).
* **CLAIM_NOT_SUPPORTED**: The choice of baselines or the need for external benchmarking; tuberculosis transmission specifically.
* **INTRODUCTION_LOCATION**: N/A (removed 2026-10-08)
* **DISCUSSION_LOCATION**: N/A (removed 2026-10-08)
* **RECOMMENDED_USE**: Not cited in the manuscript. Cite only if probabilistic interval scores are used.
* **STATUS**: NOT CITED (removed from the manuscript 2026-10-08)

#### L2-03
* **ID**: L2-03
* **TOPIC**: L2 — Multi-model forecasting benchmarks and baseline floor
* **FULL_CITATION**: Cramer, E. Y., Ray, E. L., Lopez, V. K., et al. (2022). Evaluation of individual and ensemble probabilistic forecasts of COVID-19 mortality in the United States. *Proceedings of the National Academy of Sciences*, 119(15), e2113561119.
* **YEAR**: 2022
* **DOI_OR_IDENTIFIER**: DOI: 10.1073/pnas.2113561119
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Multi-model Evaluation
* **CLAIM_SUPPORTED**: Of 27 models with complete forecasts of COVID-19 deaths in the United States, two thirds were more accurate than a naive baseline, with high variability in skill across time, locations and horizons (abstract level).
* **CLAIM_NOT_SUPPORTED**: That the present study's own result (fractional SEIT vs external baselines); universality of compartmental failures.
* **INTRODUCTION_LOCATION**: Optional
* **DISCUSSION_LOCATION**: Paragraph 2 (D2)
* **RECOMMENDED_USE**: Cite in the Discussion only as an example of a large forecast evaluation that uses a naive baseline as reference.
* **STATUS**: KEEP

#### L2-04
* **ID**: L2-04
* **TOPIC**: L2 — Time-series cross-validation and standard baseline models
* **FULL_CITATION**: Hyndman, R. J., & Athanasopoulos, G. (2018). *Forecasting: principles and practice* (2nd ed.). Melbourne, Australia: OTexts.
* **YEAR**: 2018
* **DOI_OR_IDENTIFIER**: ISBN 978-0987507112 (URL: otexts.com/fpp2)
* **SOURCE_TYPE**: Authoritative Textbook / Methodology
* **CLAIM_SUPPORTED**: Standard definitions of naive, seasonal naive, SARIMA, expanding-window rolling-origin evaluation, and multi-step forecast horizon metrics.
* **CLAIM_NOT_SUPPORTED**: Epidemiological compartmental ODEs.
* **INTRODUCTION_LOCATION**: Optional (Methods §2.10–2.11)
* **DISCUSSION_LOCATION**: N/A
* **RECOMMENDED_USE**: Foundational reference for rolling-origin evaluation and standard statistical benchmarks.
* **STATUS**: KEEP (Optional for Intro/Discussion)

---

### L3 — Fractional-Order Compartmental Models in Infectious-Disease Modelling

#### L3-01
* **ID**: L3-01
* **TOPIC**: L3 — Fractional-order compartmental modeling
* **FULL_CITATION**: Diethelm, K. (2013). A fractional calculus based model for the simulation of an outbreak of dengue fever. *Nonlinear Dynamics*, 71(4), 613–619.
* **YEAR**: 2013
* **DOI_OR_IDENTIFIER**: DOI: 10.1007/s11071-012-0475-2
* **SOURCE_TYPE**: Peer-reviewed Primary Research
* **CLAIM_SUPPORTED**: Fractional-order derivatives replace standard integer-order rates with non-local operators, providing a mathematical framework for non-exponential waiting times and memory-dependent dynamics in compartmental disease models.
* **CLAIM_NOT_SUPPORTED**: Empirical proof of immunological or biological memory in human hosts.
* **INTRODUCTION_LOCATION**: Paragraph 2 (I2)
* **DISCUSSION_LOCATION**: Paragraph 4 (D4)
* **RECOMMENDED_USE**: Cite in Introduction I2 to document fractional differential equations as compartmental extensions.
* **STATUS**: KEEP

#### L3-02
* **ID**: L3-02
* **TOPIC**: L3 — Caputo fractional epidemic formulations
* **FULL_CITATION**: Area, I., Batarfi, H., Losada, J., Nieto, J. J., Shammakh, W., & Torres, Á. (2015). On a fractional order Ebola epidemic model. *Advances in Difference Equations*, 2015, 278. DOI: 10.1186/s13662-015-0613-5.
* **YEAR**: 2015
* **DOI_OR_IDENTIFIER**: DOI: 10.1186/s13662-015-0613-5
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Applied Mathematics
* **CLAIM_SUPPORTED**: A fractional-order SEIR model for Ebola, compared with the classical SEIR model and with WHO case counts; the fractional order is presented as an index of memory and the derivatives are non-local (full text read 2026-10-08).
* **CLAIM_NOT_SUPPORTED**: That the model uses the Caputo derivative: the paper defines the Riemann–Liouville derivative, recalls the Caputo derivative, and writes the system with an unlabeled D^α (solved with the Adams–Bashforth–Moulton PECE scheme). Operational forecasting efficacy against external benchmarks.
* **INTRODUCTION_LOCATION**: Paragraph 2 (I2)
* **DISCUSSION_LOCATION**: N/A
* **RECOMMENDED_USE**: Cite in I2 to anchor Caputo fractional derivative applications in compartmental epidemiology.
* **STATUS**: KEEP

#### L3-03
* **ID**: L3-03
* **TOPIC**: L3 — Mathematical foundations of fractional differential equations
* **FULL_CITATION**: Baleanu, D., Diethelm, K., Scalas, E., & Trujillo, J. J. (2012). *Fractional Calculus: Models and Numerical Methods*. Singapore: World Scientific.
* **YEAR**: 2012
* **DOI_OR_IDENTIFIER**: DOI: 10.1142/8180
* **SOURCE_TYPE**: Authoritative Monograph
* **CLAIM_SUPPORTED**: Mathematical definition and properties of Caputo fractional derivatives, non-local power-law kernels, and Adams-Bashforth-Moulton predictor-corrector numerical methods.
* **CLAIM_NOT_SUPPORTED**: Specific TB epidemiology.
* **INTRODUCTION_LOCATION**: Optional (Methods §2.3)
* **DISCUSSION_LOCATION**: N/A
* **RECOMMENDED_USE**: Foundational mathematical citation.
* **STATUS**: KEEP

---

### L4 — Parameter and Functional Identifiability in Compartmental Models

#### L4-01
* **ID**: L4-01
* **TOPIC**: L4 — Structural and practical identifiability in outbreak models
* **FULL_CITATION**: Tuncer, N., & Le, T. T. (2018). Structural and practical identifiability analysis of outbreak models. *Mathematical Biosciences*, 299, 1–18.
* **YEAR**: 2018
* **DOI_OR_IDENTIFIER**: DOI: 10.1016/j.mbs.2018.02.004
* **SOURCE_TYPE**: Peer-reviewed Methodological / Primary Research
* **CLAIM_SUPPORTED**: Practical non-identifiability arises when calibrating compartmental models against aggregate incidence data; multiple disparate parameter vectors yield nearly identical calibration errors (flat profile objectives).
* **CLAIM_NOT_SUPPORTED**: Fractional tuberculosis models specifically.
* **INTRODUCTION_LOCATION**: Paragraph 3 (I3)
* **DISCUSSION_LOCATION**: Paragraph 4 (D4)
* **RECOMMENDED_USE**: Cite in I3 and D4 to establish the concept of practical non-identifiability and flat objective landscapes in compartmental calibration.
* **STATUS**: KEEP

#### L4-02
* **ID**: L4-02
* **TOPIC**: L4 — Computational parameter identifiability and profile likelihood
* **FULL_CITATION**: Roosa, K., & Chowell, G. (2019). Assessing parameter identifiability in compartmental dynamic models using a computational approach: application to infectious disease transmission models. *Theoretical Biology and Medical Modelling*, 16, 1.
* **YEAR**: 2019
* **DOI_OR_IDENTIFIER**: DOI: 10.1186/s12976-018-0097-6
* **SOURCE_TYPE**: Peer-reviewed Methodological Research
* **CLAIM_SUPPORTED**: Computational audits (multiseed optimization and profile sweeps) reveal parameter indeterminacy and correlations in compartmental transmission models.
* **CLAIM_NOT_SUPPORTED**: Universal solvability of all identifiability issues.
* **INTRODUCTION_LOCATION**: Paragraph 3 (I3)
* **DISCUSSION_LOCATION**: Paragraph 4 (D4)
* **RECOMMENDED_USE**: Cite in I3/D4 to support the computational profile/multiseed methodology for diagnosing parameter indeterminacy.
* **STATUS**: KEEP

#### L4-03
* **ID**: L4-03
* **TOPIC**: L4 — Identifiable parameter combinations and composite quantities
* **FULL_CITATION**: Meshkat, N., Kuo, C. E., & DiStefano, J. (2014). On finding and using identifiable parameter combinations in nonlinear dynamic systems biology models and COMBOS: a novel web implementation. *PLOS ONE*, 9(10), e110261.
* **YEAR**: 2014
* **DOI_OR_IDENTIFIER**: DOI: 10.1371/journal.pone.0110261
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Systems Biology
* **CLAIM_SUPPORTED**: Structural identifiability: which parameters are quantifiable in principle from input-output data, and the algebraic combinations of parameters that are not individually identifiable (abstract level).
* **CLAIM_NOT_SUPPORTED**: Practical identifiability from noisy aggregate data; robustness of $R_0$ (not stated in the abstract); fractional-order derivatives.
* **INTRODUCTION_LOCATION**: N/A (removed 2026-10-08)
* **DISCUSSION_LOCATION**: Paragraph 5 (D5)
* **RECOMMENDED_USE**: Cite in D5 only for structural identifiability and identifiable parameter combinations; the present analysis is of practical identifiability.
* **STATUS**: KEEP

#### L4-04
* **ID**: L4-04
* **TOPIC**: L4 — Profile likelihood and functional/prediction identifiability
* **FULL_CITATION**: Raue, A., Kreutz, C., Maiwald, T., Bachmann, J., Schilling, M., Klingmüller, U., & Timmer, J. (2009). Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. *Bioinformatics*, 25(15), 1923–1929.
* **YEAR**: 2009
* **DOI_OR_IDENTIFIER**: DOI: 10.1093/bioinformatics/btp358
* **SOURCE_TYPE**: Peer-reviewed Methodological Paper
* **CLAIM_SUPPORTED**: A profile-likelihood approach that detects structural non-identifiabilities (functionally related parameters) and practical non-identifiabilities (limited amount and quality of data) and yields confidence intervals (abstract level).
* **CLAIM_NOT_SUPPORTED**: Fractional calculus.
* **INTRODUCTION_LOCATION**: Optional
* **DISCUSSION_LOCATION**: Paragraph 4 (D4) / Paragraph 5 (D5)
* **RECOMMENDED_USE**: Foundational citation for profile objective analysis and functional prediction stability.
* **STATUS**: KEEP

---

### L5 — Gate 2: Adversarial Direct-Precedent Test

**Search close date**: 2026-09-05  
**Purpose**: Attempt to falsify the manuscript's distinctive methodological contribution before any novelty language is frozen.

A source counts as a **direct precedent** only if the same study jointly includes:

1. a fractional-order mechanistic epidemic model;
2. a comparable integer-order counterpart;
3. external statistical and/or naive forecasting baselines;
4. genuine out-of-sample temporal evaluation; and
5. evaluation across multiple forecast horizons and/or origins under a common protocol.

The conclusion of this gate is deliberately bounded: **no direct precedent was located in the searched corpus satisfying all five conditions simultaneously**. This is not evidence that no such study exists and does not support a `first study`, `never`, or universal absence claim.

#### L5-01 — Chishtie et al. (2026)
* **TOPIC**: Closest direct methodological neighbor: fractional vs integer under rolling-origin OOS evaluation.
* **FULL_CITATION**: Chishtie, F., Drozd, J., Li, X., Benterki, A., & Valluri, S. (2026). A robust compartmental modeling framework for infectious disease monitoring and analysis via fractional differential equations. *Epidemics*, 54, 100887.
* **DOI_OR_IDENTIFIER**: DOI: 10.1016/j.epidem.2026.100887
* **WHAT_IT_HAS**: A fractional SEIQRDP model reported as more accurate than classical integer-order models when fitted to Canadian COVID-19 data (two waves) and, separately, out-of-sample rolling-origin cross-validation at 7-, 14-, and 21-day horizons (abstract only; full text not read, so it is not established that the fractional-versus-integer comparison used rolling origin).
* **WHAT_IT_LACKS_FOR_GATE_2**: No external statistical/naive forecasting baseline is described in the abstract.
* **NOVELTY_EFFECT**: Kills any claim that rolling-origin or multi-horizon OOS validation of fractional epidemic models is itself new. Does not answer whether within-family fractional improvement survives comparison with external baselines.
* **STATUS**: ABSORB — high-priority direct neighbor.

#### L5-02 — Alzahrani et al. (2024)
* **TOPIC**: Fractional epidemic model compared with ARIMA.
* **FULL_CITATION**: Alzahrani, S. M., Saadeh, R., Abdoon, M. A., Qazza, A., El Guma, F., & Berir, M. (2024). Numerical Simulation of an Influenza Epidemic: Prediction with Fractional SEIR and the ARIMA Model. *Applied Mathematics & Information Sciences*, 18(1), 1–12.
* **DOI_OR_IDENTIFIER**: DOI: 10.18576/amis/180101
* **WHAT_IT_HAS**: Fractional SEIR (Atangana–Baleanu–Caputo operator); comparison of fit (RMSE, MAE) with ARIMA(2,0,1) on weekly influenza data, Saudi Arabia 2017–2022; the fractional model is reported as better, and no held-out evaluation is described (full text read 2026-10-01).
* **WHAT_IT_LACKS_FOR_GATE_2**: No common rolling-origin design, no multiple forecast origins/horizons under an equivalent protocol, and no persistence/seasonal-naive baseline.
* **NOVELTY_EFFECT**: Kills any claim that fractional epidemic models have never been compared with ARIMA. Does not provide the same external-skill test as the present design.
* **STATUS**: ABSORB — high-priority neighbor.

#### L5-03 — Rajagopal et al. (2020)
* **TOPIC**: Fractional vs integer prediction on held-out epidemic data.
* **FULL_CITATION**: Rajagopal, K., Hasanzadeh, N., Parastesh, F., Hamarash, I., Jafari, S., & Hussain, I. (2020). A fractional-order model for the novel coronavirus (COVID-19) outbreak. *Nonlinear Dynamics*, 101, 711–718.
* **DOI_OR_IDENTIFIER**: DOI: 10.1007/s11071-020-05757-6
* **WHAT_IT_HAS**: Integer and fractional models; real-data parameter estimation; prediction evaluated on test data.
* **WHAT_IT_LACKS_FOR_GATE_2**: No external statistical/naive forecasting baseline and no rolling-origin multi-horizon benchmark.
* **NOVELTY_EFFECT**: Kills any claim that fractional-vs-integer out-of-sample prediction is itself new.
* **STATUS**: ABSORB — direct conceptual neighbor.

#### L5-04 — Kharazmi et al. (2021)
* **TOPIC**: Integer/fractional epidemiological models, identifiability, uncertainty, and predictability.
* **FULL_CITATION**: Kharazmi, E., Cai, M., Zheng, X., Zhang, Z., Lin, G., & Karniadakis, G. E. (2021). Identifiability and predictability of integer- and fractional-order epidemiological models using physics-informed neural networks. *Nature Computational Science*, 1, 744–753.
* **DOI_OR_IDENTIFIER**: DOI: 10.1038/s43588-021-00158-0
* **WHAT_IT_HAS**: Integer and fractional epidemic formulations; structural/practical identifiability; forecasting and uncertainty analysis.
* **WHAT_IT_LACKS_FOR_GATE_2**: No external persistence/SARIMA/seasonal-naive benchmark answering whether within-family fractional improvement survives outside the model family.
* **NOVELTY_EFFECT**: Kills novelty claims based on merely combining fractional modeling, identifiability, and forecasting.
* **STATUS**: KEEP / already cited in manuscript.

#### L5-05 — Kalizhanova et al. (2024)
* **TOPIC**: Tuberculosis mechanistic-vs-statistical forecasting friction.
* **FULL_CITATION**: Kalizhanova, A., Yerdessov, S., Sakko, Y., Tursynbayeva, A., Kadyrov, S., Gaipov, A., et al. (2024). Modeling tuberculosis transmission dynamics in Kazakhstan using SARIMA and SIR models. *Scientific Reports*, 14, 24824.
* **DOI_OR_IDENTIFIER**: DOI: 10.1038/s41598-024-76721-2
* **WHAT_IT_HAS**: TB surveillance data; SARIMA and mechanistic SIR comparison; SARIMA trained on 2014–2018 and tested on 2019, basic constant-parameter SIR trained on 2014–2017 and tested on 2018–2019 (different windows, single partition); SARIMA shows superior predictive accuracy in that empirical setting (full text read 2026-10-08).
* **WHAT_IT_LACKS_FOR_GATE_2**: No fractional-order model and no fractional-vs-integer within-family contrast.
* **NOVELTY_EFFECT**: Establishes that, in TB, mechanistic interpretation and statistical forecasting performance can diverge. Strengthens the scientific friction but is not a direct precedent for the full present design.
* **STATUS**: ABSORB — high-priority TB neighbor.

#### L5-06 — Jiru & Kumaravel (2026)
* **TOPIC**: Fractional/integer epidemic model with an external OLS comparator.
* **FULL_CITATION**: Jiru, M., & Kumaravel, S. K. (2026). A memory-driven pneumonia dynamics model validated against Ethiopian mortality data: a fractional-order differential equation framework. *Scientific Reports*, 16.
* **DOI_OR_IDENTIFIER**: DOI: 10.1038/s41598-026-56464-y
* **WHAT_IT_HAS**: Fractional and integer SEIHR formulations; external OLS comparator; nominal train/validation framing.
* **WHAT_IT_LACKS_FOR_GATE_2**: Only three annual observations (2018–2020), no rolling-origin design, no genuine multi-horizon benchmark comparable to the present monthly evaluation, and no strong statistical/naive baseline suite.
* **NOVELTY_EFFECT**: Prevents broad absence claims about fractional + integer + external comparator, but does not close the present forecasting-evaluation friction.
* **STATUS**: ABSORB — bounded neighbor.

#### L5-07 — Muhafzan et al. (2024)
* **TOPIC**: Structural TB neighbor: fractional SEIT.
* **FULL_CITATION**: Muhafzan, Baqi, A. I., Narwen, Rudianto, B., Yulianti, L., Zulakmal, Hanan, H. A., & Ayu, L. T. (2024). Dynamical analysis of a fractional order SEIT epidemic model for TB spread under influence of vaccination. *Communications in Mathematical Biology and Neuroscience*, 2024, Article 102.
* **DOI_OR_IDENTIFIER**: DOI: 10.28919/cmbn/8853
* **WHAT_IT_HAS**: Fractional SEIT model for tuberculosis; equilibrium/stability analysis; vaccination effects on $R_0$ and infected population.
* **WHAT_IT_LACKS_FOR_GATE_2**: No out-of-sample forecasting, no external forecasting baseline, no practical-identifiability analysis of the present type.
* **NOVELTY_EFFECT**: Kills any structural novelty claim based on fractional SEIT + TB alone; useful as a close structural contrast.
* **STATUS**: ABSORB — structural neighbor.

---

## Gate 2 Closure Record

```text
GATE_2_EXTERNAL_VERIFICATION = CLOSED
DATE                         = 2026-09-05
SEARCH_OUTCOME               = NO_DIRECT_PRECEDENT_LOCATED_IN_SEARCHED_CORPUS
UNIVERSAL_ABSENCE_CLAIM      = PROHIBITED
FIRST_STUDY_CLAIM            = PROHIBITED
NOVELTY_BASIS                = SCIENTIFIC_FRICTION_NOT_EXACT_COMBINATION
PORTFOLIO_DECISION           = ABSORB
NEW_EXPERIMENT_REQUIRED      = NO
```

**Scientific friction retained**: the literature separately shows that fractional epidemic formulations can outperform integer-order counterparts and that mechanistic epidemic models can fail against statistical forecasting references. The unresolved manuscript-relevant question is whether a favorable fractional-vs-integer conclusion survives when the same model is subjected to external statistical/naive baselines under a common temporal multi-horizon evaluation protocol.

**Bounded conclusion**: the searched corpus did not reveal a direct precedent satisfying all five Gate 2 conditions simultaneously. This finding is used only to delimit the contribution; it is not converted into a historical-priority claim.

---

## Summary of Matrix Review

* **Core support sources documented (L1–L4)**: 11.
* **Gate 2 adversarial neighbors documented (L5)**: 7.
* **Gate 2 direct precedents satisfying all five conditions**: 0 located in the searched corpus.
* **Novelty / Gap Claims Invented**: 0.
* **Permitted contribution framing**: scientific friction and change in inference when the benchmark set is expanded beyond the fractional/integer model family.
* **Forbidden framing**: `first study`, `never evaluated`, universal absence, generic fractional superiority, or novelty based only on the exact combination of model + disease + dataset + baselines.
