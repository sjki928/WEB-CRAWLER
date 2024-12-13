import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import json



def setup_session():
    """
    requests 세션 설정: 재시도와 타임아웃 기본값을 추가.
    """
    session = requests.Session()
    retries = Retry(
        total=5,  # 최대 5회 재시도
        backoff_factor=1,  # 재시도 간격 증가
        status_forcelist=[500, 502, 503, 504],  # 재시도할 HTTP 상태 코드
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def save_failed_url(failed_url, error_message, output_dir):
    """
    실패한 URL과 에러 메시지를 파일에 저장.
    """
    failed_file = os.path.join(output_dir, "failed_files.txt")

    with open(failed_file, "a", encoding="utf-8") as file:
        file.write(f"{failed_url} - {error_message}\n")
    print(f"Error logged for: {failed_url}")


def get_file_name_from_response(response, file_url):
    """
    HTTP 응답에서 파일 이름 추출. 깨진 한글 파일명 문제를 해결하기 위해 적절한 디코딩 처리 포함.
    """
    file_name = None
    content_disposition = response.headers.get("Content-Disposition")

    if content_disposition:
        # 헤더에서 파일 이름 추출 (filename* 우선 처리)
        if "filename*" in content_disposition:
            # UTF-8로 인코딩된 파일 이름 추출
            file_name = content_disposition.split("filename*=")[1].split(";")[0].strip()
            if file_name.startswith("UTF-8''"):
                file_name = file_name.replace("UTF-8''", "")
                file_name = unquote(file_name)  # URL 디코딩
        elif "filename=" in content_disposition:
            # 일반 파일 이름 추출
            file_name = content_disposition.split("filename=")[1].split(";")[0].strip('"')
            file_name = unquote(file_name)

    if not file_name:
        # URL에서 기본 파일 이름 추출
        file_name = os.path.basename(urlparse(file_url).path)

    return file_name


def download_file(session, file_url, output_dir):
    """
    주어진 파일 URL을 다운로드하고 저장.
    """
    try:
        print(f"Downloading: {file_url}")
        response = session.get(file_url, timeout=10, stream=True)
        if response.status_code == 200:
            # 파일 이름 추출
            file_name = get_file_name_from_response(response, file_url)
            # 파일 저장
            file_path = os.path.join(output_dir,file_name)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File saved: {file_path}")
        else:
            print(f"Failed to download file: {file_url} (status code: {response.status_code})")
            save_failed_url(file_url, f"HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {file_url}: {e}")
        save_failed_url(file_url, str(e), output_dir)


def crawl_files(url, output_dir):
    """
    주어진 URL에서 파일 링크를 파싱하고 다운로드.
    """
    session = setup_session()

    try:
        # 요청 및 페이지 파싱
        response = session.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch the page: {url} (status code: {response.status_code})")
            save_failed_url(url, f"HTTP {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        file_tags = soup.find_all("a", href=True)  # 모든 링크 태그 검색

        for tag in file_tags:
            href = tag.get("href")
            if not href:
                continue

            # 절대 URL로 변환
            file_url = urljoin(url, href)

            # 특정 다운로드 경로 필터링 (예: downloadDirect.do 포함 여부)
            if "downloadDirect.do" in file_url:
                download_file(session, file_url, output_dir)

    except Exception as e:
        print(f"Error processing {url}: {e}")
        save_failed_url(url, str(e))
        
if __name__ == '__main__':
    from pathlib import Path
    import argparse
    
    # 인자값을 받을 수 있는 인스턴스 생성
    parser = argparse.ArgumentParser(description='사용법 테스트입니다.')

    # 입력받을 인자값 등록
    parser.add_argument('--target_dir', required=False, default='crawled_subpages.json',)
    
    args = parser.parse_args()
    
    with open(Path(__file__).parents[1] / 'data' / 'temp' / args.target_dir,'rb') as f:
        subpages = json.load(f)


    output_dir = Path(__file__).parents[1] / 'data' / 'files'
    os.makedirs(output_dir,exist_ok=True)
    
    # 크롤링 실행
    for url in subpages:
        crawl_files(url,output_dir)

