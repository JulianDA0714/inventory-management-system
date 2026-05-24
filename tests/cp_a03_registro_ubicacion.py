import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# ============================================================
# CP-A03: Registro exitoso de ubicación válida
# Técnica: Partición de equivalencia (clase válida)
# Requisito: RF02
# Campos reales del form: warehouse_name, loc_type, protected
# ============================================================

BASE_URL = "http://127.0.0.1:5000"
DRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver.exe")

def test_cp_a03():
    print("\n" + "="*60)
    print("CP-A03: Registro exitoso de ubicación válida")
    print("="*60)

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        # Verificar cuántas ubicaciones hay antes
        driver.get(BASE_URL + "/location")
        time.sleep(1)
        texto_antes = driver.find_element(By.TAG_NAME, "body").text
        print(f"[1] Verificando si 'Bodega Auto 01' ya existe...")

        if "Bodega Auto 01" in texto_antes:
            print("    Ya existe. Usando una ubicación diferente: 'Bodega Auto 02'")
            nombre_ubicacion = "Bodega Auto 02"
        else:
            nombre_ubicacion = "Bodega Auto 01"

        # POST con follow_redirects via session
        print(f"[2] Enviando POST para registrar '{nombre_ubicacion}'...")
        session = requests.Session()
        data = {
            "warehouse_name": nombre_ubicacion,
            "loc_type": "Warehouse",
            "protected": "No"
        }
        # Flask redirige después del POST — seguir la redirección
        resp = session.post(BASE_URL + "/location", data=data, allow_redirects=True)
        print(f"    Respuesta HTTP final: {resp.status_code}")

        print("[3] Verificando en el navegador...")
        driver.get(BASE_URL + "/location")
        time.sleep(2)
        page_text = driver.find_element(By.TAG_NAME, "body").text

        if nombre_ubicacion in page_text:
            print(f"\n✅ RESULTADO: APROBADO")
            print(f"   La ubicación '{nombre_ubicacion}' aparece correctamente en el listado.")
        else:
            print(f"\n❌ RESULTADO: FALLIDO")
            print(f"   La ubicación '{nombre_ubicacion}' NO aparece en el listado.")
            print(f"   Contenido de la página: {page_text[:300]}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

    finally:
        time.sleep(3)
        driver.quit()
        print("="*60)

if __name__ == "__main__":
    test_cp_a03()
