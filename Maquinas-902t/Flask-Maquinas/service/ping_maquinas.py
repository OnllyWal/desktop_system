import os

def ping_ip(ip):

    """
    Função para verificar o status de um IP utilizando o comando ping.
    """

    comando = f"ping -c 1 {ip}"
    resposta = os.system(comando)
    return resposta == 0

def ler_arquivo_de_ips(arquivo_de_ips):

    """
    Função para ler os IPs de um arquivo e retornar uma lista de dicionários.
    """

    lista_de_ips = []

    with open(arquivo_de_ips, 'r') as arquivo:
        for linha in arquivo:
            ip = linha.strip()
            lista_de_ips.append({'ip': ip, 'ip_status': False})

    return lista_de_ips

def ping_nas_maquinas(lista_de_ips):
    
    """
    Função para verificar o status de uma lista de IPs.
    """

    for maquina in lista_de_ips:
        if maquina['ip'] == "172.19.113.0":
            ip = "vazio"
            maquina['ip_status'] = False
        else:
            ip = maquina['ip']
            maquina['ip_status'] = ping_ip(ip)
    return lista_de_ips