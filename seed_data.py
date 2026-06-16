import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from orgen.models import *
import datetime

print("🌱 بدء إنشاء البيانات...")

# ===== Ministry =====
if not Ministry.objects.exists():
    ministry = Ministry.objects.create(
        national_id='12345',
        name='وزارة الصحة والسكان',
        email='ministry@health.gov.eg',
        phone='0220000000',
    )
    ministry.set_password('ministry123')
    MinistryToken.objects.get_or_create(ministry=ministry)
    print("✅ وزارة تم إنشاؤها")
else:
    ministry = Ministry.objects.first()
    print("⚠️ وزارة موجودة بالفعل")

# ===== Hospitals =====
hospitals_data = [
    {
        'name': 'مستشفى القصر العيني',
        'city': 'القاهرة',
        'location': 'شارع القصر العيني، القاهرة',
        'license_number': 'LIC-001',
        'phone': '0223456789',
        'emergency_phone': '0223456790',
        'email': 'kasr@hospital.eg',
        'working_hours': '24/7',
        'hospital_type': 'حكومي',
        'password': 'hospital123',
    },
    {
        'name': 'مستشفى الشيخ زايد',
        'city': 'الجيزة',
        'location': 'مدينة الشيخ زايد، الجيزة',
        'license_number': 'LIC-002',
        'phone': '0238000000',
        'emergency_phone': '0238000001',
        'email': 'zayed@hospital.eg',
        'working_hours': '24/7',
        'hospital_type': 'حكومي',
        'password': 'hospital123',
    },
    {
        'name': 'مستشفى كليوباترا',
        'city': 'القاهرة',
        'location': 'مصر الجديدة، القاهرة',
        'license_number': 'LIC-003',
        'phone': '0224567890',
        'emergency_phone': '0224567891',
        'email': 'cleopatra@hospital.eg',
        'working_hours': '24/7',
        'hospital_type': 'خاص',
        'password': 'hospital123',
    },
]

hospitals = []
for h_data in hospitals_data:
    password = h_data.pop('password')
    hospital, created = Hospital.objects.get_or_create(
        email=h_data['email'],
        defaults={**h_data, 'ministry': ministry, 'status': 'نشط'}
    )
    if created:
        hospital.set_password(password)
        HospitalToken.objects.get_or_create(hospital=hospital)
        print(f"✅ مستشفى {hospital.name} تم إنشاؤه")
    hospitals.append(hospital)

# ===== Doctors =====
doctors_data = [
    {'name': 'أحمد محمد علي', 'specialty': 'جراحة الكلى', 'phone': '01001234567', 'hospital': hospitals[0]},
    {'name': 'سارة خالد حسن', 'specialty': 'جراحة الكبد', 'phone': '01002345678', 'hospital': hospitals[0]},
    {'name': 'محمود عبدالله', 'specialty': 'جراحة القلب', 'phone': '01003456789', 'hospital': hospitals[1]},
    {'name': 'نور الدين إبراهيم', 'specialty': 'جراحة الكلى', 'phone': '01004567890', 'hospital': hospitals[1]},
    {'name': 'هالة يوسف', 'specialty': 'جراحة الكبد', 'phone': '01005678901', 'hospital': hospitals[2]},
]

doctors = []
for d_data in doctors_data:
    doctor, created = Doctor.objects.get_or_create(
        name=d_data['name'],
        defaults=d_data
    )
    if created:
        print(f"✅ دكتور {doctor.name} تم إنشاؤه")
    doctors.append(doctor)

# ===== Chronic Diseases =====
diseases_names = ['السكري', 'ضغط الدم', 'الفشل الكلوي', 'تليف الكبد', 'أمراض القلب']
diseases = []
for name in diseases_names:
    disease, created = ChronicDisease.objects.get_or_create(name=name)
    diseases.append(disease)
print("✅ أمراض مزمنة تم إنشاؤها")

