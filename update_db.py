import pandas as pd
import pyodbc

# Cấu hình kết nối SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=hms_hqt;"
    "UID=sa;"
    "PWD=abcd@1234"
)
cursor = conn.cursor()

# Đọc file CSV chứa các bản ghi cần cập nhật
df = pd.read_csv("./dataset/appointments.csv", encoding="utf-8")

# Lặp qua từng dòng và thực hiện UPDATE vào bảng appointment
for _, row in df.iterrows():
    cursor.execute("""
        UPDATE appointment
        SET
            reason = ?,
            status = ?,
            phone = ?,
            location = ?,
            appointment_type = ?
        WHERE id = ?
    """, row['reason'], row['status'], row['phone'], row['location'], row['appointment_type'], row['appointment_id'])

# Commit và đóng kết nối
conn.commit()
conn.close()
print("✅ Đã cập nhật nội dung bảng 'appointment' thành công.")
