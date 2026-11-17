"""
Chart Honesty Lab
Business-chart data are simulated practice data; Anscombe's quartet is canonical published data.
Requires: numpy, pandas, matplotlib
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUT = Path("chart_honesty_lab")
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
plt.rcParams.update({"font.size": 9, "axes.titlesize": 12, "axes.labelsize": 10})

def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")
    plt.close(fig)

# Simulated practice data
dates = pd.date_range("2023-01-01", periods=36, freq="MS")
revenue = np.linspace(85000, 145000, 36) * (1 + .10*np.sin(np.arange(36)*2*np.pi/12)) + rng.normal(0,5000,36)
monthly = pd.DataFrame({"month":dates, "revenue_usd":revenue})
categories = np.array(["Electronics","Home","Beauty","Clothing","Sports","Books","Toys","Garden"])
cat_rev = np.array([520000,505000,498000,490000,482000,478000,472000,465000])
ages = np.clip(rng.normal(39,12,1200),18,80).round().astype(int)
salaries = pd.concat([pd.DataFrame({"department":d,"annual_salary_usd":np.clip(rng.normal(mu,sd,n),35000,220000)}) for d,mu,sd,n in [
    ("Engineering",118000,22000,180),("Sales",85000,28000,150),("Finance",96000,18000,90),("Operations",76000,16000,130),("Support",62000,12000,110)]],ignore_index=True)
ad_spend = rng.uniform(500,20000,500)
ad_sales = 12000 + 4.2*ad_spend + rng.normal(0,18000,500)
base = rng.normal(size=(1000, 4))
numeric = pd.DataFrame({
    "revenue_k":100+18*base[:,0]+rng.normal(0,5,1000),
    "orders_k":20+4*base[:,0]+rng.normal(0,2,1000),
    "ad_spend_k":12+5*base[:,1]+rng.normal(0,2,1000),
    "site_visits_k":80+15*base[:,1]+rng.normal(0,8,1000),
    "conversion_pct":3.5+.7*base[:,2]+rng.normal(0,.3,1000),
    "avg_order_value":65+9*base[:,2]+rng.normal(0,4,1000),
    "returns_pct":4+.8*base[:,3]+rng.normal(0,.5,1000),
    "customer_rating":4.1-.25*base[:,3]+rng.normal(0,.15,1000),
    "discount_pct":12+4*base[:,1]+rng.normal(0,2,1000),
    "profit_margin_pct":18-.35*base[:,1]+.2*base[:,2]+rng.normal(0,2,1000)
})

# 1 Line chart
fig, ax = plt.subplots(figsize=(10,4.8))
ax.plot(monthly.month,monthly.revenue_usd,marker="o",markersize=3)
ax.set(title="Revenue rose over three years, with recurring seasonal dips",xlabel="Month",ylabel="Revenue (USD)")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f"${x/1000:.0f}k")); ax.tick_params(axis="x",rotation=35); ax.grid(axis="y",alpha=.25)
save(fig,"01_monthly_revenue_line.png")

# 2 Honest and misleading bar charts
order=np.argsort(cat_rev)[::-1]
fig,ax=plt.subplots(figsize=(9,4.8)); ax.bar(categories[order],cat_rev[order])
ax.set(title="Category revenue is relatively close across the eight groups",xlabel="Product category",ylabel="Revenue (USD)",ylim=(0,600000))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f"${x/1000:.0f}k")); ax.tick_params(axis="x",rotation=30); ax.grid(axis="y",alpha=.2)
save(fig,"02_category_revenue_honest.png")
fig,ax=plt.subplots(figsize=(9,4.8)); ax.bar(categories[order],cat_rev[order])
ax.set(title="MISLEADING: truncated axis exaggerates small category differences",xlabel="Product category",ylabel="Revenue (USD)",ylim=(450000,530000))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f"${x/1000:.0f}k")); ax.tick_params(axis="x",rotation=30); ax.grid(axis="y",alpha=.2)
save(fig,"02b_category_revenue_truncated.png")
fig,axs=plt.subplots(1,2,figsize=(13,5))
for ax,ymin,title in [(axs[0],0,"Honest: zero baseline"),(axs[1],450000,"Misleading: truncated baseline")]:
    ax.bar(categories[order],cat_rev[order]); ax.set_ylim(ymin,600000 if ymin==0 else 530000)
    ax.set(title=title,xlabel="Category",ylabel="Revenue (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f"${x/1000:.0f}k")); ax.tick_params(axis="x",rotation=45,labelsize=8)
fig.suptitle("Same values, different visual impression"); fig.tight_layout(); save(fig,"02c_honest_vs_truncated_side_by_side.png")

# 3 Histogram
fig,ax=plt.subplots(figsize=(8,4.8)); ax.hist(ages,bins=np.arange(15,86,5),edgecolor="white")
ax.set(title="Most customers are in their thirties and forties",xlabel="Customer age (years)",ylabel="Number of customers (people)"); ax.grid(axis="y",alpha=.2)
save(fig,"03_customer_age_distribution.png")

# 4 Boxplot
depts=["Engineering","Sales","Finance","Operations","Support"]
fig,ax=plt.subplots(figsize=(9,5)); ax.boxplot([salaries.loc[salaries.department==d,"annual_salary_usd"] for d in depts],labels=depts,showfliers=False)
ax.set(title="Engineering has the highest median salary and widest typical range",xlabel="Department",ylabel="Annual salary (USD per year)")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f"${x/1000:.0f}k")); ax.tick_params(axis="x",rotation=20); ax.grid(axis="y",alpha=.2)
save(fig,"04_salary_by_department_boxplot.png")

# 5 Scatter
fig,ax=plt.subplots(figsize=(8,5)); ax.scatter(ad_spend,ad_sales,alpha=.45,s=18)
coef=np.polyfit(ad_spend,ad_sales,1); xx=np.linspace(ad_spend.min(),ad_spend.max(),100); ax.plot(xx,np.polyval(coef,xx),linewidth=2)
ax.set(title="Sales generally increase with advertising spend in this sample",xlabel="Advertising spend (USD)",ylabel="Sales (USD)")
ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_:f"${x/1000:.0f}k")); ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f"${x/1000:.0f}k")); ax.grid(alpha=.2)
save(fig,"05_ad_spend_vs_sales_scatter.png")

# 6 Correlation heatmap (10 numeric columns)
corr=numeric.corr()
fig,ax=plt.subplots(figsize=(10,8)); im=ax.imshow(corr.values,vmin=-1,vmax=1,aspect="auto")
ax.set_xticks(range(len(corr.columns)),labels=corr.columns,rotation=45,ha="right"); ax.set_yticks(range(len(corr.columns)),labels=corr.columns)
ax.set_title("Correlation strength varies across the ten numeric metrics")
cb=fig.colorbar(im,ax=ax); cb.set_label("Pearson correlation (unitless)")
for i in range(len(corr)):
    for j in range(len(corr)): ax.text(j,i,f"{corr.iloc[i,j]:.2f}",ha="center",va="center",fontsize=7)
save(fig,"06_numeric_correlation_heatmap.png")

# C: 100,000 points
x=rng.normal(size=100000); y=.65*x+rng.normal(scale=.8,size=100000)
for filename,title,mode in [
    ("07a_overplotting_useless.png","Overplotting: 100,000 opaque points hide density","opaque"),
    ("07b_overplotting_alpha.png","Fix 1: transparency reveals dense regions","alpha"),
    ("07c_overplotting_sampling.png","Fix 2: random sample of 5,000 points","sample"),
    ("07d_overplotting_hexbin.png","Fix 3: hexbin summarizes point density","hexbin")]:
    fig,ax=plt.subplots(figsize=(7,5))
    if mode=="opaque": ax.scatter(x,y,s=5)
    elif mode=="alpha": ax.scatter(x,y,s=5,alpha=.04,rasterized=True)
    elif mode=="sample":
        idx=rng.choice(len(x),size=5000,replace=False); ax.scatter(x[idx],y[idx],s=7,alpha=.45)
    else:
        hb=ax.hexbin(x,y,gridsize=45,mincnt=1); cb=fig.colorbar(hb,ax=ax); cb.set_label("Points per hexagon (count)")
    ax.set(title=title,xlabel="Feature X (standard deviations)",ylabel="Feature Y (standard deviations)")
    save(fig,filename)

# D: Anscombe's quartet, embedded
quartet={
"I":([10,8,13,9,11,14,6,4,12,7,5],[8.04,6.95,7.58,8.81,8.33,9.96,7.24,4.26,10.84,4.82,5.68]),
"II":([10,8,13,9,11,14,6,4,12,7,5],[9.14,8.14,8.74,8.77,9.26,8.10,6.13,3.10,9.13,7.26,4.74]),
"III":([10,8,13,9,11,14,6,4,12,7,5],[7.46,6.77,12.74,7.11,7.81,8.84,6.08,5.39,8.15,6.42,5.73]),
"IV":([8,8,8,8,8,8,8,8,8,8,19],[6.58,5.76,7.71,8.84,8.47,7.04,5.25,5.56,7.91,6.89,12.50])}
rows=[]
for group,(xs,ys) in quartet.items():
    for xv,yv in zip(xs,ys): rows.append({"group":group,"x":xv,"y":yv})
df=pd.DataFrame(rows); stats=[]
for group,g in df.groupby("group"):
    stats.append({"group":group,"x_mean":g.x.mean(),"y_mean":g.y.mean(),"x_variance_sample":g.x.var(ddof=1),"y_variance_sample":g.y.var(ddof=1),"pearson_correlation":g.x.corr(g.y)})
stats=pd.DataFrame(stats).round(3); print("Anscombe statistics (sample variance):"); print(stats.to_string(index=False))
stats.to_csv(OUT/"anscombe_statistics.csv",index=False); df.to_csv(OUT/"anscombe_quartet_data.csv",index=False)
fig,axs=plt.subplots(2,2,figsize=(9,8))
for ax,group in zip(axs.flat,["I","II","III","IV"]):
    g=df[df.group==group]; ax.scatter(g.x,g.y,s=35); slope,intercept=np.polyfit(g.x,g.y,1); xx=np.linspace(g.x.min()-.5,g.x.max()+.5,100)
    ax.plot(xx,slope*xx+intercept,linewidth=1.5); ax.set(title=f"Dataset {group}",xlabel="X (unitless)",ylabel="Y (unitless)"); ax.grid(alpha=.2)
fig.suptitle("Anscombe's quartet: similar summaries, different patterns"); fig.tight_layout(); save(fig,"08_anscombe_quartet.png")

# Save data used for practice charts
monthly.to_csv(OUT/"practice_monthly_revenue.csv",index=False)
pd.DataFrame({"category":categories,"revenue_usd":cat_rev}).to_csv(OUT/"practice_category_revenue.csv",index=False)
pd.DataFrame({"customer_age_years":ages}).to_csv(OUT/"practice_customer_ages.csv",index=False)
salaries.to_csv(OUT/"practice_department_salaries.csv",index=False)
pd.DataFrame({"advertising_spend_usd":ad_spend,"sales_usd":ad_sales}).to_csv(OUT/"practice_ad_spend_sales.csv",index=False)
numeric.to_csv(OUT/"practice_ten_numeric_columns.csv",index=False); corr.to_csv(OUT/"practice_correlation_matrix.csv")
print(f"Charts and CSV files saved to: {OUT.resolve()}")
