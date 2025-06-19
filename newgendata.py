from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os
import numpy as np

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

fake = Faker("vi_VN")  # Set locale to Vietnamese

# Data sizes
num_patients = 4000   # 40,000 patients
num_doctors = 100    # 1,000 doctors
num_records = num_patients * 2  # 80,000 vital signs
num_appointments = num_patients * 3  # 1,20,000 appointments
num_lab_results = num_patients * 2  # 80,000 lab results

# Create directory for data
if not os.path.exists('./data1k'):
    os.makedirs('./data1k')

# Patients (Bệnh nhân)
# Age distribution: more patients aged 51–65, then 36–50, fewer in 0–18
def generate_age():
    age_dist = np.random.choice(
        [
            np.random.randint(0, 18),    # 0–18 years
            np.random.randint(19, 35),   # 19–35 years
            np.random.randint(36, 50),   # 36–50 years
            np.random.randint(51, 65),   # 51–65 years
            np.random.randint(66, 90)    # 66–90 years
        ],
        p=[0.06, 0.15, 0.24, 0.34, 0.21]  # Adjusted probabilities
    )
    return age_dist.item()  # Convert numpy.int64 to Python int

patients = []
for i in range(1, num_patients + 1):
    dob = (datetime.now() - timedelta(days=generate_age() * 365)).strftime('%Y-%m-%d')
    patient = {
        'patient_id': i,
        'name': fake.name(),
        'gender': random.choice(['Nam', 'Nữ']),
        'dob': dob,
        'address': fake.address().replace("\n", ", "),
        'phone': fake.phone_number(),
        'email': fake.email()
    }
    patients.append(patient)

df_patients = pd.DataFrame(patients)
df_patients.to_csv('./data1k/patients.csv', index=False)
patient_phone_map = {p['patient_id']: p['phone'] for p in patients}

# Doctors (Bác sĩ)
# Skewed specialization distribution
specialties = [
    "Tổng quát"] * 40 + ["Tim mạch"] * 15 + ["Nội tiết"] * 10 + ["Da liễu"] * 8 + ["Thần kinh"] * 7 + \
    ["Ung bướu"] * 5 + ["Nhi khoa"] * 10 + ["Tiêu hóa"] * 8 + ["Sản phụ khoa"] * 8 + ["Tâm thần"] * 5 + \
    ["Hô hấp"] * 8 + ["Chấn thương chỉnh hình"] * 6 + ["Tai Mũi Họng"] * 7 + ["Mắt"] * 6 + \
    ["Tiết niệu"] * 5 + ["Cơ xương khớp"] * 5 + ["Miễn dịch"] * 2

doctors = []
for i in range(1, num_doctors + 1):
    doctor = {
        'doctor_id': i,
        'Name': fake.name(),
        'last_name': fake.last_name(),
        'specialization': random.choice(specialties),
        'phone': fake.phone_number(),
        'email': fake.email()
    }
    doctors.append(doctor)

df_doctors = pd.DataFrame(doctors)
df_doctors.to_csv('./data1k/doctors.csv', index=False)

# Appointments (Cuộc hẹn)
# Weighted to have more appointments on Saturday and Sunday
# Top 3 doctors have the most appointments, others decrease gradually
appointment_reasons = [
    "Khám sức khỏe định kỳ", "Tư vấn dinh dưỡng", "Theo dõi bệnh mãn tính", "Đau đầu", "Khó thở",
    "Đau ngực", "Xét nghiệm máu", "Siêu âm", "Khám thai", "Khám da liễu", "Khám thần kinh",
    "Khám tiêu hóa", "Tiêm chủng", "Khám hậu COVID", "Tư vấn tâm lý", "Khám dị ứng", "Khám mắt", "Khám tai mũi họng"
]

locations = [
    "Bệnh viện Đa khoa Trung ương", "Phòng khám đa khoa Hòa Bình", "Bệnh viện Tim Hà Nội", "Phòng khám chuyên khoa Mắt",
    "Bệnh viện Nhi Đồng", "Phòng khám Phụ sản", "Bệnh viện Đại học Y Hà Nội", "Phòng khám tư nhân Minh Khai"
]

appointment_types = [
    "Khám bệnh", "Chăm sóc sức khỏe định kỳ", "Điều trị sau phẫu thuật", "Kiểm tra sức khỏe cho công ty", "Tư vấn tâm lý"
]

