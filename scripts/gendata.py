from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker("vi_VN")   # Set locale to Vietnamese

num_patients = 1000000  # 1 triệu bệnh nhân
num_doctors = 200000  # 20 ngàn bác sĩ
num_records = num_patients * 2  # 2 triệu chỉ số vital signs
num_appointments = num_patients * 3 # 3 triệu cuộc hẹn
num_lab_results = num_patients * 2 # 2 triệu kết quả xét nghiệm

# Tạo thư mục để lưu trữ dữ liệu
import os
if not os.path.exists('./data1m'):
    os.makedirs('./data1m')
    
# Patients (Bệnh nhân)
patients = []
for i in range(1, num_patients+1):
    patient = {
        'patient_id': i,
        'name': fake.name(),
        'gender': random.choice(['Nam', 'Nữ']),
        'dob': fake.date_of_birth(minimum_age=0, maximum_age=90).strftime('%Y-%m-%d'),
        'address': fake.address().replace("\n", ", "),
        'phone': fake.phone_number(),
        'email': fake.email()
    }
    patients.append(patient)

df_patients = pd.DataFrame(patients)
df_patients.to_csv('./data1m/patients.csv', index=False)
patient_phone_map = {p['patient_id']: p['phone'] for p in patients}



# Doctors (Bác sĩ)
specialties = [
    "Tim mạch", "Nội tiết", "Da liễu", "Thần kinh", "Ung bướu", "Nhi khoa", "Tiêu hóa",
    "Sản phụ khoa", "Tâm thần", "Hô hấp", "Chấn thương chỉnh hình", "Tổng quát", "Tai Mũi Họng",
    "Mắt", "Tiết niệu", "Cơ xương khớp", "Miễn dịch"
]
doctors = []
for i in range(1, num_doctors+1):
    doctor = {
        'doctor_id': i,
        'name': fake.name(),
        'last_name': fake.last_name(),
        'specialization': random.choice(specialties),
        'phone': fake.phone_number(),
        'email': fake.email()
    }
    doctors.append(doctor)

df_doctors = pd.DataFrame(doctors)
df_doctors.to_csv('./data1m/doctors.csv', index=False)



# Appointments (Nâng cấp)
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

appointments = []
for i in range(1, num_appointments + 1):
    pat_id = random.randint(1, num_patients)
    doc_id = random.randint(1, num_doctors)
    date = datetime.now() - timedelta(days=random.randint(0, 365))
    start_time = datetime(date.year, date.month, date.day, random.randint(7, 17), random.randint(0, 59))
    end_time = start_time + timedelta(minutes=random.randint(30, 90))  # Tính thời gian kết thúc cuộc hẹn
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
df_appointments.to_csv('./data1m/appointments.csv', index=False)



# Các chỉ số vital signs
vital_signs = []
for vs_id in range(1, num_records+1):
    pat_id = random.randint(1, num_patients)
    
    # Tạo các chỉ số vital signs
    blood_pressure = f"{random.randint(90, 180)}/{random.randint(60, 120)}"  # Huyết áp có thể cao
    heart_rate = random.randint(50, 120)  # Nhịp tim có thể thấp hoặc cao
    respiratory_rate = random.randint(10, 30)  # Nhịp thở có thể thấp hoặc cao
    temperature = round(random.uniform(35.0, 40.0), 1)  # Nhiệt độ cơ thể có thể cao hoặc thấp
    spO2 = random.randint(90, 100)  # Oxygen saturation, từ 90% đến 100%
    blood_sugar = random.randint(70, 250)  # Mức đường huyết (mg/dL)
    
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
df_vitals.to_csv('./data1m/vital_signs.csv', index=False)



