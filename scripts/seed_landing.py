import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')

import django
django.setup()

from apps.dashboard.models import *

# Site Settings
if not SiteSetting.objects.exists():
    SiteSetting.objects.create()
    print("SiteSetting created")
else:
    print("SiteSetting already exists")

# Hero Section
if not HeroSection.objects.exists():
    HeroSection.objects.create()
    print("HeroSection created")
else:
    print("HeroSection already exists")

# Why Choose Items
if not WhyChooseItem.objects.exists():
    items = [
        ('bi bi-person-badge-fill', 'Qualified Professionals', 'Our team of experienced doctors and specialists deliver expert care.'),
        ('bi bi-cash-coin', 'Affordable Healthcare', 'Quality medical services at prices accessible to all members of our community.'),
        ('bi bi-motherboard-fill', 'Modern Equipment', 'State-of-the-art diagnostic and treatment equipment for accurate results.'),
        ('bi bi-heart-fill', 'Patient-Centered Care', 'Your health and comfort are our top priorities, every step of the way.'),
        ('bi bi-lightning-fill', 'Fast Service Delivery', 'Minimal waiting times and efficient service to get you treated quickly.'),
        ('bi bi-shield-check', 'Safe & Clean Environment', 'We maintain the highest standards of hygiene and infection control.'),
    ]
    for i, (icon, title, desc) in enumerate(items):
        WhyChooseItem.objects.create(icon=icon, title=title, description=desc, order=i)
    print("WhyChooseItems created")
else:
    print("WhyChooseItems already exist")

# Service Categories with Items
if not ServiceCategory.objects.exists():
    cats = [
        ('A. OPD Services', 'bi bi-hospital', ['General Consultation', 'Minor Procedures', 'Medical Reviews', 'Referrals']),
        ('B. Under-Five Clinic', 'bi bi-people', ['Growth Monitoring', 'Child Health Assessment', 'Immunization', 'Nutrition Monitoring']),
        ('C. Antenatal Care (ANC)', 'bi bi-flower1', ['Pregnancy Monitoring', 'Maternal Health Assessment', 'Health Education', 'Birth Preparedness']),
        ('D. Family Planning', 'bi bi-chat-heart-fill', ['Counseling', 'Contraceptive Services', 'Reproductive Health Education']),
        ('E. Laboratory Services', 'bi bi-microscope', ['Blood Tests', 'Urine Tests', 'Diagnostic Screening']),
        ('F. Pharmacy Services', 'bi bi-capsule', ['Prescription Dispensing', 'Medication Counseling', 'Stock Management']),
    ]
    for ci, (name, icon, items) in enumerate(cats):
        cat = ServiceCategory.objects.create(name=name, icon=icon, order=ci)
        for ii, item_text in enumerate(items):
            ServiceItem.objects.create(category=cat, text=item_text, order=ii)
    print("ServiceCategories created")
else:
    print("ServiceCategories already exist")

# Departments
if not Department.objects.exists():
    depts = [
        ('OPD', 'bi bi-hospital'),
        ('Maternal Health', 'bi bi-flower1'),
        ('Child Health', 'bi bi-people'),
        ('Family Planning', 'bi bi-chat-heart-fill'),
        ('Laboratory', 'bi bi-microscope'),
        ('Pharmacy', 'bi bi-capsule'),
    ]
    for i, (name, icon) in enumerate(depts):
        Department.objects.create(name=name, icon=icon, order=i)
    print("Departments created")
else:
    print("Departments already exist")

# Statistics
if not Statistic.objects.exists():
    stats = [
        ('Patients Served', 15000, 'bi bi-people-fill'),
        ('Appointments Completed', 45000, 'bi bi-calendar-check-fill'),
        ('Deliveries Supported', 5000, 'bi bi-heart-fill'),
        ('Children Vaccinated', 12000, 'bi bi-shield-plus'),
    ]
    for i, (label, value, icon) in enumerate(stats):
        Statistic.objects.create(label=label, value=value, icon=icon, order=i)
    print("Statistics created")
else:
    print("Statistics already exist")

# Testimonials
if not Testimonial.objects.exists():
    tests = [
        ('Jane Mwangi', 'The staff was incredibly professional and caring. I received excellent treatment and follow-up care.', 'OPD Patient', 'primary'),
        ('Alice Wanjiku', 'The ANC program at this clinic is amazing. I felt supported throughout my pregnancy journey.', 'ANC Patient', 'success'),
        ('Peter Kamau', 'My children receive all their immunizations here. The under-five clinic is very child-friendly.', 'Parent', 'info'),
        ('Sarah Njoroge', 'Affordable and quality healthcare. The pharmacy always has the medicines I need and the staff are helpful.', 'Pharmacy Patient', 'warning'),
    ]
    for i, (name, content, designation, color) in enumerate(tests):
        Testimonial.objects.create(patient_name=name, content=content, designation=designation, avatar_color=color, order=i)
    print("Testimonials created")
else:
    print("Testimonials already exist")

# Contact Info
if not ContactInfo.objects.exists():
    contacts = [
        ('phone', 'Phone', 'bi bi-telephone-fill', '+265 999 401 674', '+254 700 100 300'),
        ('email', 'Email', 'bi bi-envelope-fill', 'info@hopeclinic.co.ke', 'admin@hopeclinic.co.ke'),
        ('address', 'Address', 'bi bi-geo-alt-fill', 'Chinamwali, Zomba - Malawi', ''),
        ('hours', 'Working Hours', 'bi bi-clock-fill', 'Mon - Sat: 7:00 AM - 8:00 PM', 'Sunday: Closed (Emergencies Only)'),
    ]
    for i, (typ, label, icon, val, val2) in enumerate(contacts):
        ContactInfo.objects.create(info_type=typ, label=label, icon=icon, value=val, value_2=val2, order=i)
    print("ContactInfos created")
else:
    print("ContactInfos already exist")

# Health Articles
if not HealthArticle.objects.exists():
    articles = [
        ('bi bi-heart-pulse-fill', 'Importance of Antenatal Care', 'Regular ANC visits ensure healthy pregnancy, early detection of complications, and better outcomes for mother and baby.'),
        ('bi bi-shield-plus', 'Child Immunization Benefits', 'Vaccines protect children from life-threatening diseases. Stay up to date with the national immunization schedule.'),
        ('bi bi-chat-heart-fill', 'Family Planning Awareness', 'Access to family planning services empowers families to make informed decisions about spacing and number of children.'),
        ('bi bi-basket-fill', 'Nutrition Tips for Families', 'A balanced diet rich in fruits, vegetables, proteins, and whole grains supports growth, immunity, and overall health.'),
        ('bi bi-virus', 'Preventing Common Diseases', 'Hand washing, vaccination, safe water, and mosquito control are simple ways to prevent many infectious diseases.'),
        ('bi bi-activity', 'Chronic Disease Management', 'Regular check-ups, medication adherence, and lifestyle changes help manage hypertension, diabetes, and other chronic conditions.'),
    ]
    for icon, title, summary in articles:
        HealthArticle.objects.create(icon=icon, title=title, summary=summary, content=summary)
    print("HealthArticles created")
else:
    print("HealthArticles already exist")

print("All seed data complete!")
