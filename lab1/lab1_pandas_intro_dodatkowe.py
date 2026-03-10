import pandas as pd

print("=== WCZYTYWANIE DANYCH ===")
df = pd.read_csv("sales_raw.csv")


# =====================================================
# PODSTAWOWE ZADANIE
# =====================================================

print("\n=== PODSTAWOWE OBLICZENIA ===")

df["total_value"] = df["quantity"] * df["unit_price"]

sales_by_country = df.groupby("country")["total_value"].sum()
sales_by_product = df.groupby("product_name")["total_value"].sum()

print("\nSprzedaż wg kraju:\n", sales_by_country)
print("\nSprzedaż wg produktu:\n", sales_by_product)

df_high_value = df[df["total_value"] > 1000]
df_high_value.to_csv("high_value_sales.csv", index=False)

transactions_by_country = df_high_value.groupby("country").size()
print("\nTransakcje >1000 wg kraju:\n", transactions_by_country)


# =====================================================
# ZADANIE 1 - TRANSFORMACJA
# =====================================================

print("\n=== TRANSFORMACJA DANYCH ===")

df = df.drop_duplicates()

df["total_price"] = df["quantity"] * df["unit_price"]

country_iso = {
    "Poland": "PL",
    "Germany": "DE"
}
df["country_iso"] = df["country"].map(country_iso)

df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["day"] = df["order_date"].dt.day

q1 = df["unit_price"].quantile(0.25)
q3 = df["unit_price"].quantile(0.75)
iqr = q3 - q1

price_outliers = df[
    (df["unit_price"] < q1 - 1.5 * iqr) |
    (df["unit_price"] > q3 + 1.5 * iqr)
]

print("Znalezione nietypowe ceny:", len(price_outliers))


# =====================================================
# ZADANIE 2 - ANALIZA CZASOWA
# =====================================================

print("\n=== ANALIZA CZASOWA ===")

monthly_sales = df.groupby(["country", "year", "month"]).agg({
    "total_price": "sum",
    "quantity": "sum"
})

df["quarter"] = df["order_date"].dt.to_period("Q")

avg_price_quarter = df.groupby(["product_name", "quarter"])["unit_price"].mean()

laptops = df[df["product_name"] == "Laptop"]
trend = laptops[laptops["country"].isin(["Poland", "Germany"])]

trend_grouped = trend.groupby(["country", "year", "month"])["total_price"].sum()


# =====================================================
# ZADANIE 3 - RANKING
# =====================================================

print("\n=== RANKINGI ===")

top_clients = (
    df.groupby(["country", "customer_name"])["total_price"]
    .sum()
    .reset_index()
    .sort_values(["country", "total_price"], ascending=[True, False])
    .groupby("country")
    .head(3)
)

product_ranking = df.groupby("product_name")["total_price"].sum().sort_values(ascending=False)

category_share = (
    df.groupby("category")["total_price"].sum() /
    df["total_price"].sum()
)


# =====================================================
# ZADANIE 4 - KOSZYK
# =====================================================

print("\n=== ANALIZA KOSZYKA ===")

basket = df.groupby("order_id")["product_name"].apply(list)
avg_products = df.groupby("order_id")["product_name"].count().mean()
correlation = df["unit_price"].corr(df["quantity"])

print("Średnia liczba produktów w zamówieniu:", avg_products)
print("Korelacja cena vs ilość:", correlation)


# =====================================================
# ZADANIE 5 - MODEL HURTOWNI
# =====================================================

print("\n=== MODEL HURTOWNI ===")

dim_customer = df[["customer_name", "country"]].drop_duplicates()
dim_product = df[["product_name", "category"]].drop_duplicates()

fact_sales = df[[
    "order_id",
    "customer_name",
    "order_date",
    "quantity",
    "total_price"
]]

olap = df.pivot_table(
    values="total_price",
    index="country",
    columns="category",
    aggfunc="sum"
)

dim_time = df[["order_date", "year", "month", "quarter"]].drop_duplicates()


# =====================================================
# ZAPIS
# =====================================================

dim_customer.to_csv("dim_customer.csv", index=False)
dim_product.to_csv("dim_product.csv", index=False)
fact_sales.to_csv("fact_sales.csv", index=False)
dim_time.to_csv("dim_time.csv", index=False)

print("\n=== GOTOWE ===")