from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .models import ContactInfo, ContactMessage


def contact(request):
    """
    Contact page. Office/contact details come from ContactInfo;
    department, university, and social links are already available
    everywhere via the profile context processor (Phase 2) — not
    duplicated here.

    Assumed ContactInfo model fields (singleton, like Profile):
      email             — EmailField
      phone             — CharField, blank=True
      office_location   — CharField, blank=True
      office_hours      — CharField, blank=True (free text — e.g.
                           "Mon & Wed, 2–4 PM, or by appointment")
      map_embed_url     — URLField, blank=True (a Google Maps
                           embed src; if blank, the template shows
                           a static placeholder instead of an iframe)
    """
    context = {'contact_info': ContactInfo.objects.first()}
    return render(request, 'contact/contact.html', context)


def contact_submit(request):
    """
    Handles the contact form POST. Template-only per the brief —
    no email sending, no persistence. Just acknowledges the
    submission and redirects back (redirect-after-POST avoids a
    duplicate submission on page refresh).

    Whenever real delivery is wanted (email backend, or saving to
    a Message model), this is the one function that changes —
    nothing in the template needs to move.
    """
    if request.method == 'POST':
        # request.POST.get('name'), .get('email'), .get('subject'), .get('message')
        # are available here whenever real handling is added.
        messages.success(request, "Thanks for reaching out — your message has been received.")
    return redirect(reverse('contact:contact'))


def _get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


# ── POST: handle AJAX form submission ─────────────────────────────────────────
@require_POST
@csrf_protect
def contact_submith(request):
    """
    Accepts a JSON POST from Alpine's submitForm() fetch call.
    Returns JSON: { "ok": true } on success or { "ok": false, "errors": {...} } on failure.

    Alpine fetch call (already in the template's submitForm()):
        await fetch('/contact/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(this.form),
        });
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"ok": False, "errors": {"__all__": "Invalid request."}}, status=400)

    # ── Server-side validation ────────────────────────────────────────────────
    errors = {}

    name        = data.get("name", "").strip()
    email       = data.get("email", "").strip()
    affiliation = data.get("affiliation", "").strip()
    category    = data.get("category", "").strip()
    subject     = data.get("subject", "").strip()
    message     = data.get("message", "").strip()
    consent     = data.get("consent", False)

    if len(name) < 2:
        errors["name"] = "Please enter your full name."

    import re
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        errors["email"] = "Please enter a valid email address."

    if not category:
        errors["category"] = "Please select an enquiry type."

    if len(subject) < 5:
        errors["subject"] = "Please enter a subject (at least 5 characters)."

    if len(message) < 20:
        errors["message"] = "Please write a message of at least 20 characters."

    if not consent:
        errors["consent"] = "Please confirm your consent before submitting."

    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=422)

    # ── Save to database ──────────────────────────────────────────────────────
    msg = ContactMessage.objects.create(
        name        = name,
        email       = email,
        affiliation = affiliation,
        category    = category,
        subject     = subject,
        message     = message,
        consent     = consent,
        ip_address  = _get_client_ip(request),
    )


    try:
        context = {
            "msg": msg,
            "admin_message_url": f"{settings.SITE_URL}/admin/contact/contactmessage/{msg.pk}/change/",
            "admin_messages_list_url": f"{settings.SITE_URL}/admin/contact/contactmessage/",
        }
        html_body  = render_to_string("emails/admin_contact_notification_email.html", context)
        plain_body = f"New message from {msg.name} ({msg.email})\nSubject: {msg.subject}\n\n{msg.message}"

        email_obj = EmailMultiAlternatives(
            subject   = f"[MitchellLab Contact] {msg.subject}",
            body      = plain_body,
            from_email= settings.DEFAULT_FROM_EMAIL,
            to        = [settings.CONTACT_NOTIFICATION_EMAIL],
            reply_to  = [msg.email],
        )
        email_obj.attach_alternative(html_body, "text/html")
        email_obj.send()
    except Exception as e:
        print("Email failed:", e)
        return JsonResponse({"success": False, "error": str(e)})
        
    return JsonResponse({"ok": True})


