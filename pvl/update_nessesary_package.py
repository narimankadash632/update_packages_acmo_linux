from dotenv import load_dotenv
import os
import paramiko
import datetime
import sys
sys.stdout.reconfigure(encoding="utf-8")
# Загружаем переменные из .env_pvl
load_dotenv(".env_pvl")

host = os.getenv("SSH_HOST")
user = os.getenv("SSH_USER")
password = os.getenv("SSH_PASS")
ansible_pass = os.getenv("ANSIBLE_PASS")

# команда для выполнения (пример: ansible-playbook)
command = f"ansible-playbook -i /home/kuat.saparov/ansible/inventory /home/kuat.saparov/ansible/update_packages_test_pvl.yml --extra-vars 'ansible_sudo_pass={ansible_pass}'"

# локальный лог-файл
log_file = "ansible_command.log"


def run_remote_command():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"[+] Подключение к {host} ...")
    ssh.connect(host, username=user, password=password)

    print(f"[+] Выполнение команды:\n{command}")
    stdin, stdout, stderr = ssh.exec_command(command)

    # читаем вывод
    output = stdout.read().decode("utf-8", errors="ignore")
    error = stderr.read().decode("utf-8", errors="ignore")

    ssh.close()

    # сохраняем в лог
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.datetime.now()} ---\n")
        f.write(f"Команда: {command}\n")
        f.write("Результат:\n")
        f.write(output if output else "(пусто)\n")
        if error:
            f.write("\nОшибки:\n")
            f.write(error)
        f.write("\n" + "-"*40 + "\n")

    print(f"[✓] Результаты сохранены в {log_file}")


if __name__ == "__main__":
    run_remote_command()
