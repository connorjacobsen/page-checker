import requests
import smtplib
import sys
import time
from email.mime.text import MIMEText

# The email body, read from a file.
fp = open('msg.txt', 'rb')
# Create a text/plain message.
msg = MIMEText(fp.read())
fp.close()

# Infinite loop.
while True:
	try:
		# Open the source file for reading and writing.
		f = open('announcements.html', 'r+')
		# Read out the source.
		source = f.read()

		# GET the current webpage.
		print 'Checking source...'
		r = requests.get('http://www.cise.ufl.edu/class/cda3101sp14/announcements.htm')
		# Slicing out the first two characters because they showed up as '??', weird.
		current_source = r.content[2:]

		# List of email addresses.
		emails = ['jacobsen.connor@gmail.com']

		if current_source != source:
			# The page has changed, most likely this means that there has been a new
			# update posted. (It is also possible some style on the page has changed,
			# this will be accounted for in future versions.)
			print 'Changes detected!'

			# Update the file that contains the source.
			f.write(current_source)

			for email in emails:
				msg['Subject'] = '[CDA3101] New Announcement!'
				msg['From'] = 'jacobsen.connor@gmail.com'
				msg['To'] = email

				# Send the message via the SMTP server.
				s = smtplib.SMTP('localhost')
				s.sendmail(msg['From'], msg['To'], msg.as_string())
				s.quit()

				# Let me know via stdout.
				print 'Sent email to %s' % msg['To']

		# Only run once per every 12 hours.
		time.sleep(43200)
	except KeyboardInterrupt:
		# Exit the program if ^C is pressed.
		sys.exit(0)
