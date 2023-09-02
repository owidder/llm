import os
import json
import openai
import collections

SOURCE_LANGUAGE = "German"
openai.api_key = os.getenv("OPENAI_API_KEY")

LANGUAGES = {
  "alb": "Albanian",
  "arm": "Armenian",
  "awa": "Awadhi",
  "aze": "Azerbaijani",
  "baq": "Basque",
  "bel": "Belarusian",
  "ben": "Bengali",
  "bho": "Bhojpuri",
  "bos": "Bosnian",
  "por": "Portuguese",
  "bul": "Bulgarian",
  "cat": "Catalan",
  "chi": "Chinese",
  "hrv": "Croatian",
  "cze": "Czech",
  "dan": "Danish",
  "doi": "Dogri",
  "dut": "Dutch",
  "est": "Estonian",
  "fao": "Faroese",
  "fin": "Finnish",
  "glg": "Galician",
  "geo": "Georgian",
  "gre": "Greek",
  "guj": "Gujarati",
  "hin": "Hindi",
  "hun": "Hungarian",
  "ind": "Indonesian",
  "gle": "Irish",
  "ita": "Italian",
  "jpn": "Japanese",
  "jav": "Javanese",
  "kan": "Kannada",
  "kas": "Kashmiri",
  "kaz": "Kazakh",
  "kok": "Konkani",
  "kor": "Korean",
  "kir": "Kyrgyz",
  "lav": "Latvian",
  "lit": "Lithuanian",
  "mac": "Macedonian",
  "mai": "Maithili",
  "may": "Malay",
  "mlt": "Maltese",
  "mar": "Marathi",
  "mwr": "Marwari",
  "mon": "Mongolian",
  "cnr": "Montenegrin",
  "nep": "Nepali",
  "nor": "Norwegian",
  "ori": "Oriya",
  "pus": "Pashto",
  "per": "Persian",
  "pol": "Polish",
  "pan": "Punjabi",
  "raj": "Rajasthani",
  "rum": "Romanian",
  "san": "Sanskrit",
  "sat": "Santali",
  "srp": "Serbian",
  "snd": "Sindhi",
  "sin": "Sinhala",
  "slo": "Slovak",
  "slv": "Slovenian",
  "ukr": "Ukrainian",
  "urd": "Urdu",
  "uzb": "Uzbek",
  "vie": "Vietnamese",
  "wel": "Welsh"
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
  return response["choices"][0]["message"]["content"]


def translate_and_back_translate(source_text: str, target_language: str) -> (str, str):
  translation = translate_text(
    text=source_text,
    source_language=SOURCE_LANGUAGE,
    target_language=target_language
  )
  back_translation = translate_text(
    text=translation,
    source_language=target_language,
    target_language=SOURCE_LANGUAGE
  )
  return (translation, back_translation)


def translate_in_all_languages(source_text: str, existing_translations: dict) -> dict:
  translations = existing_translations.copy()
  for language_code in LANGUAGES.keys():
    if not language_code in translations:
      translation, back_translation = translate_and_back_translate(source_text, LANGUAGES[language_code])
      translations[language_code] = translation
      translations[f"{language_code}_back"] = back_translation
      print(f"{source_text}\n--------------\n{LANGUAGES[language_code]}:{translation}\n-----------------\nBack:{back_translation}\n######################")
  return translations


def translate_dict(dict_to_translate: dict) -> dict:
  source_text = dict_to_translate["de"]
  translations = translate_in_all_languages(source_text=source_text, existing_translations=dict_to_translate)
  ordered_translations = collections.OrderedDict(sorted(translations.items()))
  return ordered_translations


def translate_polls(folder_path: str):
  for subdir, dirs, files in os.walk(folder_path):
      for file in files:
        file_abs_path = subdir + os.path.sep + file
        with open(file_abs_path, "r") as f:
          poll = json.load(f)
          translated_poll = dict(poll).copy()
          translated_poll["heading"] = translate_dict(poll["heading"])

        with open(file_abs_path, "w", encoding='utf8') as f:
          json.dump(translated_poll, f, ensure_ascii=False, indent=2)


translate_polls("./i18n/polls")
