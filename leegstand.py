# python 3
import os.path
from pathlib import Path
import time
import wget
import smtplib
import email.utils
from email.mime.text import MIMEText
import filecmp
import pdb
import subprocess


leegstandsregister = 'http://www.huisvesting-regio-izegem.be/websites/35/uploads/html/inventarislijst_ingelmunster.html'

var = 1

while var == 1:
	leegstand_backup = 'lsbup.html'
	lsbup = Path(leegstand_backup)
	if not lsbup.exists():
		wget.download(leegstandsregister,leegstand_backup)
	print ('\n1000 seconden wachten\n')
	time.sleep(1000)
	
	new_version = r'C:\python\nieuw.html'
	new = Path(new_version)
	if new.exists():
		print ('nieuw bestand bestaat\n')
		print ('dit bestand wordt verwijderd en vervangen door een nieuwer bestand\n')
		os.remove(new_version)
		print ('nieuw bestand wordt gedownload\n')
		wget.download(leegstandsregister,new_version)
	else:
		wget.download(leegstandsregister,new_version)
	if filecmp.cmp(leegstand_backup,new_version):
		print ('\nbeide bestanden zijn gelijk')
	else:
		tekstbestand = open('mail.txt','r')
		with tekstbestand as fp:
			msg = MIMEText(fp.read())
			msg['Subject'] = 'wijziging leegstandsregister'
			me = 'reginald.carlier@ingelmunster.be'
			you = 'reginald.carlier@ingelmunster.be'
			s = smtplib.SMTP('xx.xxx.x.xxx')
			s.set_debuglevel(True)
			#pdb.set_trace()
			s.sendmail(me, you, msg.as_string())
			s.quit()
			var = 0
			os.remove('lsbup.html')
			os.rename('nieuw.html','lsbup.html')
		subprocess.call(['python','html_naar_csv.py'])

