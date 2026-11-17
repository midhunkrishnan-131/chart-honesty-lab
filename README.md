# Chart Honesty Lab

## Important data note
The six business-chart datasets in this practice pack are reproducible simulated data, not company records. They are deliberately used to practice chart construction because one public dataset does not naturally contain all six requested variables. Anscombe's quartet is the canonical published dataset and is included directly in the pack.

## Part A — chart choices
1. Monthly revenue over three years: **Line chart**, because time order and change over time are the focus.
2. Revenue across eight product categories: **Bar chart**, because categories are discrete and magnitudes need direct comparison.
3. Customer age distribution: **Histogram**, because age is numeric and the question is how observations are distributed.
4. Salary distribution across five departments: **Box plot**, because it compares medians, spread, and potential outliers across groups.
5. Advertising spend vs sales: **Scatter plot**, because both variables are numeric and the relationship matters.
6. Correlation among ten numeric columns: **Correlation heatmap**, because color and annotated values summarize pairwise correlations compactly.

All charts are built with Matplotlib's object-oriented API (`fig, ax = plt.subplots()`), and exported at 200 DPI with `bbox_inches='tight'`.

## Part B — deliberate truncation
Part B — 150-word explanation

The honest bar chart starts at zero, so each bar's height is proportional to its full revenue. The truncated version starts at $450,000 instead. That removes the lower $450,000 of every bar from view, making the visible bar heights represent only the excess above that baseline. The difference between $520,000 and $465,000 is $55,000, about 11.8% of the smaller value, but the visible portions are $70,000 and $15,000. Visually, the first bar's visible portion is nearly five times the last one's, even though the actual revenues differ by only about 12%. This encourages readers to overestimate the business importance of the gap. Bar lengths encode magnitude from a baseline, so a nonzero baseline is especially misleading. A line chart can sometimes use a truncated axis more defensibly because viewers often focus on changes and slopes, not bar length; still, it must be clearly labelled and the scale must not exaggerate a claim. Zero-based line charts may be better when absolute magnitude matters.


## Part C — overplotting
- Opaque scatter: 100,000 points obscure density.
- Alpha: transparency shows where points overlap.
- Sampling: quick overview, but can hide rare clusters or outliers.
- Hexbin: best default to ship for a large dataset when density is the goal; it uses all points and communicates concentration. If individual outliers or exact points matter, pair it with a sample or interactive plot.

## Part D — Anscombe's quartet
Statistics below use sample variance (ddof=1).
       x_mean  y_mean  x_variance_sample  y_variance_sample  pearson_correlation
group                                                                           
I         9.0   7.501               11.0              4.127                0.816
II        9.0   7.501               11.0              4.128                0.816
III       9.0   7.500               11.0              4.123                0.816
IV        9.0   7.501               11.0              4.123                0.817

Part D — 100-word explanation

Anscombe's quartet shows why summary statistics alone are not enough. The four datasets have nearly identical means, variances, and Pearson correlations, yet their scatter plots tell very different stories. One looks approximately linear, another is curved, a third is mostly linear but contains an influential outlier, and the fourth has most x-values concentrated at one position with a single high-leverage point. A report that lists only averages and correlation would hide these structural differences. Always visualize data before interpreting a model or statistic, inspect outliers, and check assumptions. Numerical summaries are useful, but they cannot replace looking at the observations themselves.


## Run it
Install dependencies:
    pip install numpy pandas matplotlib

Then run:
    python chart_honesty_lab.py

The script creates the PNGs and CSVs in a `chart_honesty_lab` folder.
