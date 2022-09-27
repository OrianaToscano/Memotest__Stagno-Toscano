
import sqlite3
from flask import Flask, jsonify, render_template, request, url_for, redirect,session

app = Flask(__name__)
app.secret_key = 'esto-es-una-clave-muy-secreta'

# -------------------- APP ROUTES BASE
@app.route('/')
def index():
    session['nombre'] = ""
    return render_template('login.html')

@app.route('/registro')
def registro():
    session['nombre'] = ""
    return render_template('registro.html')

@app.route('/juego')
def juego():
    if session['nombre'] != "":
      return render_template('juego.html')
    else:
      return 'Logeate!'


#-----------------------------------------------------

# ------------------ LOGIN ---------------------------  
@app.route('/login', methods=['POST'])
def login():
  
  session['nombre'] = request.form['nombre']
  session['contra'] = request.form['contra']
  
  if checkearSiEsta(session['nombre'],session['contra']) == True:
    if session['nombre']=='admin' and session['contra']=='admin':
      session['admin']= True
      
    return "True"
  else:
    return "Usuario inexistente"


@app.route('/registrarse', methods=['POST'])
def registrarse():
  session['admin'] = False
  session['nombre'] = request.form['nombre']
  session['contra'] = request.form['contra']
  if checkearSiEsta(session['nombre'],session['contra']) == True:
    return "Usuario en uso"
  else:
    con = sqlite3.connect('memotest.db')
    q = f"""INSERT INTO Jugadores (nombre,contraseña) VALUES ('{session['nombre']}', '{session['contra']}')"""
    con.execute(q)
    con.commit()
    con.close()
    return 'True'

#existe?
def checkearSiEsta(unUsuario, unaContraseña):
    conn = sqlite3.connect('memotest.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT *
                      FROM Jugadores
                      WHERE nombre = '{unUsuario}'AND contraseña = '{unaContraseña}';
                  """)
    user = cur.fetchall()
    conn.commit()
    conn.close()
    if user != []:
      return True

# --------------------------------------------

@app.route('/tablero/<nivel>')
def obtenerTableros(nivel):
  if nivel != '1' and nivel != '2' and nivel != '3':
    return 'Numero de tablero no valido'
  elif session['nombre'] != "":
    conn = sqlite3.connect('memotest.db')
    cur = conn.cursor()
    # TOMA VALORES DEL TABLERO
    cur.execute(f"""SELECT valor
                    FROM Tableros
                    WHERE idTablero = {int(nivel)-1}
                    ORDER BY numeroFila ASC, numeroColumna ASC;""")
    datosBase = cur.fetchall()
    
    # TOMA CANTIDAD DE FILAS DEL TABLERO
    cur.execute(f"""SELECT numeroFila
                    FROM Tableros
                    WHERE idTablero = {int(nivel)-1}
                    GROUP BY numeroFila;""")  
    cantFilas = cur.fetchall()
    
    conn.commit()
    conn.close()
    
    datosFormateados = []
  
    # DIVIDE LOS VALORES ENTRE LA CANTIDAD DE FILAS QUE HAYA
    mitad = int(len(datosBase)/len(cantFilas))
    
    # RECORRE TODOS LOS VALORES
    for i in range(0,len(cantFilas)):
      fila = []
      
      # RECORRE LA FRACCION DE LOS VALORES BASE CORRESPONDIENTE A UNA FILA
      for k in datosBase[0:mitad]:
        #Agrega el valor al array FILA
        fila.append(k)
        #Borra de los datos base el valor que acaba de agregar a FILA
        datosBase.pop(datosBase.index(k))
  
      # AGREGA LA FILA RESULTANTE A DATOS FORMATEADOS
      datosFormateados.append(fila)
  
    
    pagina = f"""tablero{nivel}"""
    return render_template(f"""{pagina}.html""", datosFormateados = datosFormateados, usuario=session['nombre'])
  else:
    return 'Logeate!'
  

      
# Lista usuarios
def listaUsuarios():
  if session['admin']==True:
    conn = sqlite3.connect('memotest.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT *
                        FROM Jugadores;
                    """)
    rows = cur.fetchall()
    usuarios = []
    for fila in rows:
        usuario = {
            "id": fila[0],
            "nombre": fila[1],
            "contraseña": fila[2],
        }
        usuarios.append(usuario)
    return jsonify(usuarios)




app.run(host='0.0.0.0', port=81)
