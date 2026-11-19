from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm, PerfilForm
from .models import Usuario, Perfil


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)   

        if form.is_valid():
            usuario = form.save()
            Perfil.objects.get_or_create(usuario=usuario)  # Crear perfil automáticamente al registrar usuario
            login(request, usuario)  # Iniciar sesión automáticamente después del registro
            return redirect("inicio")  # Redirigir a la página de inicio después del registro
    else:
        form = RegistroForm()

    return render(request, "cuentas/registro.html", {"form": form})

@login_required
def perfil(request):
    if request.method == "POST":
        form = PerfilForm(
            request.POST,
            request.FILES,
            instance=request.user.perfil

        )

        if form.is_valid():
            form.save()
            return redirect("perfil")

    else:
        form = PerfilForm(instance=request.user.perfil)

    return render(request, "cuentas/perfil.html", {"form": form})


