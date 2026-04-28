import os
import json
import tempfile
import requests
import time

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, ContactRequestForm


User = get_user_model()


PREFERENCE_DEFAULTS = {
    "dark_mode": False,
    "notifications": True,
    "show_timer": True,
    "shuffle_questions": False,
    "ai_explanation": True,
    "site_language": "kk",
}


def normalize_language_code(value):
    mapping = {
        "kk": "kk",
        "ru": "ru",
        "en": "en",
        "Қазақша": "kk",
        "Русский": "ru",
        "English": "en",
    }
    return mapping.get(value, "kk")


def get_user_preferences(request):
    if request.user.is_authenticated:
        return {
            "dark_mode": getattr(request.user, "dark_mode", False),
            "notifications": getattr(request.user, "notifications", True),
            "show_timer": getattr(request.user, "show_timer", True),
            "shuffle_questions": getattr(request.user, "shuffle_questions", False),
            "ai_explanation": getattr(request.user, "ai_explanation", True),
            "site_language": normalize_language_code(getattr(request.user, "site_language", "kk")),
        }
    return PREFERENCE_DEFAULTS.copy()


def build_page_context(request, extra=None):
    context = get_user_preferences(request)
    if extra:
        context.update(extra)
    return context


def home(request):
    return render(request, "accounts/index.html", build_page_context(request))


def guide_view(request):
    return render(request, "accounts/guide.html", build_page_context(request))


def downloads_view(request):
    return redirect("/courses/#materialsPanel")


def courses_view(request):
    return render(request, "accounts/courses.html", build_page_context(request))


def quiz_view(request):
    return render(request, "accounts/quiz.html", build_page_context(request))


@ensure_csrf_cookie
def ai_chat_view(request):
    return render(request, "accounts/ai_chat.html", build_page_context(request))


def get_demo_reply(user_message):
    return (
        "AI уақытша жауап бере алмады. "
        "GEMINI_API_KEY дұрыс қойылғанын тексеріңіз немесе кейін қайта сұрап көріңіз."
    )


@require_POST
def ai_web_chat_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"ok": False, "error": "Сұрақ бос."}, status=400)

        api_key = getattr(settings, "GEMINI_API_KEY", "").strip()

        if not api_key:
            return JsonResponse({
                "ok": True,
                "answer": "GEMINI_API_KEY орнатылмаған."
            })

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Сен EduMentor AI атты оқу көмекшісісің. "
                                "Қазақша қысқа әрі түсінікті жауап бер.\n\n"
                                f"Сұрақ: {user_message}"
                            )
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload, timeout=30)
        result = response.json()

        if response.status_code != 200:
            error_message = result.get("error", {}).get("message", "Gemini API қатесі шықты.")
            return JsonResponse({"ok": True, "answer": f"AI қатесі: {error_message}"})

        answer_text = result["candidates"][0]["content"]["parts"][0]["text"]

        return JsonResponse({"ok": True, "answer": answer_text})

    except Exception as e:
        return JsonResponse({"ok": True, "answer": f"AI қатесі: {str(e)}"})


def contact_view(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Сұранысыңыз қабылданды. Жақын арада сізбен байланысамыз.")
            return redirect("contact")
    else:
        form = ContactRequestForm()

    return render(request, "accounts/contact.html", build_page_context(request, {"form": form}))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Тіркелу сәтті өтті.")
            return redirect("home")
        else:
            messages.error(request, "Мәліметтерді дұрыс толтырыңыз.")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", build_page_context(request, {"form": form}))


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        username_or_email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                found_user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=found_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Қош келдіңіз!")
            return redirect("home")

        messages.error(request, "Username/email немесе құпия сөз қате.")

    return render(request, "accounts/login.html", build_page_context(request, {"form": form}))


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль жаңартылды.")
            return redirect("profile")
        else:
            messages.error(request, "Профиль мәліметтерін тексеріңіз.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = build_page_context(request, {
        "form": form,
        "xp": 320,
        "xp_percent": 53,
        "streak_days": 7,
        "completed_topics": 24,
        "accuracy": 71,
        "active_days": 7,
        "profile_fill": 76,
        "total_tests": 120,
        "weekly_progress": 68,
    })
    return render(request, "accounts/profile.html", context)


@login_required
def profile_progress_view(request):
    context = build_page_context(request, {
        "weekly_progress": 68,
        "completed_topics": 24,
        "accuracy": 71,
        "active_days": 7,
        "total_tests": 120,
    })
    return render(request, "accounts/profile_progress.html", context)


@login_required
def profile_grants_view(request):
    context = build_page_context(request, {
        "user_score": 80,
        "max_score": 140,
    })
    return render(request, "accounts/profile_grants.html", context)


@login_required
def profile_leaderboard_view(request):
    context = build_page_context(request, {})
    return render(request, "accounts/profile_leaderboard.html", context)


@login_required
def profile_settings_view(request):
    if request.method == "POST":
        request.user.dark_mode = request.POST.get("dark_mode") == "on"
        request.user.notifications = request.POST.get("notifications") == "on"
        request.user.show_timer = request.POST.get("show_timer") == "on"
        request.user.shuffle_questions = request.POST.get("shuffle_questions") == "on"
        request.user.ai_explanation = request.POST.get("ai_explanation") == "on"
        request.user.site_language = normalize_language_code(request.POST.get("site_language", "kk"))

        request.user.save(update_fields=[
            "dark_mode",
            "notifications",
            "show_timer",
            "shuffle_questions",
            "ai_explanation",
            "site_language",
        ])

        messages.success(request, "Баптаулар сәтті сақталды.")
        return redirect("profile_settings")

    return render(request, "accounts/profile_settings.html", build_page_context(request))


def progress_view(request):
    return render(request, "accounts/progress.html", build_page_context(request))


@csrf_exempt
def transcribe_audio(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "POST method required"}, status=405)

    audio_file = request.FILES.get("audio")
    if not audio_file:
        return JsonResponse({"ok": False, "error": "Audio file not found"}, status=400)

    suffix = os.path.splitext(audio_file.name)[1] or ".webm"

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name

        return JsonResponse({
            "ok": True,
            "text": "Сәлем, бұл дауыстық хабардың demo мәтіні."
        })

    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

    finally:
        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)