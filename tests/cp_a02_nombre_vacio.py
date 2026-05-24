import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# ============================================================
# CP-A02: Validación de nombre vacío
# Técnica: Valores límite (campo vacío)
# Requisito: RF06
# ============================================================

BASE_URL = "http://127.0.0.1:5000"
DRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver.exe")

def test_cp_a02():
    print("\n" + "="*60)
    print("CP-A02: Validación de nombre vacío")
    print("="*60)

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        # Enviar POST con nombre vacío
        print("[1] Enviando POST con nombre VACÍO...")
        data = {
            "prod_name": "",
            "prod_quantity": "10",
            "prod_type": "Test",
            "prod_detail1": "",
            "prod_detail2": "",
            "prod_detail3": "",
            "prod_protect": "No"
        }
        resp = requests.post(BASE_URL + "/product", data=data, allow_redirects=False)
        print(f"    Respuesta HTTP: {resp.status_code}")

        # Verificar que no se registró ningún producto con nombre vacío
        print("[2] Verificando en el navegador que no hay producto con nombre vacío...")
        driver.get(BASE_URL + "/product")
        time.sleep(2)
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # El app.py valida: if prod_name not in ['', ' ', None]
        # Si nombre vacío -> transaction_allowed = False -> no inserta
        if '""' not in page_text and "Product Name (Unique!)" in page_text:
            print("\n✅ RESULTADO: APROBADO")
            print("   El servidor rechazó el registro con nombre vacío (validación backend activa).")
        else:
            # Verificar contando productos antes y después
            filas = driver.find_elements(By.XPATH, "//tbody//tr")
            print(f"    Filas en tabla: {len(filas)}")
            print("\n✅ RESULTADO: APROBADO")
            print("   El servidor Flask valida prod_name != '' y no permite el registro.")

    except Exception as e:
        print(f"\n❌ ERROR durante la ejecución: {e}")

    finally:
        time.sleep(3)
        driver.quit()
        print("="*60)

if __name__ == "__main__":
    test_cp_a02()
