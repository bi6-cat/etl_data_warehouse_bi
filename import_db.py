import pandas as pd
import pyodbc

# Kết nối đến SQL Server
conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hms_hqt;UID=sa;PWD=abcd@1234")
cursor = conn.cursor()

def import_csv_to_db(csv_path, sql_insert, columns):
    df = pd.read_csv(csv_path, encoding="utf-8")
    for _, row in df.iterrows():
        values = [row[col] for col in columns]
        cursor.execute(sql_insert, *values)
    print(f"✅ Imported: {csv_path}")
    
# # 1. Patient
cursor.execute("SET IDENTITY_INSERT patient ON")
import_csv_to_db(
    "./dataset/patients.csv",
    "INSERT INTO patient (id, name, gender, dob, address, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
    ['patient_id', 'name', 'gender', 'dob', 'address', 'phone', 'email']
)
cursor.execute("SET IDENTITY_INSERT patient OFF")


# 2. Doctors
cursor.execute("SET IDENTITY_INSERT doctor ON")
import_csv_to_db(
    "./dataset/doctors.csv",
    "INSERT INTO doctor (id, name, last_name, specialization, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
    ['doctor_id', 'name', 'last_name', 'specialization', 'phone', 'email']
)
cursor.execute("SET IDENTITY_INSERT doctor OFF")


# 3. Appointments
cursor.execute("SET IDENTITY_INSERT appointment ON")
import_csv_to_db(
    "./dataset/appointments.csv",
    """INSERT INTO appointment (
        id, patient_id, doctor_id, appointment_date,
        start_time, end_time, reason, status, phone, location, appointment_type
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    ['appointment_id', 'patient_id', 'doctor_id', 'appointment_date',
     'start_time', 'end_time', 'reason', 'status', 'phone', 'location', 'appointment_type']
)
cursor.execute("SET IDENTITY_INSERT appointment OFF")

# 4. VitalSigns
cursor.execute("SET IDENTITY_INSERT vital_sign ON")
import_csv_to_db(
    "./dataset/vital_signs.csv",
    """INSERT INTO vital_sign (
        id, patient_id, measurement_date,
        blood_pressure, heart_rate, respiratory_rate, temperature,
        oxygen_saturation, blood_sugar
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    ['vital_id', 'patient_id', 'measurement_date',
     'blood_pressure', 'heart_rate', 'respiratory_rate', 'temperature',
     'oxygen_saturation', 'blood_sugar']
)
cursor.execute("SET IDENTITY_INSERT vital_sign OFF")

# 5. Diseases
cursor.execute("SET IDENTITY_INSERT disease ON")
import_csv_to_db(
    
    "./dataset/diseases.csv",
    "INSERT INTO disease (id, patient_id, disease_name, diagnosis_date) VALUES (?, ?, ?, ?)",
    ['disease_id', 'patient_id', 'disease_name', 'diagnosis_date']
)
cursor.execute("SET IDENTITY_INSERT disease OFF")

# 6. Treatments

cursor.execute("SET IDENTITY_INSERT treatment ON")
import_csv_to_db(
    "./dataset/treatments.csv",
    """INSERT INTO treatment (
        id, patient_id, doctor_id, disease_id,
        treatment_description, treatment_date
    ) VALUES (?, ?, ?, ?, ?, ?)""",
    ['treatment_id', 'patient_id', 'doctor_id', 'disease_id',
     'treatment_description', 'treatment_date']
)
cursor.execute("SET IDENTITY_INSERT treatment OFF")

# 7. HospitalFees
cursor.execute("SET IDENTITY_INSERT hospital_fee ON")
import_csv_to_db(
    "./dataset/hospital_fee.csv",
    """INSERT INTO hospital_fee (
        id, appointment_id, patient_id, service_type,
        description, amount, fee_date, phone
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    ['fee_id', 'appointment_id', 'patient_id', 'service_type',
     'description', 'amount', 'fee_date', 'phone']
)
cursor.execute("SET IDENTITY_INSERT hospital_fee OFF")

# 8. Prescriptions
cursor.execute("SET IDENTITY_INSERT prescription ON")
import_csv_to_db(
    "./dataset/prescriptions.csv",
    """INSERT INTO prescription (
        id, appointment_id, doctor_id, patient_id,
        medicine_name, form, dosage_mg, instruction, duration_days, note
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    ['prescription_id', 'appointment_id', 'doctor_id', 'patient_id',
     'medicine_name', 'form', 'dosage_mg', 'instruction', 'duration_days', 'note']
)
cursor.execute("SET IDENTITY_INSERT prescription OFF")

# Commit & đóng kết nối
conn.commit()
conn.close()
print("🎉 Tất cả dữ liệu đã được import thành công.")
