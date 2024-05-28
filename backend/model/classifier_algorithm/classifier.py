import numpy as np
from .logistic_regression_model import log_reg, label_encoder

def classify_students(students_data):
    def convert_to_text(value, choices):
        return dict(choices).get(value, '')

    columns_to_encode = [
        'Escolaridad del padre', 'Escolaridad de la madre', 'Ingresos familiares mensuales',
        'Promedio de educación media superior (Bachillerato)', 'Promedio actual (Licenciatura)',
        'Preferencia de estudio', 'Preferencia al realizar actividades académicas', 'Frecuencia de estudio'
    ]

    # Choices equivalentes a las etiquetas
    parents_education_choices = [
        (1, 'Primaria y Secundaria'), (2, 'Media Superior'), (3, 'Superior o mayor')
    ]
    family_income_choices = [
        (1, 'Menor a $5,500 pesos'), (2, 'De $5,500 pesos a $11,000 pesos'), (3, 'Mayor a $11,000 pesos')
    ]
    hsgpa_choices = [
        (1, 'Menor a 7.5'), (2, 'De 7.5 a 8.5'), (3, 'Mayor a 8.5')
    ]
    academic_preferences_choices = [
        (1, 'Solo'), (2, 'Con otra persona'), (3, 'En grupo')
    ]
    study_frequency_choices = [
        (1, 'Diario'), (2, 'Una semana antes de un examen'), (3, 'Un día antes de un examen')
    ]

    features_list = []

    for student in students_data:
        features = [
            convert_to_text(student['father_education'], parents_education_choices),
            convert_to_text(student['mother_education'], parents_education_choices),
            convert_to_text(student['family_income'], family_income_choices),
            convert_to_text(student['high_school_GPA'], hsgpa_choices),
            student['current_GPA'],  # Valor numérico
            convert_to_text(student['study_preference'], academic_preferences_choices),
            convert_to_text(student['preference_academic_activities'], academic_preferences_choices),
            convert_to_text(student['study_frequency'], study_frequency_choices)
        ]
        features_list.append(features)

    features_array = np.array(features_list)

    # Encode the features using the label encoder
    encoded_features = features_array.copy()
    for i, column in enumerate(columns_to_encode):
        encoded_features[:, i] = label_encoder.fit_transform(features_array[:, i])

    # Convert encoded features to float
    encoded_features = encoded_features.astype(float)

    # Make the prediction
    predictions = log_reg.predict(encoded_features)

    return predictions.tolist()
