from django.db import models
from django.utils.text import slugify


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default='Hope Medi - Clinic')
    tagline = models.CharField(max_length=300, blank=True, default='Quality care for all')
    meta_description = models.TextField(blank=True, default='Providing compassionate, affordable and professional healthcare services for all ages.')
    meta_keywords = models.CharField(max_length=500, blank=True, default='healthcare, clinic, hospital, OPD, antenatal care, family planning, immunization, laboratory, pharmacy')
    phone = models.CharField(max_length=50, blank=True, default='+265 999 401 674')
    phone_2 = models.CharField(max_length=50, blank=True, default='+254 700 100 300')
    email = models.EmailField(blank=True, default='info@hopeclinic.co.ke')
    email_2 = models.EmailField(blank=True, default='admin@hopeclinic.co.ke')
    address = models.CharField(max_length=300, blank=True, default='Chinamwali, Zomba - Malawi')
    address_detail = models.CharField(max_length=300, blank=True, default='Next to City Hospital')
    working_hours = models.CharField(max_length=200, blank=True, default='Mon - Sat: 7:00 AM - 8:00 PM')
    sunday_hours = models.CharField(max_length=200, blank=True, default='Sunday: Closed (Emergencies Only)')
    emergency_phone = models.CharField(max_length=50, blank=True, default='+254 700 100 300')
    facebook_url = models.URLField(blank=True, default='#')
    twitter_url = models.URLField(blank=True, default='#')
    instagram_url = models.URLField(blank=True, default='#')
    youtube_url = models.URLField(blank=True, default='#')
    map_embed_url = models.TextField(blank=True, default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15955.000000000!2d36.8219!3d-1.2921!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMcKwMTcnMzEuNyJTIDM2wrA0OScxOC44IkU!5e0!3m2!1sen!2ske!4v1')
    footer_about = models.TextField(blank=True, default='Providing compassionate, affordable and professional healthcare services for all ages. Your health is our priority.')
    copyright_text = models.CharField(max_length=300, blank=True, default='All rights reserved. Powered by HMS.')
    about_heading = models.CharField(max_length=200, blank=True, default='Why Choose {site_name}')
    about_subtitle = models.TextField(blank=True, default='We are committed to providing the highest standard of medical care with compassion and professionalism.')
    services_heading = models.CharField(max_length=200, blank=True, default='Our Services')
    services_subtitle = models.TextField(blank=True, default='Comprehensive healthcare services tailored to meet the needs of our community.')
    health_heading = models.CharField(max_length=200, blank=True, default='Health Education')
    health_subtitle = models.TextField(blank=True, default='Empowering our community with knowledge for better health outcomes.')
    health_search_placeholder = models.CharField(max_length=200, blank=True, default='Search health tips...')
    departments_heading = models.CharField(max_length=200, blank=True, default='Our Departments')
    departments_subtitle = models.TextField(blank=True, default='Specialized departments working together for comprehensive healthcare delivery.')
    doctors_heading = models.CharField(max_length=200, blank=True, default='Our Medical Team')
    doctors_subtitle = models.TextField(blank=True, default='Meet our dedicated team of healthcare professionals committed to your wellbeing.')
    appointment_heading = models.CharField(max_length=200, blank=True, default='Book an Appointment')
    appointment_subtitle = models.CharField(max_length=300, blank=True, default="Schedule your visit today. We'll confirm your appointment promptly.")
    appointment_bullet_1 = models.CharField(max_length=200, blank=True, default='Same-day appointments available')
    appointment_bullet_2 = models.CharField(max_length=200, blank=True, default='Minimal waiting time')
    appointment_bullet_3 = models.CharField(max_length=200, blank=True, default='Professional medical team')
    appointment_bullet_4 = models.CharField(max_length=200, blank=True, default='Affordable consultation fees')
    appointment_form_title = models.CharField(max_length=200, blank=True, default='Request Appointment')
    appointment_btn_text = models.CharField(max_length=200, blank=True, default='Submit Appointment Request')
    testimonials_heading = models.CharField(max_length=200, blank=True, default='What Our Patients Say')
    testimonials_subtitle = models.TextField(blank=True, default='Hear from our patients about their experience at {site_name}.')
    contact_heading = models.CharField(max_length=200, blank=True, default='Contact Us')
    contact_subtitle = models.TextField(blank=True, default="We'd love to hear from you. Reach out to us through any of the channels below.")

    theme_mode = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    primary_color = models.CharField(max_length=7, default='#0d9488', help_text='Main brand color (e.g. #0d9488)')
    primary_light = models.CharField(max_length=7, default='#14b8a6', help_text='Lighter primary variant')
    primary_dark = models.CharField(max_length=7, default='#0f766e', help_text='Darker primary variant')
    accent_color = models.CharField(max_length=7, default='#f59e0b', help_text='Accent / warning color')
    sidebar_bg_start = models.CharField(max_length=7, default='#0f172a', help_text='Sidebar gradient start color')
    sidebar_bg_end = models.CharField(max_length=7, default='#1e293b', help_text='Sidebar gradient end color')
    card_bg = models.CharField(max_length=7, default='#ffffff', help_text='Card background color')
    card_border = models.CharField(max_length=7, default='rgba(0,0,0,.04)', help_text='Card border color')
    body_bg = models.CharField(max_length=7, default='#f8fafc', help_text='Page body background color')
    text_primary = models.CharField(max_length=7, default='#0f172a', help_text='Primary text color')
    text_muted = models.CharField(max_length=7, default='#94a3b8', help_text='Muted text color')
    topbar_bg = models.CharField(max_length=7, default='rgba(255,255,255,.85)', help_text='Topbar background')

    class Meta:
        db_table = 'site_settings'
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        return cls.objects.first()


class HeroSection(models.Model):
    headline = models.CharField(max_length=300, default='Quality care for all')
    subheading = models.CharField(max_length=500, default='Providing compassionate, affordable and professional healthcare services for all ages.')
    background_image = models.ImageField(upload_to='landing/', blank=True, null=True)
    book_appointment_btn_text = models.CharField(max_length=100, default='Book Appointment')
    contact_us_btn_text = models.CharField(max_length=100, default='Contact Us')
    staff_login_btn_text = models.CharField(max_length=100, default='Staff Login')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hero_sections'
        verbose_name = 'Hero Section'

    def __str__(self):
        return self.headline


class WhyChooseItem(models.Model):
    icon = models.CharField(max_length=50, default='bi bi-heart-fill', help_text='Bootstrap icon class')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'why_choose_items'
        ordering = ['order']
        verbose_name = 'Why Choose Item'

    def __str__(self):
        return self.title


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default='bi bi-hospital', help_text='Bootstrap icon class')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'service_categories'
        ordering = ['order']
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class ServiceItem(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'service_items'
        ordering = ['order']
        verbose_name = 'Service Item'

    def __str__(self):
        return self.text


class Department(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default='bi bi-hospital', help_text='Bootstrap icon class')
    description = models.CharField(max_length=300, blank=True, default='', help_text='Short tagline shown on the landing page')
    roles = models.JSONField(default=list, blank=True, help_text='List of job roles / professionals in this department')
    treatments = models.JSONField(default=list, blank=True, help_text='List of treatments or support services typically given to patients in this department')
    referrals_from = models.JSONField(default=list, blank=True, help_text='Departments / entry points that typically refer patients INTO this one (entry points)')
    referrals_to = models.JSONField(default=list, blank=True, help_text='Departments / specialists that patients are referred OUT TO from this one (exit points)')
    opening_hours = models.CharField(max_length=200, blank=True, default='Mon - Fri: 07:30 - 17:00 | Sat: 08:00 - 12:00 | Sun & Holidays: Closed', help_text='Service hours shown to the public')
    client_handling_steps = models.JSONField(default=list, blank=True, help_text='Step-by-step flow of how a client is received and discharged')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'landing_departments'
        ordering = ['order']

    def __str__(self):
        return self.name


class MedicalTeam(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default='bi bi-people-fill', help_text='Bootstrap icon class')
    description = models.CharField(max_length=300, blank=True, default='', help_text='Short tagline shown on the landing page')
    head_title = models.CharField(max_length=100, default='Team Lead', help_text='e.g. "Lead Physician", "Head Nurse"')
    roles = models.JSONField(default=list, blank=True, help_text='List of roles / professionals in the team')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'landing_medical_teams'
        ordering = ['order']
        verbose_name = 'Medical Team'
        verbose_name_plural = 'Medical Teams'

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    patient_name = models.CharField(max_length=200)
    content = models.TextField()
    designation = models.CharField(max_length=200, blank=True, default='Patient')
    avatar_color = models.CharField(max_length=20, choices=[
        ('primary', 'Blue'), ('success', 'Green'), ('info', 'Teal'),
        ('warning', 'Orange'), ('danger', 'Red'), ('secondary', 'Gray'),
    ], default='primary')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'testimonials'
        ordering = ['order']

    def __str__(self):
        return self.patient_name


class Statistic(models.Model):
    label = models.CharField(max_length=200)
    value = models.PositiveIntegerField(default=0, help_text='Target number for the animated counter')
    icon = models.CharField(max_length=50, default='bi bi-people-fill', help_text='Bootstrap icon class')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'landing_statistics'
        ordering = ['order']
        verbose_name = 'Statistic'
        verbose_name_plural = 'Statistics'

    def __str__(self):
        return self.label


class ContactInfo(models.Model):
    INFO_TYPES = [
        ('phone', 'Phone'), ('email', 'Email'),
        ('address', 'Address'), ('hours', 'Working Hours'),
    ]
    info_type = models.CharField(max_length=20, choices=INFO_TYPES)
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='bi bi-telephone-fill')
    value = models.CharField(max_length=300)
    value_2 = models.CharField(max_length=300, blank=True, help_text='Secondary value (e.g. second phone number)')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'contact_infos'
        ordering = ['order']
        verbose_name = 'Contact Info'
        verbose_name_plural = 'Contact Info'

    def __str__(self):
        return self.label


class HealthArticle(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    summary = models.TextField(max_length=500, blank=True, help_text="Short summary shown on the landing page")
    icon = models.CharField(max_length=50, default="bi bi-heart-pulse-fill", help_text="Bootstrap icon class")
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'health_articles'
        ordering = ['-published_at']
        verbose_name = 'Health Article'
        verbose_name_plural = 'Health Articles'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
