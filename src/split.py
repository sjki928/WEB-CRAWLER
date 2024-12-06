import json
import os
from pathlib import Path
from datetime import datetime
import argparse
    
# 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser(description='사용법 테스트입니다.')

# 입력받을 인자값 등록
parser.add_argument('--target_dir', required=True, default='crawled_data.json',)
parser.add_argument('--output_dir', required=False, default=datetime.now().strftime('%Y-%m-%d'),)


args = parser.parse_args()

target_dir = Path.cwd() / 'data'/ 'temp'/ args.target_dir
output_dir = Path.cwd() / 'data'/ 'temp'/ args.output_dir 
os.makedirs(output_dir, exist_ok=True)

with open(target_dir,'rb') as f:
    dictionary = json.load(f)

for k,v in dictionary.items():
    if v['title']:
        file_name = v['title']+'.json'
        file_name = file_name.replace('/','|')
        
        
        file_path = output_dir / file_name
        with open(file_path,'w',encoding='utf-8') as f:
            json.dump(v['content'],f,ensure_ascii=False)