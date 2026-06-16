import os
import django
import json
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from orgen.models import *

print("🌱 بدء إضافة الـ recipients من الـ JSON...")

hospital = Hospital.objects.first()
doctor = Doctor.objects.first()

if not hospital:
    print("❌ مفيش مستشفى في الداتابيز!")
    exit()

with open("transplant_2000_mixed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

recipients = data.get("recipients", [])
print(f"📋 عدد الـ recipients: {len(recipients)}")

created = 0
skipped = 0

for i, r in enumerate(recipients):
    recipient_id = r.get("recipient_id")

    if PatientMedicalProfile.objects.filter(recipient_id=recipient_id).exists():
        skipped += 1
        continue

    age = r.get("age", 30)
    birth_year = date.today().year - age
    birthdate = date(birth_year, random.randint(1, 12), random.randint(1, 28))

    blood_type = r.get("blood_type", "O")
    if blood_type not in ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]:
        blood_type = blood_type + "+"

    sex = r.get("sex", "M")
    gender = "ذكر" if sex in ["M", "Male", "male"] else "انثي"
    national_id = f"8{str(i+1).zfill(13)}"
    try:
        user = User.objects.create(
            national_id=national_id,
            first_name="مريض",
            last_name=recipient_id,
            role="patient",
            status="جاهز",
            birthdate=birthdate,
            blood_type=blood_type,
            gender=gender,
            height_cm=r.get("height_cm") or 170.0,
            weight_kg=r.get("weight_kg") or 70.0,
            HLA_A_1=r.get("HLA_A_1", ""),
            HLA_A_2=r.get("HLA_A_2", ""),
            HLA_B_1=r.get("HLA_B_1", ""),
            HLA_B_2=r.get("HLA_B_2", ""),
            HLA_DR_1=r.get("HLA_DR_1", ""),
            HLA_DR_2=r.get("HLA_DR_2", ""),
            PRA=float(r.get("PRA", 0)),
            CMV_status=r.get("CMV_status") == "positive",
            EBV_status=r.get("EBV_status") == "positive",
            medical_record_number=recipient_id,
            hospital=hospital,
            supervisor_doctor=doctor,
        )
        user.set_password(national_id[-4:])
        user.save()

        # organ_needed = r.get("organ_needed", "kidney_left")
        organ_mapping = {
            "lung": "lung_left",
            "lung_left": "lung_left",
            "lung_right": "lung_right",
            "lung_lobe": "lung_lobe",
        }
        organ_needed_raw = r.get("organ_needed", "kidney_left")
        organ_needed = organ_mapping.get(organ_needed_raw, organ_needed_raw)
        dialysis = r.get("dialysis_duration_days")
        meld = r.get("MELD_score")
        lung = r.get("lung_severity_score")

        LUNG_ORGANS = ["lung_right", "lung_left", "lung_lobe", "lung"]

        PatientMedicalProfile.objects.create(
            patient=user,
            organ_needed=organ_needed,
            recipient_id=recipient_id,
            urgency_level=r.get("urgency_level", "medium"),
            waitlist_time_days=r.get("waitlist_time_days", 0),
            dialysis_duration_days=dialysis if dialysis and dialysis > 0 and organ_needed in ["kidney", "kidney_right", "kidney_left"] else None,            MELD_score=meld if meld and meld > 0 else None,
            lung_severity_score=lung if lung and lung > 0 and organ_needed in LUNG_ORGANS else None,
        )

        created += 1
        if created % 100 == 0:
            print(f"✅ تم إضافة {created} مريض...")

    except Exception as e:
        print(f"❌ خطأ في {recipient_id}: {e}")
        skipped += 1
        continue

print(f"\n🎉 تم!")
print(f"   ✅ اتضافوا: {created}")
print(f"   ⚠️ اتتخطّوا: {skipped}")
print(f"   📊 إجمالي المرضى: {User.objects.filter(role='patient').count()}")