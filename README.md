# The first neural machine translation system for the Aromanian language
<br>
Aromanian is an endangered Eastern Romance dialectal language spoken mainly in Greece, but also in Albania, North Macedonia, Romania, Bulgaria, Serbia and relatively most similar with Romanian. (wiki)
<br> 
This repository contains the deployment of the first automatic translator for Aromanian. Used [NLLB-200-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) for fine-tuning under the CC-BY-NC-4.0 license.
Delivering the unquanitzed model [1], quantized model [2], and romanian-aromanian corpus[3]. Please request access as all of these are momentarily gated. 

[1] https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1
[2] https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1-ctranslate
[3] https://huggingface.co/datasets/alexjerpelea/aromanian-romanian-MT-corpus

# Deployment code

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

