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

## Deliverables
The following are released:
- [NLLB-200-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) model finetuned for Aromanian - Romanian bidirectional translations, available on [huggingface](https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1). Soon also releasing a Aromanian - Romanian - English model, which will (hopefully) be more robust.
- [Quantized version](https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1-ctranslate) (int8) of the model, using ctranslate2, for much faster inference. Deployable on CPU.
- 100k+ sentences Aromanian - Romanian [corpus](https://huggingface.co/datasets/alexjerpelea/aromanian-romanian-MT-corpus). It is momentarily gated (for copyright concerns of various sources of the text content), so please request access and we will evaluate if your use case is eligible for recieving the dataset.
- [Finetuned LaBSE model](https://huggingface.co/alexjerpelea/LaBSE-aromanian-romanian) for encoding Aromanian and Romanian sentences in the same embedding space, along text alignment class for easier future text mining, inspired by [this paper](https://arxiv.org/abs/2209.09368).

# Deployment

Locally clone the repo:
```
git clone https://github.com/lolismek/AroTranslate.git
```

From now on, operate only inside the `deployment` folder. Install requirements:
```
pip install -r requirements.txt
```

Login with huggingface using a token with access to the quanitzed model:
```
huggingface-cli login
```

Clone repo in deployment path:
```
git clone https://huggingface.co/alexjerpelea/NLLB-aromanian-romanian-v1-ctranslate2
```

Local deploy 🤗
```
python main.py
```

## Preprocessing & Training



