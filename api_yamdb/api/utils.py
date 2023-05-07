from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage


class ConfirmationCodeGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, '') or ''
        return f'{user.pk}{timestamp}{email}'

    def make_code(self, user):
        return super().make_token(user)

    def check_code(self, user, token):
        return super().check_token(user, token)


code_generator = ConfirmationCodeGenerator()


def send_mail(subject, body, to: list[str]):
    EmailMessage(subject, body, to=to).send()
