import os
import openai

TEMPLATE = """Rewrite the query exactly the same way as the  below examples:
Examples:
- Input query1: "Vẽ biểu đồ tăng trưởng GDP của Việt Nam từ năm 2012 đến năm 2022 ?"
- Output query1: "Vẽ biểu đồ tăng trưởng GDP của Việt Nam năm 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 ?"
==========
- Input query2: "Viet Nam import/export turnover from 2018-2022."
- Output query2: "Viet Nam import/export turnover 2018, 2019, 2020, 2021, 2022."
==========
- Input query3 : "Quelle est la croissance du PIB du Vietnam de 2015 à 2022 ."
- Output query2 : "Quelle est la croissance du PIB du Vietnam en 2015, 2016, 2017, 2018, 2019, 2020, 2021 et 2022 ."
==========
- Input query: $$QUERY$$
- Output query:"""

class Chatgpt_based_rewritor:
    def __init__(self, openai_api_key = ""):
        if openai_api_key != "":
            openai.api_key = openai_api_key
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
    def rewrite(self, query = ""):
        prompt = TEMPLATE.replace("$$QUERY$$", query)
        print(prompt)
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ]
        )
        return completion.choices[0].message["content"]
