import google.generativeai as genai

genai.configure(api_key='AIzaSyB4wAyGTwPKk8coP4Vd7dge9rNXJUq0UqE')

print("Available Gemini models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")