# Weight weekends (Saturday=5, Sunday=6) higher
def weighted_date():
    day_weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.25, 0.25]  # Higher weights for Sat (5) and Sun (6)
    days_ago = random.randint(0, 365)
    base_date = datetime.now() - timedelta(days=days_ago)
    while True:
        chosen_day = np.random.choice(range(7), p=day_weights).item()  # Convert numpy.int64 to Python int
        target_date = base_date - timedelta(days=(base_date.weekday() - chosen_day) % 7)
        if 0 <= (datetime.now() - target_date).days <= 365:
            return target_date

# Create a skewed distribution for doctor appointments
# Top 3 doctors get the most appointments, others follow a Zipf-like distribution
doctor_ids = list(range(1, num_doctors + 1))
# Use a Zipf distribution to assign weights (top 3 have highest weights)
doctor_weights = [1/(i+1)**1.5 for i in range(num_doctors)]
# Boost the weights of the top 3 doctors
doctor_weights[0] *= 10  # Doctor ID 1
doctor_weights[1] *= 8   # Doctor ID 2
doctor_weights[2] *= 6   # Doctor ID 3
doctor_weights = [w/sum(doctor_weights) for w in doctor_weights]  # Normalize to sum to 1

appointments = []
for i in range(1, num_appointments + 1):
    pat_id = random.randint(1, num_patients)
    doc_id = np.random.choice(doctor_ids, p=doctor_weights).item()  # Skewed doctor selection
    date = weighted_date()
    start_hour = random.randint(7, 17)
    start_minute = random.choice([0, 15, 30, 45])
    start_time = datetime(date.year, date.month, date.day, start_hour, start_minute)
    duration = random.randint(30, 90)
    end_time = start_time + timedelta(minutes=duration)
    status = np.random.choice(["Hủy", "Hoàn tất", "Đã đặt"], p=[0.049, 0.751, 0.20]).item()
    appointment = {
        'appointment_id': i,
        'patient_id': pat_id,
        'doctor_id': doc_id,
        'appointment_date': date.strftime('%Y-%m-%d'),
        'start_time': start_time.strftime('%H:%M'),
        'end_time': end_time.strftime('%H:%M'),
        'reason': random.choice(appointment_reasons),
        'status': random.choice(["Đã đặt", "Hoàn tất", "Hủy"]),
        'phone': patient_phone_map[pat_id],
        'location': random.choice(locations),
        'appointment_type': random.choice(appointment_types)
    }
    appointments.append(appointment)

df_appointments = pd.DataFrame(appointments)
df_appointments.to_csv('./data1k/appointments.csv', index=False)

# Vital Signs (Chỉ số sinh tồn)
vital_signs = []
for vs_id in range(1, num_records + 1):
    pat_id = random.randint(1, num_patients)
    bp_systolic = int(np.random.normal(120, 20))
    bp_diastolic = int(np.random.normal(80, 10))
    blood_pressure = f"{max(90, min(180, bp_systolic))}/{max(60, min(120, bp_diastolic))}"
    heart_rate = int(np.random.normal(75, 15))
    heart_rate = max(50, min(120, heart_rate))
    respiratory_rate = int(np.random.normal(16, 4))
    respiratory_rate = max(10, min(30, respiratory_rate))
    temperature = round(np.random.normal(36.6, 0.5), 1)
    temperature = max(35.0, min(40.0, temperature))
    spO2 = int(np.random.normal(98, 2))
    spO2 = max(90, min(100, spO2))
    blood_sugar = int(np.random.normal(100, 30))
    blood_sugar = max(70, min(250, blood_sugar))

    vs = {
        'vital_id': vs_id,
        'patient_id': pat_id,
        'measurement_date': (datetime.now() - timedelta(days=random.randint(0, 1000))).strftime('%Y-%m-%d'),
        'blood_pressure': blood_pressure,
        'heart_rate': heart_rate,
        'respiratory_rate': respiratory_rate,
        'temperature': temperature,
        'oxygen_saturation': spO2,
        'blood_sugar': blood_sugar
    }
    vital_signs.append(vs)

df_vitals = pd.DataFrame(vital_signs)
df_vitals.to_csv('./data1k/vital_signs.csv', index=False)

