import imaplib
import time
import os
import sys


class Checker:
    def __init__(self):
        self.__imapserver = ""
        self.__email = ""
        self.__password = ""
        self.__mask = '(FROM "{}")'
        self.__search_emails = list()
        self.__keyword = {}
        self.__all_count = 0
        self.__correct_count = 0
        self.__timeToSleep = 0

    def setEmail(self, email):
        self.__email = email

    def setPassword(self, password):
        self.__password = password

    def setOK(self):
        self.__search_emails.append("bezotveta@odnoklassniki.ru")
        self.__search_emails.append("ok.ru")
        self.__search_emails.append("odnoklassniki.ru")

    def setSTEAM(self):
        self.__search_emails.append("noreply@steampowered.com")
        self.__search_emails.append("steampowered.com")

    def setVK(self):
        self.__search_emails.append("admin@notify.vk.com")
        self.__search_emails.append("vk.com")

    def setORIGIN(self):
        self.__search_emails.append("ea@e.ea.com")
        self.__search_emails.append("ea.com")

    def clearEmails(self):
        self.__search_emails.clear()

    def showData(self):
        msg = "{}:{} {}"
        print(msg.format(self.__email, self.__password, self.__imapserver))

    def setIMAPServer(self, email):
        if (str(email).find("@yandex")) > -1 or (str(email).find("@ya")) > -1:
            self.__imapserver = "imap.yandex.com"
            return 1
        elif (str(email).find("@mail")) > -1 or (str(email).find("@list")) > -1 or (str(email).find("@bk")) > -1:
            self.__imapserver = "imap.mail.ru"
            print("MAIL.RU is not supported")
            return -1
        elif (str(email).find("@rambler")) > -1:
            self.__imapserver = "imap.rambler.ru"
            return 1
        elif (str(email).find("@gmail")) > -1:
            self.__imapserver = "imap.gmail.com"
            return 1
        else:
            return -1


    def saveResult(self):
        path = os.path.dirname(os.path.abspath(__file__))

        f = open(os.path.join(path,"result.txt"), "w")
        for key in self.__keyword.keys():
            f.write("{}:{}\n".format(key, self.__keyword[key]))
        f.close()

    def setTimeToSleep(self,second):
        self.__timeToSleep = second

    def search(self):
        if (len(self.__search_emails) == 0):
            return -1
        imap = imaplib.IMAP4_SSL(self.__imapserver)
        self.__all_count += 1
        try:
            imap.login(self.__email, self.__password)
            imap.select("INBOX")
        except:
            return -1
        self.__keyword[self.__email] = []
        self.__correct_count += 1
        for email in self.__search_emails:
            cur_mask = self.__mask.format(email)
            messages = imap.search(None, cur_mask)[1][0]
            if (len(messages) > 0):
                # print(self.__email + " " + str(messages))
                if (str(messages).find("error")>-1 or str(messages).find("ERROR")>-1 or str(messages).find("Error")>-1):
                    self.__keyword[self.__email].append(cur_mask+" ERROR! MAY IS NOT CONTAIN")
                else:
                    # print(self.__email + " " + str(messages))
                    self.__keyword[self.__email].append(cur_mask)
        imap.logout()
        time.sleep(self.__timeToSleep)
