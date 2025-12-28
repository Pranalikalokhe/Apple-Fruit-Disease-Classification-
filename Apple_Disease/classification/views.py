from django.shortcuts import render, redirect
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
from django.core.files.storage import FileSystemStorage
import os

# Load the trained model
model = load_model('E:/Internship/Apple Fruit_Disease/AppleDiseaseProject/fruit_disease_model.h5')

# Define class names
class_names = ['Apple__Bitter_Rot', 'Apple___Black_rot', 'Apple___Cedar_rust', 'Apple___healthy', 'Apple___Apple_scab']

# Disease Information Dictionary
DISEASE_INFO = {
    'Apple__Bitter_Rot': {
        'description': 'Bitter Rot is a fungal disease caused by Colletotrichum species that affects apples during warm, humid weather.',
        'symptoms': 'Circular, sunken brown lesions on fruit with concentric rings. Lesions may have a bitter taste. Infected fruit often drops prematurely.',
        'treatment': 'Remove and destroy infected fruit. Apply fungicides containing captan or thiophanate-methyl during the growing season. Prune trees to improve air circulation.',
        'prevention': 'Maintain good orchard sanitation by removing mummified fruit. Ensure proper spacing between trees. Apply preventive fungicide sprays during wet periods.'
    },
    'Apple___Black_rot': {
        'description': 'Black Rot is a serious fungal disease caused by Botryosphaeria obtusa that affects leaves, fruit, and bark of apple trees.',
        'symptoms': 'Purple spots on leaves that enlarge and turn brown. Fruit develops circular, brown to black lesions with concentric rings. Cankers may form on branches.',
        'treatment': 'Prune out dead and diseased branches. Apply fungicides like captan, mancozeb, or thiophanate-methyl. Remove infected fruit and leaves from the orchard.',
        'prevention': 'Practice good sanitation by removing all infected plant material. Avoid overhead irrigation. Apply dormant sprays and maintain tree vigor through proper fertilization.'
    },
    'Apple___Cedar_rust': {
        'description': 'Cedar Apple Rust is caused by the fungus Gymnosporangium juniperi-virginianae and requires both apple and cedar trees to complete its life cycle.',
        'symptoms': 'Bright orange or yellow spots on upper leaf surfaces in spring. Tube-like structures may form on leaf undersides. Fruit may develop raised, rough spots.',
        'treatment': 'Apply fungicides containing myclobutanil or propiconazole at bud break and continue through early summer. Remove nearby cedar trees if possible.',
        'prevention': 'Plant resistant apple varieties. Remove cedar trees within a few hundred yards of the orchard. Apply preventive fungicide sprays starting at pink bud stage.'
    },
    'Apple___healthy': {
        'description': 'Your apple appears healthy! No disease detected. The leaf shows normal color and structure without any signs of infection.',
        'symptoms': 'Vibrant green leaves, no discoloration, spots, or lesions. Normal leaf structure and growth patterns.',
        'treatment': 'No treatment needed. Continue regular orchard maintenance and monitoring.',
        'prevention': 'Maintain tree health through proper watering, fertilization, and pruning. Monitor regularly for early signs of disease. Practice good orchard sanitation.'
    },
    'Apple___Apple_scab': {
        'description': 'Apple Scab is one of the most serious diseases of apple trees, caused by the fungus Venturia inaequalis. It thrives in cool, wet conditions.',
        'symptoms': 'Olive-green to brown spots on leaves and fruit. Leaves may become distorted and drop prematurely. Fruit develops dark, scabby lesions that can crack.',
        'treatment': 'Apply fungicides such as captan, myclobutanil, or mancozeb starting at bud break. Rake and destroy fallen leaves. Prune to improve air circulation.',
        'prevention': 'Plant scab-resistant varieties. Remove leaf litter in fall. Apply preventive fungicide sprays during wet spring weather. Ensure good air circulation through proper pruning.'
    }
}

def home(request):
    return render(request, 'home.html')


def predict_disease(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if not image_file:
            return render(request, 'result.html', {'result': 'No image uploaded.'})

        try:
            # Save the uploaded file
            fs = FileSystemStorage(location='classification/static/uploads/')
            filename = fs.save(image_file.name, image_file)
            uploaded_image_url = f'/static/uploads/{filename}'

            # Preprocess image
            img_path = os.path.join('classification/static/uploads', filename)
            img = Image.open(img_path).resize((224, 224))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Make prediction
            prediction = model.predict(img_array)
            predicted_class = class_names[np.argmax(prediction)]
            
            # Get disease information
            disease_info = DISEASE_INFO.get(predicted_class, None)

            return render(request, 'result.html', {
                'result': predicted_class,
                'uploaded_image_url': uploaded_image_url,
                'disease_info': disease_info
            })

        except Exception as e:
            return render(request, 'result.html', {'result': f'Error: {str(e)}'})

    return redirect('/')
