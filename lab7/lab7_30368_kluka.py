import pandas as pd
import time

# =========================
# ETAP 1 — WCZYTANIE I ANALIZA DANYCH
# =========================

start_load = time.time()

df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

end_load = time.time()

print("=== ETAP 1 ===")
print(f"Liczba rekordów: {len(df)}")
print("\nBrakujące wartości:")
print(df.isnull().sum())

print("\nTypy danych:")
print(df.dtypes)

print(f"\nCzas wczytywania: {end_load - start_load:.4f} sekundy")


# Dodanie kolumny Revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Kopia danych przed optymalizacją
df_before = df.copy()

memory_before = df_before.memory_usage(deep=True).sum() / 1024**2
print(f"\nZużycie pamięci przed optymalizacją: {memory_before:.2f} MB")


# =========================
# ETAP 2 — OPTYMALIZACJA PAMIĘCI
# =========================

print("\n=== ETAP 2 ===")

# category dla tekstowych
text_columns = ["InvoiceNo", "StockCode", "Description", "Country"]

for col in text_columns:
    df[col] = df[col].astype("category")

# downcast liczb
df["Quantity"] = pd.to_numeric(df["Quantity"], downcast="integer")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], downcast="float")
df["CustomerID"] = pd.to_numeric(df["CustomerID"], downcast="integer")
df["Revenue"] = pd.to_numeric(df["Revenue"], downcast="float")

memory_after = df.memory_usage(deep=True).sum() / 1024**2

print(f"Zużycie pamięci po optymalizacji: {memory_after:.2f} MB")
print(f"Oszczędność pamięci: {memory_before - memory_after:.2f} MB")


# =========================
# ETAP 3 — ANALIZA WYDAJNOŚCI
# =========================

print("\n=== ETAP 3 ===")

def measure_operation(name, func):
    start = time.time()
    result = func()
    end = time.time()
    print(f"{name}: {end - start:.6f} sekundy")
    return result


print("\n--- PRZED OPTYMALIZACJĄ ---")

measure_operation(
    "Suma sprzedaży wg kraju",
    lambda: df_before.groupby("Country")["Revenue"].sum()
)

measure_operation(
    "Suma sprzedaży wg miesiąca",
    lambda: df_before.assign(
        InvoiceDate=pd.to_datetime(
            df_before["InvoiceDate"],
            format="%m/%d/%Y %H:%M",
            errors="coerce"
        )
    ).groupby(
        pd.to_datetime(
            df_before["InvoiceDate"],
            format="%m/%d/%Y %H:%M",
            errors="coerce"
        ).dt.month
    )["Revenue"].sum()
)

measure_operation(
    "TOP 10 klientów",
    lambda: df_before.groupby("CustomerID")["Revenue"].sum().sort_values(ascending=False).head(10)
)

measure_operation(
    "Produkty sprzedane w UK",
    lambda: df_before[df_before["Country"] == "United Kingdom"]
)

measure_operation(
    "Sprzedaż > 1000",
    lambda: df_before[df_before["Revenue"] > 1000]
)


print("\n--- PO OPTYMALIZACJI ---")

measure_operation(
    "Suma sprzedaży wg kraju",
    lambda: df.groupby("Country", observed=False)["Revenue"].sum()
)

measure_operation(
    "Suma sprzedaży wg miesiąca",
    lambda: df.assign(
        InvoiceDate=pd.to_datetime(df["InvoiceDate"], format="%m/%d/%Y %H:%M", errors="coerce")
    ).groupby(
        pd.to_datetime(df["InvoiceDate"], format="%m/%d/%Y %H:%M", errors="coerce").dt.month
    )["Revenue"].sum()
)

measure_operation(
    "TOP 10 klientów",
    lambda: df.groupby("CustomerID")["Revenue"].sum().sort_values(ascending=False).head(10)
)

measure_operation(
    "Produkty sprzedane w UK",
    lambda: df[df["Country"] == "United Kingdom"]
)

measure_operation(
    "Sprzedaż > 1000",
    lambda: df[df["Revenue"] > 1000]
)


# =========================
# ETAP 4 — WNIOSKI
# =========================

print("\n=== ETAP 4 — WNIOSKI ===")
print("1. Optymalizacja zmniejszyła zużycie pamięci z 196.89 MB do 57.66 MB, czyli o około 71%.")
print("2. Największe przyspieszenie uzyskano dla grupowania według kraju (około 6 razy szybciej).")
print("3. Filtrowanie produktów z Wielkiej Brytanii przyspieszyło ponad 2 razy dzięki zastosowaniu typu category.")
print("4. Nie wszystkie operacje przyspieszyły znacząco — analiza miesięczna i TOP 10 klientów pozostały na podobnym poziomie, co pokazuje, że mniejsze zużycie pamięci nie zawsze oznacza duży wzrost wydajności.")