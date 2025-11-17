# Grade Calculator System

Interactive grade calculator plus CSV archiver for organizing results.

## Requirements
- Python 3.8+
- Bash (macOS/Linux)

## Usage
1. Run the Python generator:
   ```
   python grade-generator.py
   ```
   Follow prompts to enter assignment name, category (`FA` or `SA`), grade, and weight. Summary and `grades.csv` are produced after entries finish.

2. Archive CSV outputs:
   ```
   bash organizer.sh
   ```
   or make it executable once via `chmod +x organizer.sh` and run `./organizer.sh`.

## Behavior
- Python script validates numeric inputs, prints category totals, GPA, pass/fail status, and saves all assignments to `grades.csv`.
- Bash script creates `archive/` if missing, appends detailed entries to `organizer.log`, renames files with timestamps, and moves them into the archive.

## Manual Testing Ideas
- Mix formative and summative entries to confirm weighted totals.
- Try invalid grades (>100 or negative), weights (<=0), or categories to verify re-prompts.
- Add multiple CSV files before running `organizer.sh` to see per-file log sections and timestamped names.

