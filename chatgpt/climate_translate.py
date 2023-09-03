import os
import json
import openai
import collections

SOURCE_LANGUAGE = "German"
openai.api_key = os.getenv("OPENAI_API_KEY")

LANGUAGES = {
    "alb": "Albanian",
    "arm": "Armenian",
    # "awa": "Awadhi",
    # "aze": "Azerbaijani",
    # "baq": "Basque",
    # "bel": "Belarusian",
    # "ben": "Bengali",
    # "bho": "Bhojpuri",
    # "bos": "Bosnian",
    # "por": "Portuguese",
    # "bul": "Bulgarian",
    # "cat": "Catalan",
    # "chi": "Chinese",
    # "hrv": "Croatian",
    # "cze": "Czech",
    # "dan": "Danish",
    # "doi": "Dogri",
    # "dut": "Dutch",
    # "est": "Estonian",
    # "fao": "Faroese",
    # "fin": "Finnish",
    # "glg": "Galician",
    # "geo": "Georgian",
    # "gre": "Greek",
    # "guj": "Gujarati",
    # "hin": "Hindi",
    # "hun": "Hungarian",
    # "ind": "Indonesian",
    # "gle": "Irish",
    # "ita": "Italian",
    # "jpn": "Japanese",
    # "jav": "Javanese",
    # "kan": "Kannada",
    # "kas": "Kashmiri",
    # "kaz": "Kazakh",
    # "kok": "Konkani",
    # "kor": "Korean",
    # "kir": "Kyrgyz",
    # "lav": "Latvian",
    # "lit": "Lithuanian",
    # "mac": "Macedonian",
    # "mai": "Maithili",
    # "may": "Malay",
    # "mlt": "Maltese",
    # "mar": "Marathi",
    # "mwr": "Marwari",
    # "mon": "Mongolian",
    # "cnr": "Montenegrin",
    # "nep": "Nepali",
    # "nor": "Norwegian",
    # "ori": "Oriya",
    # "pus": "Pashto",
    # "per": "Persian",
    # "pol": "Polish",
    # "pan": "Punjabi",
    # "raj": "Rajasthani",
    # "rum": "Romanian",
    # "san": "Sanskrit",
    # "sat": "Santali",
    # "srp": "Serbian",
    # "snd": "Sindhi",
    # "sin": "Sinhala",
    # "slo": "Slovak",
    # "slv": "Slovenian",
    # "ukr": "Ukrainian",
    # "urd": "Urdu",
    # "uzb": "Uzbek",
    # "vie": "Vietnamese",
    # "wel": "Welsh"
}


def translate_text(text: str, source_language: str, target_language: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert in climate policy. You will be provided with a text in {source_language} language."
                           f"Please translate this text into {target_language}. Please don't touch HTML markups"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    translation = response["choices"][0]["message"]["content"]
    return translation


def translate_and_back_translate(source_text: str, target_language: str) -> (str, str):
    translation = translate_text(
        text=source_text,
        source_language=SOURCE_LANGUAGE,
        target_language=target_language
    )
    clean_translation = translation.split("\n")[0]
    back_translation = translate_text(
        text=clean_translation,
        source_language=target_language,
        target_language=SOURCE_LANGUAGE
    )
    clean_back_translation = back_translation.split("\n")[0]
    return (clean_translation, clean_back_translation)


def translate_part(part: str, language_code: str) -> (str, str):
    rows = part.split("\n")
    translated_rows = []
    back_rows = []
    for row in rows:
        if len(row) > 0:
            translated_row, back_row = translate_and_back_translate(row, LANGUAGES[language_code])
            translated_rows.append(translated_row)
            back_rows.append(back_row)
        else:
            translated_rows.append('')
            back_rows.append('')

    translated_part = "\n".join(translated_rows)
    back_part = "\n".join(back_rows)

    return translated_part, back_part


def translate_into_one_language(existing_translations: dict, language_code: str) -> dict:
    source_text = existing_translations["de"]
    new_translations = existing_translations.copy()
    parts = source_text.split("<br>")
    translated_parts = []
    back_parts = []

    for part in parts:
        translated_part, back_part = translate_part(part=part, language_code=language_code)
        translated_parts.append(translated_part)
        back_parts.append(back_part)

    translation = "<br>".join(translated_parts)
    back_translation = "<br>".join(back_parts)
    new_translations[language_code] = translation
    new_translations[f"{language_code}_back"] = back_translation
    print(
        f"{source_text}\n--------------\n{LANGUAGES[language_code]}:{translation}\n-----------------\nBack:{back_translation}\n######################")

    ordered_translations = collections.OrderedDict(sorted(new_translations.items()))
    return ordered_translations


def write_dict_to_json_file(file_abs_path: str, dict_to_write: dict):
    with open(file_abs_path, "w", encoding='utf8') as f:
        json.dump(dict_to_write, f, ensure_ascii=False, indent=2)


def translate_polls(folder_path: str):
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            file_abs_path = subdir + os.path.sep + file
            with open(file_abs_path, "r") as f:
                poll = json.load(f)
                translated_poll = dict(poll).copy()
                for language_code in LANGUAGES.keys():
                    if not language_code in translated_poll["heading"]:
                        translated_poll["heading"] = translate_into_one_language(existing_translations=translated_poll["heading"], language_code=language_code)
                        write_dict_to_json_file(file_abs_path, translated_poll)
                    if not language_code in translated_poll["description"]:
                        translated_poll["description"] = translate_into_one_language(existing_translations=translated_poll["description"], language_code=language_code)
                        write_dict_to_json_file(file_abs_path, translated_poll)


translate_polls("./i18n/polls")
