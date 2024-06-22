from flask import Flask, jsonify, request
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kendaraan'
app.config['MYSQL_PORT'] = 3306  # Default MySQL port

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT'],
        cursorclass=pymysql.cursors.DictCursor
    )

# GET (READ)
@app.route('/kendaraan', methods=['GET'])
def kendaraan():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT kendaraan_id, mobil, sport, rilis FROM KENDARAAN")

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)

# POST (CREATE)
@app.route('/kendaraan', methods=['POST'])
def tambah_kendaraan():
    if request.is_json:
        data = request.get_json()

        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO KENDARAAN (mobil, sport, rilis) VALUES (%s, %s, %s)"
        val = (data['mobil'], data['sport'], data['rilis'])
        cursor.execute(sql, val)

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'data berhasil ditambahkan'})
    else:
        return jsonify({'error': 'data tidak valid'}), 400

# PUT (UPDATE)
@app.route('/kendaraan/<int:kendaraan_id>', methods=['PUT'])
def edit_kendaraan(kendaraan_id):
    if request.is_json:
        data = request.get_json()

        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE KENDARAAN SET mobil=%s, sport=%s, rilis=%s WHERE kendaraan_id = %s"
        val = (data['mobil'], data['sport'], data['rilis'], kendaraan_id)
        cursor.execute(sql, val)

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'data berhasil diupdate'})
    else:
        return jsonify({'error': 'data tidak valid'}), 400

# DELETE
@app.route('/kendaraan/<int:kendaraan_id>', methods=['DELETE'])
def hapus_kendaraan(kendaraan_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM KENDARAAN WHERE kendaraan_id = %s"
    val = (kendaraan_id,)
    cursor.execute(sql, val)

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'data berhasil dihapus'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50, debug=True)
