from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Conexión a la base de datos MySQL
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_CREATE_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Endpoint para actualizar un cliente
@app.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        # Consulta para actualizar al cliente
        update_query = """
            UPDATE Customers
            SET FirstName = %s,
                LastName = %s,
                Email = %s,
                PhoneNumber = %s,
                Address = %s
            WHERE CustomerID = %s
        """
        cursor.execute(update_query, (
            data['FirstName'], 
            data['LastName'], 
            data['Email'], 
            data['PhoneNumber'], 
            data.get('Address', None),  # Address es opcional
            customer_id
        ))
        conn.commit()
        rows_updated = cursor.rowcount
        cursor.close()
        conn.close()
        if rows_updated > 0:
            return jsonify({"message": "Customer updated successfully!"}), 200
        else:
            return jsonify({"message": "Customer not found"}), 404
    return jsonify({"message": "Failed to connect to database"}), 500

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
