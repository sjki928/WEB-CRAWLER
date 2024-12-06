import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# ChromeDriver 설정
def setup_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Chrome 경로

    # Chrome 옵션 추가
    chrome_options.add_argument("--headless=new")  # 새로운 헤드리스 모드
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# 트리거 요소 처리 함수
def process_triggers(driver, url, max_retries=3):
    extracted_urls = []
    driver.get(url)
    
    retries = 0
    while retries < max_retries:
        try:
            # 트리거 요소 찾기
            triggers = driver.find_elements(By.XPATH, '//a[@href="javascript:void(0);"][contains(@onclick, "fn_bbs")]')
            print(f"Found {len(triggers)} triggers.")
            
            for trigger in triggers:
                # 클릭 트리거
                driver.execute_script("arguments[0].click();", trigger)
                time.sleep(1)  # 페이지 로딩 대기
                
                # 현재 URL 저장
                current_url = driver.current_url
                if current_url not in extracted_urls:
                    extracted_urls.append(current_url)
                    print(f"URL added: {current_url}")
                
                # 이전 페이지로 돌아가기
                driver.back()
                time.sleep(1)
            
            break  # 성공적으로 실행되면 반복 종료
        
        except Exception as e:
            print(f"Error occurred: {e}. Retrying... ({retries+1}/{max_retries})")
            retries += 1
            time.sleep(2)  # 재시도 대기
            
    if retries == max_retries:
        print("Max retries reached. Exiting.")
    
    return extracted_urls

# 결과 저장 함수
def append_results_to_json(file_path, new_results):
    # 기존 데이터 로드
    data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read().strip()
                if content:  # 비어 있지 않으면 JSON 로드
                    data = json.loads(content)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON 파일 로드 중 오류 발생: {e}. 빈 데이터로 초기화합니다.")

    # 새 결과 추가
    data.extend(new_results)

    # 파일에 저장
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# 실행 코드
if __name__ == "__main__":
    import argparse
    from pathlib import Path
    from tqdm import tqdm
    
    # 인자값을 받을 수 있는 인스턴스 생성
    parser = argparse.ArgumentParser(description='사용법 테스트입니다.')

    # 입력받을 인자값 등록
    parser.add_argument('--target_dir', required=True, default='crawled_subpages.json',)
    parser.add_argument('--output_dir', required=False, default='onclick_subpages.json',)
    
    args = parser.parse_args()

    target_dir = Path.cwd() / 'data'/ 'temp'/ args.target_dir
    output_file = Path.cwd() / 'data'/ 'temp'/ args.output_dir

    with open(target_dir,'rb') as f:
        start_urls = json.load(f)
        
    driver = setup_driver()

    try:
        for i,url in enumerate(tqdm(start_urls)):
            print(f"Processing URL: {url}")
            result_urls = process_triggers(driver, url)
            append_results_to_json(output_file, result_urls)
            if i % 30 == 0 and i != 0:
                driver.quit()
                driver = setup_driver()
    finally:
        driver.quit()

    import pandas as pd

    with open(output_file,'rb') as f:
        subpages = json.load(f)

    series=pd.Series(subpages).drop_duplicates()
    li = series.to_list()
    
    with open(output_file, "w") as file:
        json.dump(li, file, indent=4, ensure_ascii=False)