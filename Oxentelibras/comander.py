from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.secret_key = 'supersecretkey'

#conectando o postgresql
def db_conn():
    conn = psycopg2.connect(database="OxenteLibras", host="localhost", user="postgres", password="GOLDgols.2024", port="5432")
    return conn



@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/retorno', methods=['POST','GET'])
def retorno():
    return redirect('/index')
@app.route('/formsugestao', methods=['POST','GET'])
def formsugestao():
    return redirect('/sugestao')

@app.route("/pesquisa", methods=['GET', 'POST'])
def pesquisa():
    if request.method == 'POST':
        palavra = request.form.get("pesquisa_palavra")
        if palavra:
            # Busca no banco de dados
            conn = db_conn()
            cur = conn.cursor()
            query =(f"SELECT * FROM termo WHERE palavra= '{palavra}';")
            cur.execute(query)
            resultado = cur.fetchall()
            cur.close()
            conn.close()

    return render_template("pesquisa.html", resultado=resultado)

@app.route('/sugestao', methods=['POST','GET'])
def sugestao():
    if request.method == 'POST':
        palavra_sugerida = request.form.get("sugerir_palavra")
        definicao = request.form.get("definicao")
        email = request.form.get("email")
        try:
            #conecta no banco de dados
            conn = db_conn()
            cur = conn.cursor()

            # Adiciona a palavra sugerida no banco de termo
            query = "INSERT INTO termo (palavra, definicao) VALUES (%s, %s);"
            cur.execute(query, (palavra_sugerida, definicao))
            conn.commit()

        finally:
            cur.close()
            conn.close()
    else:
        return render_template("sugerir.html")
    return redirect("/index")


if __name__ == '__main__':
    app.run(debug=True)
