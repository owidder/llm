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
* {
    font-family: "Gill Sans", sans-serif;
}
td, th {
    background: lightgrey;
    padding: 0.5em;
}
.bold {
    font-weight: bolder;
    font-size: 1em;
}

.language {
    font-weight: bolder;
}
'''

TABLE_HEAD = '''
<table>
    <tr>
        <th>key</th>
        <th>source text</th>
        <th>back translation</th>
        <th>translation</th>
    </tr>
'''


def format(text: str) -> str:
    return text.replace("<br>", "").replace("\n", "<br>")


def start_new_table(table_name: str, file_to_write):
    file_to_write.write(f"<h1>{table_name}</h1>")
    file_to_write.write(f"{TABLE_HEAD}")


def add_translation_row(key: str, source_text: str, translation: str, back_translation: str, file_to_write):
    file_to_write.write(
        f"<tr><td class='bold'>{key}</td><td>{format(source_text)}</td><td>{format(back_translation)}</td><td>{format(translation)}</td></tr>\n")


def add_polls(folder_path: str):
    polls = {}
    for subdir, dirs, files in os.walk(folder_path):
        for file in sorted(files):
            if file.endswith("json"):
                file_abs_path = subdir + os.path.sep + file
                print(f"translating: {file_abs_path}")
                with open(file_abs_path, "r") as f:
                    poll = json.load(f)
                    polls[file] = poll

    with open(f"{folder_path}/translations.all.html", "w") as f:
        f.write(f"<html>\n<head><style>{STYLES}</style></head>")

        for language_code in LANGUAGES.keys():
            back_key = f"{language_code}_back"
            start_new_table(table_name=LANGUAGES[language_code], file_to_write=f)
            for poll_file_name in polls.keys():
                poll = polls[poll_file_name]
                if language_code in poll["heading"]:
                    add_translation_row(key=f"{poll_file_name}/heading", source_text=poll["heading"]["de"], translation=poll["heading"][language_code], back_translation=poll["heading"][back_key], file_to_write=f)
                if language_code in poll["description"]:
                    add_translation_row(key=f"{poll_file_name}/description", source_text=poll["description"]["de"], translation=poll["description"][language_code], back_translation=poll["description"][back_key], file_to_write=f)
                for choice_index in range(0, len(poll["choices"])):
                    if language_code in poll["choices"][choice_index]["uiStrings"]:
                        add_translation_row(
                            key=f"{poll_file_name}/opt-{choice_index+1}",
                            source_text=poll["choices"][choice_index]["uiStrings"]["de"],
                            translation=poll["choices"][choice_index]["uiStrings"][language_code],
                            back_translation=poll["choices"][choice_index]["uiStrings"][back_key],
                            file_to_write=f
                        )
            f.write("</table>")

        f.write("</html>")


parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True, action='store', help='Path to the files to translate')
args = parser.parse_args()

add_polls(folder_path=args.path)
