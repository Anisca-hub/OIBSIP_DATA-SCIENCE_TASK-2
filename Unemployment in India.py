# ===============================
# Task 2: Unemployment Analysis
# ===============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load datasets (update path if needed)
# -------------------------------
df1 = pd.read_csv(r"C:\Users\anisc\Downloads\TASK 2\Unemployment in India.csv")
df2 = pd.read_csv(r"C:\Users\anisc\Downloads\TASK 2\Unemployment_Rate_upto_11_2020.csv")

# -------------------------------
# Clean column names
# -------------------------------
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# -------------------------------
# Drop missing values
# -------------------------------
df1.dropna(inplace=True)
df2.dropna(inplace=True)

# -------------------------------
# Robust Date Parsing (silences warnings)
# -------------------------------
df1["Date"] = pd.to_datetime(df1["Date"], dayfirst=True, errors='coerce')
df2["Date"] = pd.to_datetime(df2["Date"], dayfirst=True, errors='coerce')

# Drop any rows where Date could not be parsed
df1 = df1.dropna(subset=["Date"]).sort_values("Date")
df2 = df2.dropna(subset=["Date"]).sort_values("Date")

# -------------------------------
# Dataset overview
# -------------------------------
print("Dataset 1 shape:", df1.shape)
print("Dataset 2 shape:", df2.shape)
print("\nColumns:\n", df2.columns)

# -------------------------------
# Overall Trend (India)
# -------------------------------
plt.figure(figsize=(10,5))
plt.plot(df2["Date"], df2["Estimated Unemployment Rate (%)"], color="red")
plt.title("Unemployment Rate Trend in India")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.show()

# -------------------------------
# COVID Before vs After Analysis
# -------------------------------
covid_start = pd.to_datetime("2020-03-01")

before_covid = df2[df2["Date"] < covid_start]
after_covid = df2[df2["Date"] >= covid_start]

before_avg = before_covid["Estimated Unemployment Rate (%)"].mean()
after_avg = after_covid["Estimated Unemployment Rate (%)"].mean()

print("Average Unemployment Rate Before COVID:", round(before_avg, 2))
print("Average Unemployment Rate After COVID:", round(after_avg, 2))

# COVID Impact Bar Chart
plt.figure(figsize=(6,4))
plt.bar(
    ["Before COVID", "After COVID"],
    [before_avg, after_avg],
    color=["green", "orange"]
)
plt.title("COVID-19 Impact on Unemployment Rate")
plt.ylabel("Average Unemployment Rate (%)")
plt.show()

# -------------------------------
# Top 5 Regions by Average Unemployment
# -------------------------------
top_regions = (
    df2.groupby("Region")["Estimated Unemployment Rate (%)"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .index
)

df_top = df2[df2["Region"].isin(top_regions)]

plt.figure(figsize=(12,6))
sns.lineplot(
    data=df_top,
    x="Date",
    y="Estimated Unemployment Rate (%)",
    hue="Region"
)
plt.title("Top 5 Regions by Average Unemployment Rate")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.show()

# -------------------------------
# Optional: Conclusion Print
# -------------------------------
if after_avg > before_avg:
    print("Conclusion: Unemployment increased significantly after COVID-19.")
else:
    print("Conclusion: No significant increase observed after COVID-19.")