# ===== Patients =====
# patients_data = [
#     {
#         'national_id': '30101011234567',
#         'first_name': 'محمد',
#         'last_name': 'أحمد السيد',
#         'birthdate': datetime.date(1985, 3, 15),
#         'blood_type': 'A+',
#         'gender': 'ذكر',
#         'phone': '01011234567',
#         'email': 'mohamed.ahmed@email.com',
#         'city': 'القاهرة',
#         'medical_record_number': 'MR-001',
#         'height_cm': 175.0,
#         'weight_kg': 80.0,
#         'HLA_A_1': 'A2', 'HLA_A_2': 'A3',
#         'HLA_B_1': 'B7', 'HLA_B_2': 'B8',
#         'HLA_DR_1': 'DR1', 'HLA_DR_2': 'DR2',
#         'PRA': 15.0,
#         'CMV_status': True,
#         'EBV_status': False,
#         'hospital': hospitals[0],
#         'supervisor_doctor': doctors[0],
#         'organ': 'kidney_right',
#         'urgency_level': 'high',
#         'waitlist_time_days': 180,
#         'dialysis_duration_days': 90,
#     },
#     {
#         'national_id': '30205021234568',
#         'first_name': 'فاطمة',
#         'last_name': 'علي حسن',
#         'birthdate': datetime.date(1990, 7, 22),
#         'blood_type': 'B+',
#         'gender': 'انثي',
#         'phone': '01021234568',
#         'email': 'fatma.ali@email.com',
#         'city': 'الجيزة',
#         'medical_record_number': 'MR-002',
#         'height_cm': 160.0,
#         'weight_kg': 65.0,
#         'HLA_A_1': 'A1', 'HLA_A_2': 'A2',
#         'HLA_B_1': 'B5', 'HLA_B_2': 'B7',
#         'HLA_DR_1': 'DR3', 'HLA_DR_2': 'DR4',
#         'PRA': 25.0,
#         'CMV_status': False,
#         'EBV_status': True,
#         'hospital': hospitals[1],
#         'supervisor_doctor': doctors[1],
#         'organ': 'liver',
#         'urgency_level': 'critical',
#         'waitlist_time_days': 365,
#         'MELD_score': 28.5,
#     },
#     {
#         'national_id': '30308031234569',
#         'first_name': 'عمر',
#         'last_name': 'خالد محمود',
#         'birthdate': datetime.date(1978, 11, 5),
#         'blood_type': 'O+',
#         'gender': 'ذكر',
#         'phone': '01031234569',
#         'email': 'omar.khaled@email.com',
#         'city': 'الإسكندرية',
#         'medical_record_number': 'MR-003',
#         'height_cm': 180.0,
#         'weight_kg': 90.0,
#         'HLA_A_1': 'A3', 'HLA_A_2': 'A4',
#         'HLA_B_1': 'B6', 'HLA_B_2': 'B8',
#         'HLA_DR_1': 'DR2', 'HLA_DR_2': 'DR5',
#         'PRA': 10.0,
#         'CMV_status': True,
#         'EBV_status': True,
#         'hospital': hospitals[2],
#         'supervisor_doctor': doctors[2],
#         'organ': 'kidney_left',
#         'urgency_level': 'medium',
#         'waitlist_time_days': 90,
#         'dialysis_duration_days': 45,
#     },
# ]

# patients = []
# for p_data in patients_data:
#     organ               = p_data.pop('organ')
#     urgency_level       = p_data.pop('urgency_level', None)
#     waitlist_time_days  = p_data.pop('waitlist_time_days', None)
#     dialysis_duration   = p_data.pop('dialysis_duration_days', None)
#     MELD_score          = p_data.pop('MELD_score', None)

#     if User.objects.filter(national_id=p_data['national_id']).exists():
#         user = User.objects.get(national_id=p_data['national_id'])
#         print(f"⚠️ مريض {user.first_name} موجود بالفعل")
#     else:
#         user = User.objects.create(role='patient', status='جاهز', **p_data)
#         user.set_password(p_data['national_id'][-4:])
#         user.save()

#         PatientMedicalProfile.objects.create(
#             patient=user,
#             organ_needed=organ,
#             urgency_level=urgency_level,
#             waitlist_time_days=waitlist_time_days,
#             dialysis_duration_days=dialysis_duration,
#             MELD_score=MELD_score,
#         )

#         UserChronicDisease.objects.create(user=user, disease=diseases[0], severity='عالي')
#         UserChronicDisease.objects.create(user=user, disease=diseases[2], severity='متوسط')

#         Allergy.objects.create(user=user, name='البنسلين', severity='عالي')
#         Medicine.objects.create(user=user, name='سيكلوسبورين', frequency_per_day=2)

#         PatientPriority.objects.create(
#             patient=user,
#             score=70 if urgency_level == 'critical' else 40,
#             level='حرجة جداً' if urgency_level == 'critical' else 'اولوليه عاليه'
#         )

#         VitalSigns.objects.create(
#             user=user,
#             blood_pressure='120/80',
#             temperature_c=37.0,
#             heart_rate=80,
#             respiratory_rate=18,
#             oxygen_saturation=98.0
#         )

#         Alert.objects.create(
#             user=user,
#             message_title='مرحباً بك في النظام',
#             message='تم تسجيل حسابك بنجاح في نظام STODS',
#             alert_type='معلومة'
#         )

#         print(f"✅ مريض {user.first_name} {user.last_name} تم إنشاؤه")

#     patients.append(user)

