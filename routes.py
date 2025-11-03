from app import app
from flask import render_template, request
import pandas
import sqlite3


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/animal')
def animal():
    return render_template('animal_form.html')


@app.route('/identify_animal', methods=['POST'])
def identify_animal():
    color = request.form['color']
    size = request.form['size']
    sound = request.form['sound']

    if color == 'marrom' and size == 'médio' and sound == 'latido':
        animal = 'cachorro'
    elif color == 'cinza' and size == 'pequeno' and sound == 'miado':
        animal = 'gato'
    else:
        animal = 'desconhecido'

    return render_template('animal_result.html', animal=animal)


@app.route('/contamination')
def contaminacao():
    return render_template('contamination_form.html')


@app.route('/detect_contamination', methods=['POST'])
def detect_contamination():
    temperature = request.form['temperature']
    has_mold = request.form['has_mold']
    expired_food = request.form['expired_food']
    odor = request.form['odor']
    higienizacao = request.form['higienizacao']

    problemas=[]

    if temperature == 'high':
        problemas.append('Temperatura alta. Risco de contaminação!')
    elif temperature == 'low':
        problemas.append('Temperatura muito baixa. Pode prejudicar alguns alimentos.')

    if has_mold == 'yes':
        problemas.append('Presença de mofo detectada. Ação necessária!')

    if expired_food == 'yes':
        problemas.append('Alimentos fora da validade. Risco de contaminação!')

    if odor == 'yes':
        problemas.append('Mau cheiro identificado. Verifique os alimentos.')

    if higienizacao == 'não':
        problemas.append('Necessária higienização da geladeira.')
    elif higienizacao == 'yes':
        result = 'A geladeira está limpa. Nenhuma contaminação detectada.'

    if problemas:
        result = "Problemas encontrados:\n" + "\n- ".join(problemas)
    else:
        result = "A geladeira está limpa. Nenhuma contaminação detectada."

    return render_template('contamination_result.html', result=result)


@app.route('/personality')
def perso():
    return render_template('personality_form.html')


@app.route('/analyze_personality', methods=['POST'])
def analyze_personality():
    name = request.form['name']
    age = int(request.form['age'])
    movie_genre = request.form['movie_genre']
    likes_studying = request.form['likes_studying']
    programming_language = request.form['programming_language']
    likes_beach = request.form['likes_beach']

    # Lógica para analisar a personalidade com base nas respostas

    personality = ''

    if movie_genre in ['comédia', 'ação'] and programming_language == 'Python' and likes_studying == 'sim' and likes_beach == 'sim':
        personality = 'positiva'
    elif movie_genre in ['comédia', 'ação'] and programming_language == 'Python' and likes_studying == 'não' and likes_beach == 'não':
        personality = 'sem sal'
    else:
        personality = 'mal humorada'

    return render_template('personality_result.html', name=name, personality=personality)


@app.route('/soma', methods=['GET', 'POST'])
def soma():
    resultado = None
    if request.method == 'POST':
        try:
            num1 = int(request.form.get('num1'))
            num2 = int(request.form.get('num2'))
            resultado = num1 + num2
        except ValueError:
            resultado = 'Por favor, insira números válidos.'
    
    return render_template('soma.html', resultado=resultado)

data_frame = pandas.read_csv("data/pet.csv")

@app.route("/petshop", methods=["GET", "POST"])
def index():
    dono = ""
    nome = ""
    especie = ""
    raca = ""
    sexo = ""
    cor = ""
    castrado = ""
    peso = ""
    tamanho = ""
    resultados = []

    if request.method == "POST":
        dono = request.form.get("dono", "").strip()
        nome = request.form.get("nome", "").strip()
        especie = request.form.get("especie", "").strip()
        raca = request.form.get("raca", "").strip()
        sexo = request.form.get("sexo", "").strip()
        cor = request.form.get("cor", "").strip()
        castrado = request.form.get("castrado", "").strip()
        peso = request.form.get("peso", "").strip()
        tamanho = request.form.get("tamanho", "").strip()
        filtrar = data_frame.copy()

        if not any([dono, nome, especie, raca, sexo, cor, castrado, peso, tamanho]):
            filtrar = filtrar.head(10)

        if dono:
            filtrar = filtrar[filtrar["Dono"].str.contains(dono, case=False, na=False)]
        if nome:
            filtrar = filtrar[filtrar["Nome"].str.contains(nome, case=False, na=False)]
        if especie:
            filtrar = filtrar[filtrar["Especie"].str.contains(especie, case=False, na=False)]
        if raca:
            filtrar = filtrar[filtrar["Raca"].str.contains(raca, case=False, na=False)]
        if sexo:
            filtrar = filtrar[filtrar["Sexo"].str.contains(sexo, case=False, na=False)]
        if cor:
            filtrar = filtrar[filtrar["Cor"].str.contains(cor, case=False, na=False)]
        if castrado:
            filtrar = filtrar[filtrar["Castrado"].str.contains(castrado, case=False, na=False)]
        if peso:
            try:
                peso_val = float(peso)
                filtrar = filtrar[filtrar["Peso_KG"] == peso_val]
            except ValueError:
                pass
        if tamanho:
            try:
                tamanho_val = float(tamanho)
                filtrar = filtrar[filtrar["Tamanho_CM"] == tamanho_val]
            except ValueError:
                pass

        resultados = filtrar.to_dict(orient="records")

    return render_template("petshop.html", resultados=resultados, total_resultados=len(resultados))
