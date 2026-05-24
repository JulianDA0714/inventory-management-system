import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# ============================================================
# CP-A04: Registro con cantidad no numérica — Defecto DEF-001
# Técnica: Partición de equivalencia (clase inválida)
# Requisito: RF06
# NOTA: Se espera FALLIDO — Flask guarda quantity como texto sin validar
# El campo prod_quantity se inserta directo en SQLite sin conversión
# ============================================================

BASE_URL = "http://127.0.0.1:5000"
DRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver.exe")

def test_cp_a04():
    print("\n" + "="*60)
    print("CP-A04: Registro con cantidad no numérica (Defecto DEF-001)")
    print("="*60)

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        # Primero contar cuántos productos hay actualmente
        resp_antes = requests.get(BASE_URL + "/product")
        driver.get(BASE_URL + "/product")
        time.sleep(1)
        filas_antes = driver.find_elements(By.XPATH, "//table[1]//tbody//tr")
        print(f"[1] Productos antes del test: {len(filas_antes)}")

        print("[2] Enviando POST con cantidad='ASASDAD' (no numérica)...")
        data = {
            "prod_name": "Producto Invalido DEF001",
            "prod_quantity": "ASASDAD",
            "prod_type": "Test",
            "prod_detail1": "",
            "prod_detail2": "",
            "prod_detail3": "",
            "prod_protect": "No"
        }
        resp = requests.post(BASE_URL + "/product", data=data)
        print(f"    Respuesta HTTP: {resp.status_code}")

        print("[3] Verificando si el producto aparece en el listado...")
        driver.get(BASE_URL + "/product")
        time.sleep(2)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        filas_despues = driver.find_elements(By.XPATH, "//table[1]//tbody//tr")
        print(f"    Productos después del test: {len(filas_despues)}")

        if "Producto Invalido DEF001" in page_text:
            print("\n❌ RESULTADO: FALLIDO — DEFECTO DEF-001 CONFIRMADO")
            print("   El sistema aceptó 'ASASDAD' como cantidad válida.")
            print("   app.py línea 137: quantity se inserta sin validar tipo numérico.")
        else:
            print("\n✅ RESULTADO: APROBADO")
            print("   El sistema rechazó el texto en el campo cantidad.")

    except Exception as e:
        print(f"\n❌ ERROR durante la ejecución: {e}")

    finally:
        time.sleep(3)
        driver.quit()
        print("="*60)

if __name__ == "__main__":
    test_cp_a04()
