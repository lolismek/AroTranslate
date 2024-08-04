# The first neural machine translation system for the Aromanian Language

Aromanian is an endagered Romance language spoken in the Balkans, similar to Romanian. 
We present the first comprehensive Aromanian Translator, a 100k+ sentences aromanian - romanian corpus, and other deliverables, in support of the Aromanian tongue and its speakers. 
<div align="center">
  <img src="https://github.com/user-attachments/assets/0c77ec40-4c47-4fda-a608-a73a430bfcfd" alt="Example Image" width="400">
  <p><em>"Bridging the gap", AI-generated </em></p>
</div>



## Table of contents
- [Motivation](##Motivation)
- [Deliverables](##Deliverables)
- [Deployment](##Deployment)
- [Preprocessing & Training](##Training)
- [License](##License)
- [Future challenges](##Future-challenges)
- [Acknowledgments](##Acknowledgments)

## Motivation

Aromanian is an Eastern Romance language, part of the Proto-Romanian language family. With more than 300k speakers, it has a rich cultural heritage but remains underrepresented in modern technological advancements, particularly in the field of natural language processing. 
<br><br>
Spoken mainly in Greece, Albania, Romania but also North Macedonia, Bulgaria, and Serbia, the Aromanian language has the [endangered](https://endangeredlanguages.com/lang/963) status as speakers tend to assimilate more and more with their national language and culture, and do not pass the tongue to the new generations.
<br><br>
There are very little initiatives for supporting the Aromanian language, mostly due to the governments lack of support. It is only oficially recognized in [North Macedonia and Albania](https://en.wikipedia.org/wiki/Aromanian_language#:~:text=2021%20Australian%20census.-,Official%20status,subject%20in%20some%20primary%20schools.). 
<br><br>
This project, through the tools and data it presents, aims to:
- make digital content more accesible
- allow young Aromanians (and not only) to reconnect with their languages
- increase interest for this subject, especially within the academic medium


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

