#!/usr/bin/env python3
"""
AEMET OpenData API Client
Cliente reutilizable para la API de meteorología de AEMET (España)
Documentación: https://opendata.aemet.es/
"""

import os
import json
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path

# Ruta por defecto para credenciales
DEFAULT_CREDENTIALS_PATH = Path.home() / ".openclaw" / "credentials" / "aemet.json"

# Códigos de Comunidades Autónomas
CCAA_CODES = {
    "and": "Andalucía",
    "arn": "Aragón",
    "ast": "Asturias",
    "bal": "Balears, Illes",
    "coo": "Canarias",
    "can": "Cantabria",
    "cle": "Castilla y León",
    "clm": "Castilla - La Mancha",
    "cat": "Cataluña",
    "val": "Comunitat Valenciana",
    "ext": "Extremadura",
    "gal": "Galicia",
    "mad": "Madrid, Comunidad de",
    "mur": "Murcia, Región de",
    "nav": "Navarra, Comunidad Foral de",
    "pva": "País Vasco",
    "rio": "La Rioja"
}

# Códigos de áreas para avisos
AREA_CODES = {
    "esp": "España",
    "61": "Andalucía",
    "62": "Aragón",
    "63": "Asturias, Principado de",
    "64": "Balears, Illes",
    "65": "Canarias",
    "66": "Cantabria",
    "67": "Castilla y León",
    "68": "Castilla - La Mancha",
    "69": "Cataluña",
    "70": "Extremadura",
    "71": "Galicia",
    "72": "Madrid, Comunidad de",
    "73": "Murcia, Región de",
    "74": "Navarra, Comunidad Foral de",
    "75": "País Vasco",
    "76": "La Rioja",
    "77": "Comunitat Valenciana",
    "78": "Ceuta",
    "79": "Melilla"
}


