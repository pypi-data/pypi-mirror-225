from pathlib import Path
from typing import Callable

from osgeo import ogr

from ._functions import find_or_create_field

FLOOD_CLASSES = {
    "Geen risico;Geen risico;Geen risico": "Geen risico",
    "Geen risico;Geen risico;Risico, lokale herkomst": "Lokaal",
    "Geen risico;Geen risico;Risico, regionale herkomst": "Gecombineerd",
    "Geen risico;Risico;Geen risico": "Landelijk",
    "Geen risico;Risico;Risico, lokale herkomst": "Landelijk",
    "Geen risico;Risico;Risico, regionale herkomst": "Landelijk",
    "Risico;Geen risico;Geen risico": "Stedelijk",
    "Risico;Geen risico;Risico, lokale herkomst": "Stedelijk",
    "Risico;Geen risico;Risico, regionale herkomst": "Stedelijk",
    "Risico;Risico;Geen risico": "Landelijk en stedelijk",
    "Risico;Risico;Risico, lokale herkomst": "Landelijk en stedelijk",
    "Risico;Risico;Risico, regionale herkomst": "Landelijk en stedelijk",
}

REQUIRED_COLUMNS = [
    "landelijk_t10",
    "landelijk_t25",
    "landelijk_t100",
    "stedelijk_t10",
    "stedelijk_t25",
    "stedelijk_t100",
    "gebiedsbreed_t10",
    "gebiedsbreed_t25",
    "gebiedsbreed_t100",
]


def get_combined_classification(stedelijk: str, landelijk: str, gebiedsbreed: str) -> str:
    key_value = f"{stedelijk};{landelijk};{gebiedsbreed}"
    if key_value in FLOOD_CLASSES.keys():
        return FLOOD_CLASSES[key_value]
    return ""


def combine_classification(buildings_path: Path, callback_function: Callable[[float], None] = None) -> None:
    buildings_ds: ogr.DataSource = ogr.Open(buildings_path.as_posix(), True)
    buildings_layer: ogr.Layer = buildings_ds.GetLayer()

    for column in REQUIRED_COLUMNS:
        index = buildings_layer.FindFieldIndex(column, True)
        if index == -1:
            raise ValueError("Column {} is needed but does not exist in the data.".format(column))

    klasse_t10_index = find_or_create_field(buildings_layer, "klasse_t10", ogr.OFTString)
    klasse_t25_index = find_or_create_field(buildings_layer, "klasse_t25", ogr.OFTString)
    klasse_t100_index = find_or_create_field(buildings_layer, "klasse_t100", ogr.OFTString)

    feature: ogr.Feature
    i = 0
    for feature in buildings_layer:
        feature.SetField(
            klasse_t10_index,
            get_combined_classification(
                feature["stedelijk_t10"], feature["landelijk_t10"], feature["gebiedsbreed_t10"]
            ),
        )

        feature.SetField(
            klasse_t25_index,
            get_combined_classification(
                feature["stedelijk_t25"], feature["landelijk_t25"], feature["gebiedsbreed_t25"]
            ),
        )

        feature.SetField(
            klasse_t100_index,
            get_combined_classification(
                feature["stedelijk_t100"], feature["landelijk_t100"], feature["gebiedsbreed_t100"]
            ),
        )

        buildings_layer.SetFeature(feature)

        if callback_function:
            callback_function((i / buildings_layer.GetFeatureCount()) * 100)

        i += 1

    buildings_layer = None
    buildings_ds = None
