import time
import os
import sqlite3
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# ============================================================
# CP-A05: Verificación del historial de movimientos
# Técnica: Partición de equivalencia (clase válida)
# Requisito: RF04
# El historial está en la sección "Logistics History" del /movement
# La tabla solo aparece si logs tiene datos válidos
# ============================================================

BASE_URL = "http://127.0.0.1:5000"
DRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver.exe")
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "inventory", "inventory.sqlite"
)

def test_cp_a05():
    print("\n" + "="*60)
    print("CP-A05: Verificación del historial de movimientos")
    print("="*60)

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        # Paso 1: Leer BD para obtener prod_id y loc_id reales
        print(f"[1] Leyendo base de datos: {DB_PATH}")
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()

        cursor.execute("SELECT prod_id, prod_name FROM products LIMIT 1")
        producto = cursor.fetchone()
        cursor.execute("SELECT loc_id, loc_name FROM location LIMIT 1")
        ubicacion = cursor.fetchone()

        print(f"    Producto: {producto}")
        print(f"    Ubicación: {ubicacion}")

        if not producto or not ubicacion:
            print("\n⚠️  Ejecuta CP-A01 y CP-A03 primero para crear producto y ubicación.")
            return

        prod_id = producto[0]
        loc_id = ubicacion[0]

        # Paso 2: Verificar si ya hay movimientos en logistics
        cursor.execute("SELECT COUNT(*) FROM logistics")
        total_logs = cursor.fetchone()[0]
        print(f"[2] Movimientos actuales en BD: {total_logs}")

        if total_logs == 0:
            print("    Insertando movimiento de prueba...")
            cursor.execute("""
                INSERT INTO logistics (prod_id, to_loc_id, prod_quantity, needs_quantity)
                VALUES (?, ?, 3, 0)
            """, (prod_id, loc_id))
            db.commit()
            print("    Movimiento insertado.")

        db.close()

        # Paso 3: Abrir /movement y buscar "Logistics History"
        print("[3] Abriendo /movement en el navegador...")
        driver.get(BASE_URL + "/movement")
        time.sleep(2)

        page_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"    Texto visible en página (primeros 500 chars):")
        print(f"    {page_text[:500]}")

        # La tabla de historial aparece bajo "Logistics History"
        # Si hay logs, aparece una tabla con columnas Transaction ID, Product Name, etc.
        if "Logistics History" in page_text and "Data not available yet" not in page_text:
            print("\n✅ RESULTADO: APROBADO")
            print("   La sección 'Logistics History' muestra el historial de movimientos.")
        elif "Logistics History" in page_text and "Data not available yet" in page_text:
            print("\n❌ RESULTADO: FALLIDO")
            print("   Flask no cargó los logs correctamente desde la BD.")
            print("   El movimiento está en BD pero MapIds2Names no lo renderiza.")
        else:
            print("\n❌ RESULTADO: FALLIDO")
            print("   No se encontró la sección 'Logistics History' en la página.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        time.sleep(3)
        driver.quit()
        print("="*60)

if __name__ == "__main__":
    test_cp_a05()
