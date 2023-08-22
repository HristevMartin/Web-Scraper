import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass",
    database="state_extracted_buildings"
)