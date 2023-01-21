# -*- coding: UTF-8 -*-

# MIT License
#
# Copyright (c) 2023 Zhiwei Li (https://github.com/mtics)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from iMail.utils import *


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
