import os

from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import nltk
from nltk import sent_tokenize
nltk.download('punkt')

import torch

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)

load_dotenv()

model = AutoModelForSeq2SeqLM.from_pretrained(os.environ['MODEL_PATH'])
tokenizer = AutoTokenizer.from_pretrained(os.environ['MODEL_PATH'])

def generate(title, words, **kwargs):
    storyline = ', '.join(words)
    prompt = f'<extra_id_0> {storyline} <extra_id_1> {title}'

    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    input_ids = input_ids.to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            **kwargs
        ).to('cpu')

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

app = Flask(__name__)
CORS(app, resources={r'/api/v1/*': {'origins': os.environ['CORS_ORIGINS']}})
limiter = Limiter(app, key_func=get_remote_address)

@app.route(r'/api/v1/write', methods=['POST'])
@limiter.limit('1/second')
def write():
    data = request.get_json()

    title = None
    if 'title' in data and type(data['title']) == str:
        title = data['title'].strip()

    words = []
    if 'storyline' in data and type(data['storyline']) == list:
        for word in data['storyline']:
            if type(word) == str:
                word = word.strip()
                if word:
                    words.append(word)

    lines = []
    if title and words:
        story = generate(title, words, top_p=0.9, max_length=1000, do_sample=True, no_repeat_ngram_size=3)
        lines = sent_tokenize(story)
    return jsonify(lines)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
