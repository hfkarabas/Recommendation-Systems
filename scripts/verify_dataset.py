import os
import sys
import hashlib
import csv
from datetime import datetime, timezone
from collections import deque
import pandas as pd

DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

EXPECTED_MD5 = {
    "links.csv": "8f033867bcb4e6be8792b21468b4fa6e",
    "movies.csv": "0df90835c19151f9d819d0822e190797",
    "ratings.csv": "cf12b74f9ad4b94a011f079e26d4270a",
    "tags.csv": "963bf4fa4de6b8901868fddd3eb54567",
}

EXPECTED_STATS = {
    "ratings_count": 32000204,
    "ratings_unique_users": 200948,
    "movies_unique_movies": 87585,
    "tags_count": 2000072,
    "min_rating": 0.5,
    "max_rating": 5.0,
    "min_date_expected": "1995-01-09",
    "max_date_expected": "2023-10-12",
}

def compute_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_file_info(filename):
    filepath = os.path.join(DATASET_DIR, filename)
    exists = os.path.isfile(filepath)
    if not exists:
        return {"filename": filename, "exists": False, "size_bytes": 0, "size_mb": 0.0, "size_mib": 0.0, "readable": False}
    size_bytes = os.path.getsize(filepath)
    readable = os.access(filepath, os.R_OK)
    # verify read by opening
    try:
        with open(filepath, "rb") as f:
            _ = f.read(1024)
    except Exception:
        readable = False
    return {
        "filename": filename,
        "filepath": filepath,
        "exists": exists,
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / 1_000_000, 2),
        "size_mib": round(size_bytes / (1024 * 1024), 2),
        "readable": readable,
    }

def get_csv_preview_and_line_count(filepath):
    # Get first 5 rows and last 5 rows and exact line count
    first_5 = []
    last_5 = deque(maxlen=5)
    row_count = 0
    header = None
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            row_count += 1
            if len(first_5) < 5:
                first_5.append(row)
            last_5.append(row)
    return header, row_count, first_5, list(last_5)

