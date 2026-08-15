# Literature Search Log

This log documents the targeted, reproducible literature search conducted to verify the four consolidated background and methodological topics in `manuscript_draft/INTRODUCTION_DRAFT.md` and `manuscript_draft/DISCUSSION_DRAFT.md`.

---

## Search Metadata

* **Repository Author / Scientific Lead**: fedeg
* **Date of Search**: 2026-08-15
* **Execution Mode**: Targeted support verification (non-opportunistic, no gap-hunting, no novelty claims).
* **Databases / Engines Queried**: PubMed, Web of Science, Google Scholar / Vertex AI Search, CrossRef / DOI Resolvers.

---

## Topic-by-Topic Query Log

### L1 — Tuberculosis Epidemiology and Surveillance in Brazil

* **Search Objective**: Verify that (1) tuberculosis remains a persistent public health burden in Brazil, and (2) SINAN surveillance notifications constitute the national standardized epidemiological source.
* **Queries Run**:
  * `"WHO Global Tuberculosis Report" "Brazil" "SINAN" tuberculosis surveillance`
  * `"Pelissari" "tuberculosis" "Brazil" "SINAN" Epidemiol Serv Saude doi`
* **Inclusion Criteria**: Peer-reviewed epidemiological studies of Brazilian TB surveillance and official WHO/PAHO global health reports.
* **Exclusion Criteria**: Highly localized clinic-level case reports without national surveillance relevance; commercial summaries.
* **Key Retrieved Sources**:
  * WHO Global Tuberculosis Report (2022).
  * Pelissari et al. (2020), *Epidemiol. Serv. Saude*, DOI: 10.5123/S1679-49742020000100009.

---

### L2 — External-Baseline Evaluation of Mechanistic Epidemic Forecasting Models

* **Search Objective**: Verify the methodological principle that historical calibration fit and nested/within-family ablations do not guarantee out-of-sample forecasting skill, and that external statistical baselines (persistence, seasonal naive, SARIMA) are necessary to evaluate predictive value.
* **Queries Run**:
  * `"Reich" "epidemic forecasting" baseline models "evaluating" "mechanistic" doi`
  * `"Epidemic forecasting is messier than weather forecasting" Moran 2016 doi`
  * `"evaluating epidemic forecasts" "baseline" "forecasting skill" "PLOS Computational Biology"`
* **Inclusion Criteria**: High-impact peer-reviewed papers on infectious disease forecasting evaluation, benchmark hubs, and time-series cross-validation principles.
* **Exclusion Criteria**: Papers claiming model novelty without rigorous baseline comparisons; opinion pieces lacking formal evaluation methodology.
* **Key Retrieved Sources**:
  * Moran et al. (2016), *J. Infect. Dis.*, DOI: 10.1093/infdis/jiw375.
  * Bracher, Ray, Gneiting, & Reich (2021), *PLOS Comput. Biol.*, DOI: 10.1371/journal.pcbi.1008618.
  * Cramer et al. (2022), *PNAS*, DOI: 10.1073/pnas.2113561119.
  * Hyndman & Athanasopoulos (2018), *Forecasting: Principles and Practice* (2nd ed.).

---

### L3 — Fractional-Order Compartmental Models in Infectious-Disease Modelling

* **Search Objective**: Verify that fractional-order differential operators (specifically Caputo type) are established tools for modeling power-law temporal dependence and non-exponential residence times in compartmental epidemiology.
* **Queries Run**:
  * `Diethelm 2013 "A fractional calculus based model for the simulation of an outbreak of dengue fever" doi`
  * `"fractional order" "epidemic model" "Caputo" "Applied Mathematics Letters" doi`
* **Inclusion Criteria**: Foundational peer-reviewed mathematical biology and fractional calculus papers introducing fractional compartmental formulations.
* **Exclusion Criteria**: Non-peer-reviewed preprints claiming unverified biological superiority without mathematical rigor.
* **Key Retrieved Sources**:
  * Diethelm (2013), *Nonlinear Dyn.*, DOI: 10.1007/s11071-012-0475-2.
  * Area et al. (2015), *Appl. Math. Lett.*, DOI: 10.1016/j.aml.2014.09.006.
  * Baleanu et al. (2012), *Fractional Calculus: Models and Numerical Methods*, World Scientific, DOI: 10.1142/8180.

---

### L4 — Parameter and Functional Identifiability in Compartmental Models

* **Search Objective**: Verify (1) practical and structural identifiability challenges in ODE/compartmental systems, (2) the coexistence of flat objective surfaces with stable trajectory fits, and (3) standard terminology for identifiable parameter combinations and robustness of composite threshold functionals (such as $R_0$).
* **Queries Run**:
  * `"identifiability" "epidemiological models" "profile likelihood" "R0" "parameter combinations" doi`
  * `"practical identifiability" "compartmental dynamic models" "Chowell" doi`
  * `"finding identifiable parameter combinations" Meshkat 2014 doi`
* **Inclusion Criteria**: Peer-reviewed studies on identifiability analysis, profile likelihood, and parameter combinations in mathematical epidemiology and systems biology.
* **Exclusion Criteria**: General identifiability papers outside dynamic/differential equation systems.
* **Key Retrieved Sources**:
  * Tuncer & Le (2018), *Math. Biosci.*, DOI: 10.1016/j.mbs.2018.02.004.
  * Roosa & Chowell (2019), *Theor. Biol. Med. Model.*, DOI: 10.1186/s12976-018-0094-2.
  * Meshkat, Kuo, & Sullivant (2014), *PLOS ONE*, DOI: 10.1371/journal.pone.0110261.
  * Raue et al. (2009), *Bioinformatics*, DOI: 10.1093/bioinformatics/btp358.

---

## Terminology Gate: "Functional Identifiability"

* **Findings**: In mathematical biology and dynamical systems, the standard terminology for non-identifiable parameters combining into identifiable derived quantities is **identifiable parameter combinations** (Meshkat et al. 2014) and **practical identifiability / robustness of composite functionals / threshold quantities** (Tuncer & Le 2018; Raue et al. 2009).
* **Decision**: Adopt "identifiable parameter combinations" and "practical robustness of the derived functional" alongside "practical-identifiability envelope" in the manuscript to adhere strictly to standard literature conventions.
