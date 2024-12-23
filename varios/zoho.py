import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def message(
    address_send, subject="Python Notification", text="", img=None, attachment=None
):
    # build message contents
    msg = MIMEMultipart()
    msg["Subject"] = subject  # add in the subject
    msg.attach(MIMEText(text))  # add text contents

    # comprobar si tenemos algo dado en el parámetro img
    if img is not None:
        # si lo hacemos, queremos iterar a través de las imágenes, así que comprobemos eso
        # lo que tenemos en realidad es una lista
        if type(img) is not list:
            img = [img]  # Si no es una lista, hazla una
        # ahora iterar a través de nuestra lista
        for one_img in img:
            img_data = open(
                one_img, "rb"
            ).read()  # leer los datos binarios de la imagen
            # adjuntamos los datos de la imagen a MIMEMultipart usando MIMEImage, agregamos
            # el nombre de archivo dado usa os.basename
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

    # hacemos lo mismo con los archivos adjuntos que con las imágenes
    if attachment is not None:
        if type(attachment) is not list:
            attachment = [attachment]  # Si no es una lista, hazla una

        for one_attachment in attachment:
            with open(one_attachment, "rb") as f:
                # read in the attachment using MIMEApplication
                file = MIMEApplication(f.read(), name=os.path.basename(one_attachment))
            # aquí editamos los metadatos del archivo adjunto
            file["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(one_attachment)}"'
            )
            msg.attach(file)  # finally, add the attachment to our message object

    # Create server object with SSL option
    # Change below smtp.zoho.com, corresponds to your location in the world.
    # For instance smtp.zoho.eu if you are in Europe or smtp.zoho.in if you are in India.
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)

    # Perform operations via server
    server.login("jdorantes@bantel.net.ve", "V183291145*")
    server.sendmail("jdorantes@bantel.net.ve", address_send, msg.as_string())
    server.quit()
    print("Correo enviado.")
