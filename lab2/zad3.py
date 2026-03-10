import pandas as pd

# wczytanie danych
df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

# usunięcie wierszy bez CustomerID
df = df.dropna(subset=["CustomerID"])

# ===== CUSTOMER =====
customers = df[["CustomerID", "Country"]].drop_duplicates()
customers["CustomerID"] = customers["CustomerID"].astype(int)

# ===== PRODUCT =====
products = df[["StockCode", "Description", "UnitPrice"]].drop_duplicates()

# ===== INVOICE =====
invoices = df[["InvoiceNo", "InvoiceDate", "CustomerID"]].drop_duplicates()
invoices["CustomerID"] = invoices["CustomerID"].astype(int)

# ===== SALES (relacja między fakturą i produktem) =====
sales = df[["InvoiceNo", "StockCode", "Quantity"]]

# zapis tabel do plików CSV
customers.to_csv("customers.csv", index=False)
products.to_csv("products.csv", index=False)
invoices.to_csv("invoices.csv", index=False)
sales.to_csv("sales.csv", index=False)

print("Znormalizowane tabele zostały utworzone.")