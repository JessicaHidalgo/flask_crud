import os
from flask import Flask,request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "estados.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Estado (db.Model):
    clave = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    description = db.Column(db.String(80))
    
    def __repr__(self):
        return f"<Descripción:{self.description}" 

@app.route("/", methods=['GET','POST'])
def index():
    estados = None
    if request.form:
        try:
            clave = request.form.get("clave")
            description = request.form.get("description")
            estado = Estado(clave=clave, description=description)
            db.session.add(estado)
            db.session.commit()
        except Exception as e:
            print(f"Error al agregar un estado {e}") 
    estados = Estado.query.all()
    return render_template("estados.html", estados= estados)

@app.route("/update", methods=["POST"])
def update():
    try: 
          nueva_description= request.form.get("nueva_description")
          clave = request.form.get("clave")
          estado = Estado.query.filter_by(clave=clave).first()
          estado.description = nueva_description
          db.session.commit()
    except Exception as e:
        print(f"Error al actualizar el estado: \n {e}")
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    try: 
          clave = request.form.get("clave")
          estado = Estado.query.filter_by(clave=clave).first()
          db.session.delete(estado)
          db.session.commit()
    except Exception as e:
        print(f"Error al borrar el estado: \n {e}")
    return redirect("/")
