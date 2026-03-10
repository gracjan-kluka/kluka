import pandas as pd

# wczytanie pliku CSV do DataFrame
df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

# liczba rekordów i kolumn
print("Shape (rows, columns):")
print(df.shape)

# liczba rekordów
print("Number of records:")
print(df.shape[0])

# liczba kolumn
print("Number of columns:")
print(df.shape[1])

# nazwy kolumn
print("Columns:")
print(df.columns)

# 5 przykładowych wierszy
print("Sample rows:")
print(df.head())