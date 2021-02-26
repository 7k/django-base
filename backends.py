import logging
import requests

from django.contrib.auth.backends import RemoteUserBackend
from django.conf import settings


SUPERUSER_EMAILS = getattr(settings, 'CLOUDFLARE_ACCESS_BACKEND_SUPERUSER_EMAILS', [])
CF_ACCESS_URL = getattr(settings, 'CLOUDFLARE_ACCESS_BACKEND_IDENTITY_URL', None)


class CloudFlareAccessUserBackend(RemoteUserBackend):
    create_unknown_user = True

    def authenticate(self, request, remote_user):
        if remote_user == '(null)':
            remote_user = request.META.get('Cf-Access-Claim-Common-Name', 'service-user')

        user = super(CloudFlareAccessUserBackend, self).authenticate(request, remote_user)

        return user

    def configure_user(self, request, user):
        user = super(CloudFlareAccessUserBackend, self).configure_user(request, user)

        email = request.META.get('HTTP_CF_ACCESS_CLAIM_EMAIL', None)
        token = request.META.get('HTTP_CF_ACCESS_JWT_ASSERTION', None)

        if token is not None and CF_ACCESS_URL is not None:
            r = requests.get(CF_ACCESS_URL, cookies={'CF_Authorization': token})
            if r.status_code == 200:
                info = r.json()
                logging.info(f'CF : {info}')

                name = info.get('name', None)
                if name is not None:
                    names = name.split()
                    if len(names) > 0:
                        user.first_name = names[0]
                    if len(names) > 1:
                        user.last_name = names[len(names) - 1]

                verified_email = info.get('email', None)
                if verified_email is not None:
                    if email is not None and email != verified_email:
                        logging.error('Email different from CF get-identity')
                    else:
                        if verified_email in SUPERUSER_EMAILS:
                            # We only allow auto superuser if the email address
                            # is from the identity info obtained using a signed JWT
                            user.is_superuser = True

                        email = verified_email
            else:
                logging.error(r.content)

        if email is not None:
            user.email = email

        user.is_staff = True

        user.save()

        return user
