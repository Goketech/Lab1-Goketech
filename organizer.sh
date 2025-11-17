#!/bin/bash
set -euo pipefail

archive_dir="archive"
log_file="organizer.log"

mkdir -p "$archive_dir"

shopt -s nullglob
csv_files=(*.csv)
shopt -u nullglob

if [ ${#csv_files[@]} -eq 0 ]; then
  echo "No CSV files found to archive."
  exit 0
fi

for file in "${csv_files[@]}"; do
  [ -e "$file" ] || continue

  timestamp="$(date +"%Y%m%d-%H%M%S")"
  basename="${file%.csv}"
  new_name="${basename}-${timestamp}.csv"

  {
    echo "========================================"
    echo "Archive Date: $(date)"
    echo "Original File: $file"
    echo "New File: $new_name"
    echo "----------------------------------------"
    cat "$file"
    echo "========================================"
    echo ""
  } >> "$log_file"

  mv "$file" "${archive_dir}/${new_name}"
  echo "Archived $file -> ${archive_dir}/${new_name}"
done

