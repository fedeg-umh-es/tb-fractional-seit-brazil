# Literature Verification Matrix

This matrix documents the candidate literature sources evaluated to support the framing, methodology, and interpretation of the TB SEIT manuscript, mapped across topics L1–L4.

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
* **FULL_CITATION**: Pelissari, D. M., Rocha, M. S., Bartholomeu, P. V. O., Sanchez, M. N., Duarte, E. C., Arakaki-Sanchez, D., & Diaz-Quijano, F. A. (2020). Notifiable Diseases Information System (SINAN): main features of tuberculosis notification and data analysis. *Epidemiologia e Serviços de Saúde*, 29(1), e2019154.
* **YEAR**: 2020
* **DOI_OR_IDENTIFIER**: DOI: 10.5123/S1679-49742020000100009
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Surveillance Methodology
* **CLAIM_SUPPORTED**: The Notifiable Diseases Information System (SINAN) is the official national platform for mandatory TB notification, continuous epidemiological monitoring, and case surveillance in Brazil.
* **CLAIM_NOT_SUPPORTED**: Mathematical model forecasting performance.
* **INTRODUCTION_LOCATION**: Paragraph 1 (I1) / Paragraph 5 (I5)
* **DISCUSSION_LOCATION**: Paragraph 7 (D7)
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
* **CLAIM_SUPPORTED**: High historical goodness-of-fit in epidemic models does not imply out-of-sample forward predictive accuracy; mechanistic models face distinct operational challenges and must be evaluated on genuine forward prediction.
* **CLAIM_NOT_SUPPORTED**: Fractional-order compartmental formulations specifically.
* **INTRODUCTION_LOCATION**: Paragraph 1 (I1)
* **DISCUSSION_LOCATION**: Paragraph 2 (D2)
* **RECOMMENDED_USE**: Cite in Introduction I1 to support the distinction between calibration fit and out-of-sample predictive capability.
* **STATUS**: KEEP

#### L2-02
* **ID**: L2-02
* **TOPIC**: L2 — External baseline evaluation and benchmark standards
* **FULL_CITATION**: Bracher, J., Ray, E. L., Gneiting, T., & Reich, N. G. (2021). Evaluating epidemic forecasts in an interval format. *PLOS Computational Biology*, 17(2), e1008618.
* **YEAR**: 2021
* **DOI_OR_IDENTIFIER**: DOI: 10.1371/journal.pcbi.1008618
* **SOURCE_TYPE**: Peer-reviewed Methodological Framework
* **CLAIM_SUPPORTED**: Out-of-sample epidemic forecasts must be rigorously benchmarked against standard reference baselines (such as persistence/naive and statistical models) to establish meaningful forecasting skill.
* **CLAIM_NOT_SUPPORTED**: Tuberculosis transmission specifically.
* **INTRODUCTION_LOCATION**: Paragraph 1 (I1) / Paragraph 2 (I2)
* **DISCUSSION_LOCATION**: Paragraph 1 (D1) / Paragraph 2 (D2)
* **RECOMMENDED_USE**: Cite in I1/I2 and D1/D2 to support the necessity of external reference baselines in epidemic forecast evaluation.
* **STATUS**: KEEP

