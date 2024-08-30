from flask import Flask, render_template, request, redirect, url_for, flash
from nyoka import PMML44 as pmml
from pypmml import Model

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Carregar o modelo PMML
modelo_pmml = Model.load('PMML_Attrition.pmml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Pegar os dados do formulário
        idade = request.form['age']
        business_travel = request.form['business_travel']
        daily_rate = request.form['daily_rate']
        departamento = request.form['department']
        distance_from_home = request.form['distance_from_home']
        education = request.form['education']
        education_field = request.form['education_field']

        # Criar o dicionário de dados de entrada para o modelo
        input_data = {
            'Age': int(idade),
            'BusinessTravel': business_travel,
            'DailyRate': int(daily_rate),
            'Department': departamento,
            'DistanceFromHome': int(distance_from_home),
            'Education': int(education),
            'EducationField': education_field,
            # Adicionar outras features conforme necessário
        }

        # Fazer a predição usando o modelo PMML
        prediction = modelo_pmml.predict(input_data)
        resultado = prediction['Attrition']

        # Renderizar a página de resultados
        return render_template('result.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