# # ===== Donors =====
# donors_data = [
#     {
#         'national_id': '30401041234570',
#         'first_name': 'كريم',
#         'last_name': 'عبدالرحمن',
#         'birthdate': datetime.date(1992, 4, 10),
#         'blood_type': 'A+',
#         'gender': 'ذكر',
#         'phone': '01041234570',
#         'email': 'karim.abd@email.com',
#         'city': 'القاهرة',
#         'medical_record_number': 'MR-D001',
#         'height_cm': 178.0,
#         'weight_kg': 75.0,
#         'HLA_A_1': 'A2', 'HLA_A_2': 'A3',
#         'HLA_B_1': 'B7', 'HLA_B_2': 'B9',
#         'HLA_DR_1': 'DR1', 'HLA_DR_2': 'DR3',
#         'PRA': 5.0,
#         'CMV_status': False,
#         'EBV_status': False,
#         'hospital': hospitals[0],
#         'supervisor_doctor': doctors[0],
#         'organ': 'kidney_right',
#         'donation_type': 'living',
#         'organ_full_or_partial': 'full',
#         'kdpi_score': 15.0,
#         'donor_code': 'D00001',
#     },
#     {
#         'national_id': '30502051234571',
#         'first_name': 'منى',
#         'last_name': 'إبراهيم سعد',
#         'birthdate': datetime.date(1988, 9, 25),
#         'blood_type': 'B+',
#         'gender': 'انثي',
#         'phone': '01051234571',
#         'email': 'mona.ibrahim@email.com',
#         'city': 'الجيزة',
#         'medical_record_number': 'MR-D002',
#         'height_cm': 163.0,
#         'weight_kg': 60.0,
#         'HLA_A_1': 'A1', 'HLA_A_2': 'A2',
#         'HLA_B_1': 'B5', 'HLA_B_2': 'B7',
#         'HLA_DR_1': 'DR3', 'HLA_DR_2': 'DR5',
#         'PRA': 8.0,
#         'CMV_status': True,
#         'EBV_status': False,
#         'hospital': hospitals[1],
#         'supervisor_doctor': doctors[1],
#         'organ': 'liver',
#         'donation_type': 'living',
#         'organ_full_or_partial': 'lobe',
#         'donor_code': 'D00002',
#     },
#     {
#         'national_id': '30603061234572',
#         'first_name': 'يوسف',
#         'last_name': 'طارق نصر',
#         'birthdate': datetime.date(1995, 1, 30),
#         'blood_type': 'O+',
#         'gender': 'ذكر',
#         'phone': '01061234572',
#         'email': 'yousef.tarek@email.com',
#         'city': 'الإسكندرية',
#         'medical_record_number': 'MR-D003',
#         'height_cm': 182.0,
#         'weight_kg': 85.0,
#         'HLA_A_1': 'A3', 'HLA_A_2': 'A4',
#         'HLA_B_1': 'B6', 'HLA_B_2': 'B8',
#         'HLA_DR_1': 'DR2', 'HLA_DR_2': 'DR4',
#         'PRA': 3.0,
#         'CMV_status': False,
#         'EBV_status': True,
#         'hospital': hospitals[2],
#         'supervisor_doctor': doctors[2],
#         'organ': 'kidney_left',
#         'donation_type': 'living',
#         'organ_full_or_partial': 'full',
#         'kdpi_score': 12.0,
#         'donor_code': 'D00003',
#     },
# ]

# donors = []
# for d_data in donors_data:
#     organ               = d_data.pop('organ')
#     donation_type       = d_data.pop('donation_type')
#     organ_full_or_partial = d_data.pop('organ_full_or_partial')
#     kdpi_score          = d_data.pop('kdpi_score', None)
#     donor_code          = d_data.pop('donor_code')

#     if User.objects.filter(national_id=d_data['national_id']).exists():
#         user = User.objects.get(national_id=d_data['national_id'])
#         print(f"⚠️ متبرع {user.first_name} موجود بالفعل")
#     else:
#         user = User.objects.create(role='donor', status='جاهز', **d_data)
#         user.set_password(d_data['national_id'][-4:])
#         user.save()

#         DonorMedicalProfile.objects.create(
#             donor=user,
#             organ_available=organ,
#             donation_type=donation_type,
#             organ_full_or_partial=organ_full_or_partial,
#             kdpi_score=kdpi_score,
#             donor_code=donor_code,
#         )

#         DonorHealthStatus.objects.create(
#             donor=user,
#             status='ممتازة',
#             notes='المتبرع في صحة جيدة جداً'
#         )

#         UserChronicDisease.objects.create(user=user, disease=diseases[1], severity='منخفض')
#         Allergy.objects.create(user=user, name='الأسبرين', severity='متوسط')
#         Medicine.objects.create(user=user, name='فيتامين د', frequency_per_day=1)

