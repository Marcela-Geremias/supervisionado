from flask import Flask, request, render_template
from pypmml import Model

app = Flask(__name__)

# Carregando o modelo PMML
model = Model.load('PMML_Attrition_Performance.pmml')

# Função para normalizar os dados com base no PMML
def normalize_value(value, orig_min, orig_max, norm_min, norm_max):
    return norm_min + (value - orig_min) * (norm_max - norm_min) / (orig_max - orig_min)

def preprocess_input(data):
    # Convertendo as entradas para os formatos esperados pelo modelo PMML
    # Valores normalizados conforme especificações no arquivo PMML
    normalized_data = {
        'Age': normalize_value(data['Age'], 0.0, 1.0, -2.0714872299761633, 2.5260259477766707),
        'BusinessTravel': normalize_value(data['BusinessTravel'], 0.0, 1.0, -2.4156150692204643, 0.589847606830392),
        'DailyRate': normalize_value(data['DailyRate'], 0.0, 1.0, -1.7359849242154624, 1.7261426961913966),
        'Department': normalize_value(data['Department'], 0.0, 1.0, -1.4010355584854202, 2.3883338453297904),
        'DistanceFromHome': normalize_value(data['DistanceFromHome'], 0.0, 1.0, -1.010565437699911, 2.443297670805304),
        'Education': normalize_value(data['Education'], 0.0, 1.0, -1.8677901251727733, 2.0378307624573524),
        'EducationField': normalize_value(data['EducationField'], 0.0, 1.0, -1.767006019887672, 1.3289401651360209),
        'EmployeeCount': normalize_value(data['EmployeeCount'], 0.0, 1.0, -0.0, 1.0),
        'EmployeeNumber': normalize_value(data['EmployeeNumber'], 0.0, 1.0, -1.7007041856237415, 1.73271184152686),
    }
    print("Normalized Data:", normalized_data)  # Adicione esta linha para depuração
    return normalized_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Coletar dados do formulário
        input_data = {
            'Age': float(request.form['Age']),
            'BusinessTravel': float(request.form['BusinessTravel']),
            'DailyRate': float(request.form['DailyRate']),
            'Department': float(request.form['Department']),
            'DistanceFromHome': float(request.form['DistanceFromHome']),
            'Education': float(request.form['Education']),
            'EducationField': float(request.form['EducationField']),
            'EmployeeCount': float(request.form['EmployeeCount']),
            'EmployeeNumber': float(request.form['EmployeeNumber']),
        }
        
        print("Input Data:", input_data)  # Adicione esta linha para depuração
        
        # Pré-processar os dados
        normalized_data = preprocess_input(input_data)
        
        # Fazer a previsão
        try:
            result = model.predict(normalized_data)
            print("Prediction Result:", result)  # Adicione esta linha para depuração
            
            # Interpretar o resultado da previsão
            # Verifique o formato do resultado
            if isinstance(result, dict):
                # Suponha que o resultado seja um dicionário com chave 'Attrition'
                prediction = result.get('Attrition', 'Unknown')
            else:
                prediction = "Resultado desconhecido"
            
            # Mapeia valores para "Sim" e "Não"
            if prediction == 'Yes':
                prediction = 'Sim'
            elif prediction == 'No':
                prediction = 'Não'
            else:
                prediction = "Resultado desconhecido"
        except Exception as e:
            print("Error during prediction:", e)
            prediction = "Error"
        
        return render_template('result.html', prediction=prediction)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
