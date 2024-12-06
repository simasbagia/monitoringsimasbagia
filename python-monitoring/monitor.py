import mysql.connector
import logging
import time

# Konfigurasi logging
logging.basicConfig(
    filename='database_monitor.log',  # Nama file log
    level=logging.DEBUG,              # Level log DEBUG untuk informasi lebih banyak
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format log
)

# Konfigurasi koneksi ke database
config = {
        'user': 'dp4kb_user',
        'password': 'Bocahkreative89',
        'host': '103.86.138.65',  # IP VPS
        'database': 'monitoring_db',
        'port': 3306  # Port default untuk MySQL/MariaDB
    }

def monitor_database():
    try:
        logging.info("Mencoba menghubungkan ke database...")
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        logging.info("Koneksi berhasil!")

        # Menjalankan query untuk mendeteksi perubahan
        logging.info("Menjalankan query untuk memeriksa perubahan...")
        cursor.execute("SELECT * FROM log_table WHERE change_time > NOW() ORDER BY change_time ASC")
        logging.info("Query dijalankan!")

        # Ambil data terakhir
        last_row = cursor.fetchone()

        if last_row:
            logging.info(f"Perubahan terdeteksi: {last_row}")
        else:
            logging.info("Tidak ada perubahan terbaru.")

        cursor.close()
        connection.close()
        logging.info("Koneksi ditutup.")
    except mysql.connector.Error as err:
        logging.error(f"Terjadi kesalahan pada koneksi database: {err}")
    except Exception as e:
        logging.error(f"Terjadi kesalahan tak terduga: {e}")

# Jalankan monitoring setiap 60 detik
while True:
    monitor_database()
    time.sleep(60)  # Menunggu 1 menit sebelum melakukan pengecekan lagi