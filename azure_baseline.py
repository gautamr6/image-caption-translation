import requests, uuid, json
import sacrebleu
from decouple import config

# Add your subscription key and endpoint
subscription_key = config('KEY')
endpoint = "https://api.cognitive.microsofttranslator.com"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = config('LOCATION')

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'es',
    'to': 'en'
}
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# Number of instances to use (total is 27367)
n = 1

englishFile = open("en-es/source.final.file-found")
spanishFile = open("en-es/reference.final.file-found")

pred = []
refs = []

for i in range(n):
    spanishLine = spanishFile.readline()
    body = [{
        'text': spanishLine
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    translation = response[0]["translations"][0]["text"]
    pred.append(translation)
    print(translation)

    englishLine = englishFile.readline()
    refs.append(englishLine)
    print(englishLine)
    print()

bleu = sacrebleu.corpus_bleu(pred, [refs])
print(bleu.score)