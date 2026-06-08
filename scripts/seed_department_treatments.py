"""Seed the 'treatments' (treatments or support given) field on all 16 departments.

Idempotent: updates every Department row regardless of current state.
Run: venv\\Scripts\\python.exe scripts\\seed_department_treatments.py
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from apps.dashboard.models import Department


DEPT_TREATMENTS = {
    'OPD & General Medicine': [
        'General medical consultations for adults and children',
        'Diagnosis and treatment of common illnesses (malaria, flu, infections)',
        'Routine medical check-ups and follow-up reviews',
        'Prescription refills and dosage adjustments',
        'Issuance of medical certificates and sick notes',
        'Referral to specialists and other departments',
        'Minor ailment treatment (headache, cough, diarrhea)',
        'Health education and lifestyle counselling',
    ],
    'Inpatient & Wards': [
        '24-hour bedside nursing care and monitoring',
        'Medication administration (oral, IV, IM, SC)',
        'Vital signs monitoring (BP, pulse, temperature, oxygen)',
        'Wound dressing and aseptic care',
        'Pre-operative and post-operative care',
        'Patient and family education on recovery',
        'Discharge planning and follow-up scheduling',
        'Pain management and palliative support',
    ],
    'Maternity & Delivery': [
        'Normal vaginal delivery',
        'Assisted delivery (vacuum / forceps)',
        'Caesarean section (emergency and elective)',
        'Neonatal resuscitation and immediate newborn care',
        'Post-partum monitoring (mother and baby)',
        'Active management of third stage of labour',
        'Birth companion support and pain relief',
        'Post-natal counselling and family-planning referral',
    ],
    'Antenatal & Postnatal Care': [
        'Pregnancy confirmation and dating',
        'Antenatal profile labs (HIV, syphilis, Hb, blood group, urine)',
        'Routine ANC visits and foetal growth monitoring',
        'Ultrasound scan referral (dating, anomaly, growth)',
        'Iron, folate and calcium supplementation',
        'Tetanus toxoid immunisation',
        'Birth preparedness and complication-readiness counselling',
        'Post-natal review at 6 weeks (mother and newborn)',
    ],
    'Pediatric & Under-Five Clinic': [
        'Growth monitoring and nutrition assessment (weight, height, MUAC)',
        'Routine childhood immunisation (EPI schedule)',
        'Vitamin A supplementation and deworming',
        'Integrated Management of Neonatal and Childhood Illnesses (IMNCI)',
        'Treatment of pneumonia, diarrhoea and malaria in children',
        'Developmental milestone screening',
        'Caregiver education on feeding and danger signs',
        'Follow-up of low-birth-weight and preterm babies',
    ],
    'Family Planning & Reproductive Health': [
        'Contraceptive counselling and method choice',
        'Oral contraceptive pills (combined and progestin-only)',
        'Injectable contraceptives (Depo, Sayana Press)',
        'Sub-dermal implant insertion and removal',
        'Intrauterine device (IUD / copper-T) insertion and removal',
        'Permanent methods referral (tubal ligation, vasectomy)',
        'Cervical cancer screening (VIA / Pap smear)',
        'STI screening, treatment and partner notification',
    ],
    'Surgical & Minor Theatre': [
        'Minor surgical procedures (excisions, incisions, biopsies)',
        'Intermediate surgery (hernia repair, lump removal)',
        'Suturing of lacerations and wound closure',
        'Suture removal and wound review',
        'Sterile dressing changes and wound care',
        'Local anaesthesia administration',
        'Pre-operative assessment and post-op recovery',
        'Surgical instrument sterilisation and tray preparation',
    ],
    'Laboratory & Diagnostics': [
        'Full blood count and differential',
        'Malaria rapid diagnostic test and microscopy',
        'Urine analysis and urine pregnancy test',
        'Stool examination (parasites, occult blood)',
        'HIV rapid testing and confirmatory tests',
        'Sputum AFB smear for TB diagnosis',
        'Blood sugar and HbA1c testing',
        'Blood grouping, cross-match and syphilis serology',
    ],
    'Pharmacy': [
        'Prescription dispensing with dosage verification',
        'Patient counselling on drug use and side effects',
        'Chronic medication refills and adherence support',
        'Drug interaction and allergy screening',
        'Stock control and expiry-date monitoring',
        'Issuance of over-the-counter (OTC) medicines',
        'Compounding and reconstitution of syrups',
        'Reporting of adverse drug reactions',
    ],
    'HIV / AIDS & TB Clinic': [
        'HIV testing services (HTS) with counselling',
        'CD4 count and viral load testing',
        'Antiretroviral therapy (ART) initiation and refills',
        'Adherence counselling and psychosocial support',
        'Tuberculosis screening (GeneXpert, sputum AFB)',
        'TB treatment (DOTS) and follow-up',
        'Management of opportunistic infections',
        'Index testing and partner notification',
    ],
    'NCD (Chronic Disease) Clinic': [
        'Blood pressure measurement and hypertension management',
        'Random and fasting blood sugar testing',
        'HbA1c testing for diabetes monitoring',
        'Lipid profile testing and cardiovascular risk assessment',
        'Lifestyle and dietary counselling',
        'Medication refills and adherence review',
        'Screening for diabetic complications (eyes, feet, kidneys)',
        'Asthma and COPD management with inhaler technique',
    ],
    'Emergency & Trauma': [
        'Triage and colour-coded priority assessment',
        'Airway, breathing and circulation stabilisation',
        'Cardiopulmonary resuscitation (CPR)',
        'Wound care, suturing and haemorrhage control',
        'Fracture immobilisation and splinting',
        'Snake-bite and poisoning management',
        'Ambulance transfer and referral coordination',
        '24/7 emergency admission to wards or theatre',
    ],
    'Dental & Oral Health': [
        'Oral examination and treatment planning',
        'Scaling and polishing (oral prophylaxis)',
        'Dental fillings (composite and GIC)',
        'Tooth extraction (simple and surgical)',
        'Root canal treatment and pulp therapy',
        'Fluoride application and fissure sealants',
        'Denture fitting and minor denture repairs',
        'Oral health education and hygiene instructions',
    ],
    'Eye & Vision Care': [
        'Visual acuity testing (Snellen chart)',
        'Refraction and eyeglass prescription',
        'Intra-ocular pressure (IOP) measurement',
        'Cataract screening and surgical referral',
        'Dilated fundus examination for diabetic retinopathy',
        'Treatment of conjunctivitis and minor eye infections',
        'Foreign body removal from the eye',
        'Issuance of reading glasses and referrals',
    ],
    'Nutrition & Wellness': [
        'Anthropometric measurement and growth monitoring',
        'Mid-Upper Arm Circumference (MUAC) screening',
        'Therapeutic feeding for moderate and severe malnutrition',
        'Ready-to-Use Therapeutic Food (RUTF) distribution',
        'Micronutrient supplementation (vitamin A, iron, zinc)',
        'Individual and group dietary counselling',
        'Community nutrition education and cooking demonstrations',
        'Maternal, infant and young child nutrition (MIYCN) support',
    ],
    'Administration & Finance': [
        'Patient registration and file retrieval',
        'Billing, invoicing and receipt issuance',
        'Cash, mobile-money and bank-payment processing',
        'NHIMA and insurance claim submission',
        'Human resources and payroll support',
        'Procurement, supplier payment and stock control',
        'Medical records management and confidentiality',
        'Customer service and patient feedback handling',
    ],
}


def run():
    departments = {d.name: d for d in Department.objects.all()}
    print(f"Found {len(departments)} departments in DB")
    updated = 0
    skipped = 0
    for name, treatments in DEPT_TREATMENTS.items():
        dept = departments.get(name)
        if not dept:
            print(f"  ! '{name}' not found in DB - skipping")
            skipped += 1
            continue
        dept.treatments = treatments
        dept.save()
        updated += 1
        print(f"  + {name}: {len(treatments)} treatments/support items")
    print(f"\nDone. {updated} updated, {skipped} skipped.")


if __name__ == '__main__':
    run()
