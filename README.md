# 🎣 R.I.P.H. | Reverse Intelligence Phishing Honeypot

![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge)
![Security Level](https://img.shields.io/badge/Security-Advanced-red?style=for-the-badge)
![Stage](https://img.shields.io/badge/Stage-Alpha-orange?style=for-the-badge)

# R.I.P.H. (Reverse Intelligence Phishing Honeypot)

> **⚠️ AVISO DE USO:** Esta herramienta está diseñada exclusivamente para equipos de **Defensa Cibernética, CSIRTs y Analistas de Inteligencia**. Su uso para actividades ofensivas no autorizadas está prohibido. El autor no se hace responsable por el uso indebido del código.

##  Resumen

**R.I.P.H.** es un ecosistema de **SIGINT-Web (Signal Intelligence)** diseñado para la disección automatizada, segura y pasiva de campañas de phishing.

 R.I.P.H. Actúa como una **Sonda de Interacción Pasiva** que despliega entornos de navegación instrumentados y aislados. Su objetivo no es solo detectar una URL maliciosa, sino interactuar con ella simulando ser una víctima real para forzar al kit de phishing a revelar su infraestructura subyacente (C2, scripts de exfiltración, y patrones de ataque).

###  Objetivos 

- **Interacción Pasiva:** Navegación "Headless" indetectable que simula comportamiento humano.
    
- **Anti-Evasión:** Bypass de técnicas de _cloaking_ (geolocalización y fingerprinting) utilizadas por atacantes modernos.
    
- **Soberanía de Datos:** Prioridad en el enriquecimiento de datos local (GeoIP offline, YARA local) para evitar fugas de información operacional.
    
- **Interoperabilidad:** Generación nativa de reportes en formato **STIX 2.1** para integración con MISP y SIEMs.
    

##  Arquitectura Modular

El sistema está diseñado bajo principios de defensa en profundidad, dividido en módulos estancos:

1. **Harvester (Ingesta):** Normalización y priorización de feeds de amenazas (PhishStats, URLHaus).
    
2. **Orchestrator (Control):** Gestión de contenedores efímeros y rotación de identidad de red.
    
3. **Engine (Detonación):** Motor basado en `Playwright` optimizado para captura de evidencia forense (DOM snapshots, PCAP, Screenshots).
    
4. **Vault (Persistencia):** Almacenamiento estructurado y exportación de IoCs.
    

## Instalación y Despliegue

### Prerrequisitos

- Python 3.10 o superior.
    
- Entorno Linux (Debian/Kali) o Windows (para desarrollo).
    
- Recomendado: Ejecución dentro de Máquina Virtual o Contenedor para aislamiento.
    

### Paso a Paso

1. **Clonar el Repositorio**
    
    ```
    git clone https://github.com/djotahub/R.I.P.H.-Reverse-Intelligence-Phishing-Honeypot.git
    cd R.I.P.H.-Reverse-Intelligence-Phishing-Honeypot
    ```
    
2. **Configurar Entorno Virtual**
    
    Es crítico aislar las dependencias del sistema operativo base.
    
    ```
    # Linux / MacOS
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Windows (PowerShell)
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```
    
3. **Instalar Dependencias**
    
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    
4. **Instalar Binarios de Navegación**
    
    El motor requiere los binarios de Chromium para funcionar.
    
    ```
    playwright install chromium
    ```
    

## ⚙️ Manual de Uso (MVP)

Actualmente, el módulo funcional es el **Motor de Detonación (`core/engine/detonator.py`)**. Este script permite realizar una prueba de concepto sobre una URL específica.

### Ejecución de Prueba (Dry-Run)

```
# Asegúrese de estar en el directorio raíz del proyecto y con el venv activo
python core/engine/detonator.py
```

> **Nota:** Por defecto, el script apunta a una URL segura de prueba (`example.com`). Para analizar una amenaza real, se debe modificar la entrada en el script o esperar a la implementación de la CLI (ver Roadmap).

### Resultados

La evidencia recolectada se almacenará automáticamente en la carpeta `data/samples/`, generando:

- `{CASE_ID}_screenshot.png`: Evidencia visual del sitio.
    
- `{CASE_ID}_dom.html`: Código fuente procesado (útil para analizar scripts ofuscados).
    

## 🚧 Roadmap y Estado Actual

El proyecto se encuentra en fase **Alpha (v0.1.0)**.

- [x] **Fase I: Core Engine**
    
    - [x] Implementación de Playwright con perfil de evasión básico.
        
    - [x] Captura de Screenshot y DOM.
        
    - [x] Estructura de proyecto modular.
        
- [ ] **Fase II: Ingesta & Red (En Desarrollo)**
    
    - [ ] Conector API para PhishStats y URLHaus.
        
    - [ ] Intercepción de tráfico HTTP/S (Mitmproxy wrapper).
        
- [ ] **Fase III: Inteligencia**
    
    - [ ] Integración de reglas YARA locales.
        
    - [ ] Exportador JSON/STIX.
        

## 🤝 Contribución

Las contribuciones son bienvenidas, especialmente aquellas enfocadas en:

- Nuevas reglas de detección de kits de phishing.
    
- Mejoras en el OPSEC del motor de navegación (evasión de detección de bots).
    
- Integraciones con plataformas SOAR.
    

Por favor, abra un _Issue_ para discutir cambios mayores antes de enviar un _Pull Request_.

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la licencia **MIT**. Consulte el archivo `LICENSE` para más detalles.

**Desarrollado con enfoque en Ciberdefensa e Inteligencia de Amenazas.**
