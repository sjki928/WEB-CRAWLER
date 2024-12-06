## Document Storage

```tree
.
|-- snapshots
|   |-- 2024-12-06(example)
|   `-- README.md
`-- temp
    |-- README.md
    |-- crawled_data.json
    |-- crawled_data_onclick.json
    |-- crawled_subpages.json
    `-- crawled_subpages_onclick.json

```

- `data/temp`에서 crawl된 데이터들이 RAG에 사용되기 위한 각 사이트별 파일로 분리된 디렉토리를 저장하는 디렉토리입니다.
- crawling한 날짜가 디렉토리의 이름이 되고 내부엔 사이트의 `title`이 제목이고 `content`가 내용인 파일들이 존재합니다.
- `title`로 `url`을 얻을 수 있는 딕셔너리가 저장된 `url_title.json`이 존재합니다.