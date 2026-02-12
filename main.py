from dotenv import load_dotenv
import os
from ollama import Client
import json
import pandas as pd

load_dotenv()  # load environment variables from .env

OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY')

def decode_json_from_codeblock(text: str):
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

def count_work_steps(client, feature_list):
    message = f"""
システム名: 社内向けタスク・進捗管理システム 
機能一覧:
{feature_list}

あなたは優秀なソフトウェアエンジニアです。上記のシステムの機能一覧をもとに、各機能を実現するために必要な作業工程を全て洗い出します。まずは、それぞれの機能の実現に必要な作業工程の数を予想してください。以下のJSONスキーマに従って出力します。

JSON Schema:
{{
  "type": "array",
  "items": {{
    "type": "object",
    "required": ["機能id", "機能名", "作業工程数"],
    "properties": {{
      "機能id": {{
        "type": "string"
      }},
      "機能名": {{
        "type": "string"
      }},
      "作業工程数": {{
        "type": "integer",
        "minimum": 0
      }}
    }},
    "additionalProperties": false
  }}
}}
"""

    messages = [
        {
            "role": "user",
            "content": message
        }
    ]

    response = client.chat('gpt-oss:20b-cloud', messages=messages)
    return response.message.content

def generate_work_steps(client, feature_work_step_counts):
    message = f"""
システム名: 社内向けタスク・進捗管理システム 
機能別必要作業工程数一覧:
{feature_work_step_counts}

あなたは優秀なソフトウェアエンジニアです。上記のシステムの機能別必要作業工程数一覧をもとに、各機能を実現するために必要な作業工程を全て洗い出してください。以下のJSONスキーマに従って出力します。

JSON Schema:
{{
  "type": "array",
  "items": {{
    "type": "object",
    "required": ["機能id", "機能名", "作業工程数"],
    "properties": {{
      "機能id": {{
        "type": "string"
      }},
      "機能名": {{
        "type": "string"
      }},
      "作業工程数": {{
        "type": "integer",
        "minimum": 0
      }},
      "作業工程一覧": {{
        "type": "array",
        "items": {{
          "type": "string"
        }}
      }}
    }},
    "additionalProperties": false
  }}
}}
"""

    messages = [
        {
            "role": "user",
            "content": message
        }
    ]

    response = client.chat('gpt-oss:20b-cloud', messages=messages)
    return response.message.content

def main():
    client = Client(host='https://ollama.com', headers={'Authorization': 'Bearer ' + OLLAMA_API_KEY})

    print("機能一覧の読み込み...")
    with open("features.csv", "r", encoding="utf-8") as f:
        feature_list = f.read()
    print("機能一覧の読み込み完了")

    print("機能別作業工程数の計算...")
    feature_work_step_counts = count_work_steps(client, feature_list)
    print("機能別作業工程数の計算完了")

    print("機能別作業工程の考案...")
    feature_work_steps = generate_work_steps(client, feature_work_step_counts)
    print("機能別作業工程の考案完了")

    print("LLMからの応答のデコード...")
    data = decode_json_from_codeblock(feature_work_steps)
    rows = []
    for item in data:
        for idx, step in enumerate(item["作業工程一覧"], start=1):
            rows.append({
                "機能ID": item["機能id"],
                "機能名": item["機能名"],
                "作業工程番号": idx,
                "作業工程": step
            })
    df = pd.DataFrame(rows)
    print("LLMからの応答のデコード完了")

    print("Excelに変換...")
    # Excelに書き出し
    df.to_excel("work_steps.xlsx", index=False)
    print("Excelに変換完了: work_steps.xlsx")


if __name__ == "__main__":
    main()