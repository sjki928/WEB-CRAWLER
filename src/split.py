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

target_dir = Path.cwd()/ 'data'/ 'temp'/ args.target_dir
output_dir = Path.cwd()/ 'data'/ 'snapshots'/ args.output_dir 
os.makedirs(output_dir, exist_ok=True)

with open(target_dir,'rb') as f:
    dictionary = json.load(f)

# 기존 데이터 로드
url_path = output_dir/ 'url_title.json'
data = {}
if os.path.exists(url_path):
    try:
        with open(url_path, "r") as file:
            content = file.read().strip()
            if content:  # 비어 있지 않으면 JSON 로드
                data = json.loads(content)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON 파일 로드 중 오류 발생: {e}. 빈 데이터로 초기화합니다.")


for k,v in dictionary.items():
    if v['title']:
        file_name = v['title']+'.json'
        file_name = file_name.replace('/','|')
        
        data[v['title']] = k
        
        file_path = output_dir / file_name
        with open(file_path,'w',encoding='utf-8') as f:
            json.dump(v['content'],f,ensure_ascii=False)
            
# 파일에 저장
with open(url_path, "w") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
