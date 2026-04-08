import serial, json, requests, time

PORTA = 'COM6' 
URL = 'http://localhost:5000/leituras'

try:
    arduino = serial.Serial(PORTA, 9600, timeout=1)
    print(f"Lendo Arduino na {PORTA}...")
    while True:
        linha = arduino.readline().decode('utf-8').strip()
        if linha and linha.startswith('{'):
            try:
                payload = json.loads(linha)
                # Envia para a API do Flask
                requests.post(URL, json=payload)
                print(f"Enviado com sucesso: {payload}")
            except Exception as e:
                print(f"Erro ao processar/enviar: {e}")
        time.sleep(0.1)
except Exception as e:
    print(f"Erro na conexao serial: {e}")