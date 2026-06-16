import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from orgen.models import User
from orgen.ai_matching import trigger_ai_matching

donors = User.objects.filter(role='donor')
print(f"عدد المتبرعين: {donors.count()}")

for donor in donors:
    print(f"\n🔄 جاري معالجة المتبرع: {donor.first_name} {donor.last_name}")
    result = trigger_ai_matching(donor)
    if result:
        print(f"✅ تم! عدد المتطابقين: {len(result.get('top_matches', []))}")
    else:
        print("❌ فشل أو مفيش مرضى بنفس العضو")

from orgen.models import OrganMatching
print(f"\n🎉 إجمالي المطابقات في الداتابيز: {OrganMatching.objects.count()}")