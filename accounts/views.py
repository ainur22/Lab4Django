import os
import json
import tempfile

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib import messages

from openai import OpenAI

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, ContactRequestForm


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def home(request):
    return render(request, 'accounts/index.html')


def guide_view(request):
    return render(request, 'accounts/guide.html')


def downloads_view(request):
    return render(request, 'accounts/downloads.html')


def courses_view(request):
    return render(request, 'accounts/courses.html')


def quiz_view(request):
    return render(request, 'accounts/quiz.html')


@ensure_csrf_cookie
def ai_chat_view(request):
    return render(request, 'accounts/ai_chat.html')


@require_POST
def ai_web_chat_api(request):
    client = get_openai_client()
    if client is None:
        return JsonResponse({
            'ok': False,
            'error': 'OPENAI_API_KEY орнатылмаған'
        }, status=500)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({
                'ok': False,
                'error': 'Сұрақ бос.'
            }, status=400)

        response = client.responses.create(
            model='gpt-5.4-mini',
            instructions=(
                "Сен EduMentor AI атты білім беру көмекшісісің. "
                "Пайдаланушыға қазақ тілінде жауап бер. "
                "Жауап қысқа, нақты, түсінікті болсын. "
                "Егер интернеттен ақпарат алынса, жауапта дереккөздерге қысқаша сілтеме бер."
            ),
            input=user_message,
            tools=[
                {
                    "type": "web_search"
                }
            ]
        )

        answer_text = getattr(response, 'output_text', '').strip()

        if not answer_text:
            try:
                parts = []
                for item in response.output:
                    if getattr(item, 'type', '') == 'message':
                        for content in getattr(item, 'content', []):
                            if getattr(content, 'type', '') == 'output_text':
                                parts.append(getattr(content, 'text', ''))
                answer_text = "\n".join(parts).strip()
            except Exception:
                answer_text = ""

        if not answer_text:
            answer_text = "Кешір, қазір жауапты шығару мүмкін болмады."

        return JsonResponse({
            'ok': True,
            'answer': answer_text
        })

    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)


def progress_view(request):
    return render(request, 'accounts/progress.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Сұранысыңыз қабылданды. Жақын арада сізбен байланысамыз.'
            )
            return redirect('contact')
    else:
        form = ContactRequestForm()

    return render(request, 'accounts/contact.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = 'Пайдаланушы аты немесе құпия сөз қате.'
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@csrf_exempt
def transcribe_audio(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST method required'}, status=405)

    client = get_openai_client()
    if client is None:
        return JsonResponse({
            'ok': False,
            'error': 'OPENAI_API_KEY орнатылмаған'
        }, status=500)

    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'ok': False, 'error': 'Audio file not found'}, status=400)

    suffix = os.path.splitext(audio_file.name)[1] or '.webm'

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name

        with open(temp_path, 'rb') as f:
            transcript = client.audio.transcriptions.create(
                model='gpt-4o-mini-transcribe',
                file=f
            )

        text = getattr(transcript, 'text', '').strip()

        return JsonResponse({
            'ok': True,
            'text': text
        })

    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)

    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)