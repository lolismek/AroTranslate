import re

def clean_text(text, lang):
    global cnt
    if isinstance(text, float):
        cnt += 1
        return text

    # consecutive spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # old romanian î in the middle of the word
    text = re.sub(r'(?<=\w)î(?=\w)', 'â', text)

    # specific to this book !
    # text = text.replace(',,', '"')

    if lang == 'ron':
        text = text.replace('Ş', 'Ș')
        text = text.replace('ş', 'ș')
        text = text.replace('Ţ', 'Ț')
        text = text.replace('ţ', 'ț')
    else:
        text = text.replace('ş', 'sh')
        text = text.replace('ș', 'sh')
        text = text.replace('ţ', 'ts')
        text = text.replace('ț', 'ts')
        text = text.replace('Ş', 'Sh')
        text = text.replace('Ș', 'Sh')
        text = text.replace('Ţ', 'Ts')
        text = text.replace('Ț', 'Ts')

        text = text.replace('ľ', 'lj')
        text = text.replace('Ľ', 'L')

        text = text.replace("l'", "lj")
        text = text.replace("l’", "lj")
        text = text.replace("L'", "Lj")
        text = text.replace("L’", "Lj")

        text = text.replace('ḑ', 'dz')
        text = text.replace('Ḑ', 'dz')
        text = text.replace('ḍ', 'dz')
        text = text.replace('Ḍ', 'Dz')

        # TODO: add n'
        text = text.replace('ń', 'nj')
        text = text.replace('Ń', 'Nj')
        text = text.replace('ñ', 'nj')
        text = text.replace('Ñ', 'Nj')

        text = text.replace('ă', 'ã')
        text = text.replace('Â', 'Ã')
        text = text.replace('â', 'ã')
        text = text.replace('Ă', 'Ã')
        text = text.replace('á', 'ã')
        text = text.replace('à', 'ã')
        text = text.replace('Á', 'Ã')
        text = text.replace('À', 'Ã')

        text = text.replace('Î', 'Ã')
        text = text.replace('î', 'ã')

        # weird foreign characters
        text = text.replace('ŭ', 'u')
        text = text.replace('ς', 'c')
        text = text.replace('é', 'e')
        text = text.replace('í', 'i')
        text = text.replace('ū', 'u')
        text = text.replace('ì', 'i')
        text = text.replace('ā', 'a')
        text = text.replace('ĭ', 'i')
        text = text.replace('γ', 'y')
        text = text.replace('ï', 'i')
        text = text.replace('ó', 'o')
        text = text.replace('θ', 'O')

    # for both languages:
    text = text.replace('—', '-')
    text = text.replace('–', '-')
    text = text.replace('…', '...')
    text = text.replace('*', '')
    text = text.replace('<', '')
    text = text.replace('>', '')

    text = text.replace('„', '"')
    text = text.replace('”', '"')
    text = text.replace('“', '"')
    text = text.replace('”', '"')

    # TODO: seriously think about this one!!!
    #text = text.replace('"', '')

    text = text.replace('\xa0', '')
    text = text.replace('\ufeff', '')
    text = text.replace('\n', '') 

    return text

def post_process(text):
    # weird bug probably because i handled badly the '-' character
    text = text.replace('<unk>', '-')
    return text