# Bệnh án
benhly = [
    # Tim mạch
    "Tăng huyết áp", "Bệnh tim mạch", "Đột quỵ", "Loạn nhịp tim", "Suy tim",
    # Tiểu đường
    "Tiểu đường tuýp 1", "Tiểu đường tuýp 2",
    # Hô hấp
    "Hen suyễn", "Viêm phổi", "Bệnh phổi tắc nghẽn mạn tính (COPD)",
    # Tiêu hóa
    "Viêm loét dạ dày", "Bệnh gan", "Viêm đại tràng", "Hội chứng ruột kích thích",
    # Thần kinh
    "Trầm cảm", "Rối loạn lo âu", "Chấn thương sọ não", "Bệnh Alzheimer",
    # Các bệnh khác
    "Ung thư", "Cảm cúm", "Viêm gan B", "Loãng xương", "Béo phì", "Thiếu máu", "COVID-19"
]

# Bổ sung các bệnh lý hiếm gặp hơn
benhly += [
    "Bệnh Parkinson", "Lupus ban đỏ", "Viêm khớp dạng thấp", "Bệnh Crohn", "HIV/AIDS", 
    "Xơ gan", "Sởi", "Cúm gia cầm", "Sốt xuất huyết", "Bệnh tự miễn", "Thalassemia"
]

diseases = []
d_id = 1
for pat in range(1, num_patients+1):
    # Mỗi bệnh nhân có thể mắc từ 0 đến 3 bệnh
    num_diseases = random.randint(0, 3)
    # Đảm bảo không tạo trùng bệnh cho một bệnh nhân
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
df_diseases.to_csv('./data1m/diseases.csv', index=False)


# Treatments
treatments = []
t_id = 1
for dis in diseases:
    disease_name = dis['disease_name']
    treatment_options = []

    # Cấu hình điều trị theo từng bệnh lý
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
    else :
        treatment_options = ["Điều trị bệnh lý", "Dùng thuốc", "Tư vấn dinh dưỡng", "Tập luyện phục hồi", "Chế độ ăn kiêng", "Phẫu thuật"]
    # Lựa chọn điều trị cho từng bệnh
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
df_treatments.to_csv('./data1m/treatments.csv', index=False)



# Hospital Fees
service_types = [
    {"type": "Khám tổng quát", "min": 100, "max": 300},
    {"type": "Khám nội tiết", "min": 150, "max": 350},
    {"type": "Khám tim mạch", "min": 200, "max": 400},
    {"type": "Khám da liễu", "min": 120, "max": 250},
    {"type": "Khám tiêu hóa", "min": 150, "max": 300},
    {"type": "Khám hô hấp", "min": 140, "max": 280},
    {"type": "Khám thần kinh", "min": 180, "max": 350},
    {"type": "Khám sản phụ khoa", "min": 150, "max": 350},
    {"type": "Khám nhi khoa", "min": 100, "max": 250},
    {"type": "Khám tai mũi họng", "min": 120, "max": 250},

    {"type": "Xét nghiệm máu", "min": 80, "max": 150},
    {"type": "Xét nghiệm nước tiểu", "min": 70, "max": 120},
    {"type": "Xét nghiệm chức năng gan", "min": 100, "max": 200},
    {"type": "Xét nghiệm chức năng thận", "min": 100, "max": 200},
    {"type": "Xét nghiệm mỡ máu", "min": 100, "max": 180},
    {"type": "Xét nghiệm đường huyết", "min": 70, "max": 150},
    {"type": "Xét nghiệm viêm gan", "min": 120, "max": 220},
    {"type": "Xét nghiệm đông máu", "min": 100, "max": 200},

    {"type": "Chụp X-quang", "min": 150, "max": 300},
    {"type": "Chụp CT Scan", "min": 500, "max": 1200},
    {"type": "Chụp MRI", "min": 800, "max": 2000},
    {"type": "Siêu âm bụng tổng quát", "min": 120, "max": 250},
    {"type": "Siêu âm tim", "min": 200, "max": 400},
    {"type": "Siêu âm tuyến giáp", "min": 150, "max": 300},

    {"type": "Nội soi dạ dày", "min": 600, "max": 1200},
    {"type": "Nội soi đại tràng", "min": 700, "max": 1500},
    {"type": "Điện tim (ECG)", "min": 150, "max": 350},
    {"type": "Điện não đồ (EEG)", "min": 200, "max": 500},
    {"type": "Đo loãng xương", "min": 250, "max": 500},

    {"type": "Tiêm chủng", "min": 100, "max": 300},
    {"type": "Chăm sóc vết thương", "min": 100, "max": 250},
    {"type": "Thay băng", "min": 50, "max": 150},
    {"type": "Truyền dịch", "min": 200, "max": 400},
    {"type": "Cắt chỉ", "min": 60, "max": 120},

    {"type": "Phẫu thuật nhỏ", "min": 1000, "max": 3000},
    {"type": "Nhập viện", "min": 500, "max": 3000},
    {"type": "Lưu viện ban ngày", "min": 300, "max": 800},
    {"type": "Thuốc men", "min": 50, "max": 400},

    {"type": "Tư vấn chuyên khoa", "min": 200, "max": 500},
    {"type": "Tư vấn dinh dưỡng", "min": 150, "max": 350},
    {"type": "Tư vấn tâm lý", "min": 250, "max": 600},
    {"type": "Vật lý trị liệu", "min": 200, "max": 600},
    {"type": "Khám lại", "min": 50, "max": 150}
]

