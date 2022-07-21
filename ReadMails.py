with open('/home/argus/argus/mail.txt') as f:
    lines = f.readlines()
print(lines[0].split(';'))