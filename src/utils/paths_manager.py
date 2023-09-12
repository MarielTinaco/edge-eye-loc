
from pathlib import Path

LFPW_RAW_SOURCE_PATH = Path(__file__) / '../../..' / 'datasets' / 'raw' / 'lfpw-labelled-face-parts-in-the-wild'
HELEN_RAW_SOURCE_PATH = Path(__file__) / '../../..' / 'datasets' / 'raw' / 'HELEN'

if __name__ == "__main__":
    print(LFPW_RAW_SOURCE_PATH.exists())
    print(HELEN_RAW_SOURCE_PATH.exists())