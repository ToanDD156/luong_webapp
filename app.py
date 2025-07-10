from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_user(mnv_input):
    """
    Chuẩn hóa mã nhân viên từ input và tìm trong cơ sở dữ liệu
    """
    try:
        # --- THAY ĐỔI TẠI ĐÂY ---
        # Chuyển đổi input của người dùng thành số nguyên để so sánh
        mnv_int = int(float(str(mnv_input).strip()))
        mnv_to_query = str(mnv_int) # Chuyển lại thành chuỗi số nguyên (vd: 12)
        # --- HẾT THAY ĐỔI ---

        conn = sqlite3.connect("data.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # So sánh MNV trong DB (đã được chuẩn hóa thành số nguyên dạng chuỗi)
        cur.execute("SELECT * FROM luong WHERE `MNV` = ?", (mnv_to_query,))
        user = cur.fetchone()
        conn.close()
        return user
    except ValueError:
        # Xử lý trường hợp input không phải là số hợp lệ
        return None

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        mnv = request.form["mnv"].strip()
        password = request.form["password"].strip()
        
        # Kiểm tra mã nhân viên và mật khẩu phải giống nhau
        # --- THAY ĐỔI TẠI ĐÂY ---
        try:
            mnv_val = int(float(mnv))
            password_val = int(float(password))

            if mnv_val != password_val:
                error = "❌ Mã nhân viên và mật khẩu phải giống nhau!"
            else:
                user = get_user(mnv_val) # Truyền giá trị số nguyên đã chuẩn hóa
                if user:
                    return render_template("salary.html", user=dict(user))
                else:
                    error = "❌ Không tìm thấy mã nhân viên trong hệ thống!"
        except ValueError:
            error = "❌ Mã nhân viên hoặc mật khẩu không hợp lệ. Vui lòng nhập số!"
        # --- HẾT THAY ĐỔI ---
    
    return render_template("login.html", error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