# Diseases (Bệnh án)
benhly_common = [
    "Tăng huyết áp"] * 20 + ["Tiểu đường tuýp 2"] * 15 + ["Cảm cúm"] * 10 + ["Viêm loét dạ dày"] * 8 + \
    ["Trầm cảm"] * 7 + ["Hen suyễn"] * 6 + ["Béo phì"] * 5 + ["Thiếu máu"] * 5
benhly_rare = [
    "Bệnh tim mạch", "Đột quỵ", "Loạn nhịp tim", "Suy tim", "Tiểu đường tuýp 1", "Viêm phổi", 
    "Bệnh phổi tắc nghẽn mạn tính (COPD)", "Bệnh gan", "Viêm đại tràng", "Hội chứng ruột kích thích", 
    "Rối loạn lo âu", "Chấn thương sọ não", "Bệnh Alzheimer", "Ung thư", "Viêm gan B", "Loãng xương", 
    "COVID-19", "Bệnh Parkinson", "Lupus ban đỏ", "Viêm khớp dạng thấp", "Bệnh Crohn", "HIV/AIDS", 
    "Xơ gan", "Sởi", "Cúm gia cầm", "Sốt xuất huyết", "Bệnh tự miễn", "Thalassemia"
]
benhly = benhly_common + benhly_rare

diseases = []
d_id = 1
for pat in range(1, num_patients + 1):
    num_diseases = np.random.choice([0, 1, 2, 3], p=[0.2, 0.5, 0.25, 0.05])
    patient_diseases = random.sample(benhly, num_diseases)
    for disease in patient_diseases:
        diseases.append({
            'disease_id': d_id,
            'patient_id': pat,
            'disease_name': disease,
            'diagnosis_date': (datetime.now() - timedelta(days=random.randint(30, 2000))).strftime('%Y-%m-%d')
        })
        d_id += 1

df_diseases = pd.DataFrame(diseases)
df_diseases.to_csv('./data1k/diseases.csv', index=False)

# Treatments (Điều trị)
treatments = []
t_id = 1
for dis in diseases:
    disease_name = dis['disease_name']
    treatment_options = []
    if "ung thư" in disease_name.lower():
        treatment_options = ["Hóa trị", "Xạ trị", "Phẫu thuật", "Điều trị bằng thuốc kháng sinh"]
    elif "tiểu đường" in disease_name.lower():
        treatment_options = ["Điều trị tiểu đường", "Chế độ ăn kiêng", "Dùng thuốc", "Tập luyện phục hồi"]
    elif "tim mạch" in disease_name.lower():
        treatment_options = ["Điều trị bệnh tim mạch", "Điều trị huyết áp cao", "Phẫu thuật", "Điều trị bằng thuốc giảm đau"]
    elif "viêm gan" in disease_name.lower():
        treatment_options = ["Điều trị viêm gan", "Dùng thuốc", "Nội soi"]
    elif "trầm cảm" in disease_name.lower():
        treatment_options = ["Tư vấn tâm lý", "Điều trị trầm cảm", "Chế độ ăn kiêng"]
    elif "hen suyễn" in disease_name.lower():
        treatment_options = ["Điều trị hen suyễn", "Dùng thuốc", "Tập luyện phục hồi"]
    else:
        treatment_options = ["Điều trị bệnh lý", "Dùng thuốc", "Tư vấn dinh dưỡng", "Tập luyện phục hồi", 
                             "Chế độ ăn kiêng", "Phẫu thuật"]
    for _ in range(random.randint(1, 3)):
        treatments.append({
            'treatment_id': t_id,
            'patient_id': dis['patient_id'],
            'doctor_id': random.randint(1, num_doctors),
            'disease_id': dis['disease_id'],
            'treatment_description': random.choice(treatment_options),
            'treatment_date': (datetime.now() - timedelta(days=random.randint(0, 1500))).strftime('%Y-%m-%d')
        })
        t_id += 1

df_treatments = pd.DataFrame(treatments)
df_treatments.to_csv('./data1k/treatments.csv', index=False)

