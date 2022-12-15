from peewee import *
import peewee
import datetime

database = peewee.MySQLDatabase(
    'tiendaa',
    port = 3306,
    host = 'localhost',
    user = 'root',
    password = 'tu password'
)

class User(Model):
    nombre = CharField(unique=True,null=False,max_length=50)
    correo = CharField(unique=True,null=False,max_length=50)
    contraseña = IntegerField()
    fecha_creacion = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = database
        db_table = 'users'
    
  
    
class Product(Model):
    nombre = CharField(max_length=50)
    precio = IntegerField()
    descripcion = CharField(max_length=50)
    user = ForeignKeyField(User,backref='products')
    fecha_creacion = DateField( default=datetime.datetime.now())
   
   
 

    class Meta:
        database = database
        db_table = 'products'