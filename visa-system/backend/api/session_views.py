from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def custom_login_view(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        if user.is_superuser:
            return redirect("/admin/")  # superuser -> Django admin
        return redirect("/dashboard")  # normal user -> Vue route

    return redirect("/login")  # invalid credentials -> back to Vue login


@require_http_methods(["POST"])
def custom_logout_view(request):
    logout(request)
    return redirect("/login")

