import os

def check_format(mail_addr):
    """
    Check an email address whether a valid address
    :param mail_addr: str, the email address needs to be checked
    :return: True or raise ValueError
    """
    import re

    assert isinstance(mail_addr, str)

    mail_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(mail_regex, mail_addr):
        return True
    else:
        raise ValueError('{} is not a valid email address. Please check your input!'.format(mail_addr))


def file_size(file_path):
    """
    Returns the file size in MB unit
    :param file_path: the file's path
    :return: the file size in MB unit
    """
    return os.stat(file_path).st_size / 2 ** 20


def check_attach_size(attach_size, limited_size=5):
    """
    Check the size of attaches,
    if it is over the limited size, return -1
    :param attach_size: the total size of attaches in MB unit
    :param limited_size: Maximum size of attachments for a single email
    :return: status code: -1 for overflow, or 1 for feasible
    """

    if attach_size >= limited_size:
        return -1
    else:
        return 1


def compress_image(img_src, quality=75):
    """
    Compressing images
    :param img_src: str, image source address
    :param quality: int, should be in [1-100], wuality of image compression
    :return: temporary storage address of images
    """
    import PIL
    from PIL import Image

    # if path isn't an image file, return
    if os.path.isdir(img_src) or not img_src.split('.')[-1:][0] in ['png', 'jpg', 'jpeg']:
        return

    img_name = os.path.basename(img_src)
    img_dst = 'tmp_{}.{}'.format(img_name.split('.')[:-1][0], img_name.split('.')[-1:][0])

    # load the image to progressive
    img = Image.open(img_src)

    img_format = img_src.split('.')[-1:][0] if img_src.split('.')[-1:][0] != 'jpg' else 'JPEG'

    # temp save the compressed image
    try:
        img.save(img_dst, img_format, quality=quality, optimize=True, progressive=True)
    except IOError:
        PIL.ImageFile.MAXBLOCK = img.size[0] * img.size[1]
        img.save(img_dst, img_format, quality=quality, optimize=True, progressive=True)

    return img_dst


def package_files(files, zip_name='tmp', save_path='./', format='zip'):
    import zipfile

    zip_path = os.path.join(save_path, '{}.{}'.format(zip_name, format))

    zip_obj = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        zip_obj.write(file)

    zip_obj.close()

    return zip_path

