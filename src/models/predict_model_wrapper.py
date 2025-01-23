import pickle
import os

def predict_release_risk(release_properties, path_to_model='trained/model_lr.pkl'):
    """
    Пример того что нужно передавать в `release_properties`
    release_properties = [[
        5, #'Importance of Business Processes'
        4, #'Technical Complexity'
        4, #'Team Experience'
        2, #'Level of Integration with Other Systems'
        1, #'Reaction to Mistakes'
        2, #'Criticality of Streams'   
    ]]
    """
    # Получаем абсолютный путь к файлу, учитывая местоположение скрипта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, path_to_model)

    # Загружаем модель
    with open(model_path, 'rb') as f:
        m = pickle.load(f)
        
    # Получаем результат предсказания
    result = m.predict(release_properties)
    return result.tolist()  # Преобразуем numpy array в обычный список
