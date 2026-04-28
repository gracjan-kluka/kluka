import pandas as pd

# --- dane ---
df1 = pd.read_csv('Online_Retail.csv', encoding='ISO-8859-1')
df2 = pd.read_csv('Online_Retail_2.csv', encoding='ISO-8859-1')

df = pd.concat([df1, df2], ignore_index=True)

# --- czyszczenie ---
df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

df['InvoiceDate'] = pd.to_datetime(
    df['InvoiceDate'],
    dayfirst=True,
    errors='coerce'
)

df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month


# =========================
# ZADANIE 1 - PIVOT
# =========================
pivot = pd.pivot_table(
    df,
    values='TotalPrice',
    index='Country',
    columns='Month',
    aggfunc='sum',
    fill_value=0
)

print("\n=== ZADANIE 1 - PIVOT ===")
print(pivot)

monthly_sum = pivot.sum(axis=0)

best_month = monthly_sum.idxmax()
best_value = monthly_sum.max()

months = {
    1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
    7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"
}

print("\nNajlepszy miesiąc:")
print(months[best_month], best_value)


# =========================
# ZADANIE 2 - TOP 10 KRAJÓW
# =========================
ranking = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)
top10 = ranking.head(10)

print("\n=== ZADANIE 2 - TOP 10 KRAJÓW ===")
print(top10)


# =========================
# ZADANIE 3 - KLIENCI
# =========================
customers = df.groupby('CustomerID')['TotalPrice'].sum()

top_customers = customers.sort_values(ascending=False).head(10)
avg_revenue = customers.mean()

print("\n=== ZADANIE 3 - TOP KLIENCI ===")
print(top_customers)

print("\nŚredni przychód na klienta:")
print(avg_revenue)


# =========================
# ZADANIE 4 - SEGMENTACJA
# =========================
country_revenue = ranking.copy()

q1 = country_revenue.quantile(0.25)
q3 = country_revenue.quantile(0.75)

def segment(x):
    if x >= q3:
        return 'Top 25%'
    elif x <= q1:
        return 'Bottom 25%'
    else:
        return 'Middle 50%'

segments = country_revenue.apply(segment)

segment_df = pd.DataFrame({
    'Revenue': country_revenue,
    'Segment': segments
})

print("\n=== ZADANIE 4 - SEGMENTACJA ===")
print(segment_df.sort_values('Revenue', ascending=False))


# =========================
# ZADANIE 5 - WNIOSKI
# =========================
print("\n=== ZADANIE 5 - WNIOSKI ===")

print("\nKluczowe kraje:")
print(top10.index.tolist())

print("\nCzy sprzedaż jest równomierna?")
print("Nie, UK dominuje zdecydowanie")

print("\nSezonowość:")
print("Największa sprzedaż pod koniec roku (Q4)")