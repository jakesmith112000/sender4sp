'''
    Email sender through Simple Mail Transform Protocol
'''
from threading import Thread
from queue import Queue
from base64 import b64encode
from email.message import EmailMessage
from smtplib import SMTP
from random import choice
from email.utils import make_msgid
from typing import Any
from queue import Queue
from threading import Thread

class Inboxing:
    def __init__(self,spoofed:str,smtps:list,letter:str,subject:str):
        self.spoofed_fname,self.spoofed_lname,self.spoof = spoofed.split(",")
        self.smtps = smtps
        self.letter = letter
        self.subject = subject
        self.sender = self.spoofed_fname  + " " + self.spoofed_lname
    def send(self, lead :str):
        '''
        :param lead: a string input. sending one email per thread
        :return: None
        this is going to look complicated
        '''
        SMTPs = self.smtps #choosing a random smtp ['0','565',fdsfdsf]
        #Some SMTP informations
        fname,lead = lead.split(",")
        sender_email = SMTPs[2]
        sender_password = SMTPs[3]
        email_content = self.letter
        subject = self.subject #choosing a randome subject

        '''
        Preparing for sending 
        Setting HTML variables
        '''
        email_content = email_content.replace("[email]", lead)
        email_content = email_content.replace("[name]", fname)
        email_content = email_content.replace("[spoofedfname]", self.spoofed_fname)
        email_content = email_content.replace("[spoofedlname]", self.spoofed_lname)
        email_content = email_content.replace("[spoofedfullname]", self.sender)
        '''
        Setting subject and senderid variables
        '''
        subject = subject.replace("[email]", lead)
        subject = subject.replace("[name]", fname)
        subject = subject.replace("[spoofedfname]", self.spoofed_fname)
        subject = subject.replace("[spoofedlname]", self.spoofed_lname)
        subject = subject.replace("[spoofedfullname]", self.sender)

        '''
        Setting MIME
        '''
        msg = EmailMessage()
        msg["To"] = lead
        msg["From"] = f"{self.sender} <{self.spoof}>"
        msg['Subject'] = subject

        '''
        Setting embedded image to content
        '''
        msg.add_alternative(email_content, "html")
        '''
        Setting Server
        '''
        try:server = SMTP(SMTPs[0] + ":" + str(SMTPs[1]), timeout=10);server.starttls()
        except:server = SMTP(SMTPs[0] + ":" + str(SMTPs[1]), timeout=10)
        server.ehlo()
        server.login(sender_email,sender_password)
        server.sendmail(msg['From'], [lead], msg.as_string())
        print(f" Message sent to ! {lead}")
    def imageembedded(self,lead):
        cid = {}
        name_section = []
        try:
            for x, d in zip(self.img_list, range(len(self.img_list))):
                image_cid = make_msgid(domain=lead.split("@")[1])
                name = "#IMAGE" + str(d + 1)
                cid[name] = image_cid
                name_section.append(name)
        except:
            pass
        return name_section,cid
    def payloadImg(self,msg,cid={}):
        for x in range(len(self.img_list)):
            mp = "#IMAGE" + str(x + 1)
            msg.get_payload()[0].add_related(self.img_list[x],
                                             maintype="image",
                                             subtype="png",
                                             cid=cid[mp])
        return msg
    def openingfiles(self):
        '''
        Opening files that contain some random informations
        such as random operating system, random lacatuins and random links
        :return: bunch of lists inherited in class
        '''
        names = open("env/names.txt","r")
        self.names = list(names.read().splitlines())
        names.close()
        randoms = open("env/random.txt","r")
        self.random_browser= randoms.read().splitlines()
        randoms.close()
        os = open("env/os.txt","r")
        self.OSs= os.read().splitlines()
        os.close()
        os = open("env/locations.txt","r")
        self.LOCs= os.read().splitlines()
        os.close()
        os = open("env/link.txt","r")
        self.Links= os.read().splitlines()
        os.close()
    def queue_th_config(self,q):
        while not q.empty():
            i=q.get()
            try:self.send(i)
            except Exception as e:
                print(e)
                print("Dead SMTP or Internet")
            q.task_done()

    def start(self,emails:list,bot,msg):
        for email in emails:
            self.send(email)
            bot.send_message(msg,"Sent to : {}".format(email))
        """job = Queue()
        for jobs in emails:
            job.put(jobs)
        
        for i in range(5):
            th = Thread(target= self.queue_th_config,args=(job,))
            th.daemon = True
            th.start()"""

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value