from flask import Flask, request, jsonify
from transformers import ViTImageProcessor, AutoModelForImageClassification
from PIL import Image
import io

app = Flask(__name__)

# Initialize the image processor and model for image classification
processor = ViTImageProcessor.from_pretrained("metadome/face_shape_classification")
model = AutoModelForImageClassification.from_pretrained("metadome/face_shape_classification")

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify(success=False, message='No image uploaded.')

    gender = request.form.get('gender')
    file = request.files['image']
    
    try:
        # Open the uploaded image
        image = Image.open(io.BytesIO(file.read()))
        
        # Preprocess the image for the model
        inputs = processor(images=image, return_tensors="pt")

        # Perform face shape classification
        outputs = model(**inputs)
        logits = outputs.logits  # Get the logits from the output
        predicted_class_idx = logits.argmax(-1).item()  # Get the predicted class index

        # Map index to face shape label (you need to define this mapping)
        face_shape_labels = ["oval", "square", "round", "heart"]  # Example labels
        face_shape = face_shape_labels[predicted_class_idx]

        # Generate suggestions based on gender and face shape
        suggestions = generate_suggestions(gender, face_shape)

        return jsonify(success=True, data={
            'face_shape': face_shape,
            'suggestions': suggestions,
            'gender': gender
        })
    
    except Exception as e:
        return jsonify(success=False, message=str(e))

def generate_suggestions(gender, face_shape):
    # Define suggestions based on gender and face shape
    male_suggestions = {
        "oval": "A beard style that adds definition to your jawline.",
        "square": "Try a full beard to soften your angular features.",
        "round": "Consider a goatee to elongate your face.",
        "heart": "A short beard can balance your chin.",
    }
    
    female_suggestions = {
        "oval": "Long hairstyles with layers will complement your features.",
        "square": "Soft waves or curls can soften your jawline.",
        "round": "Longer hairstyles that add height can elongate your appearance.",
        "heart": "Side-swept bangs can balance your forehead.",
    }

    if gender == 'male':
        suggestion = male_suggestions.get(face_shape, "No specific suggestions available.")
    else:
        suggestion = female_suggestions.get(face_shape, "No specific suggestions available.")

    return {'male': suggestion if gender == 'male' else "", 
            'female': suggestion if gender == 'female' else ""}

if __name__ == '__main__':
    app.run(debug=True)
