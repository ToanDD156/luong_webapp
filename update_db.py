import pandas as pd
import sqlite3

excel_file = "BL.xlsx"
database_file = "data.db"

expected_sheets = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
    "CD", "HT", "KHO", "CUT", "QA", "PKT", "BVVS", "QDNS", "KTKD", "BEP"
]

xls = pd.ExcelFile(excel_file)
available_sheets = xls.sheet_names
missing = [s for s in expected_sheets if s not in available_sheets]
if missing:
    print("⚠️ Thiếu sheet:", missing)

all_data = []
total_valid = 0

for sheet in expected_sheets:
    if sheet not in available_sheets:
        continue
    try:
        print(f"📄 Đọc sheet: {sheet}")
        df = pd.read_excel(xls, sheet_name=sheet, skiprows=2)
        df["DonVi"] = sheet

        # 🔍 Chuẩn hóa tên cột mã nhân viên
        for col in df.columns:
            if str(col).strip().lower() in ["mnv", "mã số", "mã nv", "manv"]:
                df = df.rename(columns={col: "MNV"})
                break

        if "MNV" not in df.columns:
            print(f"⚠️ Sheet '{sheet}' không có cột mã nhân viên.")
            continue

        df = df[df["MNV"].notna()]
        
        # --- THAY ĐỔI TẠI ĐÂY ---
        # Chuyển đổi cột MNV về dạng số nguyên và sau đó về chuỗi để đồng nhất
        df["MNV"] = df["MNV"].apply(lambda x: str(int(float(x))) if pd.notna(x) and str(x).replace('.', '', 1).isdigit() else None)
        df = df.dropna(subset=["MNV"]) # Loại bỏ các giá trị MNV không hợp lệ sau chuyển đổi
        # --- HẾT THAY ĐỔI ---

        count = len(df)
        total_valid += count
        all_data.append(df)
        print(f"✅ Sheet '{sheet}': {count} dòng hợp lệ.")
    except Exception as e:
        print(f"❌ Lỗi sheet '{sheet}': {e}")

if all_data:
    full_df = pd.concat(all_data, ignore_index=True)
    conn = sqlite3.connect(database_file)
    full_df.to_sql("luong", conn, if_exists="replace", index=False)
    conn.close()
    print(f"\n🎯 Đã lưu {total_valid} dòng từ {len(all_data)} sheet.")
else:
    print("❌ Không có dữ liệu nào hợp lệ.")
