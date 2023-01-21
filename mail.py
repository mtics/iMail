import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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


class EMAIL(object):

    def __init__(self, host, sender_addr, pwd, sender_name='no_reply', port=25):

        # First check whether the sender's address is valid
        check_format(sender_addr)

        # Set the sender info
        self.sender_info = {
            'host': host,  # specify the mail server
            'port': port,  # specify the port to connect
            'address': sender_addr,  # set your email address
            'pwd': pwd,  # set the password or authorization code
            'sender': sender_name  # set the nickname of the sender
        }

        # Specify a list of receiver addresses
        self.receivers = []

        self.msg = None

    def set_receiver(self, receiver):
        """
        Set the receivers, which is a list
        :param receiver: str or list
        :return:
        """

        # First check whether the address valid
        # If valid, add it to the list
        # else raise error
        if isinstance(receiver, str):
            check_format(receiver)
            self.receivers.append(receiver)
        elif isinstance(receiver, str):
            for addr in receiver:
                check_format(addr)
            self.receivers.extend(receiver)
        else:
            raise TypeError('set_receiver() only accepts str type or string type')

    def new_mail(self, subject='Subject', encoding='utf-8'):
        # New an email

        self.msg = MIMEMultipart('related')  # 'related' allows to use many formats
        self.msg['From'] = '{}<{}>'.format(self.sender_info['sender'], self.sender_info['address'])
        self.msg['Subject'] = Header(subject, encoding)

        to_list = ''
        for receiver in self.receivers:
            to_list += receiver + ','

        self.msg['To'] = to_list

    def add_text(self, content='', subtype='plain', encoding='utf-8'):
        self.msg.attach(MIMEText(content, subtype, encoding))

    def attach_images(self, images, compressed=True, quality=75):

        images = [images] if isinstance(images, str) else images

        for image in images:

            image = compress_image(image, quality) if compressed else image

            self._attach_image(image)

            if compressed:
                os.remove(image)

    def _attach_image(self, image_path):

        image_data = open(image_path, 'rb')
        msg_image = MIMEImage(image_data.read())
        image_data.close()

        msg_image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))

        self.msg.attach(msg_image)

    def attach_files(self, file_paths, limited_size=5, zip_name='tmp.zip', zip_path='./'):

        file_paths = [file_paths] if isinstance(file_paths, str) else file_paths

        zip_path = package_files(file_paths, zip_name=zip_name, save_path=zip_path)

        if check_attach_size(file_size(zip_path), limited_size) == -1:
            self.add_text(content='Attachment size exceeded the maximum limit and could not be uploaded!')
        else:
            attachment = MIMEApplication(open(zip_path, 'rb').read())
            attachment.add_header('Content-Disposition', 'attachment', filename=zip_name)
            self.msg.attach(attachment)

        os.remove(zip_path)

    def send_mail(self):
        try:
            stp = smtplib.SMTP()

            stp.connect(self.sender_info['host'], self.sender_info['port'])

            stp.login(self.sender_info['address'], self.sender_info['pwd'])

            stp.sendmail(self.sender_info['address'], self.receivers, self.msg.as_string())

            stp.quit()

            print('Sending email successfully!')

        except smtplib.SMTPException as e:
            print('SMTP Error', e)
