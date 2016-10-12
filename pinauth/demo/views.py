from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import pyotp

@login_required
def index(request):
    totp = pyotp.TOTP(request.user.psk.secret_key)
    context = {
        'qr_code': totp.provisioning_uri(name='{}@django-demo'.format(request.user.username)),
        'code': request.user.psk.secret_key,
    }
    return render(request, 'index.html', context=context)
