import time
import random
import matplotlib.pyplot as plt
from google.cloud import storage

# Configuração do Google Cloud Storage
bucket_name = 'your-bucket-name'
file_name = 'water_level_data.csv'
client = storage.Client()
bucket = client.bucket(bucket_name)

# Função para simular a leitura do sensor de nível de água
def read_water_level():
    # Simula um nível de água entre 0 e 100
    return random.uniform(0, 100)

# Função para salvar dados em um arquivo CSV
def save_data_to_csv(data):
    with open(file_name, 'w') as file:
        file.write("timestamp,water_level\n")
        for timestamp, level in data:
            file.write(f"{timestamp},{level}\n")

# Função para enviar o arquivo CSV para o Google Cloud Storage
def upload_to_cloud_storage():
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)
    print(f"File {file_name} uploaded to {bucket_name}.")

# Função para visualizar os dados
def visualize_data(data):
    timestamps, levels = zip(*data)
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, levels, marker='o', linestyle='-', color='b')
    plt.xlabel('Timestamp')
    plt.ylabel('Water Level')
    plt.title('Water Level Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Dados simulados
    data = []
    
    # Coleta de dados por 1 hora
    start_time = time.time()
    while time.time() - start_time < 3600:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        water_level = read_water_level()
        data.append((timestamp, water_level))
        time.sleep(60)  # Espera 1 minuto entre as leituras
    
    # Salva e faz upload dos dados
    save_data_to_csv(data)
    upload_to_cloud_storage()
    
    # Visualiza os dados
    visualize_data(data)

if __name__ == "__main__":
    main()
