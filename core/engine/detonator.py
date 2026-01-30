# -*- coding: utf-8 -*-
import os
import time
import hashlib
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

class PhishingDetonator:
    """
    Motor de navegación instrumentada para detonación segura de URLs.
    Cumple con estándares de aislamiento y recolección de evidencia forense.
    """

    def __init__(self, evidence_path="data/samples"):
        self.evidence_path = evidence_path
        # Asegurar que el directorio de evidencia exista
        os.makedirs(self.evidence_path, exist_ok=True)
        
        # Configuración de OPSEC (Operational Security)
        # Disfrazamos el bot como un usuario de Windows 10 con Chrome estándar
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.viewport = {'width': 1920, 'height': 1080}

    def _generate_case_id(self, url):
        """Genera un identificador único para el caso basado en hash MD5 de la URL y timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        return f"{timestamp}_{url_hash}"

    def detonate(self, target_url):
        """
        Ejecuta el ciclo de detonación completo:
        Navegación -> Espera -> Captura -> Cierre.
        """
        case_id = self._generate_case_id(target_url)
        print(f"[*] Iniciando detonación para: {target_url}")
        print(f"[*] Case ID: {case_id}")

        results = {
            "case_id": case_id,
            "url": target_url,
            "timestamp": datetime.now().isoformat(),
            "status": "failed",
            "files": {}
        }

        with sync_playwright() as p:
            # 1. Lanzamiento del Navegador (Headless = Sin interfaz gráfica)
            # args: Evitan detección de automatización básica
            browser = p.chromium.launch(
                headless=True, 
                args=['--disable-blink-features=AutomationControlled']
            )
            
            # 2. Creación del Contexto (Perfil de Víctima)
            context = browser.new_context(
                user_agent=self.user_agent,
                viewport=self.viewport,
                locale="es-AR", # Simulamos ubicación local
                timezone_id="America/Argentina/Buenos_Aires"
            )

            page = context.new_page()

            try:
                # 3. Navegación (Timeout de 30 segundos)
                response = page.goto(target_url, timeout=30000, wait_until="networkidle")
                
                # Espera extra para scripts diferidos (anti-análisis)
                page.wait_for_timeout(3000) 

                # 4. Extracción de Evidencia
                # A. Captura de Pantalla
                screenshot_filename = f"{case_id}_screenshot.png"
                screenshot_path = os.path.join(self.evidence_path, screenshot_filename)
                page.screenshot(path=screenshot_path, full_page=True)
                
                # B. Extracción del DOM (Código fuente procesado)
                html_filename = f"{case_id}_dom.html"
                html_path = os.path.join(self.evidence_path, html_filename)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(page.content())

                print(f"[+] Evidencia guardada en: {self.evidence_path}")
                
                results["status"] = "success"
                results["http_status"] = response.status if response else 0
                results["files"] = {
                    "screenshot": screenshot_path,
                    "html": html_path
                }

            except PlaywrightTimeoutError:
                print("[-] Error: Tiempo de espera agotado (Timeout).")
                results["error"] = "Timeout"
            except Exception as e:
                print(f"[-] Error crítico durante detonación: {e}")
                results["error"] = str(e)
            finally:
                # 5. Limpieza y Cierre (Kill Switch)
                context.close()
                browser.close()
        
        return results

# Bloque de prueba unitaria (para ejecutar este archivo directamente)
if __name__ == "__main__":
    # URL de prueba segura (Ejemplo de documentación)
    # En producción, esto vendrá del Harvester
    TEST_URL = "https://example.com" 
    
    engine = PhishingDetonator()
    report = engine.detonate(TEST_URL)
    print("\n--- REPORTE FINAL ---")
    print(report)