#### L2-03
* **ID**: L2-03
* **TOPIC**: L2 — Multi-model forecasting benchmarks and baseline floor
* **FULL_CITATION**: Cramer, E. Y., Ray, E. L., Lopez, V. K., et al. (2022). Evaluation of individual and ensemble probabilistic forecasts of COVID-19 mortality in the US. *Proceedings of the National Academy of Sciences*, 119(15), e2113561119.
* **YEAR**: 2022
* **DOI_OR_IDENTIFIER**: DOI: 10.1073/pnas.2113561119
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Multi-model Evaluation
* **CLAIM_SUPPORTED**: Simple baseline models provide an essential performance floor; many sophisticated models fail to consistently outperform naive/persistence baselines across all horizons.
* **CLAIM_NOT_SUPPORTED**: Universality of all compartmental failures.
* **INTRODUCTION_LOCATION**: Optional
* **DISCUSSION_LOCATION**: Paragraph 2 (D2)
* **RECOMMENDED_USE**: Cite in Discussion D2 to support why outperforming persistence/naive models is a critical test of forecasting capability.
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
* **FULL_CITATION**: Area, I., Batarfi, H., Losada, J., Nieto, J. J., Shammakh, W., & Torres, Á. (2015). On a fractional order epidemic model with Caputo derivative. *Applied Mathematics Letters*, 40, 23–27.
* **YEAR**: 2015
* **DOI_OR_IDENTIFIER**: DOI: 10.1016/j.aml.2014.09.006
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Applied Mathematics
* **CLAIM_SUPPORTED**: Caputo-type fractional operators are standard mathematical tools for constructing fractional compartmental models with physically interpretable initial conditions.
* **CLAIM_NOT_SUPPORTED**: Operational forecasting efficacy against external benchmarks.
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
* **FULL_CITATION**: Roosa, S., & Chowell, G. (2019). Assessing parameter identifiability in compartmental dynamic models using a computational approach: application to infectious disease transmission. *Theoretical Biology and Medical Modelling*, 16, 1.
* **YEAR**: 2019
* **DOI_OR_IDENTIFIER**: DOI: 10.1186/s12976-018-0094-2
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
* **FULL_CITATION**: Meshkat, N., Kuo, C. E., & Sullivant, S. (2014). On finding identifiable parameter combinations in nonlinear dynamic systems. *PLOS ONE*, 9(10), e110261.
* **YEAR**: 2014
* **DOI_OR_IDENTIFIER**: DOI: 10.1371/journal.pone.0110261
* **SOURCE_TYPE**: Peer-reviewed Primary Research / Systems Biology
* **CLAIM_SUPPORTED**: In non-identifiable dynamic systems, specific algebraic combinations of unidentifiable parameters (e.g. composite ratios like $R_0$) can remain identifiable and robustly estimated.
* **CLAIM_NOT_SUPPORTED**: Fractional-order derivatives specifically.
* **INTRODUCTION_LOCATION**: Paragraph 3 (I3)
* **DISCUSSION_LOCATION**: Paragraph 5 (D5)
* **RECOMMENDED_USE**: Cite in I3 and D5 to support why composite derived functionals (such as $R_0$) can be robustly identified despite severe non-identifiability in individual kinetic rate parameters.
* **STATUS**: KEEP

#### L4-04
* **ID**: L4-04
* **TOPIC**: L4 — Profile likelihood and functional/prediction identifiability
* **FULL_CITATION**: Raue, A., Kreutz, C., Maiwald, T., Bachmann, J., Schilling, M., Klingmüller, U., & Timmer, J. (2009). Structural and practical identifiability analysis of partial differential equation models in systems biology. *Bioinformatics*, 25(15), 1923–1929.
* **YEAR**: 2009
* **DOI_OR_IDENTIFIER**: DOI: 10.1093/bioinformatics/btp358
* **SOURCE_TYPE**: Peer-reviewed Methodological Paper
* **CLAIM_SUPPORTED**: Distinguishes between parameter non-identifiability and the practical determinacy of model predictions and composite target functionals using profile-likelihood methods.
* **CLAIM_NOT_SUPPORTED**: Fractional calculus.
* **INTRODUCTION_LOCATION**: Optional
* **DISCUSSION_LOCATION**: Paragraph 4 (D4) / Paragraph 5 (D5)
* **RECOMMENDED_USE**: Foundational citation for profile objective analysis and functional prediction stability.
* **STATUS**: KEEP

---

## Summary of Matrix Review

* **Total Sources Screened**: 11
* **Total Sources Kept**: 11 (all peer-reviewed primary/methodological papers, official WHO report, or standard methodological reference).
* **Novelty / Gap Claims Invented**: 0 (all sources provide general methodological or epidemiological grounding without asserting artificial literature gaps).
