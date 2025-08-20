import paramiko
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Конфигурация
servers = [
    {"host": "10.66.104.111", "user": "kuat.saparov",
        "password": "OJ*+t8YRTCn", "path": "/home/kuat.saparov/ansible/"},
]

file_to_send = r"C:\Users\Nariman.Kadash\Desktop\git\automatization\aks\update_packages_test_aks.yml"  # локальный файл


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
