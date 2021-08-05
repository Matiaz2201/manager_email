#coding:utf-8

import os
import smtplib
import email.mime.application
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError, SMTPDataError

# Descrição dos parametros
'''
    Descrição dos parametros

    smtp_server = Servidor SMTP do e-mail que será utilizado para fazer o envio
    Exemplo smtp_server = smtp.gmail.com

    destinatarios = lista de e-mails a receberem o e-mail enviado
    Exemplo destinatarios = ['meuamigo@gmail.com']

    remetente_email = e-mail que vai ser usado para logar no servidor SMTP e fazer o envio
    Exemplo remetente_email = 'meuemail@gmail.com'

    assunto = assunto do e-mail
    Exemplo assunto = 'Teste manager_email'

    remetente_password = senha do e-mail que vai ser usado para logar no servidor SMTP e fazer o envio
    Exemplo remetente_password = 'senha123*'

    texto = texto que vai no corpo do e-mail em html
    Exemplo texto = '<p>Esse é o texto do meu e-mail de teste</p>'

    path_assinatura = path da do arquivo da assinatura em html
    Exemplo path_assinatura = assinatura.html

    path_anexo = lista com anexos do e-mail
    Exemplo path_anexo = ['anexos/anexo1.pdf', 'anexos/anexo2.txt']

'''

class Email:

    def __init__(self, smtp_server, port, destinatarios, remetente_email, assunto, remetente_password, texto, path_assinatura=None, path_anexo=None, **kwargs):
        self.smtp_server = smtp_server
        self.port = port
        self.destinatarios = destinatarios
        self.remetente_email = remetente_email
        self.assunto = assunto
        self.remetente_password = remetente_password
        self.texto = texto
        self.path_assinatura = path_assinatura
        self.path_anexo = path_anexo
        self.kwargs = kwargs
        self.msg = ''
    
    def anexos(self):
        for anexo in self.path_anexo:
            path_base = os.path.dirname(os.path.abspath(__file__))
            path_final = os.path.join(path_base, anexo)
            fp = open(path_final, 'rb')
            attachment = email.mime.application.MIMEApplication(fp.read(), _subtype=anexo.split('.')[-1])
            fp.close()

            attachment.add_header('Content-Disposition', 'attachment', filename=anexo.split('/')[-1])
            self.msg.attach(attachment)

    def montar_email(self):
        subject = self.assunto
        email_from = self.remetente_email

        for email_destino in self.destinatarios:
            if self.destinatarios.index(email_destino) == 0:
                email_to = email_destino
            else:
                email_to = email_to  + ',' + email_destino

        table_html = self.texto

        self.msg = MIMEMultipart()
        self.msg['Subject'] = subject
        self.msg['From'] = email_from
        self.msg['To'] = email_to

        path_base = os.path.dirname(os.path.abspath(__file__))
        path_final = os.path.join(path_base, self.path_assinatura)
        
        try:
            with open(path_final, "r") as file:
                file_read = file.read()
                file_edit = file_read.format(table_html=table_html)

            body = MIMEText(file_edit, "html")
            self.msg.attach(body)

        except Exception as e:
            print(e)

    def enviar_email(self):
        user_email = self.remetente_email
        user_password = self.remetente_password
        smtp_url = self.smtp_server
        smtp_port = self.port
        send_email = False
        try:
            s = smtplib.SMTP(smtp_url, smtp_port)
            s.ehlo()
            s.starttls()
            s.login(user_email, user_password)
            s.send_message(self.msg)
            s.quit()
            send_email = True
        except SMTPAuthenticationError as e:
            print(f'''Erro ao fazer login no servidor SMTP''')
            send_email=False
            return send_email

        except SMTPDataError as e:
            print(f'''Erro com os dados do e-mail ''')
            send_email=False
            return send_email

        except Exception as e:
            print(f'''Erro inesperado com o envio do E-mail ''')
            send_email=False
            return send_email

        return send_email

    def process(self):

        self.montar_email()

        if len(self.path_anexo) != 0:
            self.anexos()

        send = self.enviar_email()

        return send

if __name__ == '__main__':
    pass
