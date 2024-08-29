import qrcode
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from .forms import UserProfileForm
from .models import Profile
from django.contrib.auth.models import User
from io import BytesIO


def index(request):
    return render(request, "index.html")


def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {"profile": profile}
    return render(request, "profile.html", context)


def create_profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            print(form)
            profile = form.save(commit=False)
            profile.save()

            # Generate the QR code
            profile_url = request.build_absolute_uri(profile.get_absolute_url())
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(profile_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code image to a file-like object
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Save the image in the Profile model's `qr_code` field
            profile.qr_code_image.save(
                f"{profile.user.username}_qr.png", ContentFile(buffer.read()), save=True
            )

            # Redirect to the newly created profile page
            return redirect("profile", username=profile.user.username)
    else:
        form = UserProfileForm()

    return render(request, "create_profile.html", {"form": form})
