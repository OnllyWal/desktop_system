import paramiko

def get_last_logins(ip, username='fbro', password='F!n0$BR0', key_filepath=None):
    """
    Função que se conecta via SSH à máquina remota e executa o comando 'last -i'
    para recuperar os últimos logins com o IP, retornando apenas o login e o timestamp.
    """

    try:
        # Cria um cliente SSH
        client = paramiko.SSHClient()

        # Carrega as chaves do sistema
        client.load_system_host_keys()

        # Adiciona a chave do host automaticamente (não recomendado para produção)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta à máquina remota usando senha ou chave privada
        if password:
            client.connect(ip, username=username, password=password)
        elif key_filepath:
            client.connect(ip, username=username, key_filename=key_filepath)
        else:
            raise ValueError("Você precisa fornecer senha ou caminho para a chave privada.")

        # Executa o comando 'last -i' na máquina remota
        stdin, stdout, stderr = client.exec_command('last -i')

        # Recupera a saída do comando
        output = stdout.read().decode('utf-8')

        # Fecha a conexão SSH
        client.close()

        # Processa a saída e extrai as informações
        logins = output.splitlines()
        login_info = []

        # Processa as linhas retornadas
        for line in logins:
            if 'down' in line or 'wtmp' in line:
                continue

            parts = line.split()
            if len(parts) < 4:
                continue

            user = parts[0]
            timestamp = " ".join(parts[4:])  # Pega a data e hora

            login_info.append({
                'user': user,
                'timestamp': timestamp
            })

        # Retorna os 5 últimos logins com login e timestamp
        print(login_info)
        return login_info[:5]

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return []
