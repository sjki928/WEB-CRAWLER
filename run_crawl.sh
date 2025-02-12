#!/bin/bash

set -e
set -x

# 스크립트 위치로 이동
script_dir=$(dirname "$(realpath "$0")")
cd "$script_dir"

# 로그 파일 경로 설정 (스크립트를 실행한 디렉토리에 생성)
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
log_file="execution_log_${timestamp}.out"
exec > >(tee -a "$log_file") 2>&1

# 변수 설정
crawled_subpages_dir="crawled_subpages"
crawled_subpages_json="${crawled_subpages_dir}.json"

# Python 스크립트 실행
python src/subpage.py --output_dir "$crawled_subpages_json"
python src/onclick.py --target_dir "$crawled_subpages_json" --output_dir "${crawled_subpages_dir}_onclick.json"

# 파일 배열 설정
target_files=("${crawled_subpages_json}" "${crawled_subpages_dir}_onclick.json")
output_files=("crawled_data.json" "crawled_data_onclick.json")

# 파일별로 text.py 실행
for i in "${!target_files[@]}"; do
    target_file="${target_files[i]}"
    output_file="${output_files[i]}"

    echo "Processing $target_file..."
    python src/text.py --target_dir "$target_file" --output_dir "$output_file"
done

echo "All files crawled!"

# 파일별로 split.py 실행
for file in "${output_files[@]}"; do
    echo "Processing $file..."
    python src/split.py --target_dir "$file"
done

echo "All files split!"

# # 파일별로 files.py 실행
# for file in "${target_files[@]}"; do
#     echo "Download files in $file..."
#     python src/files.py --target_dir "$file"
# done