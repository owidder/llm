import json
import os
import argparse
from Levenshtein import distance as levenshtein_distance


EU_LANGUAGES = {
    "bul": "Bulgarian",
    "hrv": "Croatian",
    "cze": "Czech",
    "dan": "Danish",
    "dut": "Dutch",
    "est": "Estonian",
    "fin": "Finnish",
    "gre": "Greek",
    "hun": "Hungarian",
    "gle": "Irish",
    "ita": "Italian",
    "lav": "Latvian",
    "lit": "Lithuanian",
    "mlt": "Maltese",
    "pol": "Polish",
    "rum": "Romanian",
    "slo": "Slovak",
    "slv": "Slovenian",
    "swe": "Swedish",
    "spa": "Spanish"
}

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
        <th>check</th>
        <th>translation</th>
    </tr>
'''


def format(text: str) -> str:
    return text.replace("<br>", "").replace("\n", "<br>")


def start_new_table(table_name: str, file_to_write):
    file_to_write.write(f"<h1>{table_name}</h1>")
    file_to_write.write(f"{TABLE_HEAD}")


def add_translation_row(key: str, source_text: str, translation: str, back_translation: str, check: str, file_to_write):
    distance = levenshtein_distance(source_text, back_translation)
    check_formatted = "" if check == "Yes" or distance < 2 else check.replace("<br>", "<br><br>")
    background_color = "rgba(166, 236, 153, .5)" if len(check_formatted) == 0 or distance < 2 else "rgba(242, 169, 59, .5)"
    file_to_write.write(
        f"<tr><td class='bold' style='background: {background_color}'>{key}</td><td style='background: {background_color}'>{format(source_text)}</td><td style='background: {background_color}'>{format(back_translation)}</td><td style='background: {background_color}'>{check_formatted}</td><td style='background: {background_color}'>{format(translation)}</td></tr>\n")


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

    with open(f"{folder_path}/translations.eu.html", "w") as f:
        f.write(f"<html>\n<head><style>{STYLES}</style></head>")

        for language_code in EU_LANGUAGES.keys():
            back_key = f"{language_code}_back"
            check_key = f"{language_code}_checks"
            start_new_table(table_name=EU_LANGUAGES[language_code], file_to_write=f)
            for poll_file_name in polls.keys():
                poll = polls[poll_file_name]
                if language_code in poll["heading"]:
                    add_translation_row(
                        key=f"{poll_file_name}/heading",
                        source_text=poll["heading"]["de"],
                        translation=poll["heading"][language_code],
                        back_translation=poll["heading"][back_key],
                        check=poll["heading"][check_key],
                        file_to_write=f
                    )
                if language_code in poll["description"]:
                    add_translation_row(
                        key=f"{poll_file_name}/description",
                        source_text=poll["description"]["de"],
                        translation=poll["description"][language_code],
                        back_translation=poll["description"][back_key],
                        check=poll["description"][check_key],
                        file_to_write=f
                    )
                for choice_index in range(0, len(poll["choices"])):
                    if language_code in poll["choices"][choice_index]["uiStrings"]:
                        add_translation_row(
                            key=f"{poll_file_name}/opt-{choice_index+1}",
                            source_text=poll["choices"][choice_index]["uiStrings"]["de"],
                            translation=poll["choices"][choice_index]["uiStrings"][language_code],
                            back_translation=poll["choices"][choice_index]["uiStrings"][back_key],
                            check=poll["choices"][choice_index]["uiStrings"][check_key],
                            file_to_write=f
                        )
            f.write("</table>")

        f.write("</html>")


parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True, action='store', help='Path to the files to translate')
args = parser.parse_args()

add_polls(folder_path=args.path)
