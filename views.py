# signatures/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Signature
from PIL import Image
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

# Function to calculate similarity between images
def calculate_similarity(image1, image2):
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
    image1_resized = cv2.resize(image1_gray, (image2_gray.shape[1], image2_gray.shape[0]))
    similarity = ssim(image1_resized, image2_gray)
    return similarity

@login_required
def verify_signature(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('signature_image')
        if uploaded_image:
            image = Image.open(uploaded_image)
            image_data = np.array(image)
            best_match = None
            best_similarity = 0
            signatures = Signature.objects.all()
            if signatures.exists():
                for signature in signatures:
                    stored_image = Image.open(signature.signature_image)
                    stored_image_data = np.array(stored_image)
                    similarity = calculate_similarity(image_data, stored_image_data)
                    if similarity > best_similarity:
                        best_match = signature
                        best_similarity = similarity
                if best_match and best_similarity >= 0.9:
                    return render(request, 'verification.html', {'result': {'match': True, 'similarity': best_similarity * 100}})
                else:
                    return render(request, 'verification.html', {'result': {'match': False, 'similarity': best_similarity * 100}})
            else:
                return render(request, 'verification.html', {'error': "No signatures found in the database."})
    return render(request, 'verification.html')

@login_required
def upload_signature(request):
    if request.method == 'POST':
        user = request.user
        signature_image = request.FILES.get('signature_image')
        signature, created = Signature.objects.get_or_create(user=user)
        if signature_image:
            signature.signature_image = signature_image
            signature.save()
        return redirect('verify_signature')
    return render(request, 'upload.html')

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('verify_signature')  # Redirect to the verification page
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing_page')

def landing_page(request):
    return render(request, 'landing.html')

def verification_page(request):
    return render(request, 'verification.html')