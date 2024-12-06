import mariadb  # Menggunakan mariadb sebagai konektor
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
    'database': 'rkm',
    'port': 3306  # Port default untuk MySQL/MariaDB
}

# Header tabel
columns = [
    "id", "nama", "kec_id", "kel_id", "rw_id", "rt_id", "kk_id", 
    "tgl_lahir", "agama", "jk", "pendidikan", "lulus", "pekerjaan", 
    "dtks", "posisi", "warneg", "disabilitas", "stunting", "jamkes", 
    "gangguan_jiwa", "jkn_kis", "vaksin", "imunisasi", "terlantar", 
    "ket", "created_at", "updated_at",
    "before_nama", "before_kec_id", "before_kel_id", "before_rw_id", "before_rt_id", 
    "before_kk_id", "before_tgl_lahir", "before_agama", "before_jk", "before_pendidikan", 
    "before_lulus", "before_pekerjaan", "before_dtks", "before_posisi", "before_warneg", 
    "before_disabilitas", "before_stunting", "before_jamkes", "before_gangguan_jiwa", 
    "before_jkn_kis", "before_vaksin", "before_imunisasi", "before_terlantar", "before_ket"
]

def monitor_database():
    try:
        logging.info("Mencoba menghubungkan ke database...")
        # Membuat koneksi ke database menggunakan MariaDB connector
        connection = mariadb.connect(**config)
        cursor = connection.cursor()
        logging.info("Koneksi berhasil!")

        # Menjalankan query untuk memeriksa perubahan
        logging.info("Menjalankan query untuk memeriksa perubahan...")
        cursor.execute("""
            SELECT 
                k.id, k.nama, k.kec_id, k.kel_id, k.rw_id, k.rt_id, k.kk_id,
                k.tgl_lahir, k.agama, k.jk, k.pendidikan, k.lulus, k.pekerjaan,
                k.dtks, k.posisi, k.warneg, k.disabilitas, k.stunting, k.jamkes, 
                k.gangguan_jiwa, k.jkn_kis, k.vaksin, k.imunisasi, k.terlantar, 
                k.ket, k.created_at, k.updated_at,
                h.nama AS before_nama, h.kec_id AS before_kec_id, h.kel_id AS before_kel_id, 
                h.rw_id AS before_rw_id, h.rt_id AS before_rt_id, h.kk_id AS before_kk_id,
                h.tgl_lahir AS before_tgl_lahir, h.agama AS before_agama, h.jk AS before_jk,
                h.pendidikan AS before_pendidikan, h.lulus AS before_lulus, h.pekerjaan AS before_pekerjaan,
                h.dtks AS before_dtks, h.posisi AS before_posisi, h.warneg AS before_warneg, 
                h.disabilitas AS before_disabilitas, h.stunting AS before_stunting, 
                h.jamkes AS before_jamkes, h.gangguan_jiwa AS before_gangguan_jiwa, 
                h.jkn_kis AS before_jkn_kis, h.vaksin AS before_vaksin, h.imunisasi AS before_imunisasi,
                h.terlantar AS before_terlantar, h.ket AS before_ket
            FROM keluarga k
            LEFT JOIN keluarga_history h ON k.id = h.id
            WHERE k.updated_at > NOW() - INTERVAL 24 HOUR
            ORDER BY k.updated_at DESC;
        """)
        logging.info("Query dijalankan!")

        # Ambil data perubahan
        rows = cursor.fetchall()

        # Jika ada perubahan, buat tabel HTML
        if rows:
            html_table = generate_html_table(rows)
            # Simpan hasil ke file HTML
            with open("database_changes.html", "w") as file:
                file.write(html_table)
            logging.info("Tabel HTML berhasil dibuat dan disimpan.")
        else:
            logging.info("Tidak ada perubahan terbaru.")

        cursor.close()
        connection.close()
        logging.info("Koneksi ditutup.")
    except mariadb.Error as err:
        logging.error(f"Terjadi kesalahan pada koneksi database: {err}")
    except Exception as e:
        logging.error(f"Terjadi kesalahan tak terduga: {e}")

def generate_html_table(rows):
    """
    Fungsi untuk menghasilkan HTML tabel dari hasil query.
    """
    html = """<html>
    <head>
        <title>Database Changes</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            h2 {
                text-align: center;
                margin-top: 30px;
            }
            table {
                margin: 30px auto;
                width: 90%;
            }
        </style>
    </head>
    <body>
        <h2>Perubahan Data Keluarga</h2>
        <div class="container">
            <table class="table table-bordered table-striped">
                <thead class="thead-dark">
                    <tr>"""
    
    # Menambahkan header tabel
    for column in columns:
        html += f"<th>{column}</th>"
    html += "</tr></thead><tbody>"

    # Menambahkan data tabel
    for row in rows:
        html += "<tr>"
        for value in row:
            html += f"<td>{value}</td>"
        html += "</tr>"

    html += """</tbody></table>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
</html>"""
    
    return html

# Jalankan monitoring setiap 60 detik
while True:
    monitor_database()
    time.sleep(60)  # Menunggu 1 menit sebelum melakukan pengecekan lagi
