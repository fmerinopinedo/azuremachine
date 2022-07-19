import email, smtplib, ssl
import psycopg2
import pandas as pd

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmails(receiver_emails):
    for receiver_email in receiver_emails:
        # Create a multipart message and set headers
        receiver_email = "fernando.merino@servexternos.gruposantander.com"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = "operacion.xlsx"  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn

def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # Turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df

# Connection parameters
param_dic = {
    "host"      : "argus-db-serverpro.postgres.database.azure.com",
    "database"  : "argus",
    "user"      : "argus@argus-db-serverpro",
    "password"  : "Proyectoeoi2019"
}

conn = connect(param_dic)

column_names = ["id", "timestamp", "publishedat", "title", "summary", "url", "urlToImage", "feedback", "entity", "score"] 

df = postgresql_to_dataframe(conn, "select * from argus_dj_articles order by publishedat desc limit 100", column_names)
df.to_excel("output.xlsx")
print("Terminado")

subject = "Informe noticias actualidad"
body = "Adjunto archivo con las ultimas noticias de actualidad"
sender_email = "merinogrepolis@gmail.com"
receiver_emails = ["fernando.merino@servexternos.gruposantander.com", "ernesto.budia@gruposantander.com"]
password = "qbeeiuvtsqbrzmuu"

sendmails(receiver_emails)