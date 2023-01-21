import mail

if __name__ == '__main__':

    # Create an email object
    mail_obj = mail.EMAIL(host='EMAIL_SERVER', sender_addr='SENDER_ADDRESS', pwd='PASSWORD', sender_name='SENDER')

    # Set the receiver list
    mail_obj.set_receiver('RECEIVER_ADDRESS')

    # New an email
    mail_obj.new_mail(subject='Demo', encoding='utf-8')

    # Write content
    mail_obj.add_text(content='Test the script')

    # Construct an image list for test
    imgs = [
        'figures/1.jpg',
        'figures/2.jpg'
    ]

    # Attach images
    mail_obj.attach_images(imgs)

    # Attach files
    mail_obj.attach_files(imgs)

    # Send the email
    mail_obj.send_mail()
