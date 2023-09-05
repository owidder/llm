import json
import os
import argparse


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
    "wel": "Welsh",
    "swe": "Swedish"
}


STYLES = '''
td, th {
    border: 1px solid black;
}
.source-text {
    font-weight: bolder;
    font-size: 2em;
}

.language {
    font-weight: bolder;
}
'''

TABLE_HEAD = '''
<table>
    <tr>
        <th>language</th>
        <th>translation</th>
        <th>back translation</th>
    </tr>
'''


def format(text: str) -> str:
    return text.replace("<br>", "").replace("\n", "<br>")


def start_new_table(table_name: str, source_text: str, file_to_write):
    file_to_write.write(f"<h1>[{table_name}]</h1>")
    file_to_write.write(f"<span class='source-text'>\"{format(source_text)}\"</span>")
    file_to_write.write(f"{TABLE_HEAD}")


def add_translation_rows(translations: dict, file_to_write):
    for language_code in translations:
        if len(language_code) == 3:
            back_key = f"{language_code}_back"
            file_to_write.write(
                f"<tr><td class='language'>{LANGUAGES[language_code]}</td><td>{format(translations[language_code])}</td><td>{format(translations[back_key])}</td></tr>\n")


def add_polls(folder_path: str):
    for subdir, dirs, files in os.walk(folder_path):
        for file in sorted(files):
            if file.endswith("json"):
                file_abs_path = subdir + os.path.sep + file
                print(f"translating: {file_abs_path}")
                with open(file_abs_path, "r") as f:
                    poll = json.load(f)
                with open(f"{file_abs_path}.html", "w") as f:
                    f.write(f"<html>\n<head><style>{STYLES}</style></head>")

                    start_new_table(table_name="heading", source_text=poll["heading"]["de"], file_to_write=f)
                    add_translation_rows(translations=poll["heading"], file_to_write=f)
                    f.write("</table>")

                    start_new_table(table_name="description", source_text=poll["description"]["de"], file_to_write=f)
                    add_translation_rows(translations=poll["description"], file_to_write=f)
                    f.write("</table>")

                    for choice_index in range(0, len(poll["choices"])):
                        start_new_table(table_name=f"opt-{choice_index+1}", source_text=poll["choices"][choice_index]["uiStrings"]["de"], file_to_write=f)
                        add_translation_rows(translations=poll["choices"][choice_index]["uiStrings"], file_to_write=f)
                        f.write("</table>")

                    f.write("</html>")


parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True, action='store', help='Path to the files to translate')
args = parser.parse_args()

add_polls(folder_path=args.path)
