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
    with open('/workspace/crawled_subpages.json','rb') as f:
        data = json.load(f)
    start_urls = list(data.values())
    
    output_file = "/workspace/onclick_subpages.json"

    driver = setup_driver()

    try:
        for url in start_urls:
            print(f"Processing URL: {url}")
            result_urls = process_triggers(driver, url)
            append_results_to_json(output_file, result_urls)
            print(f"Results from {url} appended to {output_file}.")
    finally:
        driver.quit()
