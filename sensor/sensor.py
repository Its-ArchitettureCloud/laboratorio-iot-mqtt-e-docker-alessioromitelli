import time
import random
import os
import socket
import paho.mqtt.client as mqtt

# === Parametri configurabili via environment ===
BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVAL = int(os.getenv("SEND_INTERVAL", "5"))
SENSOR_ID = os.getenv("SENSOR_ID", "sensore01")

print(f"[BOOT] Sensore {SENSOR_ID} avviato", flush=True)
print(f"[BOOT] Broker MQTT: {BROKER}:{PORT}", flush=True)
print(f"[BOOT] Intervallo invio: {INTERVAL}s", flush=True)

# === Attesa attiva del broker ===
def wait_for_broker(host, port):
    print("[WAIT] Attendo il broker MQTT...", flush=True)
    while True:
        try:
            socket.create_connection((host, port), timeout=5)

            print("[WAIT] Broker MQTT raggiungibile", flush=True)
            return
        except OSError as e:
            print(f"[WAIT] Broker non disponibile ({e}), ritento...", flush=True)
            time.sleep(2)

# Aspettiamo che Mosquitto sia davvero pronto
wait_for_broker(BROKER, PORT)

# === Client MQTT (API aggiornata) ===
client = mqtt.Client(
    client_id=SENSOR_ID,
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.connect(BROKER, PORT)
print("[MQTT] Connesso al broker", flush=True)

# === Loop principale del sensore ===
while True:
    temperatura = round(random.uniform(15, 35), 1)
    topic = f"iot/aula/{SENSOR_ID}/temperatura"

    result = client.publish(topic, temperatura)

    print(f"[PUBLISH] {topic} → {temperatura} °C (rc={result.rc})", flush=True)

    time.sleep(INTERVAL)