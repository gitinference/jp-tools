import jp_tools

data = {
    "http://data.bls.gov/cew/data/api/2015/3/area/33015.csv": "data/raw/us-qcew-2015-3-33015.parquet",
    "http://data.bls.gov/cew/data/api/2019/2/area/26045.csv": "data/raw/us-qcew-2019-2-26045.parquet",
    "http://data.bls.gov/cew/data/api/2016/2/area/44001.csv": "data/raw/us-qcew-2016-2-44001.parquet",
    "http://data.bls.gov/cew/data/api/2014/1/area/18153.csv": "data/raw/us-qcew-2014-1-18153.parquet",
    "http://data.bls.gov/cew/data/api/2024/4/area/21085.csv": "data/raw/us-qcew-2024-4-21085.parquet",
    "http://data.bls.gov/cew/data/api/2018/2/area/56005.csv": "data/raw/us-qcew-2018-2-56005.parquet",
    "http://data.bls.gov/cew/data/api/2015/4/area/78030.csv": "data/raw/us-qcew-2015-4-78030.parquet",
    "http://data.bls.gov/cew/data/api/2017/1/area/51137.csv": "data/raw/us-qcew-2017-1-51137.parquet",
    "http://data.bls.gov/cew/data/api/2017/4/area/51137.csv": "data/raw/us-qcew-2017-4-51137.parquet",
    "http://data.bls.gov/cew/data/api/2018/4/area/51137.csv": "data/raw/us-qcew-2018-4-51137.parquet",
    "http://data.bls.gov/cew/data/api/2019/1/area/51137.csv": "data/raw/us-qcew-2019-1-51137.parquet",
    "http://data.bls.gov/cew/data/api/2019/3/area/51137.csv": "data/raw/us-qcew-2019-3-51137.parquet",
    "http://data.bls.gov/cew/data/api/2019/4/area/51137.csv": "data/raw/us-qcew-2019-4-51137.parquet",
    "http://data.bls.gov/cew/data/api/2020/2/area/51137.csv": "data/raw/us-qcew-2020-2-51137.parquet",
    "http://data.bls.gov/cew/data/api/2020/3/area/51137.csv": "data/raw/us-qcew-2020-3-51137.parquet",
    "http://data.bls.gov/cew/data/api/2020/4/area/51137.csv": "data/raw/us-qcew-2020-4-51137.parquet",
    "http://data.bls.gov/cew/data/api/2021/1/area/51137.csv": "data/raw/us-qcew-2021-1-51137.parquet",
    "http://data.bls.gov/cew/data/api/2021/2/area/51137.csv": "data/raw/us-qcew-2021-2-51137.parquet",
    "http://data.bls.gov/cew/data/api/2021/3/area/51137.csv": "data/raw/us-qcew-2021-3-51137.parquet",
    "http://data.bls.gov/cew/data/api/2021/4/area/51137.csv": "data/raw/us-qcew-2021-4-51137.parquet",
}


def main():
    jp_tools.download(
        url="https://raw.githubusercontent.com/gitinference/jp-tools/refs/heads/main/LICENSE",
        filename="data/raw/DELETE.txt",
    )
    # jp_tools.batch_download(file_map=data)


if __name__ == "__main__":
    main()