# Hospital Fees (Chi phí bệnh viện)
service_types = [
    {"type": "Khám tổng quát", "min": 100, "max": 300, "weight": 20},
    {"type": "Khám nội tiết", "min": 150, "max": 350, "weight": 10},
    {"type": "Khám tim mạch", "min": 200, "max": 400, "weight": 10},
    {"type": "Khám da liễu", "min": 120, "max": 250, "weight": 8},
    {"type": "Khám tiêu hóa", "min": 150, "max": 300, "weight": 8},
    {"type": "Khám hô hấp", "min": 140, "max": 280, "weight": 8},
    {"type": "Khám thần kinh", "min": 180, "max": 350, "weight": 5},
    {"type": "Khám sản phụ khoa", "min": 150, "max": 350, "weight": 5},
    {"type": "Khám nhi khoa", "min": 100, "max": 250, "weight": 5},
    {"type": "Khám tai mũi họng", "min": 120, "max": 250, "weight": 5},
    {"type": "Xét nghiệm máu", "min": 80, "max": 150, "weight": 15},
    {"type": "Xét nghiệm nước tiểu", "min": 70, "max": 120, "weight": 10},
    {"type": "Chụp X-quang", "min": 150, "max": 300, "weight": 5},
    {"type": "Chụp CT Scan", "min": 500, "max": 1200, "weight": 2},
    {"type": "Chụp MRI", "min": 800, "max": 2000, "weight": 1},
    {"type": "Siêu âm bụng tổng quát", "min": 120, "max": 250, "weight": 5},
    {"type": "Nội soi dạ dày", "min": 600, "max": 1200, "weight": 2},
    {"type": "Điện tim (ECG)", "min": 150, "max": 350, "weight": 5},
    {"type": "Tiêm chủng", "min": 100, "max": 300, "weight": 5},
    {"type": "Tư vấn tâm lý", "min": 250, "max": 600, "weight": 3}
]

weights = [s['weight'] for s in service_types]
hospital_fees = []
fee_id = 1
for appt in appointments:
    num_services = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
    used_services = random.choices(service_types, weights=weights, k=num_services)
    for service in used_services:
        hospital_fees.append({
            'fee_id': fee_id,
            'appointment_id': appt['appointment_id'],
            'patient_id': appt['patient_id'],
            'service_type': service['type'],
            'description': f"{service['type']} cho bệnh nhân ID {appt['patient_id']}",
            'amount': round(random.uniform(service['min'], service['max']), 2),
            'fee_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'phone': patient_phone_map[appt['patient_id']]
        })
        fee_id += 1

df_fees = pd.DataFrame(hospital_fees)
df_fees.to_csv('./data1k/hospital_fee.csv', index=False)

# Prescriptions (Đơn thuốc)
medication_info = [
    {"name": "Paracetamol", "form": "viên nén", "dosage_mg": [500], "weight": 20},
    {"name": "Amoxicillin", "form": "viên nang", "dosage_mg": [250, 500], "weight": 15},
    {"name": "Metformin", "form": "viên nén", "dosage_mg": [500, 850], "weight": 10},
    {"name": "Omeprazole", "form": "viên nang", "dosage_mg": [20], "weight": 10},
    {"name": "Amlodipine", "form": "viên nén", "dosage_mg": [5, 10], "weight": 8},
    {"name": "Ibuprofen", "form": "viên nén", "dosage_mg": [200, 400], "weight": 8},
    {"name": "Salbutamol", "form": "ống hít", "dosage_mg": [100], "weight": 5},
    {"name": "Cetirizine", "form": "viên nén", "dosage_mg": [10], "weight": 5},
    {"name": "Sertraline", "form": "viên nén", "dosage_mg": [50, 100], "weight": 3},
    {"name": "Insulin", "form": "dung dịch tiêm", "dosage_mg": [10, 20, 30], "weight": 2}
]

med_weights = [m['weight'] for m in medication_info]
instructions = [
    "1 viên x 2 lần/ngày sau ăn",
    "1 viên trước khi ngủ",
    "2 viên sáng, 1 viên tối",
    "1 viên mỗi 8 giờ",
    "1 viên mỗi ngày vào buổi sáng",
    "Uống sau ăn sáng",
    "Dùng sau ăn tối",
    "1 viên mỗi 6 giờ nếu cần"
]
notes = [
    "Uống nhiều nước",
    "Không dùng chung với sữa",
    "Tránh lái xe sau khi dùng",
    "Theo dõi đường huyết",
    "Không uống khi đói",
    "Tránh dùng chung với thuốc kháng acid",
    "Theo dõi huyết áp hằng ngày",
    "Dùng đúng giờ"
]

