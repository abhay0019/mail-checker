#!/usr/bin/python

import smtplib
import imapclient
import pyzmail
import webbrowser
import os
import time
import sys

if len(sys.argv)!=3:
  print "usage: ./mail_checker.py my_email@gmail.com password" 
  sys.exit()
def send():
  smtpobj=smtplib.SMTP_SSL('smtp.gmail.com', 465)
  smtpobj.ehlo()
  smtpobj.login(sys.argv[1],sys.argv[2])
  sendto=raw_input("Send To : ")
  subject=raw_input("Subject : ")
  body=raw_input("Body : ")
  failed=smtpobj.sendmail(sys.argv[0],sendto,'Subject:'+subject+'\n'+body)
  smtpobj.quit()
  print "Mail Sent .."
  
def watch_delete():
  imapobj=imapclient.IMAPClient('imap.gmail.com',ssl=True)
  imapobj.login(sys.argv[1],sys.argv[2])
  imapobj.select_folder('INBOX',readonly=False)
  UIDs = imapobj.search(['ALL'])
  for uid in UIDs:
    rawmsg=imapobj.fetch([uid],['BODY[]','FLAGS'])
    message = pyzmail.PyzMessage.factory(rawmsg[uid]['BODY[]'])
    print "\n",message.get_addresses('from'),"\n"
    choice=raw_input("\nWanna :-\n\n1)See Content and chooses to delete\n2)Delete directly\n3)Pass on\n4)Exit\n\n")
    if choice=='1':
      print "Subject:",message.get_subject()
      if message.text_part:
        print message.text_part.get_payload().decode(message.text_part.charset)
      elif message.html_part:
        f=open("mymail.html","w")
        f.write(message.html_part.get_payload().decode(message.html_part.charset))
        f.close()
        webbrowser.open(os.path.join(os.getcwd(),"mymail.html"))
      else:
        print "Neither text nor html !!"
      time.sleep(3)  
      choice=raw_input("Wanna delete?(y/n)")
      if choice.lower()=='y':
        imapobj.delete_messages([uid])
        print "Deleted .."
    elif choice=='2':
      imapobj.delete_messages([uid])
      print "Deleted .."
    elif choice=='4':
      imapobj.expunge()
      imapobj.logout()
      sys.exit()  
    else:
      pass
  imapobj.expunge()           
  imapobj.logout()
      
def read_by_search():
  imapobj=imapclient.IMAPClient('imap.gmail.com',ssl=True)
  imapobj.login(sys.argv[1],sys.argv[2])
  imapobj.select_folder('INBOX',readonly=True)
  search=raw_input("Search String : ")
  UIDs=imapobj.gmail_search(search)
  f1=open("searched_mail.txt","w")
  
  for uid in UIDs:
    string=''
    string+="####################################################################################################################\n"
    print "####################################################################################################################"
    rawmsg=imapobj.fetch([uid],['BODY[]','FLAGS'])
    message = pyzmail.PyzMessage.factory(rawmsg[uid]['BODY[]'])
    string+="\n"+str(message.get_addresses('from'))+"\n\n"
    string+="Subject:"+str(message.get_subject())+"\n"
    print "\n",message.get_addresses('from'),"\n"
    print "Subject:",message.get_subject()
    if message.text_part:
      string+=message.text_part.get_payload().decode(message.text_part.charset)+"\n"
      print message.text_part.get_payload().decode(message.text_part.charset)
    elif message.html_part:
      f=open("mymail.html","w")
      f.write(message.html_part.get_payload().decode(message.html_part.charset))
      f.close()
      string+="ITS BODY HAS HTML CODE ... BROWSER IS ALREADY LOADED ..\n"
      webbrowser.open(os.path.join(os.getcwd(),"mymail.html"))
    else:
      print "Neither text nor html !!"
    print "####################################################################################################################"
    string+="####################################################################################################################\n"
    f1.write(string)
    time.sleep(1)  
  imapobj.logout()
if __name__=='__main__':
  while True:
    choice=raw_input('Select:-\n1)Send mail\n2)Watch and Delete\n3)Read by Search\n4)Exit\n')
    if choice=='1':
      send()
    elif choice=='2':
      watch_delete()
    elif choice=='3':
      read_by_search()
    elif choice=='4':
      sys.exit()   
    else:
      print "Wrong Choice..reselect .."
