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
        ('A. OPD Services', 'bi bi-hospital', [
            'General Consultation',
            'Specialist Referrals',
            'Medical Reviews',
            'Minor Outpatient Procedures',
        ]),
        ('B. Antenatal Care (ANC)', 'bi bi-flower1', [
            'Pregnancy Monitoring',
            'Ultrasound Scans',
            'Birth Preparedness',
            'Maternal Nutrition & Health Education',
        ]),
        ('C. Postnatal Care (PNC)', 'bi bi-flower2', [
            'Post-delivery Checkups',
            'Newborn Care',
            'Breastfeeding Support',
            'Maternal Recovery Monitoring',
        ]),
        ('D. Under-Five Clinic', 'bi bi-people', [
            'Growth & Developmental Monitoring',
            'Childhood Immunization',
            'Nutrition Assessment',
            'Common Childhood Illness Treatment',
        ]),
        ('E. Family Planning', 'bi bi-chat-heart-fill', [
            'Contraceptive Counseling',
            'Contraceptive Methods & Provision',
            'Reproductive Health Education',
            'Infertility Support & Referral',
        ]),
        ('F. Maternity & Delivery', 'bi bi-gender-female', [
            'Normal Vaginal Delivery',
            'Caesarean Section',
            'Emergency Obstetric Care',
            'Neonatal Resuscitation',
        ]),
        ('G. Immunization & Vaccination', 'bi bi-shield-plus', [
            'Expanded Programme on Immunization (EPI)',
            'Adult & Travel Vaccines',
            'COVID-19 Vaccination',
            'HPV Vaccination',
        ]),
        ('H. HIV / AIDS Services', 'bi bi-droplet-half', [
            'HIV Testing & Counseling (HTS)',
            'Antiretroviral Therapy (ART)',
            'Prevention of Mother-to-Child Transmission (PMTCT)',
            'Pre-Exposure Prophylaxis (PrEP)',
        ]),
        ('I. Tuberculosis (TB) Services', 'bi bi-lungs', [
            'TB Screening & Diagnosis',
            'Sputum Smear Microscopy & GeneXpert',
            'DOTS Treatment & Follow-up',
            'TB Contact Tracing',
        ]),
        ('J. Laboratory Services', 'bi bi-microscope', [
            'Haematology & Blood Tests',
            'Biochemistry',
            'Microbiology & Parasitology',
            'Diagnostic Screening',
        ]),
        ('K. Pharmacy Services', 'bi bi-capsule', [
            'Prescription Dispensing',
            'Medication Counseling',
            'Refills & Drug Interaction Checks',
            'Over-the-Counter Medicines',
        ]),
        ('L. Inpatient & Wards', 'bi bi-bed', [
            'General Male & Female Wards',
            'Maternity & Pediatric Wards',
            'Private Rooms',
            '24-Hour Nursing Care',
        ]),
        ('M. Minor Theatre & Surgery', 'bi bi-scissors', [
            'Wound Suturing & Dressing',
            'Minor Surgical Procedures',
            'Abscess Drainage',
            'Male Circumcision (VMMC)',
        ]),
        ('N. Chronic Disease (NCD) Clinic', 'bi bi-heart-pulse', [
            'Diabetes Screening & Management',
            'Hypertension Care',
            'Asthma & Respiratory Care',
            'Lifestyle & Dietary Counseling',
        ]),
        ('O. Nutrition Services', 'bi bi-basket-fill', [
            'Therapeutic Feeding Programmes',
            'Micronutrient Supplementation',
            'Dietary Counseling',
            'Malnutrition Management',
        ]),
        ('P. Dental & Oral Health', 'bi bi-emoji-smile', [
            'Dental Check-ups & Cleaning',
            'Tooth Extractions',
            'Fillings & Minor Oral Surgery',
            'Oral Health Education',
        ]),
        ('Q. Eye & Vision Care', 'bi bi-eye', [
            'Visual Acuity Testing',
            'Cataract Screening',
            'Reading Glasses & Referrals',
            'Eye Infection Treatment',
        ]),
        ('R. Emergency & Ambulance', 'bi bi-truck', [
            '24/7 Emergency Care',
            'First Aid & Stabilization',
            'Ambulance Transfer Services',
            'Trauma & Accident Care',
        ]),
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
        ('OPD & General Medicine', 'bi bi-hospital',
         'First point of contact for outpatient consultations and follow-up reviews.',
         ['General Practitioners', 'Doctors', 'Nurses', 'Receptionists']),
        ('Inpatient & Wards', 'bi bi-bed',
         'Round-the-clock inpatient care across general, private and pediatric wards.',
         ['Doctors', 'Nurses', 'Ward Attendants', 'Hospital Aides']),
        ('Maternity & Delivery', 'bi bi-gender-female',
         'Comprehensive delivery services including normal, assisted and caesarean births.',
         ['Obstetricians', 'Midwives', 'Theatre Nurses', 'Neonatal Nurses']),
        ('Antenatal & Postnatal Care', 'bi bi-flower1',
         'Pregnancy monitoring and post-delivery support for mothers and newborns.',
         ['Doctors', 'Midwives', 'Nurses', 'Maternal Health Counselors']),
        ('Pediatric & Under-Five Clinic', 'bi bi-people',
         'Specialized child health services from newborn through age five.',
         ['Pediatricians', 'Nurses', 'Nutritionists', 'Vaccinators']),
        ('Family Planning & Reproductive Health', 'bi bi-chat-heart-fill',
         'Contraceptive services, reproductive health education and counseling.',
         ['Doctors', 'Nurses', 'Reproductive Health Counselors', 'Community Health Workers']),
        ('Surgical & Minor Theatre', 'bi bi-scissors',
         'Minor and intermediate surgical procedures under sterile conditions.',
         ['Surgeons', 'Anesthetists', 'Theatre Nurses', 'Sterilization Technicians']),
        ('Laboratory & Diagnostics', 'bi bi-microscope',
         'Full diagnostic laboratory services supporting clinical decision-making.',
         ['Laboratory Technicians', 'Pathologists', 'Microbiologists', 'Phlebotomists']),
        ('Pharmacy', 'bi bi-capsule',
         'Dispensing of prescribed medications with patient counseling.',
         ['Pharmacists', 'Pharmacy Technicians', 'Dispensers', 'Inventory Clerks']),
        ('HIV / AIDS & TB Clinic', 'bi bi-droplet-half',
         'Testing, treatment and follow-up for HIV, AIDS and tuberculosis.',
         ['Doctors', 'HIV Counselors', 'Nurses', 'Laboratory Technicians']),
        ('NCD (Chronic Disease) Clinic', 'bi bi-heart-pulse',
         'Long-term management of diabetes, hypertension and other chronic conditions.',
         ['Doctors', 'Nurses', 'Nutritionists', 'Lifestyle Counselors']),
        ('Emergency & Trauma', 'bi bi-truck',
         '24/7 emergency care, stabilization and ambulance transfer services.',
         ['Emergency Physicians', 'Nurses', 'Paramedics', 'Triage Officers']),
        ('Dental & Oral Health', 'bi bi-emoji-smile',
         'Preventive, restorative and minor surgical dental services.',
         ['Dentists', 'Dental Therapists', 'Dental Assistants', 'Oral Health Educators']),
        ('Eye & Vision Care', 'bi bi-eye',
         'Vision screening, refraction and minor ophthalmic procedures.',
         ['Ophthalmologists', 'Optometrists', 'Ophthalmic Nurses', 'Refractionists']),
        ('Nutrition & Wellness', 'bi bi-basket-fill',
         'Therapeutic feeding, dietary counseling and community nutrition programs.',
         ['Nutritionists', 'Dietitians', 'Nurses', 'Community Health Workers']),
        ('Administration & Finance', 'bi bi-gear-fill',
         'Hospital administration, finance, HR and procurement support.',
         ['Hospital Administrator', 'Accountants', 'Cashiers', 'HR Officers']),
    ]
    for i, (name, icon, desc, roles) in enumerate(depts):
        Department.objects.create(
            name=name, icon=icon, description=desc, roles=roles, order=i,
        )
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

