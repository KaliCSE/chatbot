from flask import Flask,request,jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

GOOGLE_API_KEY='AIzaSyAbxushsr1GUNEymoIHkWXnd_Qmeg0nJNI'
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_instruction = "Gather diverse oncology medical reports and preprocess them to ensure privacy and standardization. Fine-tune a pretrained NLP model specifically for oncology terminology and concepts. Develop algorithms for the chatbot to generate suitable responses based on medical report content. Implement techniques to infuse empathy and sensitivity into the chatbot's responses.Design an interactive system for users to engage with the chatbot in natural conversations while receiving support and information regarding their medical reports."

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def image_format(image_path):
    img = Path(image_path)

    if not img.exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {
            "mime_type": "image/png", ## Mime type are PNG - image/png. JPEG - image/jpeg. WEBP - image/webp
            "data": img.read_bytes()
        }
    ]
    return image_parts

def gemini_output(image_path, system_prompt, user_prompt):

    image_info = image_format(image_path)
    input_prompt= [system_prompt, image_info[0], user_prompt]
    response = model.generate_content(input_prompt)
    return response.text

@app.route("/", methods=['POST'])
def bot():
    system_prompt = """
                   You are a specialist in comprehending receipts.
                   Input images in the form of receipts will be provided to you,
                   and your task is to respond to questions based on the content of the input image.
                   """

    file = request.files['image']
    file.save(secure_filename("New.jpg"))

    image_path = "New.jpg"
    user_prompt = request.form.get("input")

    if not image_path:
        return jsonify({"error": "No image provided"}), 400

    response_text = gemini_output(image_path, system_prompt, user_prompt)
    return jsonify({"message": response_text})

if __name__ == "__main__":
    app.run(debug=True)

