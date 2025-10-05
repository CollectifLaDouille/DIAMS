import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from typing import List, Type

import pandas as pd

from Configuration import Ids, PREFERRED, EMAIL, SELECTED_WORKSHOP, PARTICIPANT_NAME, DESCRIPTION
from WorkshopSlot import WorkshopSlot


class MailingMachine:

    PRIORITY_SUBJECT = "La Douille : Attribution des ateliers (accès prioritaire)"
    PRIORITY_BODY = f"""
<p>Salut, {{{PARTICIPANT_NAME}}} !</p>

<p>On a la grande joie de t&#39;annoncer que tu vas pouvoir participer à un atelier de la douille !</p>

<p><strong>Quelques précisions avant tout :</strong></p>

<ul style="line-height: 1.5;">
    <li><strong>Pour les ateliers :</strong> rendez-vous à <a href="https://www.google.com/maps?q=La+Friche+Lamartine,+21+rue+Saint-Victorien,+Lyon+3">La Friche Lamartine, 21 rue Saint-Victorien, Lyon 3</a>. Ouverture des portes dès 9h et jusqu&#39;à 18h.</li>
    <li><strong>Pour la soirée :</strong> rendez-vous samedi 11/10 à <a href="https://www.google.com/maps/place/11+Rue+Claudius+Pionchon,+69003+Lyon/">La Friche Lamartine, 11 rue Claudius Pionchon, Lyon 3</a> à partir de 18h (et jusqu&#39;à 23h).</li>
    <li><strong>La douille :</strong> est un festival à prix libre (entrée du festival, atelier auquel tu participes, soirée). La participation à prix libre sera en cash uniquement. L&#39;argent récolté nous sert à acheter le matériel, défrayer les animateur·trices venant de loin et faire  vivre le festival d&#39;année en année !</li>
    <li><strong>Les ateliers :</strong> ont un nombre de places limité, mais en tant qu'animateur·ice/organisateur·ice, ta place en tant que participant·e est validée d'office ! Si d'ici le festival tes disponibilités changent et tu ne peux plus participer à l'atelier auquel tu es inscrit·e, on te demande de bien penser à te désinscrire pour céder ta place, soit en cliquant ici : <p><a href="mailto:inscriptions-ladouille@mailo.com?subject=Desinscription&body=Bonjour, je ne pourrai finalement pas participer à mon atelier à la Douille, je me désinscris et cède ma place à quelqu'un d'autre. Merci !">Désinscription</a></p> soit par simple retour de mail avec dans l&#39;objet <em>&quot;[Désinscription]&quot;</em>.</li>
    <li><strong>Certains ateliers :</strong> nécessitent de porter des  vêtements spécifiques ou d&#39;apporter quelque chose, merci donc de lire  attentivement le descriptif de ton atelier.</li>
    <li><strong>Merci de venir :</strong> au minimum <strong><em>15 minutes avant</em></strong> l&#39;heure de début de l&#39;atelier.</li>
    <li><strong>Accessibilité PMR :</strong> Le festival est accessible  PMR sauf pour les ateliers partir en itinérance, sécurité montagne, couture sac à pain, couture trousse, photo, couture cuir, et réparation petit électroménager. Si tu as un besoin spécifique d&#39;assistance, n&#39;hésite pas à nous écrire pour que nous puissions faciliter au mieux ta participation au festival.</li>
    <li><strong>Sur place :</strong> tu trouveras une <u>buvette</u> mais il n&#39;y aura pas de restauration le midi sur le site (sauf pour les bénévoles). Le samedi soir, il y aura une <u>cantine à prix libre</u> en plus de la buvette.</li>
    <li><strong>Bambinerie :</strong> Nous proposons une garde d&#39;enfants le <u>samedi et le dimanche de 10h à 13h</u>. Les enfants resteront sur le lieu du festival et auront accès à des activités adaptées à leur âge, afin de permettre aux parents de plus facilement participer à des ateliers sur le festival. La bambinerie est ouverte aux enfants à partir de 4 ans. Pour inscrire un enfant, merci de nous écrire un mail à <a href="mailto:contact-ladouille@mailo.com">contact-ladouille@mailo.com</a> avec dans l&#39;objet <em>&quot;[Bambinerie]&quot;</em>.</li>
</ul>


<div style="border: 2px solid #d63384; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
    <h2 style="color: #d63384;">{{{SELECTED_WORKSHOP}}}</h2>
    <p>{{{DESCRIPTION}}}</p>
</div> 


<p>A bientôt!</p>
<p>- La Douille</p>
    """

    STANDARD_SUBJECT = "La Douille : Attribution des ateliers"
    STANDARD_BODY = f"""
<p>Salut, {{{PARTICIPANT_NAME}}} !</p>

<p>On a la grande joie de t&#39;annoncer que tu vas pouvoir participer à un atelier de la douille !</p>

<h3>ATTENTION : Pour que ta place soit validée, il faut que tu envoies une <u>réponse à ce mail</u> pour confirmer ta venue, si possible avant mercredi 08/10. Sans mail de confirmation de ta part, ta place ne sera plus assurée.</h3>

<p>Quelques précisions avant tout :</p>
<ul style="line-height: 1.5;">
    <li><strong>Pour les ateliers :</strong> rendez-vous à <a href="https://www.google.com/maps?q=La+Friche+Lamartine,+21+rue+Saint-Victorien,+Lyon+3">La Friche Lamartine, 21 rue Saint-Victorien, Lyon 3</a>. Ouverture des portes dès 9h et jusqu&#39;à 18h.</li>
    <li><strong>Pour la soirée :</strong> rendez-vous samedi 11/10 à <a href="https://www.google.com/maps/place/11+Rue+Claudius+Pionchon,+69003+Lyon/">La Friche Lamartine, 11 rue Claudius Pionchon, Lyon 3</a> à partir de 18h (et jusqu&#39;à 23h).</li>
    <li><strong>La douille :</strong> est un festival à prix libre (entrée du festival, atelier auquel tu participes, soirée). La participation à prix libre sera en cash uniquement. L&#39;argent récolté nous sert à acheter le matériel, défrayer les animateur·trices venant de loin et faire  vivre le festival d&#39;année en année !</li>
    <li><strong>Les ateliers :</strong> ont un nombre de places limité, il faut donc que tu <u><strong><em>confirmes ta participation</em></strong></u> afin que ta place soit définitivement validée ! Tu peux confirmer ta place en cliquant ici : <p><a href="mailto:inscriptions-ladouille@mailo.com?subject=Confirmation%20de%20mon%20inscription&body=Bonjour, je confirme mon inscription à mon atelier à la Douille, merci !">Confirmation</a></p> ou par simple retour de mail. Sans confirmation de ta part, ta participation à l&#39;atelier ne sera pas assurée; tu pourras quand même venir sur le festival, profiter des activités en passage libre et tenter ta chance sur les places restées libres. Les places libres restantes resteront ouvertes aux <u>inscriptions sur place le jour de l&#39;atelier</u> sur un mode &quot;premier·e arrivé·e, premier·e servi·e&quot;. Si tu ne peux finalement pas venir à l'atelier sélectionner, merci de nous prévenir en cliquant ici : <p><a href="mailto:inscriptions-ladouille@mailo.com?subject=Désinscription&body=Bonjour, je ne pourrai finalement pas participer à mon atelier à la Douille, je me désinscris et cède ma place à quelqu'un d'autre. Merci !">Désinscription</a></p> ou par simple retour de mail. Si tu as confirmé ta place mais que tu te rends compte dans la semaine que tu ne pourras finalement pas être présent·e, on te demande de nous prévenir en nous envoyant un mail à <a href="mailto:inscriptions-ladouille@mailo.com">inscriptions-ladouille@mailo.com</a> avec dans l&#39;objet <em>&quot;[Désinscription]&quot;</em>.</li>
    <li><strong>Certains ateliers :</strong> nécessitent de porter des  vêtements spécifiques ou d&#39;apporter quelque chose, merci donc de lire  attentivement le descriptif de ton atelier.</li>
    <li><strong>Merci de venir :</strong> au minimum <strong><em>15 minutes avant</em></strong> l&#39;heure de début de l&#39;atelier.</li>
    <li><strong>Accessibilité PMR :</strong> Le festival est accessible  PMR sauf pour les ateliers partir en itinérance, sécurité montagne, couture sac à pain, couture trousse, photo, couture cuir, et réparation petit électroménager. Si tu as un besoin spécifique d&#39;assistance, n&#39;hésite pas à nous écrire pour que nous puissions faciliter au mieux ta participation au festival.</li>
    <li><strong>Sur place :</strong> tu trouveras une <u>buvette</u> mais il n&#39;y aura pas de restauration le midi sur le site (sauf pour les bénévoles). Le samedi soir, il y aura une <u>cantine à prix libre</u> en plus de la buvette.</li>
    <li><strong>Bambinerie :</strong> Nous proposons une garde d&#39;enfants le <u>samedi et le dimanche de 10h à 13h</u>. Les enfants resteront sur le lieu du festival et auront accès à des activités adaptées à leur âge, afin de permettre aux parents de plus facilement participer à des ateliers sur le festival. La bambinerie est ouverte aux enfants à partir de 4 ans. Pour inscrire un enfant, merci de nous écrire un mail à <a href="mailto:contact-ladouille@mailo.com">contact-ladouille@mailo.com</a> avec dans l&#39;objet <em>&quot;[Bambinerie]&quot;</em>.</li>
</ul>


<div style="border: 2px solid #d63384; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
    <h2 style="color: #d63384;">{{{SELECTED_WORKSHOP}}}</h2>
    <p>{{{DESCRIPTION}}}</p>
</div> 


<p>A bientôt!</p>
<p>- La Douille</p>
    """

    SAD_SUBJECT= "La Douille : C'est complet ! :("
    SAD_BODY = f"""
<p>Salut, {{{PARTICIPANT_NAME}}} !</p>

<p>Malheureusement, nous avons reçu plus de demandes que de places disponibles aux ateliers et nous n'avons pas pu t'attribuer une place parmi tes voeux d'ateliers.</p>
<p>Ce qui ne veut pas dire que tu ne peux pas venir au festival !</p>

<p>N'hésite pas à passer sur le site du festival pour :</p>
<ul>
    <li><strong>Certains ateliers :</strong>  en passage libre le samedi et le dimanche ouvert à tous·tes ! Et pour les ateliers nécessitant une inscription, on publiera la liste des places libres restantes avant l'ouverture du festival. Les places libres restantes resteront ouvertes aux <u>inscriptions sur place le jour de l&#39;atelier</u> sur un mode &quot;premier·e arrivé·e, premier·e servi·e&quot;. N'hésite pas à <a href="https://ladouille.org/planning/">consulter le programme</a> pour prévoir ta venue.</li>
    <li><strong>La soirée :</strong> du samedi à partir de 18h, il n'est pas nécessaire d'avoir participé à un atelier pour venir faire la teuf !</li>
    <li><strong>Bénévoler :</strong> si tu veux nous aider à faire vivre le festival et y participer d'une autre façon, tu peux <a href="https://framaforms.org/la-douille-inscriptions-benevolat-1757864209">t'inscrire ici</a> pour faire partie de l'équipe bénévole en donnant un peu de ton temps.</li>
</ul>

<p>Quelques précisions :</p>
<ul>
    <li><strong>Pour les ateliers :</strong> rendez-vous à <a href="https://www.google.com/maps?q=La+Friche+Lamartine,+21+rue+Saint-Victorien,+Lyon+3">La Friche Lamartine, 21 rue Saint-Victorien, Lyon 3</a>. Ouverture des portes dès 9h et jusqu&#39;à 18h.</li>
    <li><strong>Pour la soirée :</strong> rendez-vous samedi 11/10 à <a href="https://www.google.com/maps/place/11+Rue+Claudius+Pionchon,+69003+Lyon/">La Friche Lamartine, 11 rue Claudius Pionchon, Lyon 3</a> à partir de 18h (et jusqu&#39;à 23h).</li>
    <li><strong>La douille :</strong> est un festival à prix libre (entrée du festival, atelier auquel tu participes, soirée). La participation à prix libre sera en cash uniquement. L&#39;argent récolté nous sert à acheter le matériel, défrayer les animateur·trices venant de loin et faire  vivre le festival d&#39;année en année !</li>
    <li><strong>Sur place :</strong> tu trouveras une <u>buvette</u> mais il n&#39;y aura pas de restauration le midi sur le site (sauf pour les bénévoles). Le samedi soir, il y aura une <u>cantine à prix libre</u> en plus de la buvette.</li>
</ul>


<p>A bientôt!</p>
<p>- La Douille</p>
    """

    __ids = None
    __server = None
    __workshops = None


    def __init__(self, ids: Type[Ids], workshops: List[WorkshopSlot]):
        self.__ids = ids
        self.__server = None
        self.__workshops = workshops

        logging.basicConfig(filename='MailingMachine.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        return


    def __login(self):
        self.__server = smtplib.SMTP(self.__ids.SMTP_SERVER, self.__ids.SMTP_PORT)
        self.__server.starttls()
        self.__server.login(self.__ids.MAIL_ADDRESS, self.__ids.MAIL_PASSWORD)
        sleep(5)

    def __logout(self):
        self.__server.quit()

    def __send(self, subject: str, body: str, to_email: str) -> int:
        msg = MIMEMultipart()
        msg['From'] = self.__ids.mail_address
        msg['To'] = to_email
        msg['Subject'] = subject

        errors = 0
        try:
            msg.attach(MIMEText(body, 'html'))
            self.__server.send_message(msg)
            logging.info(f"Email successfully sent to {to_email}")
        except Exception as e:
            logging.error(f"Email failure ! {to_email}: {str(e)}")
            errors = 1

        return errors

    # https://stackoverflow.com/a/34325723
    @staticmethod
    def __progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iterable    - Required  : iterable object (Iterable)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        total = len(iterable)

        # Progress Bar Printing Function
        def printProgressBar(iteration):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)

        # Initial Call
        printProgressBar(0)
        # Update Progress Bar
        for i, item in enumerate(iterable):
            yield item
            printProgressBar(i + 1)
        # Print New Line on Complete
        print()


    def send_dataframe(self, dataframe: pd.DataFrame) -> int:
        self.__login()

        errors = 0
        for idx in MailingMachine.__progressBar(dataframe, prefix='Envoi en cours :'):
            p = dataframe[idx]
            w = WorkshopSlot.get_workshop_from_name(self.__workshops, p[SELECTED_WORKSHOP])

            if w is not None:
                if p[PREFERRED]:
                    subject = self.PRIORITY_SUBJECT
                    body = self.PRIORITY_BODY
                else:
                    subject = self.STANDARD_SUBJECT
                    body = self.STANDARD_BODY
                body = body.format(**p, **w.list)
            else:
                subject = self.SAD_SUBJECT
                body = self.SAD_BODY
                body = body.format(**p)

            errors += self.__send(subject, body, p[EMAIL])

        self.__logout()

        return errors

