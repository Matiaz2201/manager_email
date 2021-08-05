#coding:utf-8


from manager_email import Email

def main():
    texto_email = """
                    <p>Prezado(a), Boa Tarde!</p>\n\n

                    <p>Este é meu teste de envio de e-mail com python</p>\n\n

                    <p>Atenciosamente</p>\n\n
                    <br />
                    <br />

                """

    email_object = Email(
    smtp_server='SEU SERVIDOR SMTP', 
    port='PORTA DO SERVIDOR SMTP',
    destinatarios=['EMAIL DE DESTINO'],
    remetente_email='SUA CONTA DE E-MAIL',
    assunto='ASSUNTO DO EMAIL',
    remetente_password='SENHA DO SEU E-MAIL',
    texto=texto_email,
    path_assinatura='assinatura.html',
    path_anexo=['anexos/anexo1.pdf', 'anexos/anexo2.txt'],
    )

    if email_object.process():
        print('E-mail enviado com sucesso')

if __name__ == '__main__':
        main()
