from .consts import DATA_SOURCES
from .csvzip import CsvZipServiceInterface


DATA_SOURCES[CsvZipServiceInterface.key()] = CsvZipServiceInterface
