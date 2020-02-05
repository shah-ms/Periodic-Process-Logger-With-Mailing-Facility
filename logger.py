import os 
import time
import psutil
import smtplib
import schedule
import urllib.request
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
 
def is_connected():
	try:
		urllib.request.urlopen('http://216.58.192.142', timeout=5)
		return True
	
	except Exception as e:
		print(e)
		return False

def SendMail(filepath, emailid, time):

	try:
		fromaddr = "mehulindia1998@gmail.com"
		toaddr = emailid
		
		msg = MIMEMultipart()
		
		msg['From'] = fromaddr
		msg['To'] = toaddr
		
		body = """
		Hello %s
		Welcome to Marvellous Infosystems
		Please find attached document which contains log of running processes.
		Log file is created at : %s
		
		Do not reply to this as it is an auto-generated mail.
		
		Thanks & Regards,
		Mehul Shah
		""" %(toaddr, time)

		subject = """
		Marvellous Infosystems Process Logger Generated at : %s
		""" %(time)
		
		msg['Subject'] = subject
		
		msg.attach(MIMEText(body, 'plain'))
		attachment = open(filepath, "rb")
		
		att = MIMEBase('application', 'octet-stream')
		att.set_payload((attachment).read())
		encoders.encode_base64(att)
		att.add_header('Content-Disposition', "attachment; filename=%s" %(filepath))
		
		msg.attach(att)
		
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.starttls()
		s.login(fromaddr, "********")
		text = msg.as_string()
		s.sendmail(fromaddr, toaddr, text)
		s.quit()		
		
		print("Mail Successfully Sent")
		
	except Exception as e:
		print("Mail not sent : ", e)
			
		
def DisplayProcess(dirName, emailid):

	listprocess = []
	
	if not os.path.exists(dirName):
		try:
			os.mkdir(dirName)
		except:
			pass
				
	log_path = os.path.join(dirName, "MarvellousLog_%s" %(time.ctime()))
	
	flog = open(log_path, "w")
	
	separator = "-" * 80
	
	flog.write(separator + "\n")
	flog.write("MARVELLOUS INFOSYSTEMS PROCESS LOGGER - %s" + (time.ctime()) + "\n") 
	flog.write(separator + "\n")
	
	for proc in psutil.process_iter():
		
		try:
			pinfo = proc.as_dict(attrs=['pid','username','name'])
			vms = proc.memory_info().vms/(1024*1024)
			pinfo['vms'] = vms
			listprocess.append(pinfo)
						
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
			
	for elem in listprocess:
		flog.write("%s\n" %elem)
		
	connected = is_connected()
		
	if connected:
		SendMail(log_path, emailid, time.ctime())
	else:
		print("No internet connection")
		
def main():
	
	if len(argv) != 4:
		print("Invalid number of arguments")
		exit()
		
	try:
		schedule.every(argv[3]).minutes.do(DisplayProcess, argv[1], argv[2])
		
		while True:
			schedule.run_pending()
			time.sleep(1)
	
	except Exception as e:
		print("Not working ", e)
	
if __name__ == "__main__":
	main()
