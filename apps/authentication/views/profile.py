import sweetify
from django.shortcuts import render
from django_email_verification import send_email

from django.contrib.auth import get_user_model

User = get_user_model()

def user_profile(request):
    if request.method == "POST":
        try:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            username = request.POST.get('username')

            is_username_updated = False
            is_new_username_exists = False
            is_password_updated = False
            is_password_error = False

            user = request.user

            if username and username != user.username:
                if User.objects.filter(username=username).exists():
                    is_new_username_exists = True
                else:
                    user.username = username
                    user.is_email_verified = False
                    user.save()
                    send_email(user)
                    is_username_updated = True

            if password1 or password2:
                if password1 != password2:
                    is_password_error = True
                else:
                    user.set_password(password1)
                    user.save(update_fields=['password'])
                    is_password_updated = True

            if is_new_username_exists:
                sweetify.error(
                    request,
                    title='Error al actualizar el perfil',
                    text='El email ya está en uso. Por favor, escoge otro o autenticate con él',
                    showConfirmButton=True,
                    timer=10000,
                    icon='error'
                )
            elif is_password_error:
                sweetify.error(
                    request,
                    title='Error al actualizar el perfil',
                    text='Las contraseñas no coinciden. Por favor, inténtalo de nuevo.',
                    showConfirmButton=True,
                    timer=10000,
                    icon='error'
                )
            elif is_username_updated and is_password_updated:
                sweetify.success(
                    request,
                    title='¡Perfil actualizado!',
                    text='Email y contraseña actualizados correctamente.',
                    showConfirmButton=True,
                    timer=10000,
                    icon='success'
                )
            elif is_username_updated:
                sweetify.success(
                    request,
                    title='¡Perfil actualizado!',
                    text='Email actualizado correctamente.',
                    showConfirmButton=True,
                    timer=10000,
                    icon='success'
                )
            elif is_password_updated:
                sweetify.success(
                    request,
                    title='¡Perfil actualizado!',
                    text='Contraseña actualizada correctamente.',
                    showConfirmButton=True,
                    timer=10000,
                    icon='success'
                )
            else:
                sweetify.info(
                    request,
                    title='Sin cambios',
                    text='No se realizaron cambios en el perfil.',
                    showConfirmButton=True,
                    timer=10000,
                    icon='info'
                )
        except Exception as e:
            sweetify.error(
                request,
                title='Error al actualizar el perfil',
                text=str(e),
                showConfirmButton=True,
                timer=10000,
                icon='error'
            )
    return render(request, "profile/edit-user.html", {"segment": "profile"})