#         VitalSigns.objects.create(
#             user=user,
#             blood_pressure='115/75',
#             temperature_c=36.8,
#             heart_rate=72,
#             respiratory_rate=16,
#             oxygen_saturation=99.0
#         )

#         Alert.objects.create(
#             user=user,
#             message_title='مرحباً بك في النظام',
#             message='تم تسجيل حسابك كمتبرع بنجاح في نظام STODS',
#             alert_type='معلومة'
#         )

#         print(f"✅ متبرع {user.first_name} {user.last_name} تم إنشاؤه")

#     donors.append(user)

# ===== Organ Matching =====
# matching_data = [
#     {'patient': patients[0], 'donor': donors[0], 'organ_type': 'kidney_right'},
#     {'patient': patients[1], 'donor': donors[1], 'organ_type': 'liver'},
#     {'patient': patients[2], 'donor': donors[2], 'organ_type': 'kidney_left'},
# ]

# matches = []
# for m_data in matching_data:
#     patient = m_data['patient']
#     donor   = m_data['donor']
#     if OrganMatching.objects.filter(patient=patient, donor=donor).exists():
#         match = OrganMatching.objects.get(patient=patient, donor=donor)
#         print(f"⚠️ مطابقة موجودة بالفعل")
#     else:
#         result = OrganMatching.calculate_match(patient, donor)
#         match  = OrganMatching.objects.create(
#             patient=patient,
#             donor=donor,
#             organ_type=m_data['organ_type'],
#             match_percentage=result['match_percentage'],
#             ai_result=result['ai_result'],
#             status='تحت المطابقه'
#         )
#         print(f"✅ مطابقة {patient.first_name} ↔ {donor.first_name} تم إنشاؤها ({result['match_percentage']}%)")
#     matches.append(match)

# ===== Surgeries =====
# surgeries_data = [
#     {
#         'surgery_number': 'SUR-001',
#         'surgery_name': 'زراعة كلية يمنى',
#         'department': 'كلى',
#         'hospital': hospitals[0],
#         'doctor': doctors[0],
#         'scheduled_date': datetime.date(2026, 7, 15),
#         'scheduled_time': datetime.time(9, 0),
#         'status': 'مجدولة',
#         'duration': 180,
#         'operation_room': 'غرفة عمليات 1',
#     },
#     {
#         'surgery_number': 'SUR-002',
#         'organ_matching': matches[1],
#         'surgery_name': 'زراعة كبد',
#         'department': 'كبد',
#         'hospital': hospitals[1],
#         'doctor': doctors[1],
#         'scheduled_date': datetime.date(2026, 7, 20),
#         'scheduled_time': datetime.time(8, 0),
#         'status': 'مجدولة',
#         'duration': 360,
#         'operation_room': 'غرفة عمليات 2',
#     },
# ]

# surgeries = []
# for s_data in surgeries_data:
#     if Surgery.objects.filter(surgery_number=s_data['surgery_number']).exists():
#         surgery = Surgery.objects.get(surgery_number=s_data['surgery_number'])
#         print(f"⚠️ عملية {surgery.surgery_number} موجودة بالفعل")
#     else:
#         surgery = Surgery.objects.create(**s_data)
#         print(f"✅ عملية {surgery.surgery_number} تم إنشاؤها")
#     surgeries.append(surgery)

# ===== Hospital Alerts =====
for hospital in hospitals:
    if not AlertHospital.objects.filter(hospital=hospital).exists():
        AlertHospital.objects.create(
            hospital=hospital,
            message_title='تنبيه جديد',
            message=f'مرحباً بمستشفى {hospital.name} في نظام STODS',
            alert_type='معلومة'
        )
        print(f"✅ تنبيه مستشفى {hospital.name} تم إنشاؤه")

# ===== Ministry Alert =====
if not MinistryAlert.objects.exists():
    MinistryAlert.objects.create(
        ministry=ministry,
        sender_hospital=hospitals[0],
        message_title='تقرير شهري',
        message='تم إرسال التقرير الشهري لعمليات زراعة الأعضاء',
        alert_type='تحذير',
        ALERT_Status='قيد التحقيق',
        priority='متوسطة',
    )
    print("✅ تنبيه الوزارة تم إنشاؤه")

print("\n🎉 تم إنشاء كل البيانات بنجاح!")
print(f"   وزارة: 1")
print(f"   مستشفيات: {Hospital.objects.count()}")
print(f"   أطباء: {Doctor.objects.count()}")
print(f"   مرضى: {User.objects.filter(role='patient').count()}")
print(f"   متبرعين: {User.objects.filter(role='donor').count()}")
print(f"   مطابقات: {OrganMatching.objects.count()}")
print(f"   عمليات: {Surgery.objects.count()}")