import random
import string


def send_verification_code(user_email, length=6):

    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    send_mail(
        "verification in the amir social media",
        f"this is your verification code babe : {code}",
        "amirhossein.khalili.supn@gmail.com",
        [user_email],
        fail_silently=False,
    )

    return code
