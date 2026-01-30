import google.generativeai as genai

genai.configure(api_key="AIzaSyCi8cLJXi3W4eiJMEMYwvwf5k5iuMK5Sp0")

models = genai.list_models()

for m in models:
    print(m.name)