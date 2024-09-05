import json

with open("cunia_diaro_ngrams/fuh.json", 'r') as json_file:
    fuh = json.load(json_file)
json_file.close()

with open("cunia_diaro_ngrams/fah.json", 'r') as json_file:
    fah = json.load(json_file)
json_file.close()

def get_mask(s, index):
    ans = ""
    if index >= 2:
        ans = s[index-2:index]
    elif index >= 1:
        ans = " " + s[index-1:index]
    else:
        ans = "  "

    if index + 2 < len(s):
        ans += s[index+1:index+3]
    elif index + 1 < len(s):
        ans += s[index+1:index+2] + " "
    else:
        ans += "  "

    assert(len(ans) == 4)
    return ans

def cunia_to_diaro(text):
    try:
        changes = {
            "Sh": "Ș",
            "sh": "ș",
            "Ts": "Ț",
            "ts": "ț",
            "Lj": "Ľ",
            "lj": "ľ",
            "Nj": "Ń",
            "nj": "ń",
            "Dz": "Ḑ",
            "dz": "ḑ",
        }

        for change in changes:
            text = text.replace(change, changes[change])

        words = text.split(" ")
        arr = []
        for word in words:
            tmp = word.lower().replace('î', "â")
            new_tmp = ""
            for i, ch in enumerate(tmp):
                if ch == 'ã':
                    msk = get_mask(tmp, i)

                    cnt_ah = 0
                    if msk in fah:
                        cnt_ah = fah[msk]

                    cnt_uh = 0
                    if msk in fuh:
                        cnt_uh = fuh[msk]

                    if cnt_ah > cnt_uh:
                        new_tmp += "â"
                    else:
                        new_tmp += "ă"
                else:
                    new_tmp += ch

            if new_tmp[0] == "â":
                new_tmp = "î" + new_tmp[1:]
            if new_tmp[-1] == "â":
                new_tmp = new_tmp[:-1] + "î"


            lower_word = word.lower()
            tmp = ""
            for i, ch in enumerate(lower_word):
                if lower_word[i] != word[i]:
                    tmp += new_tmp[i].upper()
                else:
                    tmp += new_tmp[i]

            arr.append(tmp)
        
        return " ".join(arr)
    except:
        return text

def diaro_to_cunia(text):
    try:
        changes = {
            "Ă": "Ã",
            "ă": "ã",
            "Â": "Ã",
            "â": "ã",
            "Î": "Ã",
            "î": "ã",
            "Ș": "Sh",
            "ș": "sh",
            "Ț": "Ts",
            "ț": "ts",
            "Ľ": "Lj",
            "ľ": "lj",
            "Ń": "Nj",
            "ń": "nj",
            "Ḑ": "Dz",
            "ḑ": "dz",
        }
        
        new_text = ""
        for ch in text:
            if ch in changes:
                new_text += changes[ch]
            else:
                new_text += ch

        return new_text
    except:
        return text
