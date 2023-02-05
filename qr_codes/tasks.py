import os
import shutil
import zipfile
from io import BytesIO
from tempfile import TemporaryDirectory

from django.apps import apps
from django.conf import settings
from application.celery import app

from utils.storage_class import DiskStorage, CloudStorage
from qr_codes.utils import generate_qr
from utils.mail import Email


def save_to_memory(tags, qr_group) -> str:
    '''Saves images to memory and creates zipfile'''
    storage = DiskStorage(settings.DEFAULT_STORAGE_PATH)
    filename = f'{qr_group.name.replace(" ", "-")}-{qr_group.product.name.replace(" ", "-")}.zip'

    file = BytesIO()

    with zipfile.ZipFile(file, 'w', compression=zipfile.ZIP_DEFLATED) as images_zip:
        for tag in iter(tags):

            text = f'{settings.SITE_URL}/api/qrs/tags/{tag[0]}/'
            zeros = qr_group.zeros - len(str(tag[1]))
            img_name = f'{qr_group.prefix} {"0"*zeros}{tag[1]} {qr_group.suffix}.png'

            img = generate_qr(text, qr_group.logo)
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')

            images_zip.writestr(img_name, img_buffer.getvalue())

    file_path = storage.save_zip(file, filename)
    return file_path


def save_to_disk(tags, qr_group) -> str:
    '''Saves images to temp directory and makes zipfile'''
    file_name = f'{qr_group.name.replace(" ", "-")}-{qr_group.product.name.replace(" ", "-")}'
    tmp_path = settings.DEFAULT_STORAGE_PATH+file_name

    with TemporaryDirectory() as temp_dir:
        for tag in tags:
            text = f'{settings.SITE_URL}/api/qrs/tags/{tag[0]}/'
            zeros = qr_group.zeros - len(str(tag[1]))
            img_name = f'{qr_group.prefix} {"0"*zeros}{tag[1]} {qr_group.suffix}.png'

            img = generate_qr(text, qr_group.logo)
            img_path = os.path.join(temp_dir, img_name)
            img.save(img_path, format='PNG')

        shutil.make_archive(tmp_path, 'zip', temp_dir)

    tmp_path = tmp_path + '.zip'
    return tmp_path


@app.task
def save_qr_to_zip(qr_group_id: int, email_text: str) -> None:
    cloud = CloudStorage('https://transfer.sh/')
    QRGroup = apps.get_model('qr_codes', 'QRGroup')
    qr_group = QRGroup.objects.get(id=qr_group_id)

    tags = qr_group.nfc_tags.all().values_list('hw_id', 'serial_num')
    link = qr_group.create_link()

    if len(tags) > 10000: # If you have enough memory, why not?)
        url = save_to_disk(tags, qr_group)
    else:
        url = save_to_memory(tags, qr_group)

    file_name = url.split('/')[-1]
    file_link = cloud.save_zip(file_name=file_name, url=url, ttl=1)
    link.url = file_link
    link.save()
    email = Email(email_text, content=file_link)
    email.send()