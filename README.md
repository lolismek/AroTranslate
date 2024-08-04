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
- [Data collection, preprocessing & training](##Training)
- [Deployment](##Deployment)
- [License](##License)
- [Future challenges](##Future-challenges)
- [Contributions](##Contributions)
- [Acknowledgments](##Acknowledgments)

## Motivation

Aromanian is an Eastern Romance language, part of the Proto-Romanian language family. With more than 300k speakers, it has a rich cultural heritage but remains underrepresented in modern technological advancements, particularly in the field of natural language processing. 
<br><br>
Spoken mainly in Greece, Albania, Romania but also North Macedonia, Bulgaria, and Serbia, the Aromanian language has the [endangered](https://endangeredlanguages.com/lang/963) status as speakers tend to assimilate more and more with their national language and culture, and do not pass the tongue to the new generations.
<br><br>
There are very little initiatives for supporting the Aromanian language, mostly due to the governments lack of help. It is only oficially recognized in [North Macedonia and Albania](https://en.wikipedia.org/wiki/Aromanian_language#:~:text=2021%20Australian%20census.-,Official%20status,subject%20in%20some%20primary%20schools.). 
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

## Data collection, preprocessing & training
As Aromanian is very sparsely documented in the digital space, it was very hard to acquire parallely translated texts. We used a lot of OCR, web scraping and text mining through the document alignment tools we developed for Aromanian and Romanian (see [Deliverables](##Deliverables)). 
<br><br>
Our 100k+ samples corpus is definetely better than previous attempts, enabling coherent translations, but it's still a low resource corpus. We plan on making our sources and corpus fully accessible but we still have to solve some copyright issues. The models are however not affected by this issue. Any contributions you can make regarding the corpus will be very apreciatted (see [Contributions](##Contributions)).
<br><br>
Note that Aromanian is split into multiple [variaties](https://en.wikipedia.org/wiki/Aromanian_dialects), influenced by languages in the region. We do not know what the split of these is in our corpus, but the variaties are mostly mutually intelligible. Another problem, common with poorly documented tongues, is that the grammar and writing systems are not standardized. We chose to convert all Aromanian text to the Cunia (1997) ortography, as it's the most popular within Aromanians, it's the easiest to type on a keyboard (important, as our objective is public deployment) and it's also easier for the tokenizer to process. You can view the conversion code in `deployment/utils.py`.
<br>

<div align="center">
  <img width="677" alt="Screenshot 2024-08-04 at 19 57 49" src="https://github.com/user-attachments/assets/c77fecc6-fa4a-45d1-8b0c-d00efa87d047">
  <p><em>Aromanian ortographic standardizations, source: <a href="https://aclanthology.org/2024.lrec-main.75.pdf">A Multilingual Parallel Corpus for Aromanian</a></em></p>
</div> 


As mentioned, we finetune the [NLLB-200-600M](https://huggingface.co/facebook/nllb-200-distilled-600M), with respect to the [cc-by-nc-4.0](https://spdx.org/licenses/CC-BY-NC-4.0) license. You can view our experiment's parameteres in the `training` folder. NLLB-200 ("No Language Left Behind") is an awesome multilingual translator, being able to translate between any of 202 languages. *However, there are still thousands of languages left behind, and this is were we tried to make our modest contribution, with one more language. We highly encourage people around the world to pursue similar initiatives and leverage models like NLLB.* We took great inspiration from [this](https://cointegrated.medium.com/how-to-fine-tune-a-nllb-200-model-for-translating-a-new-language-a37fc706b865) blog. 
<br><br>
The model relies on language tokens to identify the source and target language, so we added a `rup_Latn` token for Aromanian (the ISO code for Aromanian is `rup`). After 50k training steps, these are the results we report:

|  | ron -> rup | rup -> ron |
|:----|:-----|:-----|
|   BLEU  |  35.31  | 54.69 |  
|   ChrF2++  |  61.27   |  68.87   |  

Altough it is common for translations towards the better documented language to achieve higher scores, a BLEU score difference of almost 20 points is shocking. We hypothesize that the Aromanian - Romanian case is special, as the two have very similar syntax and structure (the main difering point being the vocabulary ad-stratum). Thus, it is very easy for the model to infer meaning from the mere syntax (note that Romanian is one of the languages NLLB has been pretrained on). The same can not be said about the other direction. Nonetheless, this remaines a topic for further study.

Lastly, we ought to mention about the LaBSE model. It has been trained for 70k steps with the sole purpose of embedding Aromanian and Romanian sentences in a commomn space. It yileds accurate results and by applying Dynamic Programming we obtain a quadratic time complexity reliable document aligner for the language pair. 



## Deployment

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