hospital_fees = []
fee_id = 1

for appt in appointments:
    num_services = random.randint(1, 3)
    used_services = random.sample(service_types, num_services)

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
df_fees.to_csv('./data1m/hospital_fee.csv', index=False)


# Prescriptions
medication_info = [
    # Giảm đau - Hạ sốt
    {"name": "Paracetamol", "form": "viên nén", "dosage_mg": [500]},
    {"name": "Ibuprofen", "form": "viên nén", "dosage_mg": [200, 400]},
    {"name": "Diclofenac", "form": "viên nén", "dosage_mg": [25, 50]},
    {"name": "Naproxen", "form": "viên nén", "dosage_mg": [250, 500]},

    # Kháng sinh
    {"name": "Amoxicillin", "form": "viên nang", "dosage_mg": [250, 500]},
    {"name": "Ciprofloxacin", "form": "viên nén", "dosage_mg": [250, 500]},
    {"name": "Azithromycin", "form": "viên nén", "dosage_mg": [250, 500]},
    {"name": "Cefuroxime", "form": "viên nén", "dosage_mg": [250, 500]},
    {"name": "Doxycycline", "form": "viên nang", "dosage_mg": [100]},
    {"name": "Clindamycin", "form": "viên nang", "dosage_mg": [150, 300]},

    # Tiểu đường
    {"name": "Metformin", "form": "viên nén", "dosage_mg": [500, 850]},
    {"name": "Gliclazide", "form": "viên nén", "dosage_mg": [30, 60]},
    {"name": "Insulin", "form": "dung dịch tiêm", "dosage_mg": [10, 20, 30]},  # IU thay vì mg, nhưng mô phỏng như mg

    # Cao huyết áp & tim mạch
    {"name": "Lisinopril", "form": "viên nén", "dosage_mg": [10, 20]},
    {"name": "Amlodipine", "form": "viên nén", "dosage_mg": [5, 10]},
    {"name": "Losartan", "form": "viên nén", "dosage_mg": [50]},
    {"name": "Atorvastatin", "form": "viên nén", "dosage_mg": [10, 20]},
    {"name": "Simvastatin", "form": "viên nén", "dosage_mg": [10, 20]},

    # Dạ dày
    {"name": "Omeprazole", "form": "viên nang", "dosage_mg": [20]},
    {"name": "Pantoprazole", "form": "viên nén", "dosage_mg": [20, 40]},
    {"name": "Ranitidine", "form": "viên nén", "dosage_mg": [150, 300]},

    # Hô hấp, dị ứng
    {"name": "Salbutamol", "form": "ống hít", "dosage_mg": [100]},  # micrograms nhưng mô phỏng mg
    {"name": "Cetirizine", "form": "viên nén", "dosage_mg": [10]},
    {"name": "Loratadine", "form": "viên nén", "dosage_mg": [10]},
    {"name": "Montelukast", "form": "viên nén", "dosage_mg": [10]},

    # Trầm cảm - tâm thần
    {"name": "Sertraline", "form": "viên nén", "dosage_mg": [50, 100]},
    {"name": "Amitriptyline", "form": "viên nén", "dosage_mg": [10, 25]},
    {"name": "Diazepam", "form": "viên nén", "dosage_mg": [5, 10]},

    # Khác
    {"name": "Vitamin C", "form": "viên sủi", "dosage_mg": [500, 1000]},
    {"name": "Calcium carbonate", "form": "viên nhai", "dosage_mg": [500]}
]

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
    for _ in range(random.randint(0, 2)):
        med = random.choice(medication_info)
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
df_pres.to_csv('./data1m/prescriptions.csv', index=False)


