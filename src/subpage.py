import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def create_session(retries=5, backoff_factor=1):
    """
    requests.Session을 생성하고, 재시도 및 백오프 정책을 설정합니다.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,  # 최대 재시도 횟수
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,  # 재시도 간 대기 시간 증가율
        status_forcelist=[500, 502, 503, 504],  # 재시도할 HTTP 상태 코드
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def crawl_subpages(base_url, session, visited=None, max_depth=10, current_depth=0):
    """
    주어진 URL에서 내부 링크를 재귀적으로 크롤링하여 모든 하위 사이트를 찾습니다.
    
    Parameters:
        - base_url: 크롤링 시작 URL
        - session: requests.Session 객체
        - visited: 이미 방문한 URL 집합
        - max_depth: 최대 크롤링 깊이
        - current_depth: 현재 크롤링 깊이
    """
    if visited is None:
        visited = set()

    if current_depth > max_depth:
        return visited

    try:
        response = session.get(base_url, timeout=5)  # timeout 설정
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                full_url = urljoin(base_url, link["href"])
                # 같은 도메인 내부 링크만 수집
                if base_url in full_url and full_url not in visited:
                    print(f"Find a new subpage:{full_url}")
                    visited.add(full_url)
                    # 재귀적으로 하위 링크 탐색
                    crawl_subpages(full_url, session, visited, max_depth, current_depth + 1)
    except requests.exceptions.RequestException as e:
        print(f"Request error for URL {base_url}: {e}")
    
    return visited

if __name__ == '__main__':
    import json
    import argparse
    import pandas as pd
    from pathlib import Path

    # 인자값을 받을 수 있는 인스턴스 생성
    parser = argparse.ArgumentParser(description='사용법 테스트입니다.')

    # 입력받을 인자값 등록
    parser.add_argument('--output_dir', required=False, default='crawled_subpages.json',)
    parser.add_argument('--max_depth', required=False, default=4, type=int)

    args = parser.parse_args()
    
    # 메인 URL
    base_url = "https://www.kead.or.kr/"
    output_dir = Path.cwd()/ 'data'/ 'temp'/ args.output_dir

    # 세션 생성
    session = create_session()

    # 하위 페이지 크롤링
    subpages = crawl_subpages(base_url, max_depth=args.max_depth, session=session)
    
    # #으로 구분되어있지만 사실은 같은 사이트인 경우를 방지
    series=pd.Series(list(subpages))
    data = series.map(lambda x: x.split('#')[0])
    subpages = data.drop_duplicates().to_list()
    
    with open(output_dir,'w') as f:
        json.dump(subpages,f,ensure_ascii=False,indent=4)
    
    # 결과 출력
    if subpages:
        print(f"Found {len(subpages)} Subpages")
    else:
        print("No subpages found.")
