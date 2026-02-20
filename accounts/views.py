from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

import uuid
import requests

app_name = "accounts"

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Chemin vers votre templ    ate
    redirect_authenticated_user = True 
    next_page = reverse_lazy('list')


def logout_user(request):
    logout(request)
    return redirect('accounts:login')

class SignUpView(CreateView):
    form_class = UserCreationForm  # Formulaire intégré pour la création d'utilisateur
    success_url = reverse_lazy('accounts:login')  # Redirige vers la page de connexion après inscription
    template_name = 'accounts/signup.html'  # Template pour l'inscription


# France connect

FC_BASE = "https://fcp.integ01.dev-franceconnect.fr/api/v1"

CLIENT_ID = "211286433e39cce01db448d80181bdfd005554b19cd51b3fe7943f6b3b86ab6e"
CLIENT_SECRET = "2791a731e6a59f56b6b4dd0d08c9b1f593b5f3658b9fd731cb24248e2669af4b"

# Django doit tourner sur un port autorisé (3000, 4242, 8080, 1337)
REDIRECT_URI = "http://localhost:3000/callback"
POST_LOGOUT_REDIRECT = "http://localhost:3000/logout"


def fc_login(request):
    state = uuid.uuid4().hex
    nonce = uuid.uuid4().hex

    request.session["fc_state"] = state
    request.session["fc_nonce"] = nonce

    authorize_url = (
        f"{FC_BASE}/authorize?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=openid%20profile&"  
        f"state={state}&"
        f"nonce={nonce}"
    )

    print("Redirecting to FranceConnect with URL:", authorize_url)
    return redirect(authorize_url)

def fc_callback(request):
    code = request.GET.get("code")

    # 1) Échange du code contre un token
    token_response = requests.post(
        f"{FC_BASE}/token",
        data={
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
        }
    ).json()

    access_token = token_response.get("access_token")

    # 2) Récupération des infos utilisateur
    userinfo = requests.get(
        f"{FC_BASE}/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    sub = userinfo.get("sub")  # identifiant unique FranceConnect

    # 3) Création automatique du compte si nécessaire
    user, created = User.objects.get_or_create(username=sub)

    if created:
        import secrets
        random_password = secrets.token_urlsafe(16)
        user.set_password(random_password)
        user.save()

    # 4) Connexion automatique
    login(request, user)

    return redirect("watchlist")

def fc_logout(request):
    logout(request)
    logout_url = (
        f"{FC_BASE}/logout?"
        f"post_logout_redirect_uri={POST_LOGOUT_REDIRECT}"
    )
    return redirect(logout_url)
