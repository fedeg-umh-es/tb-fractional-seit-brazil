**Table S4. Calibration results of the five optimizer seeds for the fractional and integer SEIT models under the frozen primary bounds (monthly units).**

| Model | Seed | $\beta$ | $\sigma$ | $\gamma$ | $d$ | $\alpha$ | Cal. RMSE |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fractional | 20260815 | 0.0762 | **0.01002** | 0.0568 | 0.00031 | 0.9640 | 605.049 |
| Fractional | 20260816 | 0.4130 | **0.01012** | 0.2818 | 0.03652 | 0.9635 | 610.388 |
| Fractional | 20260817 | 0.0852 | **0.01015** | 0.0541 | 0.00935 | 0.9620 | 606.273 |
| Fractional | 20260818 | 0.2781 | **0.01014** | 0.1739 | 0.03858 | 0.9622 | 609.571 |
| Fractional | 20260819 | 0.3856 | **0.01004** | 0.2848 | 0.00999 | 0.9624 | 609.874 |
| Integer | 20260815 | 0.0612 | **0.01017** | 0.0532 | 0.00021 | 1 (fixed) | 776.058 |
| Integer | 20260816 | 0.0657 | **0.01008** | 0.0545 | 0.00284 | 1 (fixed) | 776.099 |
| Integer | 20260817 | 0.0590 | **0.01001** | **0.0504** | 0.00094 | 1 (fixed) | 773.341 |
| Integer | 20260818 | 0.1133 | **0.01000** | 0.0530 | 0.04644 | 1 (fixed) | 782.877 |
| Integer | 20260819 | 0.0853 | **0.01012** | 0.0576 | 0.01694 | 1 (fixed) | 780.246 |

Primary bounds: $\beta \in [0.01, 1.00]$, $\sigma \in [0.01, 0.50]$, $\gamma \in [0.05, 0.30]$, $d \in [0.0001, 0.05]$, $\alpha \in [0.50, 1.00]$ (fractional) or $\alpha = 1$ (integer). Values within 2% of a bound are in bold. The primary calibration is seed 20260815; the other seeds are diagnostic. All ten fits reported convergence.
