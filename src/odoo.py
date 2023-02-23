import xmlrpc.client
import configparser

config = configparser.ConfigParser()
config.read("c:\\qr\\config.ini")

url = config['server']['host']
db = config['server']['db']
username = config['server']['user']
password = config['server']['password']

common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def get_users():
    users = models.execute_kw(db, uid, password, 'reservaciones.usuarios', 'search_read', [],{'fields':['nombres','apellidos','cedula','email','carrera']} )
    return users

def register_user(data):
    id = models.execute_kw(db,uid,password,'reservaciones.ingresos','create',[data])
    return id
