import paramiko
import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

# Загружаем переменные окружения
load_dotenv(".env")

# Проверка обязательных переменных
required_vars = ["SERVER_HOST", "SERVER_USER",
                 "SERVER_PASSWORD", "SERVER_PATH"]
missing = [var for var in required_vars if os.getenv(var) is None]

if missing:
    raise ValueError(
        f"❌ В .env отсутствуют переменные: {', '.join(missing)}")

# Конфигурация серверов
servers = [
    {
        "host": os.getenv("SERVER_HOST"),
        "user": os.getenv("SERVER_USER"),
        "password": os.getenv("SERVER_PASSWORD"),
        "path": os.getenv("SERVER_PATH"),
    }
]

# Локальный файл для отправки
file_to_send = r"C:\Users\Nariman.Kadash\Desktop\git\automatization\ssg\update_packages_test_ssg.yml"


def send_file(server, local_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"[+] Подключение к {server['host']} ...")
    ssh.connect(
        server["host"],
        username=server["user"],
        password=server["password"],
    )

    sftp = ssh.open_sftp()
    remote_path = os.path.join(server["path"], os.path.basename(local_file))
    print(f"[+] Отправка {local_file} → {remote_path}")
    sftp.put(local_file, remote_path)

    sftp.close()
    ssh.close()
    print(f"[✓] Файл отправлен на {server['host']}")


if __name__ == "__main__":
    for srv in servers:
        try:
            send_file(srv, file_to_send)
        except Exception as e:
            print(f"[X] Ошибка при отправке на {srv['host']}: {e}")
