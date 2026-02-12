import google.generativeai as genai

genai.configure(api_key='AIzaSyB4wAyGTwPKk8coP4Vd7dge9rNXJUq0UqE')

try:
    model = genai.GenerativeModel('gemini-3-flash-preview')
    response = model.generate_content('Say hello in one sentence')
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
