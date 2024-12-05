import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import os

def cleaning_rule(soup):
    
    satisfaction_headers = soup.find_all('header')
    if satisfaction_headers:
        for satisfaction_header in satisfaction_headers:
            satisfaction_header.decompose()
    # <div class="quick_menu"> 제거
    quick_menu = soup.find('div', class_='quick_menu')
    if quick_menu:
        quick_menu.decompose()

    # <footer class="satisfaction"> 제거
    satisfaction_footers = soup.find_all('footer')
    if satisfaction_footers:
        for satisfaction_footer in satisfaction_footers:
            satisfaction_footer.decompose()

    all_menu_article = soup.find('article', class_='all_menu')
    if all_menu_article:
        all_menu_article.decompose()
    
    return soup

def crawl_and_collect(urls, failed_log="/workspace/failed_sites.txt"):
    """
    주어진 URL 리스트에서 각각의 페이지 내용을 크롤링하여 수집하며,
    실패한 URL은 별도의 파일에 저장합니다.
    """
    crawled_data = {}
    failed_sites = []

    for url in urls:
        try:
            print(f"Crawling: {url}")
            response = session.get(url, timeout=10)  # 타임아웃 설정
            response.raise_for_status()  # HTTP 상태 코드 확인

            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "No Title"
            
            # 이미지 URL을 추출하고, img 태그를 텍스트로 삽입
            image_urls = []
            for img in soup.find_all("img"):
                img_src = img.get("src")
                if img_src:
                    # 상대 경로를 절대 경로로 변환
                    full_img_url = img_src if urlparse(img_src).netloc else urlparse(url)._replace(path=img_src).geturl()
                    image_urls.append(full_img_url)
                    
            #text cleaning
            soup = cleaning_rule(soup)
            
            # body_text: 텍스트를 추출하되, img 태그는 그대로 유지
            body_text = soup.get_text(separator="\n", strip=True)

            # URL별로 데이터 저장
            crawled_data[url] = {
                "title": title,
                "content": body_text,  # 처음 1000자만 저장
                "images": image_urls  # 이미지 URL 목록 추가
            }

        except requests.exceptions.RequestException as e:
            print(f"Request error crawling {url}: {e}")
            failed_sites.append(url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            failed_sites.append(url)

    # 실패한 URL을 파일에 기록
    if failed_sites:
        os.makedirs(os.path.dirname(failed_log), exist_ok=True)
        with open(failed_log, "a", encoding="utf-8") as file:
            file.write("\n".join(failed_sites) + "\n")
        print(f"Failed sites have been logged to {failed_log}.")

    return crawled_data



# 크롤링 실행
if __name__ == "__main__":
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter
    
    # HTTP Session 설정 (Retry 지원)
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    
    with open('/workspace/crawled_subpages.json','rb') as f:
        subpages = json.load(f)
    crawled_results = crawl_and_collect(subpages, "/workspace/failed_sites.txt")

    # 결과를 JSON 파일로 저장
    output_path = "/workspace/crawled_data.json"
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(crawled_results, file, ensure_ascii=False, indent=4)

    print(f"Crawling completed. Results saved to {output_path}.")