class AemetClient:
    """Cliente para la API AEMET OpenData"""
    
    BASE_URL = "https://opendata.aemet.es/opendata"
    
    def __init__(self, api_key: str = None, credentials_path: Path = None):
        """
        Inicializa el cliente de AEMET.
        
        Args:
            api_key: Clave API de AEMET. Si no se proporciona, busca en credenciales.
            credentials_path: Ruta al archivo de credenciales JSON.
        """
        self.api_key = api_key or self._load_api_key(credentials_path)
        if not self.api_key:
            raise ValueError("Se requiere una API key de AEMET. "
                           "Obtén una gratis en: https://opendata.aemet.es/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
    
    def _load_api_key(self, credentials_path: Path = None) -> Optional[str]:
        """Carga la API key desde el archivo de credenciales."""
        path = credentials_path or DEFAULT_CREDENTIALS_PATH
        if path.exists():
            with open(path, 'r') as f:
                data = json.load(f)
                return data.get("api_key")
        return None
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """
        Hace una petición a la API de AEMET.
        La API de AEMET tiene 2 pasos:
        1. Pide el endpoint con la API key -> devuelve una URL de datos
        2. Consulta esa URL para obtener los datos reales
        """
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key
        
        # Primer paso: obtener URL de datos
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Verificar si hay error
        if "error" in data:
            raise Exception(f"Error de API: {data.get('error', 'Desconocido')}")
        
        # Segundo paso: obtener datos de la URL proporcionada
        if "datos" in data:
            data_url = data["datos"]
            data_response = self.session.get(data_url)
            data_response.raise_for_status()
            return data_response.json()
        
        return data
    
    # ========== MAESTRO ==========
    
    def get_all_municipios(self) -> List[Dict]:
        """
        Obtiene todos los municipios de España.
        Útil para buscar el ID de un municipio para predicciones.
        """
        return self._make_request("/api/maestro/municipios")
    
    def get_municipio(self, municipio: str) -> List[Dict]:
        """Obtiene información de un municipio específico."""
        return self._make_request(f"/api/maestro/municipio/{municipio}")
    
    # ========== OBSERVACIÓN ==========
    
    def get_observation_all(self) -> List[Dict]:
        """
        Obtiene datos de observación de todas las estaciones.
        Datos de las últimas 12 horas.
        """
        return self._make_request("/api/observacion/convencional/todas")
    
    def get_observation_station(self, idema: str) -> List[Dict]:
        """
        Obtiene datos de observación de una estación específica.
        
        Args:
            idema: Indicativo climatológico de la estación (ej: 'C4494E' para Utrera)
        """
        return self._make_request(f"/api/observacion/convencional/datos/estacion/{idema}")
    
    # ========== PREDICCIONES POR CCAA ==========
    
    def get_pred_ccaa_hoy(self, ccaa: str) -> Dict:
        """
        Predicción para una CCAA hoy.
        
        Args:
            ccaa: Código de comunidad (ej: 'and', 'mad', 'val')
        """
        if ccaa not in CCAA_CODES:
            raise ValueError(f"Código CCAA inválido. Opciones: {list(CCAA_CODES.keys())}")
        return self._make_request(f"/api/prediccion/ccaa/hoy/{ccaa}")
    
    def get_pred_ccaa_manana(self, ccaa: str) -> Dict:
        """Predicción para una CCAA mañana."""
        if ccaa not in CCAA_CODES:
            raise ValueError(f"Código CCAA inválido. Opciones: {list(CCAA_CODES.keys())}")
        return self._make_request(f"/api/prediccion/ccaa/manana/{ccaa}")
    
    def get_pred_ccaa_pasadomanana(self, ccaa: str) -> Dict:
        """Predicción para una CCAA pasado mañana."""
        if ccaa not in CCAA_CODES:
            raise ValueError(f"Código CCAA inválido. Opciones: {list(CCAA_CODES.keys())}")
        return self._make_request(f"/api/prediccion/ccaa/pasadomanana/{ccaa}")
    
    def get_pred_ccaa_medioplazo(self, ccaa: str) -> Dict:
        """Predicción para una CCAA a medio plazo (7 días)."""
        if ccaa not in CCAA_CODES:
            raise ValueError(f"Código CCAA inválido. Opciones: {list(CCAA_CODES.keys())}")
        return self._make_request(f"/api/prediccion/ccaa/medioplazo/{ccaa}")
    
    # ========== PREDICCIÓN POR HORAS ==========
    
    def get_pred_horaria(self, municipio_id: str) -> Dict:
        """
        Obtiene predicción horaria para un municipio.
        
        Args:
            municipio_id: ID del municipio (ej: '41095' para Utrera)
            
        Returns:
            Dict con los datos de predicción por horas
        """
        return self._make_request(f"/api/prediccion/especifica/municipio/horaria/{municipio_id}")
    
    def get_pred_horaria_formatted(self, municipio_id: str, dias: int = 2) -> str:
        """
        Obtiene predicción horaria formateada para Telegram.
        
        Args:
            municipio_id: ID del municipio (ej: '41095' para Utrera)
            dias: Número de días a mostrar (por defecto 2)
            
        Returns:
            String formateado con la predicción
        """
        data = self.get_pred_horaria(municipio_id)
        
        if not data or not isinstance(data, list):
            return "No hay datos disponibles"
        
        pred_data = data[0]
        nombre = pred_data.get("nombre", "Unknown")
        provincia = pred_data.get("provincia", "Unknown")
        elaborado = pred_data.get("elaborado", "")
        prediccion = pred_data.get("prediccion", {})
        dias_pred = prediccion.get("dia", [])
        
        result = f"⏰ *Predicción horaria - {nombre} ({provincia})*\n"
        result += f"📅 Actualizado: {elaborado[:16] if elaborado else 'N/A'}\n\n"
        
        # Mostrar los primeros dias
        for dia_data in dias_pred[:dias]:
            fecha = dia_data.get("fecha", "")[:10]
            orto = dia_data.get("orto", "")
            ocaso = dia_data.get("ocaso", "")
            
            result += f"📆 *{fecha}* (🌅 {orto} - 🌇 {ocaso})\n"
            
            # Temperaturas
            temps = dia_data.get("temperatura", [])
            if temps:
                # Obtener mín y máx del día
                temp_values = [int(t.get("value", 0)) for t in temps if t.get("value")]
                if temp_values:
                    temp_min = min(temp_values)
                    temp_max = max(temp_values)
                    result += f"   🌡️ {temp_min}° - {temp_max}°C\n"
            
            # Horas clave (mañana, tarde, noche)
            horas_clave = ["08", "12", "14", "18", "21"]
            
            # Estado del cielo
            estados = {e.get("periodo"): e.get("descripcion", "") for e in dia_data.get("estadoCielo", [])}
            temps_dict = {t.get("periodo"): t.get("value", "") for t in dia_data.get("temperatura", [])}
            humedad = {h.get("periodo"): h.get("value", "") for h in dia_data.get("humedadRelativa", [])}
            viento = {v.get("periodo"): (v.get("direccion", [""])[0], v.get("velocidad", [""])[0]) 
                     for v in dia_data.get("vientoAndRachaMax", []) if "direccion" in v}
            
            for hora in horas_clave:
                estado = estados.get(hora, "-")
                temp = temps_dict.get(hora, "-")
                hum = humedad.get(hora, "-")
                wind = viento.get(hora, ("-", "-"))
                
                emoji_clima = self._get_weather_emoji(estado)
                result += f"   {emoji_clima} {hora}:00 - {temp}° | 💧{hum}% | 💨{wind[0]} {wind[1]}km/h\n"
            
            result += "\n"
        
        return result.strip()
    
    @staticmethod
    def _get_weather_emoji(descripcion: str) -> str:
        """Convierte descripción del cielo a emoji."""
        desc = descripcion.lower() if descripcion else ""
        if "despejado" in desc:
            return "☀️"
        elif "poco nuboso" in desc:
            return "⛅"
        elif "nuboso" in desc and "muy" not in desc:
            return "⛅"
        elif "muy nuboso" in desc:
            return "☁️"
        elif "cubierto" in desc:
            return "☁️🌧️"
        elif "niebla" in desc:
            return "🌫️"
        elif "lluvia" in desc or "chubasco" in desc:
            return "🌧️"
        elif "tormenta" in desc:
            return "⛈️"
        elif "nieve" in desc:
            return "❄️"
        elif "nubes" in desc or "altas" in desc:
            return "⛅"
        elif "sol" in desc:
            return "☀️"
        else:
            return "🌤️"
    
    # ========== AVISOS ==========
    
    def get_avisos(self, area: str = "esp") -> Dict:
        """
        Obtiene los últimos avisos meteorológicos.
        
        Args:
            area: Código de área (ej: 'esp', '61' para Andalucía, 'mad' para Madrid)
        """
        return self._make_request(f"/api/avisos_cap/ultimoelaborado/area/{area}")
    
    def get_avisos_archivo(self, fecha_ini: str, fecha_fin: str) -> Dict:
        """
        Obtiene avisos en un rango de fechas.
        
        Args:
            fecha_ini: Fecha inicial (formato: AAAA-MM-DDTHH:MM:SSUTC)
            fecha_fin: Fecha final (formato: AAAA-MM-DDTHH:MM:SSUTC)
        """
        return self._make_request(
            f"/api/avisos_cap/archivo/fechaini/{fecha_ini}/fechafin/{fecha_fin}"
        )
    
    # ========== MAPAS ==========
    
    def get_mapas_analisis(self) -> Dict:
        """Obtiene mapas de análisis (presión en superficie)."""
        return self._make_request("/api/mapasygraficos/analisis")
    
    # ========== HELPERS ==========
    
    def find_municipio(self, nombre: str) -> List[Dict]:
        """
        Busca municipios por nombre.
        
        Args:
            nombre: Nombre del municipio a buscar
        """
        municipios = self.get_all_municipios()
        nombre_lower = nombre.lower()
        return [m for m in municipios if nombre_lower in m.get("nombre", "").lower()]
    
    def get_ccaa_name(self, code: str) -> str:
        """Obtiene el nombre de una CCAA por su código."""
        return CCAA_CODES.get(code, "Desconocido")
    
    @staticmethod
    def list_ccaa() -> Dict:
        """Lista todos los códigos de CCAA disponibles."""
        return CCAA_CODES.copy()


# ========== EJEMPLO DE USO ==========

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        client = AemetClient()
        
        # Listar CCAA disponibles
        print("CCAA disponibles:", client.list_ccaa())
        
        # Buscar municipio
        print("\nBuscando Utrera...")
        resultados = client.find_municipio("Utrera")
        for m in resultados[:3]:
            print(f"  - {m.get('nombre')} (ID: {m.get('idema')})")
        
        # Predicción de Andalucía hoy
        print("\nPredicción para Andalucía hoy:")
        pred = client.get_pred_ccaa_hoy("and")
        print(json.dumps(pred, indent=2, ensure_ascii=False)[:1000])
        
    except ValueError as e:
        print(f"Error de configuración: {e}")
    except Exception as e:
        print(f"Error: {e}")
