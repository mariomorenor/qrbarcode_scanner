import xmlrpc.client

url = "http://localhost:8069"
db = "datos"
username = 'bot_tecnico'
password = "bot_tecnico"

common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def get_users():
    users = models.execute_kw(db, uid, password, 'reservaciones.usuarios', 'search_read', [],{'fields':['nombres','apellidos','cedula','email','carrera']} )
    return users

def register_user(data):
    id = models.execute_kw(db,uid,password,'reservaciones.ingresos','create',[data])
    return id
