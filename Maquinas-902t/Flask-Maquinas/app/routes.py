from flask import Blueprint, render_template, request, jsonify, current_app
from service.ping_maquinas import ler_arquivo_de_ips, ping_nas_maquinas
from service.logins import get_last_logins
from service.new import collect_data_from_machine
import json

ARQUIVO_DE_IPS = "/home/wal/sistema/Maquinas-902t/Flask-Maquinas/ip.txt"

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return "Olá, Mundo!"


@routes.route('/ping', methods=['GET'])
def ping_maquinas():
    """
    Rota para verificar o status de máquinas listadas no arquivo ips.txt.
    """
    try:
        lista_de_ips = ler_arquivo_de_ips(ARQUIVO_DE_IPS)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de IPs não encontrado'}), 404

    resultado = ping_nas_maquinas(lista_de_ips)
    return render_template('maquinas_ping.html', resultado=resultado)


@routes.route('/last_logins')
def last_logins():
    lista_de_ips = ler_arquivo_de_ips(ARQUIVO_DE_IPS)
    lista_de_logins = []

    for ip in lista_de_ips:
        logins = get_last_logins(ip['ip'])
        lista_de_logins.append({
            'ip': ip['ip'],
            'logins': logins
        })

    

    # Renderiza a página com os logins
    return render_template('ultimos_login.html', lista_de_logins=lista_de_logins)


@routes.route('/data')
def full_data():
    lista_de_ips = ler_arquivo_de_ips(ARQUIVO_DE_IPS)
    lista = []

    for ip in lista_de_ips:
        total_memory, free_memory, data = collect_data_from_machine(ip['ip'])
        lista.append({
            'ip': ip['ip'],
            'total' : total_memory,
            'free': free_memory,
            'data': data
        })
    return render_template('data.html', data=lista)

@routes.route('/onoff', methods=['GET'])
def onoff():
    """
    Rota para verificar o status de máquinas listadas no arquivo ips.txt.
    """
    try:
        lista_de_ips = ler_arquivo_de_ips(ARQUIVO_DE_IPS)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de IPs não encontrado'}), 404

    resultado = ping_nas_maquinas(lista_de_ips)
    status = []
    for maquina in resultado:
        status.append(maquina['ip_status'])

    status = json.dumps(status)
    return render_template('onoff.html', states=status)