prescriptions = []
pres_id = 1
for appt in appointments:
    num_prescriptions = np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2])
    for _ in range(num_prescriptions):
        med = random.choices(medication_info, weights=med_weights, k=1)[0]
        dose = random.choice(med["dosage_mg"])
        prescription = {
            'prescription_id': pres_id,
            'appointment_id': appt['appointment_id'],
            'doctor_id': appt['doctor_id'],
            'patient_id': appt['patient_id'],
            'medicine_name': med['name'],
            'form': med['form'],
            'dosage_mg': dose,
            'instruction': random.choice(instructions),
            'duration_days': random.randint(3, 14),
            'note': random.choice(notes)
        }
        prescriptions.append(prescription)
        pres_id += 1

df_pres = pd.DataFrame(prescriptions)
df_pres.to_csv('./data1k/prescriptions.csv', index=False)

# Lab Results (Kết quả xét nghiệm)
lab_tests = [
    {
        "test_type": "Máu", "parameter": "Hemoglobin", "unit": "g/dL", "normal_range": "13.8-17.2",
        "min_val": 10, "max_val": 18, "weight": 20
    },
    {
        "test_type": "Máu", "parameter": "Glucose", "unit": "mg/dL", "normal_range": "70-99",
        "min_val": 60, "max_val": 200, "weight": 15
    },
    {
        "test_type": "Nước tiểu", "parameter": "pH", "unit": "", "normal_range": "4.6-8.0",
        "min_val": 4.0, "max_val": 9.0, "weight": 10
    },
    {
        "test_type": "X-quang", "parameter": "X-quang phổi", "unit": "", "normal_range": "Không phát hiện bất thường",
        "result_texts": ["Không phát hiện bất thường", "Có dấu hiệu viêm", "Nốt bất thường", "Tăng đậm độ mô mềm"],
        "weight": 5
    },
    {
        "test_type": "MRI", "parameter": "MRI não", "unit": "", "normal_range": "Không có bất thường",
        "result_texts": ["Không có bất thường", "Khối u nhỏ vùng trán", "Teo não nhẹ", "Viêm màng não"],
        "weight": 2
    },
    {
        "test_type": "Siêu âm", "parameter": "Siêu âm bụng", "unit": "", "normal_range": "Bình thường",
        "result_texts": ["Gan to nhẹ", "Sỏi túi mật", "Bình thường", "Dịch ổ bụng ít"],
        "weight": 8
    }
]

lab_weights = [t['weight'] for t in lab_tests]
lab_results = []
lab_result_id = 1
for _ in range(num_lab_results):
    test = random.choices(lab_tests, weights=lab_weights, k=1)[0]
    appt = random.choice(appointments)
    patient_id = appt['patient_id']
    appointment_id = appt['appointment_id']
    test_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')

    if 'result_texts' in test:
        result_value = random.choice(test['result_texts'])
        interpretation = "Bình thường" if result_value in ["Không phát hiện bất thường", "Bình thường", "Không có bất thường"] else "Bất thường"
    else:
        value = round(random.uniform(test['min_val'], test['max_val']), 1)
        result_value = value
        normal_range_parts = test['normal_range'].split('-')
        lower = float(normal_range_parts[0])
        upper = float(normal_range_parts[1])
        interpretation = "Bình thường" if lower <= value <= upper else ("Thấp" if value < lower else "Cao")

    lab_result = {
        'lab_result_id': lab_result_id,
        'appointment_id': appointment_id,
        'patient_id': patient_id,
        'test_type': test['test_type'],
        'parameter': test['parameter'],
        'value': result_value,
        'unit': test['unit'],
        'normal_range': test['normal_range'],
        'interpretation': interpretation,
        'test_date': test_date
    }
    lab_results.append(lab_result)
    lab_result_id += 1

df_lab_results = pd.DataFrame(lab_results)
df_lab_results.to_csv('./data1k/lab_results.csv', index=False)

print("Data generation completed successfully!")
print(f"Generated {num_patients} patients, {num_doctors} doctors, {num_records} vital signs, "
      f"{num_appointments} appointments, {len(diseases)} diseases, {len(treatments)} treatments, "
      f"{len(hospital_fees)} hospital fees, {len(prescriptions)} prescriptions, and {len(lab_results)} lab results.")