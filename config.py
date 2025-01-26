import os

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
#Conexion a la base de datos de forma local
#SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://Lexie\\SQLEXPRESS/Chronomax?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

#Conexion a la base de datos en produccion
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:StrongPass1!@Chronomax:1433/Chronomax?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

SQLALCHEMY_TRACK_MODIFICATIONS = False