import pandas as pd
import sqlite3

df = pd.read_excel("08.07.2025.xlsx", sheet_name="PKT", header=2)
df = df[df["MNV"].notna()]
df["MNV"] = df["MNV"].astype(int).astype(str)
df["Mã số"] = df["MNV"]
df["Mật khẩu"] = df["MNV"]

conn = sqlite3.connect("data.db")
df.to_sql("luong", conn, if_exists="replace", index=False)
print("✅ Đã lưu bảng lương đầy đủ vào data.db")
