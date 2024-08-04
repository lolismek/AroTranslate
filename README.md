# The first neural machine translation system for the Aromanian language
<br>
Aromanian is an endangered Eastern Romance dialectal language spoken mainly in Greece, but also in Albania, North Macedonia, Romania, Bulgaria, Serbia and is most similar with Romanian. (wiki)
<br> 
This repository contains the deployment of the first automatic translator for Aromanian. Used NLLB-200-600M [1] for fine-tuning under the CC-BY-NC-4.0 license.
<br>
Delivering the unquanitzed model [2], quantized model [3], and romanian-aromanian corpus[4]. Please request access as all of these are momentarily gated.    
<br>

[1] https://huggingface.co/facebook/nllb-200-distilled-600M
<br>
[2] https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1
<br>
[3] https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1-ctranslate
<br>
[4] https://huggingface.co/datasets/alexjerpelea/aromanian-romanian-MT-corpus

# Deployment code

Locally clone the repo
```
git clone https://github.com/lolismek/AroTranslate.git
```

Install requirements
```
pip install -r requirements.txt
```

Login with huggingface using a token with access to the quanitzed model 
```
huggingface-cli login
```

Clone repo in deployment path
```
git clone https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1-ctranslate2
```

Local deploy 🤗
```
python main.py
```

