import pandas as pd
import matplotlib.pyplot as plt

# --- dane ---
df1 = pd.read_csv('Online_Retail.csv', encoding='ISO-8859-1')
df2 = pd.read_csv('Online_Retail_2.csv', encoding='ISO-8859-1')

df = pd.concat([df1, df2], ignore_index=True)

# --- czyszczenie ---
df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# --- czas ---
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month

# --- OLAP ---
rollup = df.groupby('Year')['TotalPrice'].sum()
print(rollup)

drilldown = df.groupby(['Year', 'Month'])['TotalPrice'].sum()
print(drilldown)

slice_uk = df[df['Country'] == 'United Kingdom']
print(slice_uk.head())

dice = df[(df['Country'] == 'United Kingdom') & (df['Year'] == 2011)]
print(dice.head())

pivot = pd.pivot_table(df, values='TotalPrice', index='Country', columns='Year', aggfunc='sum')
print(pivot)

# --- zad 1 ---
top_countries = (
    df.groupby('Country')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- Zadanie 1: Top 10 krajów ---")
print(top_countries)

top_countries_df = top_countries.reset_index()
top_countries_df.columns = ['Country', 'TotalSales']

# --- zad 2 ---
monthly_sales = df.groupby('Month')['TotalPrice'].sum()

best_month = monthly_sales.idxmax()
best_value = monthly_sales.max()

print("\n--- Zadanie 2: Najlepszy miesiąc ---")
print("Miesiąc:", best_month, "Sprzedaż:", best_value)


# --- zad 3 ---
pivot_cube = pd.pivot_table(
    df,
    values='TotalPrice',
    index='Country',
    columns='Month',
    aggfunc='sum',
    fill_value=0
)

print("\n--- Zadanie 3: Kostka danych ---")
print(pivot_cube)

# --- zad 4 ---
country_year = df.groupby(['Country', 'Year'])['TotalPrice'].sum().reset_index()

best_year_per_country = country_year.loc[
    country_year.groupby('Country')['TotalPrice'].idxmax()
]

print("\n--- Zadanie 4: Najlepszy rok dla kraju ---")
print(best_year_per_country)

# --- zad 5 ---
country_product = (
    df.groupby(['Country', 'StockCode'])['TotalPrice']
    .sum()
    .reset_index()
)

country_product = country_product.sort_values(['Country', 'TotalPrice'], ascending=[True, False])

top5_per_country = country_product.groupby('Country').head(5)

print("\n--- Zadanie 5: Top 5 produktów ---")
print(top5_per_country)

# --- wykresy ---
top_countries_df.plot(
    x='Country',
    y='TotalSales',
    kind='bar',
    legend=False
)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

monthly_sales.sort_index().plot(kind='bar')
plt.tight_layout()
plt.show()

# heatmap (top kraje żeby było czytelnie)
pivot_top = pivot_cube.loc[top_countries_df['Country']]

plt.imshow(pivot_top, aspect='auto')
plt.colorbar()
plt.tight_layout()
plt.show()