def main():
    print(f"=== Dataset Directory: {DATASET_DIR} ===")
    
    # Step 2: File existence and sizes
    print("\n--- Step 2: File Existence and Sizes ---")
    files = ["links.csv", "movies.csv", "ratings.csv", "tags.csv"]
    file_infos = {}
    for fn in files:
        info = get_file_info(fn)
        file_infos[fn] = info
        print(f"File: {fn} | Exists: {info['exists']} | Bytes: {info['size_bytes']:,} | MB: {info['size_mb']} MB ({info['size_mib']} MiB) | Readable: {info['readable']}")

    # Step 3: MD5 Checksums
    print("\n--- Step 3: MD5 Checksums ---")
    checksum_results = {}
    all_checksums_pass = True
    for fn in files:
        if not file_infos[fn]["exists"]:
            checksum_results[fn] = {"status": "FAIL (File missing)"}
            all_checksums_pass = False
            continue
        calc_md5 = compute_md5(file_infos[fn]["filepath"])
        exp_md5 = EXPECTED_MD5[fn]
        passed = (calc_md5.lower() == exp_md5.lower())
        if not passed:
            all_checksums_pass = False
        checksum_results[fn] = {
            "calculated": calc_md5,
            "expected": exp_md5,
            "pass": passed,
            "status": "PASS" if passed else "FAIL"
        }
        print(f"File: {fn} | Calculated: {calc_md5} | Expected: {exp_md5} | Status: {'PASS' if passed else 'FAIL'}")

    if not all_checksums_pass:
        print("\n[CRITICAL ERROR] One or more MD5 checksums failed! Halting verification as per instructions.")
        sys.exit(1)

    # Step 4: CSV Structure & Row counts & Previews
    print("\n--- Step 4: Inspect CSV Structure ---")
    csv_structure = {}
    for fn in files:
        fp = file_infos[fn]["filepath"]
        header, count, first5, last5 = get_csv_preview_and_line_count(fp)
        
        # Determine dtypes using pandas sample (or complete read for smaller files)
        if fn in ["links.csv", "movies.csv"]:
            df_full = pd.read_csv(fp, nrows=100)
            dtypes = {col: str(df_full[col].dtype) for col in df_full.columns}
        elif fn == "tags.csv":
            df_full = pd.read_csv(fp, nrows=100)
            dtypes = {col: str(df_full[col].dtype) for col in df_full.columns}
        else: # ratings.csv
            df_sample = pd.read_csv(fp, nrows=100)
            dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}
            
        csv_structure[fn] = {
            "columns": header,
            "row_count": count,
            "dtypes": dtypes,
            "first_5": first5,
            "last_5": last5,
        }
        print(f"\nStructure for {fn}:")
        print(f"Columns: {header}")
        print(f"Data rows count (excluding header): {count:,}")
        print(f"Inferred sample dtypes: {dtypes}")
        print("First 5 rows:")
        for r in first5:
            print("  ", r)
        print("Last 5 rows:")
        for r in last5:
            print("  ", r)

    # Step 5 & 6: Basic statistics and timestamp inspection
    print("\n--- Step 5 & 6: Validate Basic Statistics & Timestamps ---")
    
    # 1. movies.csv
    movies_df = pd.read_csv(file_infos["movies.csv"]["filepath"])
    movies_unique_movies = movies_df["movieId"].nunique()
    print(f"movies.csv total rows: {len(movies_df):,}")
    print(f"movies.csv unique movies: {movies_unique_movies:,} (Expected: {EXPECTED_STATS['movies_unique_movies']:,})")
    
    # 2. tags.csv
    tags_df = pd.read_csv(file_infos["tags.csv"]["filepath"])
    tags_unique_users = tags_df["userId"].nunique()
    tags_unique_movies = tags_df["movieId"].nunique()
    tags_count = len(tags_df)
    print(f"tags.csv total rows: {tags_count:,} (Expected: {EXPECTED_STATS['tags_count']:,})")
    print(f"tags.csv unique users: {tags_unique_users:,}")
    print(f"tags.csv unique movies: {tags_unique_movies:,}")

    # 3. ratings.csv (Chunked reading)
    print("\nReading ratings.csv in chunks...")
    ratings_path = file_infos["ratings.csv"]["filepath"]
    chunk_size = 2_000_000
    ratings_total_rows = 0
    unique_users = set()
    unique_movies = set()
    min_rating = float("inf")
    max_rating = float("-inf")
    min_timestamp = float("inf")
    max_timestamp = float("-inf")

    chunk_idx = 0
    for chunk in pd.read_csv(
        ratings_path,
        chunksize=chunk_size,
        dtype={"userId": "int32", "movieId": "int32", "rating": "float32", "timestamp": "int64"}
    ):
        chunk_idx += 1
        ratings_total_rows += len(chunk)
        unique_users.update(chunk["userId"].unique())
        unique_movies.update(chunk["movieId"].unique())
        c_min_r = chunk["rating"].min()
        c_max_r = chunk["rating"].max()
        if c_min_r < min_rating:
            min_rating = float(c_min_r)
        if c_max_r > max_rating:
            max_rating = float(c_max_r)
            
        c_min_t = chunk["timestamp"].min()
        c_max_t = chunk["timestamp"].max()
        if c_min_t < min_timestamp:
            min_timestamp = int(c_min_t)
        if c_max_t > max_timestamp:
            max_timestamp = int(c_max_t)
        print(f"Processed chunk {chunk_idx}: {ratings_total_rows:,} rows so far...")

    min_date_utc = datetime.fromtimestamp(min_timestamp, tz=timezone.utc)
    max_date_utc = datetime.fromtimestamp(max_timestamp, tz=timezone.utc)

    print("\n--- Ratings Summary ---")
    print(f"Total rating row count: {ratings_total_rows:,} (Expected: {EXPECTED_STATS['ratings_count']:,})")
    print(f"Unique userId in ratings: {len(unique_users):,}")
    print(f"Unique movieId in ratings: {len(unique_movies):,}")
    print(f"Min rating: {min_rating} | Max rating: {max_rating} (Expected: {EXPECTED_STATS['min_rating']} - {EXPECTED_STATS['max_rating']})")
    print(f"Min timestamp: {min_timestamp} -> UTC: {min_date_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} ({min_date_utc.strftime('%B %d, %Y')})")
    print(f"Max timestamp: {max_timestamp} -> UTC: {max_date_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} ({max_date_utc.strftime('%B %d, %Y')})")

    # Links summary
    links_df = pd.read_csv(file_infos["links.csv"]["filepath"])
    print("\n--- Links Summary ---")
    print(f"links.csv total rows: {len(links_df):,}")
    print(f"links.csv unique movies: {links_df['movieId'].nunique():,}")
    print(f"links.csv null imdbId: {links_df['imdbId'].isnull().sum()}")
    print(f"links.csv null tmdbId: {links_df['tmdbId'].isnull().sum()}")

    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    main()
