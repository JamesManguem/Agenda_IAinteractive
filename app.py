from flask import Flask
from flask import render_template, request, redirect, url_for, flash, send_from_directory
#importamos el modulo que nos permite trabajar con la base de datos MySql
from flask_mysqldb import MySQL
from datetime import  datetime
#importamos os para entrar al sistema operativo y poder modificar las fotos en uploads
import os

#iniciador del servidor
app = Flask(__name__)




#Cadena de conexión, cambiar los datos para ejecutarla en su servidor local

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='contacts'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

#creapos la variable carpeta que nos permite acceder a uploads
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)


#creamos las rutas que seran mostradas.
@app.route('/')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos ')
    data = cur.fetchall()
    # print(data)
    cur.close()

    return render_template('agenda/index.html' ,contactos=data)

#Esta ruta muestra el formulario para agregar a la agenda
@app.route('/create')
def create():
    return render_template('agenda/create.html')

#En esta ruta se procesa la información ingresada al formulario
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        telefono = request.form['telefono']
        correo = request.form['correo']
        foto=request.files['foto']

        if nombre == '' or apellido_paterno == '' or telefono =='' or correo == '' or foto == '':
            flash('Recuerda llenar los datos de los campos')
            return redirect(url_for('create'))

        #obtenemos el fotmato del tiempo y lo guardamos en la varibale tiempo.
        now = datetime.now()
        tiempo=now.strftime("%Y%H%M%S")
        #si el campo foto no esta vacio, en la variable newnamepicture guardamos el tiempo y nombre de la foto
        #guardamos la foto en la carpeta uploads por la fecha de subida, para no sobreescribir fotos con el mismo nombre
        if foto.filename != '':
            newnamepicture=tiempo+foto.filename
            foto.save("uploads/"+newnamepicture)

        #se crea la variable cur para almacenar, el conector de mysql.connection
        #se executa el query con cur.excute, y se ralizar el commit para aplicar el query
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (id,nombre,apellido_paterno,apellido_materno,telefono,correo,foto) VALUES (NULL,%s,%s,%s,%s,%s,%s)',
                    (nombre,apellido_paterno,apellido_materno,telefono,correo,newnamepicture))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')
        return redirect('/')

#ruta para eliminar
@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT foto FROM contactos WHERE id={0}".format(id))
    fila = cur.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto removido satisfactoriamente')
    return redirect(url_for('index'))




#Ruta para mostrar el formulario para editar la información del contacto
@app.route('/edit/<string:id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()

    return render_template('agenda/edit.html', contactos = data)

@app.route('/update', methods = ['POST'])
def update():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        telefono = request.form['telefono']
        correo = request.form['correo']
        foto=request.files['foto']
        id=request.form['id']

        cur = mysql.connection.cursor()

        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        # recuperar y modificar foto
        if foto.filename != '':
            newnamepicture = tiempo + foto.filename
            foto.save("uploads/" + newnamepicture)
            cur.execute("SELECT foto FROM contactos WHERE id={0}".format(id))
            fila = cur.fetchall()
            os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
            cur.execute("UPDATE contactos SET foto=%s WHERE id=%s", (newnamepicture, id))
            mysql.connection.commit()

        cur.execute('UPDATE contactos SET nombre=%s,apellido_paterno=%s ,apellido_materno=%s,telefono=%s,correo=%s   WHERE id=%s',
                   (nombre, apellido_paterno,apellido_materno,telefono,correo, id))
        flash('Se ha actualizado la información del contacto')
        mysql.connection.commit()
        return redirect('index')














# para arrancar la app en modo debug en el puerto 3000
if __name__ == "__main__":
    app.run(port=3000, debug=True)