from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'coffeelab-2024'
DB = os.path.join(os.path.dirname(__file__), 'coffeelab.db')


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    con = db()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS cafes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            roaster TEXT,
            pais_origen TEXT,
            proceso TEXT,
            perfil_taza TEXT,
            fecha_compra TEXT,
            estado TEXT DEFAULT 'en_stock',
            puntuacion REAL
        );
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cafe_id INTEGER,
            metodo TEXT,
            dosis_cafe REAL,
            agua_ml INTEGER,
            temperatura INTEGER,
            tiempo_total TEXT,
            notas TEXT,
            FOREIGN KEY (cafe_id) REFERENCES cafes(id)
        );
        CREATE TABLE IF NOT EXISTS equipo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT,
            tipo TEXT,
            fecha_adquisicion TEXT,
            notas TEXT
        );
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cafe_id INTEGER,
            metodo TEXT,
            fecha TEXT,
            notas TEXT,
            puntuacion REAL,
            FOREIGN KEY (cafe_id) REFERENCES cafes(id)
        );
    """)
    con.commit()
    con.close()


# ── INDEX ──────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('cafes'))


# ── CAFES ──────────────────────────────────────────────────────────────────
@app.route('/cafes')
def cafes():
    con = db()
    rows = con.execute('SELECT * FROM cafes ORDER BY id DESC').fetchall()
    con.close()
    return render_template('cafes.html', cafes=rows, active='cafes')


@app.route('/cafes/add', methods=['POST'])
def add_cafe():
    con = db()
    con.execute(
        'INSERT INTO cafes (nombre,roaster,pais_origen,proceso,perfil_taza,fecha_compra,estado,puntuacion) VALUES (?,?,?,?,?,?,?,?)',
        (request.form['nombre'], request.form['roaster'], request.form['pais_origen'],
         request.form['proceso'], request.form['perfil_taza'], request.form['fecha_compra'],
         request.form['estado'], request.form['puntuacion'] or None)
    )
    con.commit(); con.close()
    flash('Café agregado.', 'success')
    return redirect(url_for('cafes'))


@app.route('/cafes/edit/<int:id>', methods=['GET', 'POST'])
def edit_cafe(id):
    con = db()
    if request.method == 'POST':
        con.execute(
            'UPDATE cafes SET nombre=?,roaster=?,pais_origen=?,proceso=?,perfil_taza=?,fecha_compra=?,estado=?,puntuacion=? WHERE id=?',
            (request.form['nombre'], request.form['roaster'], request.form['pais_origen'],
             request.form['proceso'], request.form['perfil_taza'], request.form['fecha_compra'],
             request.form['estado'], request.form['puntuacion'] or None, id)
        )
        con.commit(); con.close()
        flash('Café actualizado.', 'success')
        return redirect(url_for('cafes'))
    cafe = con.execute('SELECT * FROM cafes WHERE id=?', (id,)).fetchone()
    con.close()
    return render_template('edit_cafe.html', cafe=cafe, active='cafes')


@app.route('/cafes/delete/<int:id>', methods=['POST'])
def delete_cafe(id):
    con = db()
    con.execute('DELETE FROM cafes WHERE id=?', (id,))
    con.commit(); con.close()
    flash('Café eliminado.', 'info')
    return redirect(url_for('cafes'))


# ── RECETAS ────────────────────────────────────────────────────────────────
@app.route('/recetas')
def recetas():
    con = db()
    rows = con.execute(
        'SELECT r.*, c.nombre as cafe_nombre FROM recetas r LEFT JOIN cafes c ON r.cafe_id=c.id ORDER BY r.id DESC'
    ).fetchall()
    cafes_list = con.execute('SELECT id, nombre FROM cafes ORDER BY nombre').fetchall()
    con.close()
    return render_template('recetas.html', recetas=rows, cafes=cafes_list, active='recetas')


@app.route('/recetas/add', methods=['POST'])
def add_receta():
    con = db()
    con.execute(
        'INSERT INTO recetas (cafe_id,metodo,dosis_cafe,agua_ml,temperatura,tiempo_total,notas) VALUES (?,?,?,?,?,?,?)',
        (request.form['cafe_id'] or None, request.form['metodo'],
         request.form['dosis_cafe'] or None, request.form['agua_ml'] or None,
         request.form['temperatura'] or None, request.form['tiempo_total'], request.form['notas'])
    )
    con.commit(); con.close()
    flash('Receta agregada.', 'success')
    return redirect(url_for('recetas'))


@app.route('/recetas/edit/<int:id>', methods=['GET', 'POST'])
def edit_receta(id):
    con = db()
    if request.method == 'POST':
        con.execute(
            'UPDATE recetas SET cafe_id=?,metodo=?,dosis_cafe=?,agua_ml=?,temperatura=?,tiempo_total=?,notas=? WHERE id=?',
            (request.form['cafe_id'] or None, request.form['metodo'],
             request.form['dosis_cafe'] or None, request.form['agua_ml'] or None,
             request.form['temperatura'] or None, request.form['tiempo_total'], request.form['notas'], id)
        )
        con.commit(); con.close()
        flash('Receta actualizada.', 'success')
        return redirect(url_for('recetas'))
    receta = con.execute('SELECT * FROM recetas WHERE id=?', (id,)).fetchone()
    cafes_list = con.execute('SELECT id, nombre FROM cafes ORDER BY nombre').fetchall()
    con.close()
    return render_template('edit_receta.html', receta=receta, cafes=cafes_list, active='recetas')


@app.route('/recetas/delete/<int:id>', methods=['POST'])
def delete_receta(id):
    con = db()
    con.execute('DELETE FROM recetas WHERE id=?', (id,))
    con.commit(); con.close()
    flash('Receta eliminada.', 'info')
    return redirect(url_for('recetas'))


# ── EQUIPO ─────────────────────────────────────────────────────────────────
@app.route('/equipo')
def equipo():
    con = db()
    rows = con.execute('SELECT * FROM equipo ORDER BY tipo, nombre').fetchall()
    con.close()
    return render_template('equipo.html', equipo=rows, active='equipo')


@app.route('/equipo/add', methods=['POST'])
def add_equipo():
    con = db()
    con.execute(
        'INSERT INTO equipo (nombre,marca,tipo,fecha_adquisicion,notas) VALUES (?,?,?,?,?)',
        (request.form['nombre'], request.form['marca'], request.form['tipo'],
         request.form['fecha_adquisicion'], request.form['notas'])
    )
    con.commit(); con.close()
    flash('Equipo agregado.', 'success')
    return redirect(url_for('equipo'))


@app.route('/equipo/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipo(id):
    con = db()
    if request.method == 'POST':
        con.execute(
            'UPDATE equipo SET nombre=?,marca=?,tipo=?,fecha_adquisicion=?,notas=? WHERE id=?',
            (request.form['nombre'], request.form['marca'], request.form['tipo'],
             request.form['fecha_adquisicion'], request.form['notas'], id)
        )
        con.commit(); con.close()
        flash('Equipo actualizado.', 'success')
        return redirect(url_for('equipo'))
    item = con.execute('SELECT * FROM equipo WHERE id=?', (id,)).fetchone()
    con.close()
    return render_template('edit_equipo.html', item=item, active='equipo')


@app.route('/equipo/delete/<int:id>', methods=['POST'])
def delete_equipo(id):
    con = db()
    con.execute('DELETE FROM equipo WHERE id=?', (id,))
    con.commit(); con.close()
    flash('Equipo eliminado.', 'info')
    return redirect(url_for('equipo'))


# ── SESIONES ───────────────────────────────────────────────────────────────
@app.route('/sesiones')
def sesiones():
    con = db()
    rows = con.execute(
        'SELECT s.*, c.nombre as cafe_nombre FROM sesiones s LEFT JOIN cafes c ON s.cafe_id=c.id ORDER BY s.fecha DESC, s.id DESC'
    ).fetchall()
    cafes_list = con.execute('SELECT id, nombre FROM cafes ORDER BY nombre').fetchall()
    con.close()
    return render_template('sesiones.html', sesiones=rows, cafes=cafes_list, active='sesiones')


@app.route('/sesiones/add', methods=['POST'])
def add_sesion():
    con = db()
    con.execute(
        'INSERT INTO sesiones (cafe_id,metodo,fecha,notas,puntuacion) VALUES (?,?,?,?,?)',
        (request.form['cafe_id'] or None, request.form['metodo'], request.form['fecha'],
         request.form['notas'], request.form['puntuacion'] or None)
    )
    con.commit(); con.close()
    flash('Sesión registrada.', 'success')
    return redirect(url_for('sesiones'))


@app.route('/sesiones/edit/<int:id>', methods=['GET', 'POST'])
def edit_sesion(id):
    con = db()
    if request.method == 'POST':
        con.execute(
            'UPDATE sesiones SET cafe_id=?,metodo=?,fecha=?,notas=?,puntuacion=? WHERE id=?',
            (request.form['cafe_id'] or None, request.form['metodo'], request.form['fecha'],
             request.form['notas'], request.form['puntuacion'] or None, id)
        )
        con.commit(); con.close()
        flash('Sesión actualizada.', 'success')
        return redirect(url_for('sesiones'))
    sesion = con.execute('SELECT * FROM sesiones WHERE id=?', (id,)).fetchone()
    cafes_list = con.execute('SELECT id, nombre FROM cafes ORDER BY nombre').fetchall()
    con.close()
    return render_template('edit_sesion.html', sesion=sesion, cafes=cafes_list, active='sesiones')


@app.route('/sesiones/delete/<int:id>', methods=['POST'])
def delete_sesion(id):
    con = db()
    con.execute('DELETE FROM sesiones WHERE id=?', (id,))
    con.commit(); con.close()
    flash('Sesión eliminada.', 'info')
    return redirect(url_for('sesiones'))


# ── LEARNING ───────────────────────────────────────────────────────────────
@app.route('/learning')
def learning():
    return render_template('learning.html', active='learning')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
