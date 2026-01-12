# 1 : Load Data
import pandas as pd
url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv"
df = pd.read_csv(url)

# 2: Data Audit
print("Missing values per column:")
print(df.isnull().sum()) 
print(f"Total rows in dataset: {len(df)}")

# 3: Data Cleaning
cols_to_fix = ['director', 'cast', 'country']
for col in cols_to_fix:
    df[col] = df[col].fillna('Unknown')
df.dropna(subset=['date_added', 'rating'], inplace=True)
print(df.isnull().sum())
print(f"Cleaned Row Count: {len(df)}")
print(df["director"].isnull().sum())
print(df.head())

# 4: Date Conversion
df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
df['year_added'] = df['date_added'].dt.year
df['year_added'] = df['year_added'].fillna(0).astype(int)

# 5: Verification
print("--- DATE CONVERSION RESULTS ---")
print(df[['title', 'date_added', 'year_added']].head())
print("\nColumn Type for date_added:", df['date_added'].dtype) 

# 6: Summary Statistics
df_filtered = df[df["year_added"] > 0].copy()
analysis = df_filtered.groupby(['year_added', 'type'])["show_id"].count()
final_trend = analysis.unstack()
print("--- SUMMARY TABLE: CONTENT BY YEAR ---")
print(final_trend.tail(10))

# 7: Visualization
import matplotlib.pyplot as plt
chart_data = final_trend[final_trend.index >= 2008]
chart_data.plot(kind='line', marker='o', figsize=(10, 6), color=['red', 'black'])
plt.title('The Netflix Content Explosion', fontsize=16, fontweight='bold')
plt.ylabel('Count of Titles Added')
plt.xlabel('Year')
plt.legend(['Movies', 'TV Shows']) # Ensures the lines are labeled
plt.grid(True, alpha=0.3)
plt.savefig('netflix_trend_analysis.png', dpi=300, bbox_inches='tight')
plt.show()