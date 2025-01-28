from transformers import pipeline
from PIL import Image
import io

# Initialize the pipeline for image classification
pipe = pipeline("image-classification", model="metadome/face_shape_classification")

# Function to process uploaded image and classify it
def classify_image(uploaded_image):
    # Open the image from the uploaded file (assuming the uploaded image is a binary file)
    image = Image.open(io.BytesIO(uploaded_image))

    # Perform face shape classification
    result = pipe(image)

    # Return the classification result
    return result

# Example: Simulate an image upload by reading an image file (in this case, per.jpg)
# You can replace this with the actual uploaded image when using this in a web app
with open("per.jpg", "rb") as image_file:
    uploaded_image = image_file.read()

# Call the function and print the result
result = classify_image(uploaded_image)
print(result)
