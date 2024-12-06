## Crawled files

```tree
.
|-- snapshots
|   |-- 2024-12-06
|   `-- README.md
`-- temp
    |-- README.md
    |-- crawled_data.json
    |-- crawled_data_onclick.json
    |-- crawled_subpages.json
    `-- crawled_subpages_onclick.json

```

1. `crawled_subpages.json`
    - `src/subpages.py`의 base_url인 "https://www.kead.or.kr/" 에서 탐색된 subpage를 저장한 파일입니다.
2. `crawled_subpages_onclick.json`
    - `crawled_subpages.json`에서 onclick상호작용을 통해서 들어갈 수 있는 subpage를 저장한 파일입니다.
3. `crawled_data.json` & `crawled_data_onclick.json`
    - 각각 1,2의 사이트를 text crawling한 파일입니다.
    - `key`는 url이며 `value`는 title, content, image로 이뤄져있는 dictionary입니다