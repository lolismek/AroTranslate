from transformers import AutoModelForSeq2SeqLM
from transformers import NllbTokenizer
#from tqdm.auto import tqdm
from ro_diacritics import restore_diacritics

import nltk
nltk.download('punkt')

model_load_name = 'ron-rup-v2'
model = AutoModelForSeq2SeqLM.from_pretrained(model_load_name)
tokenizer = NllbTokenizer.from_pretrained(model_load_name)

punctuation = ['.', ',', '?', '!', ':', ';']

def convert_text(text, lang, add_punctuation):
    if lang == 'rup':
        text = text.replace("'", "-")
        text = text.replace("`", "-")
        text = text.replace('–', '-')
        text = text.replace('’', '-')
        text = text.replace('‘', '-')
        text = text.replace('ʹ', '-')
        text = text.replace('—', '-')

    if lang == 'ron':
        text = text.replace('ă', 'a')
        text = text.replace('Â', 'A')
        text = text.replace('â', 'a')
        text = text.replace('Ă', 'A')
        text = text.replace('Î', 'I')
        text = text.replace('î', 'i')

        text = text.replace('ş', 's')
        text = text.replace('ș', 's')
        text = text.replace('ţ', 't')
        text = text.replace('ț', 't')
        text = text.replace('Ş', 'S')
        text = text.replace('Ș', 'S')
        text = text.replace('Ţ', 'T')
        text = text.replace('Ț', 'T')
    else:
        text = text.replace('ă', 'a')
        text = text.replace('Â', 'A')
        text = text.replace('â', 'a')
        text = text.replace('Ă', 'A')
        text = text.replace('Î', 'I')
        text = text.replace('î', 'i')

        text = text.replace('ş', 'sh')
        text = text.replace('ș', 'sh')
        text = text.replace('ţ', 'ts')
        text = text.replace('ț', 'ts')
        text = text.replace('Ş', 'Sh')
        text = text.replace('Ș', 'Sh')
        text = text.replace('Ţ', 'Ts')
        text = text.replace('Ț', 'Ts')

        text = text.replace('ã', 'a')
        text = text.replace('ñ', 'n')
        text = text.replace('ŭ', 'u')
        text = text.replace('Ã', 'A')
        text = text.replace('á', 'a')
        text = text.replace('à', 'a')
        text = text.replace('ς', 'c')
        text = text.replace('é', 'e')
        text = text.replace('í', 'i')
        text = text.replace('ū', 'u')
        text = text.replace('ì', 'i')
        text = text.replace('ā', 'a')
        text = text.replace('ĭ', 'i')
        text = text.replace('γ', 'y')
        text = text.replace('Ḑ', 'D')
        text = text.replace('ń', 'n')
        text = text.replace('Ń', 'N')
        text = text.replace('ḑ', 'd')
        text = text.replace('ḍ', 'd')
        text = text.replace('ï', 'i')
        text = text.replace('ḍ', 'd')
        text = text.replace('ḍ', 'd')
        text = text.replace('Ñ', 'N')
        text = text.replace('ó', 'o')
        text = text.replace('θ', 'O')

    text = text.lower()

    if add_punctuation:
        if len(text) > 0 and not (text[len(text) - 1] in punctuation):
            text += '.'

    return text 

# create dictionaries:
ron_words = []
with open('dictionar/samples_ron.txt', 'r') as file:
    for word in file:    
        word = word.strip()
        word = word.replace('\n', '')
        ron_words.append(convert_text(word, 'ron', False))
file.close()
rup_words = []
with open('dictionar/samples_rup.txt', 'r') as file:
    for word in file:
        word = word.strip()
        word = word.replace('\n', '')
        rup_words.append(convert_text(word, 'rup', False))
file.close()

print(len(rup_words))
print(len(ron_words))
ron_rup = {}
rup_ron = {}
ind = 0
while ind < len(ron_words):
    if not ron_words[ind] in ron_rup:
        ron_rup[ron_words[ind]] = rup_words[ind]
    ind += 1
ind = 0
while ind < len(rup_words):
    if not rup_words[ind] in rup_ron:
        rup_ron[rup_words[ind]] = ron_words[ind]
    ind += 1

print("finished job!")

def capitalize_first_letter(input_string):
    for i, char in enumerate(input_string):
        if char.isalpha():
            return input_string[:i] + char.upper() + input_string[i+1:]
    return input_string

def Translate(text, src_lang='ron_Latn', tgt_lang='ron_Latn', a=32, b=3, max_input_length=1024, num_beams=4, **kwargs):
    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = tgt_lang
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=max_input_length)
    result = model.generate(
        **inputs.to(model.device),
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_new_tokens=int(a + b * inputs.input_ids.shape[1]),
        num_beams=num_beams,
        **kwargs
    )

    return tokenizer.batch_decode(result, skip_special_tokens=True)

def Big_Translate(text, FROM, TO):
    words = text.split()

    if len(words) > 128:
        return ''

    sentences = nltk.sent_tokenize(text)
    ans = ''
    for sentence in sentences:
        sentence = convert_text(sentence, FROM, True)

        found = False
        words = sentence.split()
        


        if len(words) == 1:
            if FROM == 'rup' and sentence[:-1] in rup_ron:
                found = True
                sentence = rup_ron[sentence[:-1]]
            elif FROM == 'ron' and sentence[:-1] in ron_rup:
                found = True
                sentence = ron_rup[sentence[:-1]]

        if not found:
            sentence = Translate(sentence)
            sentence = sentence[0]

        sentence = capitalize_first_letter(sentence)
        if TO == 'ron':
            sentence = restore_diacritics(sentence)
        ans += sentence
        ans += ' '

    return ans

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # from_language = request.form['from_language']
    # to_language = request.form['to_language']
    text_to_translate = request.form['text_to_translate']
    from_lang = request.form['from_lang']
    to_lang = request.form['to_lang']

    from_lang = from_lang.lower()
    to_lang = to_lang.lower()

    #translated_text = Translate(text_to_translate)
    translated_text = Big_Translate(text_to_translate, from_lang, to_lang)

    return jsonify({'translated_text': translated_text})

@app.route('/about')
def index2():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run(debug=True, port=81, host="0.0.0.0")

#API Request Failed: GET /api/v4/accounts/7f2c6bb78151b4a5cd5f00cc060fad04/workers/domains/records?zone_id=03cfc989cfa5be94a5258fed4b6f2cdc (undefined)
# "before-piatra" works better than "after-piatra" !!! 
# -----> foarte posibil sa mearga mai bine daca putem adauga o eticheta separata pt RUP