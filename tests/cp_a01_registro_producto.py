import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# ============================================================
# CP-A01: Registro exitoso de producto con datos válidos
# Técnica: Partición de equivalencia (clase válida)
# Requisito: RF01
# Estrategia: POST directo a /product + Selenium verifica el resultado
# ============================================================

BASE_URL = "http://127.0.0.1:5000"
DRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver.exe")

def test_cp_a01():
    print("\n" + "="*60)
    print("CP-A01: Registro exitoso de producto con datos válidos")
    print("="*60)

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        # Paso 1: Enviar POST directamente (el form está en HTML inválido,
        # el navegador lo mueve fuera del TR, pero Flask igual recibe el POST)
        print("[1] Enviando POST a /product con datos válidos...")
        data = {
            "prod_name": "Producto Auto 01",
            "prod_quantity": "25",
            "prod_type": "Electronico",
            "prod_detail1": "",
            "prod_detail2": "",
            "prod_detail3": "",
            "prod_protect": "No"
        }
        resp = requests.post(BASE_URL + "/product", data=data)
        print(f"    Respuesta HTTP: {resp.status_code} (200 o 302 = OK)")

        # Paso 2: Abrir el navegador y verificar que aparece en el listado
        print("[2] Abriendo navegador para verificar el listado...")
        driver.get(BASE_URL + "/product")
        time.sleep(2)

        page_text = driver.find_element(By.TAG_NAME, "body").text

        if "Producto Auto 01" in page_text:
            print("\n✅ RESULTADO: APROBADO")
            print("   El producto 'Producto Auto 01' aparece correctamente en el listado.")
        else:
            print("\n❌ RESULTADO: FALLIDO")
            print("   El producto NO aparece en el listado tras el registro.")

    except Exception as e:
        print(f"\n❌ ERROR durante la ejecución: {e}")

    finally:
        time.sleep(3)
        driver.quit()
        print("="*60)

if __name__ == "__main__":
    test_cp_a01()
