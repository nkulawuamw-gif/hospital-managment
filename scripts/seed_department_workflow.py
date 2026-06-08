"""Seed referrals_from / referrals_to / opening_hours / client_handling_steps on all 16 departments.

Idempotent: updates every Department row regardless of current state.
Run with: venv\\Scripts\\python.exe scripts\\seed_department_workflow.py
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from apps.dashboard.models import Department


DEPT_DATA = {
    'OPD & General Medicine': {
        'opening_hours': 'Mon - Fri: 07:30 - 17:00 | Sat: 08:00 - 12:00 | Sun & Holidays: Closed',
        'referrals_from': ['Walk-in patients', 'Community referrals', 'Emergency discharge follow-ups'],
        'referrals_to': ['Laboratory & Diagnostics', 'Pharmacy', 'Surgical & Minor Theatre',
                         'Inpatient & Wards', 'Specialist Clinics (Eye, Dental, NCD, HIV/TB, Maternity)'],
        'client_handling_steps': [
            'Registration at reception and file retrieval',
            'Vitals taken by nurse (BP, temperature, weight, pulse)',
            'Triage and queue assignment to a doctor',
            'Doctor consultation, examination and diagnosis',
            'Prescription, lab request or referral issued',
            'Billing at cashiers desk',
            'Pharmacy dispensing or procedure room routing',
            'Discharge with next-visit date or referral slip',
        ],
    },
    'Inpatient & Wards': {
        'opening_hours': '24 hours / 7 days a week (visiting: 12:00 - 13:00 and 17:00 - 19:00)',
        'referrals_from': ['OPD & General Medicine', 'Emergency & Trauma', 'Surgical & Minor Theatre',
                           'Maternity & Delivery'],
        'referrals_to': ['Pharmacy', 'Laboratory & Diagnostics', 'Nutrition & Wellness',
                         'Specialist review clinics (NCD, HIV/TB)'],
        'client_handling_steps': [
            'Admission paperwork and bed allocation at the ward desk',
            'Nursing intake: vitals, allergy check, history',
            'Doctor round, treatment plan and medication chart',
            'Daily nursing care, medication administration and monitoring',
            'Progress review and discharge planning',
            'Discharge education, medications and follow-up appointment',
        ],
    },
    'Maternity & Delivery': {
        'opening_hours': '24 hours / 7 days a week (labour ward always open)',
        'referrals_from': ['Antenatal & Postnatal Care', 'OPD & General Medicine',
                           'Family Planning & Reproductive Health', 'Emergency & Trauma'],
        'referrals_to': ['Pediatric & Under-Five Clinic', 'Pharmacy', 'Laboratory & Diagnostics',
                         'Inpatient & Wards (post-natal)', 'Antenatal & Postnatal Care'],
        'client_handling_steps': [
            'Admission via ANC record or direct walk-in',
            'Initial assessment by midwife (stage of labour, vitals)',
            'Active management of labour with continuous monitoring',
            'Delivery conducted by midwife / obstetrician',
            'Immediate newborn care and APGAR scoring',
            'Post-delivery observation (mother and baby)',
            'Discharge to postnatal clinic or ward',
        ],
    },
    'Antenatal & Postnatal Care': {
        'opening_hours': 'Mon - Fri: 08:00 - 16:30 | Sat: 08:00 - 12:00 | Sun: Closed',
        'referrals_from': ['Family Planning & Reproductive Health', 'OPD & General Medicine',
                           'Community Health Workers', 'Self-referral (pregnant mothers)'],
        'referrals_to': ['Laboratory & Diagnostics', 'Maternity & Delivery', 'Pharmacy',
                         'Nutrition & Wellness', 'HIV / AIDS & TB Clinic (if positive)'],
        'client_handling_steps': [
            'Registration and ANC card issuance',
            'Weight, BP, urine and fundal-height check by nurse',
            'Antenatal profile labs (HIV, syphilis, haemoglobin, blood group)',
            'Doctor / midwife consultation and pregnancy monitoring',
            'Iron, folate and nutritional supplements dispensed',
            'Education on danger signs and birth preparedness',
            'Postnatal review at 6 weeks with family-planning counselling',
        ],
    },
    'Pediatric & Under-Five Clinic': {
        'opening_hours': 'Mon - Fri: 07:30 - 17:00 | Sat: 08:00 - 13:00 | Sun: Closed',
        'referrals_from': ['Maternity & Delivery (newborns)', 'OPD & General Medicine',
                           'Nutrition & Wellness', 'Community Health Workers',
                           'Self-referral (caregivers)'],
        'referrals_to': ['Laboratory & Diagnostics', 'Pharmacy', 'Nutrition & Wellness',
                         'Inpatient & Wards', 'HIV / AIDS & TB Clinic'],
        'client_handling_steps': [
            'Registration and child health passport retrieval',
            'Growth monitoring (weight, height, MUAC, nutrition status)',
            'Vaccination check and immunization',
            'Doctor consultation and examination',
            'Treatment, prescription or lab request',
            'Caregiver counselling on feeding and danger signs',
            'Discharge with next-visit date or referral slip',
        ],
    },
    'Family Planning & Reproductive Health': {
        'opening_hours': 'Mon - Fri: 08:00 - 16:30 | Sat: 08:00 - 12:00 | Sun: Closed',
        'referrals_from': ['Antenatal & Postnatal Care', 'OPD & General Medicine',
                           'Maternity & Delivery', 'Self-referral (women of reproductive age)'],
        'referrals_to': ['Pharmacy', 'Laboratory & Diagnostics',
                         'Surgical & Minor Theatre (for procedures)', 'Maternity & Delivery (for fertility)'],
        'client_handling_steps': [
            'Registration and confidentiality briefing',
            'Counselling on available contraceptive methods',
            'Medical eligibility screening (BP, history)',
            'Method chosen and informed consent',
            'Provision of method (pills, injectables, implants, IUD, sterilization)',
            'Follow-up scheduling and side-effect education',
        ],
    },
    'Surgical & Minor Theatre': {
        'opening_hours': 'Mon - Fri: 08:00 - 17:00 (elective list) | Emergency: 24/7',
        'referrals_from': ['OPD & General Medicine', 'Emergency & Trauma',
                           'Dental & Oral Health', 'Eye & Vision Care'],
        'referrals_to': ['Inpatient & Wards', 'Pharmacy', 'Laboratory & Diagnostics',
                         'OPD & General Medicine (follow-up)'],
        'client_handling_steps': [
            'Pre-operative booking and consent',
            'Pre-op labs and anaesthetic review',
            'Patient preparation in pre-op bay',
            'Surgical procedure in theatre',
            'Post-operative recovery and monitoring',
            'Ward admission or same-day discharge',
            'Follow-up appointment scheduling',
        ],
    },
    'Laboratory & Diagnostics': {
        'opening_hours': 'Mon - Fri: 07:00 - 17:00 | Sat: 08:00 - 13:00 | Emergency: 24/7',
        'referrals_from': ['OPD & General Medicine', 'Antenatal & Postnatal Care',
                           'Inpatient & Wards', 'Surgical & Minor Theatre',
                           'HIV / AIDS & TB Clinic', 'NCD (Chronic Disease) Clinic',
                           'Maternity & Delivery', 'Pediatric & Under-Five Clinic'],
        'referrals_to': ['Requesting clinician (results returned)', 'Pharmacy (when drug monitoring)'],
        'client_handling_steps': [
            'Presentation of lab request form',
            'Verification of patient identity and tests ordered',
            'Sample collection (blood, urine, swab, stool)',
            'Sample processing in the lab',
            'Internal quality control and validation',
            'Result entry into patient file / system',
            'Results released to the requesting clinician',
        ],
    },
    'Pharmacy': {
        'opening_hours': 'Mon - Fri: 07:30 - 19:00 | Sat: 08:00 - 14:00 | Sun: 09:00 - 12:00',
        'referrals_from': ['OPD & General Medicine', 'Antenatal & Postnatal Care',
                           'Pediatric & Under-Five Clinic', 'NCD (Chronic Disease) Clinic',
                           'HIV / AIDS & TB Clinic', 'Surgical & Minor Theatre',
                           'Inpatient & Wards', 'Family Planning & Reproductive Health'],
        'referrals_to': ['OPD & General Medicine (medication review)', 'Administration & Finance (billing)'],
        'client_handling_steps': [
            'Presentation of prescription at dispensary window',
            'Verification of prescription and patient identity',
            'Stock check and pricing',
            'Billing at the cashiers desk (if not pre-paid)',
            'Dispensing with clear usage instructions',
            'Counselling on side effects and adherence',
            'File prescription and schedule refill if chronic',
        ],
    },
    'HIV / AIDS & TB Clinic': {
        'opening_hours': 'Mon - Fri: 08:00 - 16:30 | Sat: 08:00 - 12:00 | Sun: Closed',
        'referrals_from': ['OPD & General Medicine', 'Antenatal & Postnatal Care',
                           'Pediatric & Under-Five Clinic', 'Self-referral (index testing)',
                           'Community Health Workers'],
        'referrals_to': ['Laboratory & Diagnostics', 'Pharmacy (ART / TB drugs)',
                         'NCD (Chronic Disease) Clinic', 'Nutrition & Wellness',
                         'Community ART groups'],
        'client_handling_steps': [
            'Registration and confidential file opening',
            'Pre-test counselling and consent',
            'HIV testing / TB sputum examination',
            'Post-test counselling and result disclosure',
            'Enrollment into care if positive (baseline labs, CD4 / viral load)',
            'Treatment initiation and adherence counselling',
            'Routine follow-up, refills and viral-load monitoring',
        ],
    },
    'NCD (Chronic Disease) Clinic': {
        'opening_hours': 'Mon - Fri: 07:30 - 16:30 | Sat: 08:00 - 12:00 | Sun: Closed',
        'referrals_from': ['OPD & General Medicine', 'Emergency & Trauma',
                           'Inpatient & Wards (post-discharge)', 'Self-referral'],
        'referrals_to': ['Laboratory & Diagnostics', 'Pharmacy', 'Eye & Vision Care',
                         'Nutrition & Wellness', 'HIV / AIDS & TB Clinic (if co-infected)'],
        'client_handling_steps': [
            'Registration and chronic-care card retrieval',
            'Vitals check (BP, blood sugar, weight, BMI)',
            'Symptom review and medication adherence check',
            'Doctor consultation and treatment adjustment',
            'Lab request (HbA1c, lipids, creatinine, etc.)',
            'Refill prescription and lifestyle counselling',
            'Next follow-up scheduled (usually 1 - 3 months)',
        ],
    },
    'Emergency & Trauma': {
        'opening_hours': '24 hours / 7 days a week',
        'referrals_from': ['Walk-in emergencies', 'Ambulance calls from community',
                           'OPD & General Medicine (escalation)', 'Police / accident scenes'],
        'referrals_to': ['Surgical & Minor Theatre', 'Inpatient & Wards',
                         'Maternity & Delivery', 'Laboratory & Diagnostics',
                         'Pharmacy', 'Tertiary hospitals (for specialist care)'],
        'client_handling_steps': [
            'Triage on arrival (colour-coded: red / yellow / green / black)',
            'Rapid registration and patient identification',
            'Stabilization (airway, breathing, circulation, IV access)',
            'Doctor assessment and emergency investigations',
            'Emergency treatment or procedure',
            'Admission to ward, theatre, or transfer out',
            'Discharge with follow-up or referral documentation',
        ],
    },
    'Dental & Oral Health': {
        'opening_hours': 'Mon - Fri: 08:00 - 16:30 | Sat: 08:00 - 12:00 | Sun: Closed',
        'referrals_from': ['OPD & General Medicine', 'Self-referral',
                           'Pediatric & Under-Five Clinic'],
        'referrals_to': ['Surgical & Minor Theatre', 'Pharmacy',
                         'Laboratory & Diagnostics', 'Radiology (off-site)'],
        'client_handling_steps': [
            'Registration and oral-health history',
            'Clinical examination and charting',
            'X-ray or pulp vitality test if required',
            'Treatment plan discussion and consent',
            'Procedure (cleaning, restoration, extraction, minor surgery)',
            'Post-procedure instructions and prescriptions',
            'Recall appointment in 6 months',
        ],
    },
    'Eye & Vision Care': {
        'opening_hours': 'Mon - Fri: 08:00 - 16:30 | Sat: 08:00 - 12:00 | Sun: Closed',
        'referrals_from': ['OPD & General Medicine', 'NCD (Chronic Disease) Clinic (diabetic)',
                           'Pediatric & Under-Five Clinic', 'Self-referral'],
        'referrals_to': ['Surgical & Minor Theatre (cataract / minor ops)',
                         'Pharmacy (eye drops, spectacles)', 'Tertiary eye hospital (retina)'],
        'client_handling_steps': [
            'Registration and visual-acuity test',
            'Tonometry, refraction and slit-lamp examination',
            'Dilated fundus examination if indicated',
            'Diagnosis and treatment plan',
            'Prescription of spectacles or eye medication',
            'Referral for surgery or specialist review if needed',
            'Discharge with follow-up schedule',
        ],
    },
    'Nutrition & Wellness': {
        'opening_hours': 'Mon - Fri: 08:00 - 16:30 | Sat: 08:00 - 12:00 | Sun: Closed',
        'referrals_from': ['Pediatric & Under-Five Clinic', 'Antenatal & Postnatal Care',
                           'NCD (Chronic Disease) Clinic', 'Maternity & Delivery',
                           'OPD & General Medicine', 'Community Health Workers'],
        'referrals_to': ['Pharmacy (micronutrients)', 'Pediatric & Under-Five Clinic',
                         'Inpatient & Wards (severe cases)', 'Community follow-up'],
        'client_handling_steps': [
            'Registration and nutrition assessment',
            'Anthropometric measurements (weight, height, MUAC)',
            'Dietary recall and medical history',
            'Individualized nutrition counselling',
            'Therapeutic food distribution if malnourished',
            'Caregiver education on balanced diet',
            'Follow-up visit scheduled and progress monitored',
        ],
    },
    'Administration & Finance': {
        'opening_hours': 'Mon - Fri: 07:30 - 17:00 | Sat: 08:00 - 12:00 | Sun & Holidays: Closed',
        'referrals_from': ['All clinical departments (billing, HR, procurement, records)'],
        'referrals_to': ['External partners (NHIMA, suppliers, banks, government)'],
        'client_handling_steps': [
            'Reception and inquiry at the front desk',
            'Issue / request logged and routed to the right officer',
            'Documentation review and verification',
            'Processing (billing, payment, HR action, procurement, records)',
            'Approval by supervisor where required',
            'Receipt / confirmation issued to the requester',
            'File closed and archived',
        ],
    },
}


def run():
    departments = {d.name: d for d in Department.objects.all()}
    print(f"Found {len(departments)} departments in DB")
    updated = 0
    skipped = 0
    for name, payload in DEPT_DATA.items():
        dept = departments.get(name)
        if not dept:
            print(f"  ! '{name}' not found in DB — skipping")
            skipped += 1
            continue
        dept.opening_hours = payload['opening_hours']
        dept.referrals_from = payload['referrals_from']
        dept.referrals_to = payload['referrals_to']
        dept.client_handling_steps = payload['client_handling_steps']
        dept.save()
        updated += 1
        print(f"  + {name}: hours, {len(payload['referrals_from'])} in, {len(payload['referrals_to'])} out, {len(payload['client_handling_steps'])} steps")
    print(f"\nDone. {updated} updated, {skipped} skipped.")


if __name__ == '__main__':
    run()
