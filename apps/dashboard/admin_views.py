from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import (
    SiteSetting, HeroSection, WhyChooseItem,
    ServiceCategory, ServiceItem, Department,
    Testimonial, Statistic, ContactInfo, HealthArticle
)


@staff_member_required
def landing_settings_view(request):
    site = SiteSetting.get_settings()
    if site is None:
        site = SiteSetting.objects.create()
    hero = HeroSection.objects.first()
    if hero is None:
        hero = HeroSection.objects.create()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'site_settings':
            for field in ['site_name', 'tagline', 'meta_description', 'meta_keywords',
                          'phone', 'phone_2', 'email', 'email_2', 'address', 'address_detail',
                          'working_hours', 'sunday_hours', 'emergency_phone',
                          'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url',
                          'map_embed_url', 'footer_about', 'copyright_text',
                          'about_heading', 'about_subtitle',
                          'services_heading', 'services_subtitle',
                          'health_heading', 'health_subtitle', 'health_search_placeholder',
                          'departments_heading', 'departments_subtitle',
                          'doctors_heading', 'doctors_subtitle',
                          'appointment_heading', 'appointment_subtitle',
                          'appointment_bullet_1', 'appointment_bullet_2',
                          'appointment_bullet_3', 'appointment_bullet_4',
                          'appointment_form_title', 'appointment_btn_text',
                          'testimonials_heading', 'testimonials_subtitle',
                          'contact_heading', 'contact_subtitle']:
                setattr(site, field, request.POST.get(field, ''))
            site.save()
            messages.success(request, 'Site settings saved.')

        elif action == 'hero':
            for field in ['headline', 'subheading', 'book_appointment_btn_text',
                          'contact_us_btn_text', 'staff_login_btn_text']:
                setattr(hero, field, request.POST.get(field, ''))
            hero.is_active = request.POST.get('is_active') == 'on'
            hero.save()
            messages.success(request, 'Hero section saved.')

        elif action == 'why_choose':
            item_id = request.POST.get('item_id')
            if item_id:
                item = WhyChooseItem.objects.get(id=item_id)
                item.title = request.POST.get('title', item.title)
                item.description = request.POST.get('description', item.description)
                item.icon = request.POST.get('icon', item.icon)
                item.order = request.POST.get('order', item.order)
                item.is_active = request.POST.get('is_active') == 'on'
                item.save()
                messages.success(request, 'Why Choose item saved.')
            elif request.POST.get('new_item'):
                WhyChooseItem.objects.create(
                    title=request.POST.get('new_title', ''),
                    description=request.POST.get('new_description', ''),
                    icon=request.POST.get('new_icon', 'bi bi-heart-fill'),
                    order=WhyChooseItem.objects.count(),
                )
                messages.success(request, 'New Why Choose item added.')

        elif action == 'delete_why_choose':
            WhyChooseItem.objects.filter(id=request.POST.get('item_id')).delete()
            messages.success(request, 'Item deleted.')

        elif action == 'department':
            item_id = request.POST.get('item_id')
            if item_id:
                item = Department.objects.get(id=item_id)
                item.name = request.POST.get('name', item.name)
                item.icon = request.POST.get('icon', item.icon)
                item.order = request.POST.get('order', item.order)
                item.is_active = request.POST.get('is_active') == 'on'
                item.save()
                messages.success(request, 'Department saved.')
            elif request.POST.get('new_item'):
                Department.objects.create(
                    name=request.POST.get('new_name', ''),
                    icon=request.POST.get('new_icon', 'bi bi-hospital'),
                    order=Department.objects.count(),
                )
                messages.success(request, 'New department added.')

        elif action == 'delete_department':
            Department.objects.filter(id=request.POST.get('item_id')).delete()
            messages.success(request, 'Department deleted.')

        elif action == 'statistic':
            item_id = request.POST.get('item_id')
            if item_id:
                item = Statistic.objects.get(id=item_id)
                item.label = request.POST.get('label', item.label)
                item.value = request.POST.get('value', item.value)
                item.icon = request.POST.get('icon', item.icon)
                item.order = request.POST.get('order', item.order)
                item.is_active = request.POST.get('is_active') == 'on'
                item.save()
                messages.success(request, 'Statistic saved.')

        elif action == 'delete_statistic':
            Statistic.objects.filter(id=request.POST.get('item_id')).delete()
            messages.success(request, 'Statistic deleted.')

        elif action == 'testimonial':
            item_id = request.POST.get('item_id')
            if item_id:
                item = Testimonial.objects.get(id=item_id)
                item.patient_name = request.POST.get('patient_name', item.patient_name)
                item.content = request.POST.get('content', item.content)
                item.designation = request.POST.get('designation', item.designation)
                item.avatar_color = request.POST.get('avatar_color', item.avatar_color)
                item.order = request.POST.get('order', item.order)
                item.is_active = request.POST.get('is_active') == 'on'
                item.save()
                messages.success(request, 'Testimonial saved.')
            elif request.POST.get('new_item'):
                Testimonial.objects.create(
                    patient_name=request.POST.get('new_patient_name', ''),
                    content=request.POST.get('new_content', ''),
                    designation=request.POST.get('new_designation', 'Patient'),
                    avatar_color=request.POST.get('new_avatar_color', 'primary'),
                    order=Testimonial.objects.count(),
                )
                messages.success(request, 'New testimonial added.')

        elif action == 'delete_testimonial':
            Testimonial.objects.filter(id=request.POST.get('item_id')).delete()
            messages.success(request, 'Testimonial deleted.')

        elif action == 'contact_info':
            item_id = request.POST.get('item_id')
            if item_id:
                item = ContactInfo.objects.get(id=item_id)
                item.label = request.POST.get('label', item.label)
                item.value = request.POST.get('value', item.value)
                item.value_2 = request.POST.get('value_2', item.value_2)
                item.icon = request.POST.get('icon', item.icon)
                item.order = request.POST.get('order', item.order)
                item.is_active = request.POST.get('is_active') == 'on'
                item.save()
                messages.success(request, 'Contact info saved.')

        elif action == 'article':
            item_id = request.POST.get('item_id')
            if item_id:
                item = HealthArticle.objects.get(id=item_id)
                item.title = request.POST.get('title', item.title)
                item.summary = request.POST.get('summary', item.summary)
                item.icon = request.POST.get('icon', item.icon)
                item.is_published = request.POST.get('is_published') == 'on'
                item.save()
                messages.success(request, 'Health article saved.')
            elif request.POST.get('new_item'):
                HealthArticle.objects.create(
                    title=request.POST.get('new_title', ''),
                    summary=request.POST.get('new_summary', ''),
                    content=request.POST.get('new_summary', ''),
                    icon=request.POST.get('new_icon', 'bi bi-heart-pulse-fill'),
                )
                messages.success(request, 'New health article added.')

        elif action == 'delete_article':
            HealthArticle.objects.filter(id=request.POST.get('item_id')).delete()
            messages.success(request, 'Health article deleted.')

        return redirect(request.path)

    context = {
        'site': site,
        'hero': hero,
        'why_choose_items': WhyChooseItem.objects.all().order_by('order'),
        'service_categories': ServiceCategory.objects.all().order_by('order').prefetch_related('items'),
        'departments': Department.objects.all().order_by('order'),
        'statistics': Statistic.objects.all().order_by('order'),
        'testimonials': Testimonial.objects.all().order_by('order'),
        'contact_infos': ContactInfo.objects.all().order_by('order'),
        'articles': HealthArticle.objects.all().order_by('-published_at'),
        'title': 'Landing Page Settings',
    }
    return render(request, 'admin/dashboard/landing_settings.html', context)
