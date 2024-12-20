import paramiko
import re

def execute_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode().strip(), stderr.read().decode().strip()

def get_users(ssh):
    command = "awk -F: '$3 >= 1000 {print $1}' /etc/passwd"
    users_output, _ = execute_command(ssh, command)
    return users_output.splitlines()

def get_last_access(ssh, user):
    command = f"last -n 1 {user} | head -n 1"
    last_access_raw, _ = execute_command(ssh, command)
    match = re.search(r"(\w{3} \w{3} \d{1,2} \d{2}:\d{2})", last_access_raw)
    return match.group(1) if match else "NUNCA ACESSADO"

def get_memory_usage(ssh, user):
    command = f"ps -u {user} --no-headers -o rss | awk '{{sum+=$1}} END {{print sum/1024}}'"
    memory_output, _ = execute_command(ssh, command)
    try:
        return memory_output
    except ValueError:
        return "0.00"

def get_memory_info(ssh):
    total_cmd = "free -m | awk '/^Mem:/ {print $2}'"
    free_cmd = "free -m | awk '/^Mem:/ {print $7}'"
    total_memory, _ = execute_command(ssh, total_cmd)
    free_memory, _ = execute_command(ssh, free_cmd)
    return total_memory or "INDISPONÍVEL", free_memory or "INDISPONÍVEL"

def collect_data_from_machine(machine):
    data = []
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(machine, username='fbro', password='F!n0$BR0', timeout=5)

        total_memory, free_memory = get_memory_info(ssh)
        users = get_users(ssh)
        
        for user in users:
            last_access = get_last_access(ssh, user)
            memory_used = get_memory_usage(ssh, user)

            data.append({
                'user':user,
                'time':last_access,
                'used': memory_used
            })

        ssh.close()
        print(total_memory, free_memory, data)
        return total_memory, free_memory, data

    except Exception as e:
        data.append({
            'user':"erro",
            'time':"erro",
            'used': "erro"
        })
        return "erro", "erro", data