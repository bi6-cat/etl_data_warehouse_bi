import shutil

# Đường dẫn đến file gốc và file đích
def cop_csv(source_file, destination_file):

    # Mở file A.csv và đọc nội dung
    chunk_size = 1024 * 1024  # Đọc theo khối 1MB

    with open(source_file, 'r', encoding='utf-8') as src, open(destination_file, 'w', encoding='utf-8') as dest:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dest.write(chunk)

    print(f"Đã sao chép nội dung từ {source_file} sang {destination_file}")


list_path_file = [
    'dataset/appointments.csv',
    'dataset/doctors.csv',
    'dataset/patients.csv',
    'dataset/check.csv',
    'dataset/diseases.csv',
    'dataset/lab_results.csv',
    'dataset/prescriptions.csv',
    'dataset/treatments.csv',
    'dataset/vital_signs.csv',
    'dataset/hospital_fee.csv',
]

des_path_file = [
    'dataset/process_csv/appointments.csv',
    'dataset/process_csv/doctors.csv',
    'dataset/process_csv/patients.csv',
    'dataset/process_csv/check.csv',
    'dataset/process_csv/diseases.csv',
    'dataset/process_csv/lab_results.csv',
    'dataset/process_csv/prescriptions.csv',
    'dataset/process_csv/treatments.csv',
    'dataset/process_csv/vital_signs.csv',
    'dataset/process_csv/hospital_fee.csv',
]

for i in range(len(list_path_file)):
    cop_csv(list_path_file[i], des_path_file[i])