# Lab Results
lab_tests = [
    {
        "test_type": "Máu", "parameter": "Hemoglobin", "unit": "g/dL", "normal_range": "13.8-17.2",
        "min_val": 10, "max_val": 18
    },
    {
        "test_type": "Máu", "parameter": "Glucose", "unit": "mg/dL", "normal_range": "70-99",
        "min_val": 60, "max_val": 200
    },
    {
        "test_type": "Nước tiểu", "parameter": "pH", "unit": "", "normal_range": "4.6-8.0",
        "min_val": 4.0, "max_val": 9.0
    },
    {
        "test_type": "X-quang", "parameter": "X-quang phổi", "unit": "", "normal_range": "Không phát hiện bất thường",
        "result_texts": ["Không phát hiện bất thường", "Có dấu hiệu viêm", "Nốt bất thường", "Tăng đậm độ mô mềm"]
    },
    {
        "test_type": "MRI", "parameter": "MRI não", "unit": "", "normal_range": "Không có bất thường",
        "result_texts": ["Không có bất thường", "Khối u nhỏ vùng trán", "Teo não nhẹ", "Viêm màng não"]
    },
    {
        "test_type": "Siêu âm", "parameter": "Siêu âm bụng", "unit": "", "normal_range": "Bình thường",
        "result_texts": ["Gan to nhẹ", "Sỏi túi mật", "Bình thường", "Dịch ổ bụng ít"]
    }
]

lab_results = []
lab_result_id = 1

for _ in range(num_lab_results):
    test = random.choice(lab_tests)
    appt = random.choice(appointments)  # Dựa trên danh sách appointments đã có
    patient_id = appt['patient_id']
    appointment_id = appt['appointment_id']
    test_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')

    if 'result_texts' in test:
        result_value = random.choice(test['result_texts'])
        interpretation = "Bình thường" if result_value in ["Không phát hiện bất thường", "Bình thường", "Không có bất thường"] else "Bất thường"
    else:
        value = round(random.uniform(test['min_val'], test['max_val']), 1)
        result_value = value
        # Xác định bất thường
        normal_range_parts = test['normal_range'].split('-')
        lower = float(normal_range_parts[0])
        upper = float(normal_range_parts[1])
        if value < lower:
            interpretation = "Thấp"
        elif value > upper:
            interpretation = "Cao"
        else:
            interpretation = "Bình thường"

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
df_lab_results.to_csv('./data1m/lab_results.csv', index=False)

print("Data generation completed successfully!")
print(f"Generated {num_patients} patients, {num_doctors} doctors, {num_records} vital signs, {num_appointments} appointments, {len(diseases)} diseases, {len(treatments)} treatments, {len(hospital_fees)} hospital fees, {len(prescriptions)} prescriptions, and {len(lab_results)} lab results.")