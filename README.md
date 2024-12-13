# 2024-KEAD-DATA
Website Crawling and Cleaning

```
.
|-- README.md
|-- data
|   |-- snapshots
|   |   |-- 2024-12-06
|   |   `-- README.md
|   `-- temp
|       |-- README.md
|       |-- crawled_data.json
|       |-- crawled_data_onclick.json
|       |-- crawled_subpages.json
|       `-- crawled_subpages_onclick.json
|-- demo
|   `-- Crawl.ipynb
|-- run_crawl.sh
`-- src
    |-- files.py
    |-- onclick.py
    |-- split.py
    |-- subpage.py
    `-- text.py
```

## 1. Source Code
- 하위페이지 탐색, 텍스트 크롤링, 파일 크롤링, 파일분리를 위한 코드 디렉토리
1. `subpage.py` : base_url을 기준으로 재귀적으로 하위페이지를 탐색하는 파일입니다.
2. `onclick.py` : `subpage.py`로 탐색된 하위페이지에서 클릭을 통해 이동가능한 하위페이지를 탐색합니다.
3. `text.py` : 1,2의 결과를 바탕으로 텍스트를 크롤링합니다.
4. `files.py` : 1,2의 결과에서 `directDownload.do` 를 통해 저장될 수 있는 파일들을 저장합니다.
5. `split.py` : 3의 결과를 사이트당 하나의 파일로 분리하고, `{title:url}` 쌍으로 저장합니다.

## 2. Demo
- `src` 내부의 코드들을 실행해보기 위해 시도했던 cell들입니다.

## 3. Data
- 크롤링 과정에서 나온 데이터를 저장하는 `temp`와 크롤링 결과를 저장하는 `snapshot`으로 구성되어 있습니다.
- 자세한 정보는 해당 디렉토리에 README.md로 저장되어있습니다.

## 4. How to Use
- Onestop Crawling
```shell
./run_crawl.sh
```
- 하나씩 실행도 가능합니다 순서는 1.의 1->2-> 3 or 4 순으로 실행하면 됩니다.

  ```markdown
# Crontab Installation and Usage

## Crontab 설치 - CentOS

```bash
# cron 설치
sudo yum update -y
sudo yum install -y cronie

# cron 시작
sudo systemctl start crond

# cron systemctl 활성화
sudo systemctl enable crond

# cron systemctl 등록 확인
sudo systemctl list-unit-files | grep crond
```

## 자동화를 위한 Crontab 설치

```bash
# cron 설치
sudo apt update -y
sudo apt install -y cron

# cron 시작
sudo service cron start

# cron systemctl 활성화
sudo systemctl enable cron.service

# cron systemctl 등록 확인
sudo systemctl list-unit-files | grep cron
sudo service cron status
```

## Crontab 사용방법

### Crontab 명령어

```bash
# Crontab 편집
crontab -e

# Crontab List 조회
crontab -l

# Crontab List 전체 삭제
crontab -r
```

### Crontab 추가 형식

```bash
minute hour day month weekday command
```

- **minute**: 0 - 59  
- **hour**: 0 - 23  
- **day**: 1 - 31  
- **month**: 1 - 12  
- **weekday**: 0 - 6 (0: Sunday)  
- **command**: 수행하려는 작업 명령어  

### Crontab 사용 예제

```bash
# 매분마다 
* * * * * /bin/bash /path/to/2024-KEAD-DATA/run_crawl.sh

# 매일 1시에 
0 1 * * * /bin/bash /path/to/2024-KEAD-DATA/run_crawl.sh

# system_chk.sh를 월 ~ 금요일 매 5분마다 실행
*/5 * * * 1-5 /bin/bash /path/to/2024-KEAD-DATA/run_crawl.sh
```
