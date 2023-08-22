from db import mydb

mycursor = mydb.cursor()

def create_table():
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS buildings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        second_title VARCHAR(255),
        location VARCHAR(255),
        meta_description TEXT,
        src TEXT,
        advert_url VARCHAR(255),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)