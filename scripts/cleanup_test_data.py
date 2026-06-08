"""Clean up test data created during the appointment-booking flow testing.

Run: venv\Scripts\python.exe scripts\cleanup_test_data.py
"""
import os, sys, django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from apps.accounts.models import User
from apps.notifications.models import Notification, EmailLog, SMSLog
from apps.patients.models import Patient
from apps.inpatient.models import Admission
from apps.doctors.models import DoctorProfile

TEST_EMAILS = [
    'mary.mhango@example.com',
    'john.banda@example.com',
    'grace.phiri@example.com',
]

def run():
    print('--- Cleaning up test data ---')
    # 1) Test patients + their user accounts + related notifications/email/sms
    pat_count = 0
    user_count = 0
    notif_count = 0
    email_count = 0
    sms_count = 0
    for email in TEST_EMAILS:
        u = User.objects.filter(email=email).first()
        if not u:
            print(f'  {email}: no user')
            continue
        pat = Patient.objects.filter(user=u).first()
        if pat:
            n, _ = Notification.objects.filter(patient=pat).delete()
            notif_count += n
            n, _ = EmailLog.objects.filter(patient=pat).delete()
            email_count += n
            n, _ = SMSLog.objects.filter(patient=pat).delete()
            sms_count += n
            pat.delete()
            pat_count += 1
        u.delete()
        user_count += 1
        print(f'  Deleted {email}')
    print(f'Patients: {pat_count}, Users: {user_count}, Notifications: {notif_count}, Emails: {email_count}, SMS: {sms_count}')

    # 2) Test admission #1
    ad_count = Admission.objects.count()
    Admission.objects.all().delete()
    print(f'Admissions: deleted {ad_count}')

    # 3) Test doctor (Sarah Mwale was created in the e2e test)
    test_doctors = DoctorProfile.objects.filter(user__email__startswith='doctor1')
    d_count = test_doctors.count()
    for d in test_doctors:
        d.user.delete()  # cascades to DoctorProfile
    print(f'Test doctors: deleted {d_count}')

    print('--- Cleanup complete ---')
    print(f'Remaining: Patients={Patient.objects.count()}, Users={User.objects.filter(role="patient").count()}, Admissions={Admission.objects.count()}, Doctors={DoctorProfile.objects.count()}')


if __name__ == '__main__':
    run()
