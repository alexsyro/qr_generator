from random import randint
import qrcode
from PIL import Image

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def generate_qr(
    text: str,
    logo: Image=None,
    size: int=settings.DEFAULT_QR_SIZE,
    color: str=settings.DEFAULT_QR_COLOR,
) -> Image:

    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    QRcode.add_data(text)
    QRcode.make()
    QRcolor = color
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')

    if logo:
        logo = Image.open(logo)
        logo.thumbnail((size, size), Image.ANTIALIAS)

        pos = ((QRimg.size[0] - logo.size[0]) // 2,
            (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)
    return QRimg


def generate_identifier(length=5):
    rand_id = lambda: randint(0, len(ALPHA)-1)
    result = [ALPHA[rand_id()] for _ in range(0, length)]
    return ''.join(result)


def generate_password(length=20):
    '''Actually almost useless.'''
    return BaseUserManager().make_random_password(length)
