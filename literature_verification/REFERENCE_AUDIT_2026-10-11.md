# Reference audit (2026-10-11)

Scope: the 22 entries of `manuscript_latex/references.bib` that the manuscript cites: the 17 asked for (13 new references plus Kalizhanova, Kharazmi, Area and Simpson)
plus Diethelm, IBGE, WHO, the Ministry of Health and Matignon. Per entry: bibliographic data against Crossref (or against the document itself), DOI, and whether
the sentence that cites it is supported by what could be read. Details: `REFERENCE_AUDIT_2026-10-11.csv`. "Read" means abstract or full text through Crossref/OpenAlex,
PubMed, Europe PMC or the source itself; paywalled papers were not read beyond what open sources expose.

## Result

| Outcome | Entries |
|---|---|
| Bibliographic data and DOI verified, claim supported by abstract or full text | Funk 2019; Reich 2019; Cramer 2022 (see flag); Diebold and Mariano 1995; Raue 2009; Wieland 2021; Chowell 2017; van den Driessche and Watmough 2002; Petropoulos 2022 (topic level); Kalizhanova 2024 (full text) |
| Bibliographic data verified, claim supported only by title (abstract not obtainable) | Tashman 2000; Harvey, Leybourne and Newbold 1997; Storn and Price 1997; Diethelm, Ford and Freed 2002; Kharazmi 2021 |
| **Corrected** | **Area et al. 2015**: the old entry was wrong (see below) |
| **Reworded** because the source did not say what the sentence said | Area (Caputo claim); Simpson and Maclaren 2024; Hyndman and Koehler 2006 (seasonal-naive scale); placement of the Diebold-Mariano and HLN citations |
| Official documents read | WHO Global tuberculosis report 2024 (section 2.1); Ministry of Health bulletin, March 2024; IBGE 2013 methodological note |
| Provisional | Matignon 1996 (details from secondary sources; marked in the `.bib` note, which prints in the reference list) |

## Findings that need your attention

1. **Area et al. (2015) was cited with a wrong DOI, title and pages.** The entry (title "On a fractional order epidemic model with Caputo derivative", *Applied Mathematics Letters* 40, 23-27,
   DOI 10.1016/j.aml.2014.09.006) does not match a real paper: that DOI is Mortici, Rassias and Jung, "The inhomogeneous Euler equation and its Hyers-Ulam stability". The authors list matches
   a real paper, "On a fractional order Ebola epidemic model", *Advances in Difference Equations* 2015:278, DOI 10.1186/s13662-015-0613-5 (open access; read). That paper compares classical and
   fractional SEIR models with WHO data, but its system is written with D^alpha (Riemann-Liouville notation) and the Caputo derivative is only recalled in its preliminaries, so the sentence
   "Caputo formulations have been studied in epidemic models" was **not supported**. The entry is corrected and the sentence now says that fractional-order compartmental models have been fitted to outbreak data, for example a fractional SEIR model for Ebola.
   The wrong DOI (and the "verified" label) is also in older repository documents that I did not edit: `literature_verification/LITERATURE_SEARCH_LOG.md`, `LITERATURE_VERIFICATION_MATRIX.md`, and likely
   `manuscript_package/REFERENCE_AUDIT.md`, `manuscript_draft/INTRODUCTION_*.md`, `submission_bmb/*`.
2. **Cramer et al. (2022)** has a 2023 correction notice in Crossref (10.1073/pnas.2304076120). I did not read it. Its record has no page or article number.
3. **IBGE.** The 2013 methodological note exists and was read (IBGE library copy). I changed the URL to that copy because the previous one (the current IBGE page) returned 403 here. The sentence "the 2018 revision starts in 2010" rests on a table title of the IBGE yearbook;
   one IBGE page describes the 2018 revision as 2000-2060. Please confirm it before submission, or drop the clause (the argument for keeping the 2013 revision stands on its coverage of 2001-2020 and on matching the supplied series).
4. **Hyndman and Koehler (2006).** I could not read the paper; the manuscript now says the scaled error is "in the spirit of" that paper, with the seasonal-naive scale as our own definition.
5. **Matignon (1996)** stays provisional. Secondary sources (e.g. arXiv:2210.12751) give: Lille, 1996, vol. 2, pp. 963-968, and describe the criterion |arg(lambda)| > alpha*pi/2.

## Method limits

Abstracts were obtained from OpenAlex, Crossref, PubMed (van den Driessche and Watmough) and Europe PMC (Kalizhanova, Simpson). For Tashman, Hyndman and Koehler, Harvey et al., Storn and Price, Diethelm et al. and Kharazmi et al.
no abstract was available from open sources, so the support is by title and by well-known role. Scite is not usable without a subscription.
