class DevelopmentConfig():
  """ aqui se encuentra la conexion a la base de datos """
  DEBUG = True
  """ Conexión con la base de datos MYSQL """
  MYSQL_HOST = 'localhost'
  MYSQL_USER = 'root'
  MYSQL_PASSWORD = ''
  MYSQL_DB= 'crudpy'



config={
  'development':DevelopmentConfig
}