# Medical Teams
if not MedicalTeam.objects.exists():
    teams = [
        ('General Practice & OPD Team', 'bi bi-hospital',
         'First point of contact for outpatient consultations, walk-in reviews and referrals.',
         'Lead Physician',
         ['General Practitioners', 'Medical Officers', 'OPD Nurses', 'Receptionists']),
        ('Pediatric & Child Health Team', 'bi bi-people-fill',
         'Comprehensive care for newborns, infants and children up to five years old.',
         'Lead Pediatrician',
         ['Pediatricians', 'Pediatric Nurses', 'Nutritionists', 'Vaccinators']),
        ('Maternity & Obstetrics Team', 'bi bi-gender-female',
         'Pregnancy, delivery and newborn care including normal and caesarean births.',
         'Lead Obstetrician',
         ['Obstetricians', 'Gynecologists', 'Midwives', 'Neonatal Nurses']),
        ('Antenatal & Postnatal Care Team', 'bi bi-flower1',
         'Continuous maternal care from conception through six weeks post-delivery.',
         'Lead ANC Clinician',
         ['Doctors', 'Midwives', 'Maternal Health Nurses', 'ANC Counselors']),
        ('Surgical & Theatre Team', 'bi bi-scissors',
         'Minor and intermediate surgical procedures performed under sterile conditions.',
         'Lead Surgeon',
         ['Surgeons', 'Anesthetists', 'Theatre Nurses', 'Recovery Nurses']),
        ('Family Planning Team', 'bi bi-chat-heart-fill',
         'Reproductive health counseling, contraceptive services and community outreach.',
         'Lead FP Clinician',
         ['Doctors', 'FP Nurses', 'Reproductive Health Counselors', 'CHWs']),
        ('Laboratory & Diagnostics Team', 'bi bi-microscope',
         'Accurate and timely diagnostic testing across haematology, microbiology and biochemistry.',
         'Chief Lab Technologist',
         ['Pathologists', 'Microbiologists', 'Laboratory Technicians', 'Phlebotomists']),
        ('Pharmacy Team', 'bi bi-capsule',
         'Safe dispensing of medications with patient education and stock management.',
         'Chief Pharmacist',
         ['Pharmacists', 'Pharmacy Technicians', 'Dispensers', 'Inventory Officers']),
        ('HIV / AIDS & TB Team', 'bi bi-droplet-half',
         'Testing, treatment, follow-up and adherence support for HIV, AIDS and tuberculosis.',
         'Lead HIV Clinician',
         ['HIV Specialists', 'HIV Counselors', 'ART Nurses', 'Lab Technicians']),
        ('NCD (Chronic Disease) Team', 'bi bi-heart-pulse',
         'Long-term management of diabetes, hypertension, asthma and related conditions.',
         'Lead NCD Physician',
         ['Endocrinologists', 'Cardiologists', 'Diabetes Nurses', 'Nutritionists']),
        ('Emergency & Trauma Team', 'bi bi-truck',
         '24/7 stabilization, resuscitation and ambulance transfer for critical cases.',
         'Lead Emergency Physician',
         ['Emergency Physicians', 'Trauma Nurses', 'Paramedics', 'Triage Officers']),
        ('Dental & Oral Health Team', 'bi bi-emoji-smile',
         'Preventive, restorative and minor surgical dental services for all ages.',
         'Lead Dentist',
         ['Dentists', 'Dental Therapists', 'Dental Assistants', 'Oral Health Educators']),
        ('Eye Care & Vision Team', 'bi bi-eye',
         'Vision screening, refraction, treatment of eye infections and minor procedures.',
         'Lead Ophthalmologist',
         ['Ophthalmologists', 'Optometrists', 'Ophthalmic Nurses', 'Refractionists']),
        ('Nutrition & Dietetics Team', 'bi bi-basket-fill',
         'Therapeutic feeding, dietary counseling and community nutrition programs.',
         'Lead Nutritionist',
         ['Dietitians', 'Nutritionists', 'Nutrition Nurses', 'CHWs']),
        ('Mental Health & Counseling Team', 'bi bi-heart',
         'Psychosocial support, counseling and psychiatric care integrated across services.',
         'Lead Psychiatrist',
         ['Psychiatrists', 'Clinical Psychologists', 'Counselors', 'Social Workers']),
        ('Inpatient & Nursing Team', 'bi bi-bed',
         'Continuous bedside care and clinical monitoring across all hospital wards.',
         'Chief Nursing Officer',
         ['Ward Doctors', 'Charge Nurses', 'Staff Nurses', 'Ward Attendants']),
    ]
    for i, (name, icon, desc, head_title, roles) in enumerate(teams):
        MedicalTeam.objects.create(
            name=name, icon=icon, description=desc,
            head_title=head_title, roles=roles, order=i,
        )
    print("MedicalTeams created")
else:
    print("MedicalTeams already exist")

print("All seed data complete!")
