import pymysql

# Establishes the connection to database
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='090078601',
    db='sastaGoogle')
Google = conn.cursor()

Google.execute("ALTER TABLE wordfile DROP PRIMARY KEY;")
conn.commit()
Google.execute("ALTER TABLE wordfile ADD primary key (wordID, fileID);")
conn.commit()

# Closes the connection
Google.close()
conn.close()
