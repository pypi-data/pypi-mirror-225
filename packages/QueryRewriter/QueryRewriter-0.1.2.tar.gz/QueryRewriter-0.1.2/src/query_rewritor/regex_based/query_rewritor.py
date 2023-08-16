import re 
from langdetect import detect

list_pattern = {
    "vi":[
        r"từ năm (\d{4}) đến năm (\d{4})",
        r"từ năm (\d{4})-(\d{4})",
        r"từ (\d{4}) đến (\d{4})",
        r"từ (\d{4})-(\d{4})",
        r"(\d{4})-(\d{4})"
    ],  
    "en":[
        r"from (\d{4}) to (\d{4})",
        r"from (\d{4})-(\d{4})",
        r"(\d{4})-(\d{4})"
    ],
    "fr":[
        r'de (\d{4}) à (\d{4})',
        r"(\d{4})-(\d{4})"
    ],
    "pt":[
        r'(\d{4})\s*a\s*(\d{4})',
        r"(\d{4})-(\d{4})"
    ]
}


class Re_based_rewritor:
    def __init__(self, patterns = list_pattern):
        self.patterns = patterns 

    def rewrite(self, query):
        lang = self.langdetect(query)
        # print(lang)
        if lang not in self.patterns.keys():
            return "Not supported language"
        else:
            if lang == "pt":
                replacement = self.pt_replacement
            elif lang == "fr":
                replacement = self.fr_replacement
            else:
                replacement = self.norm_replacement
            for pattern in self.patterns[lang]:
                try:
                    output_sentence = re.sub(pattern, replacement, query)
                    if output_sentence.strip() != query.strip():
                        return output_sentence
                except:
                    pass
            return query

    def norm_replacement(self, match):
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        if end_year - start_year < 20:
            years = ", ".join(str(year) for year in range(start_year, end_year + 1))
            return f'{years}'
        else:
            years = ", ".join(str(year) for year in range(end_year - 19, end_year + 1))
            return f'{years}'
    def pt_replacement(self, match):
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        if end_year - start_year < 20:
            years = ", ".join(str(year) for year in range(start_year, end_year + 1))
            return f'em {years} e {end_year}'
        else:
            years = ", ".join(str(year) for year in range(end_year - 19, end_year + 1))
            return f'em {years} e {end_year}'

    def fr_replacement(self, match):
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        if end_year - start_year < 20:
            years = ", ".join(str(year) for year in range(start_year, end_year + 1))
            return f'en {years}'
        else:
            years = ", ".join(str(year) for year in range(end_year - 19, end_year + 1))
            return f'en {years}'

    def langdetect(self, query):
        return detect(query)


# rewritor = Re_based_rewritor()

# print(rewritor.rewrite("Quelle est la croissance du PIB du Vietnam de 2015 à 2022 "))