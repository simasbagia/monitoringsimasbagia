import mysql.connector
from faker import Faker

# Koneksi ke database MySQL
connection = mysql.connector.connect(
    user='Dp4kb', 
    password='Dp4kb11', 
    host='103.86.138.65', 
    database='monitoring_db', 
    port=3306
)
cursor = connection.cursor()

# Membuat objek Faker untuk data dummy
fake = Faker()

# Menambah 100 baris data dummy
for _ in range(100):
    name = fake.name()
    age = fake.random_int(min=18, max=70)
    email = fake.email()

    # Query untuk memasukkan data
    cursor.execute(
        "INSERT INTO main_table (name, value) VALUES (%s, %s, %s)", 
        (name, email)
    )

# Menyimpan perubahan
connection.commit()

# Menutup koneksi
cursor.close()
connection.close()
