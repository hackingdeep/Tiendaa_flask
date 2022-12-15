from flask import Flask
from flask import render_template,request,redirect,url_for,session
from dabase import User,Product
from peewee import *
import json

app = Flask(__name__)

db =Database(app)

app.secret_key = 'jda'

@app.route('/', methods=['GET'])
def index():
    title = 'Shopping Rhan.py'
    return render_template('index.html', title=title)


@app.route('/login',methods=['GET','POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        contraseña = request.form.get('contraseña')
         
       
        if  User.select().where(User.nombre == nombre).exists():  
            return redirect('/products')
        else:
            return redirect('/register')
            
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    title = 'Nuevo registro'
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        
        usuario = User.select().where(User.nombre == nombre).exists()
        if usuario :
            return redirect('/login')
            
        else:
            Usuarios = User.create(nombre=nombre,correo=correo,contraseña=contraseña)
            session['user'] = Usuarios.id
            return redirect('/products')
            
    return render_template('register.html', title=title)


@app.route('/products', methods=['GET'])
def products():
    title = 'Listado de productos'
    usuario = User.get(session['user'])
    # productos = Product.select().where(Product.nombre == Product.nombre
    # ,Product.descripcion == Product.descripcion)
    productos = usuario.products
    return render_template('products/index.html',productos=productos)



@app.route('/products/create', methods=['GET','POST'])
def create_product():
    title = 'Listado de productos'

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        descripcion = request.form.get('descripcion')
        
        usuario_id = User.get(session['user'])
        # usuario_id = session['user'] = User.get(User.id)
        print(usuario_id)
        Crear_productos = Product.create(nombre=nombre,precio=precio,descripcion=descripcion,user=usuario_id)
    return render_template('products/create.html')




@app.route('/product/update/<id>',methods=['GET','POST'])
def update_product(id):

    product_id =Product.select().where(Product.id == id).first() 

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        descripcion = request.form.get('descripcion')
        
        producto_update= Product.update(nombre=nombre,precio=precio,descripcion=descripcion).where(Product.id == id)
        producto_update.execute()

    return render_template('products/update.html',product_id =product_id )
       

@app.route('/product/delete/<id>')
def delete_product(id):
    
    
    delete_products = Product.delete().where(Product.id == id)
    delete_products.execute()

    if delete_products == Product.id:
        return redirect('/products')

    return render_template('products/index.html',)


@app.route('/logout')
def logout():
    # user_id =User.select().where(User.id == User.id).first()
    del session['user']

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    db.create_tables([User,Product])