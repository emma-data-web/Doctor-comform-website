import smtplib

server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
server.starttls()
server.login("emmanuelnwankwo690@gmail.com", "ecrc czyz vtmx xcqm")
print("Connected successfully")
server.quit()