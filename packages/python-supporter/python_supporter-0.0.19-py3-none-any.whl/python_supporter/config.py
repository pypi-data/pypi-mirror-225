import json
import os

def load_config_from_json_file(json_file):
    if os.path.exists(json_file):
        with open(json_file, encoding="utf8") as f:
            config = json.load(f)
        return config
    return None

def load_config_from_json_text(json_text):
    config = json.loads(json_text)
    return config

def save_config(file, config):
    with open(file, "w", encoding='utf8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False) #ensure_ascii=False 해줘야 한글이 \uac1c\ubc1c 이 아닌 개발로 정상적으로 표현

def save_json_text(file, json_text):
    #with open(file, "w", encoding='utf8') as f: 
    #    f.write(json_text)
    config = json.loads(json_text)
    save_config(file, config)
