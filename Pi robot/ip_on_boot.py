import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime

def connect_type(word_list):
    ## returns connection type
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'
    return con_type

# Change to your own account information
# Account Information
to = 'hzhang623@gmail.com' # Email to send to.
gmail_user = 'hzhang623@gmail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = '********' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()

arg='ip route list'  # Linux command to retrieve ip addresses.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate() 

# Split IP text block into three, and divide the two containing IPs into words.
ip_lines = data[0].splitlines()
split_line_a = ip_lines[1].split()
split_line_b = ip_lines[2].split()

# con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
ip_type_a = connect_type(split_line_a)
ip_type_b = connect_type(split_line_b)

#find 'src' and add one to get the index position of our ip.
ipaddr_a = split_line_a[split_line_a.index('src')+1]
ipaddr_b = split_line_b[split_line_b.index('src')+1]

# Creates a sentence for each ip address.
my_ip_a = 'Your %s ip is %s' % (ip_type_a, ipaddr_a)
my_ip_b = 'Your %s ip is %s' % (ip_type_b, ipaddr_b)

# Creates and sends message.
msg = MIMEText(my_ip_a + "\n" + my_ip_b)
msg['Subject'] = 'IPs For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())

smtpserver.quit()