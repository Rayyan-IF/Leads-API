from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Model untuk menerima data calon pembeli
class Lead(BaseModel):
    Name: str
    Phone_number: str
    Email: str

# Koneksi ke database dengan nama "leads"
def get_db_connection():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "leads"
    }
    return mysql.connector.connect(**db_config)


# Endpoint untuk "GET" data calon pembeli
@app.get("/leads/")
async def get_leads():
    try:
        # Membuat koneksi ke database
        connect = get_db_connection()
        cursor = connect.cursor()
        query = "SELECT * FROM leads"
        cursor.execute(query)
        results = cursor.fetchall()

        # Mengubah hasil query menjadi bentuk dictionary / Array of objects
        leads = []
        for row in results:
            lead = {
                "ID": row[0],
                "Name": row[1],
                "Phone_number": row[2],
                "Email": row[3],
                "Status": row[4]
            }
            leads.append(lead)

        return {"leads": leads}
    except Exception as e:
        # Mengembalikan response dengan pesan error
        raise HTTPException(status_code=500, detail=f"Gagal mengambil data leads. Error: {str(e)}")
    finally:
        # Menutup cursor dan koneksi database
        cursor.close()
        connect.close()

# Endpoint untuk "POST" data calon pembeli
@app.post("/leads/")
async def create_lead(lead: Lead):
    try:
        # Membuat koneksi ke database
        connect = get_db_connection()
        cursor = connect.cursor()
        query = "INSERT INTO leads (Name, `Phone_number`, Email, Status) VALUES (%s, %s, %s, %s)"
        values = (lead.Name, lead.Phone_number, lead.Email, "Baru")
        cursor.execute(query, values)
        connect.commit()

        return {"message": "Lead sukses ditambahkan"}
    except Exception as e:
        # Mengembalikan response dengan pesan error
        raise HTTPException(status_code=500, detail=f"Gagal menambahkan data lead. Error: {str(e)}")
    finally:
        # Menutup cursor dan koneksi database
        cursor.close()
        connect.close()

# Endpoint untuk "PUT" data calon pembeli
@app.put("/leads/{lead_id}")
async def update_lead_status(lead_id: int, status: str):
    try:
        # Membuat koneksi ke database
        connect = get_db_connection()
        cursor = connect.cursor()
        query = "UPDATE leads SET Status = %s WHERE ID = %s"
        values = (status, lead_id)
        cursor.execute(query, values)
        connect.commit()

        if cursor.rowcount < 1:
            raise HTTPException(status_code=404, detail="Data lead tidak ditemukan")

        return {"message": "Status lead berhasil diperbarui"}
    except HTTPException:
        raise
    except Exception as e:
        # Mengembalikan response dengan pesan error
        raise HTTPException(status_code=500, detail=f"Gagal memperbarui status lead. Error: {str(e)}")
    finally:
        # Menutup cursor dan koneksi database
        cursor.close()
        connect.close()

# Endpoint untuk "DELETE" data calon pembeli
@app.delete("/leads/{lead_id}")
async def delete_lead(lead_id: int):
    try:
        # Membuat koneksi ke database
        connect = get_db_connection()
        cursor = connect.cursor()
        query = "DELETE FROM leads WHERE ID = %s"
        values = (lead_id,)
        cursor.execute(query, values)
        connect.commit()

        if cursor.rowcount < 1:
            raise HTTPException(status_code=404, detail="Data lead tidak ditemukan")

        return {"message": "Lead berhasil dihapus"}
    except HTTPException:
        raise
    except Exception as e:
        # Mengembalikan response dengan pesan error
        raise HTTPException(status_code=500, detail=f"Gagal menghapus data lead. Error: {str(e)}")
    finally:
        # Menutup cursor dan koneksi database
        cursor.close()
        connect.close()