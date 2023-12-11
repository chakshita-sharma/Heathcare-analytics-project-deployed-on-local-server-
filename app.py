from flask import Flask, render_template, request
import pickle
import numpy as np

model = pickle.load(open('model_rm.pkl', 'rb'))
app = Flask(__name__, template_folder='views')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict_stay():
    case_id = int(request.form.get('case_id'))
    hospital_code = int(request.form.get('Hospital_code'))
    ward_type = request.form.get('Ward_Type')
    if ward_type.lower() == "P":
        ward_type = 0
    elif ward_type.lower() == "Q":
        ward_type = 0
    elif ward_type.lower() == "R":
        ward_type = 0
    elif ward_type.lower() == "S":
        ward_type = 0
    elif ward_type.lower() == "T":
        ward_type = 0
    elif ward_type.lower() == "U":
        ward_type = 0
    else:
        ward_type = 7
    bed_grade = int(request.form.get('Bed Grade'))

    city_code_ptient = int(request.form.get('City_Code_Patient'))
    type_of_admission = request.form.get('Type of Admission')
    if type_of_admission.lower() == 'emergency':
        type_of_admission = 0
    elif type_of_admission.lower() == 'trauma':
        type_of_admission = 1
    elif type_of_admission.lower() == 'urgent':
        type_of_admission = 2
    else:
        type_of_admission = 3
    patient_id = int(request.form.get('patientid'))
    age = int(request.form.get('Age'))
    department = request.form.get('Department')
    if department.lower() == 'tb & chest disease':
        department = 0
    elif department.lower() == 'anesthesia':
        department = 1
    elif department.lower() == 'gynecology':
        department = 2
    elif department.lower() == 'radiotherapy':
        department = 3
    elif department.lower() == 'surgery':
        department = 4
    else:
        department = 5

    visitors_with_patient = int(request.form.get('Visitors with patient'))
    severity_of_illness = request.form.get('Severity of Illness')
    if severity_of_illness.lower() == 'extreme':
        severity_of_illness = 0
    elif severity_of_illness.lower() == 'minor':
        severity_of_illness = 1
    elif severity_of_illness.lower() == 'moderate':
        severity_of_illness = 2
    else:
        severity_of_illness = 3
    admission_deposit = float(request.form.get('Admission_Deposit'))
    available_extra_rooms = float(request.form.get('Available Extra Rooms in Hospital'))

    # prediction
    fin_result = model.predict(np.array([case_id, hospital_code, ward_type, bed_grade, city_code_ptient, type_of_admission, patient_id, age, department, visitors_with_patient, severity_of_illness, admission_deposit, available_extra_rooms]).reshape(1, 13))
    result = fin_result[0]
    if result == 0:
        result = '0-10 Days'
    elif result == 1:
        result = '11-20 Days'
    elif result == 2:
        result = '21-30 Days'
    elif result == 3:
        result = '31-40 Days'
    elif result == 4:
        result = '41-50 Days'
    elif result == 5:
        result = '51-60 Days'
    elif result == 6:
        result = '61-70 Days'
    elif result == 7:
        result = '71-80 Days'
    elif result == 8:
        result = '81-90 Days'
    elif result == 9:
        result = '91-100 Days'
    else:
        result = 'More than 100 Days'
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.debug = 'True'
    app.run(host='0.0.0.0', port=8081)
