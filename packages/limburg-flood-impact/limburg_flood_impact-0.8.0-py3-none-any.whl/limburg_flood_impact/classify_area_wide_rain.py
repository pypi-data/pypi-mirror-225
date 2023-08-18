from pathlib import Path

import numpy as np
from osgeo import gdal, ogr

from ._functions import (
    RASTER_DRIVER,
    TILE_OVERLAP,
    TILE_SIZE,
    VECTOR_DRIVER,
    delete_all_features_from_layer,
    find_or_create_field,
    flood_mask,
    get_extent,
    get_layer_extent,
    get_water_height_array,
    print_progress_bar,
    raster_coordinates,
    set_field_if_higher,
    world_coordinates,
)
from .extent_tile import Extent


def field_name_with_puddles(type: str) -> str:
    return f"max_waterdiepte_gebiedsbreed_incl_kleine_plassen_{type}"


def field_name_without_puddles(type: str) -> str:
    return f"max_waterdiepte_gebiedsbreed_excl_kleine_plassen_{type}"


def classify_water_height(
    buildings_layer: ogr.Layer,
    t10_with_puddles: gdal.Dataset,
    t25_with_puddles: gdal.Dataset,
    t100_with_puddles: gdal.Dataset,
    t10: gdal.Dataset,
    t25: gdal.Dataset,
    t100: gdal.Dataset,
    field_name: str = "gebiedsbreed",
    qgis_feedback=None,
):
    layer_spatial_filter = get_layer_extent(buildings_layer)

    t10_index = find_or_create_field(buildings_layer, f"{field_name}_t10", ogr.OFTString)
    t25_index = find_or_create_field(buildings_layer, f"{field_name}_t25", ogr.OFTString)
    t100_index = find_or_create_field(buildings_layer, f"{field_name}_t100", ogr.OFTString)

    wdp_t10_index = find_or_create_field(buildings_layer, field_name_with_puddles("t10"), ogr.OFTReal)
    wdp_t25_index = find_or_create_field(buildings_layer, field_name_with_puddles("t25"), ogr.OFTReal)
    wdp_t100_index = find_or_create_field(buildings_layer, field_name_with_puddles("t100"), ogr.OFTReal)

    wd_t10_index = find_or_create_field(buildings_layer, field_name_without_puddles("t10"), ogr.OFTReal)
    wd_t25_index = find_or_create_field(buildings_layer, field_name_without_puddles("t25"), ogr.OFTReal)
    wd_t100_index = find_or_create_field(buildings_layer, field_name_without_puddles("t100"), ogr.OFTReal)

    inv_gt = gdal.InvGeoTransform(t10.GetGeoTransform())
    gt = t10.GetGeoTransform()

    t10_band_with_puddles: gdal.Band = t10_with_puddles.GetRasterBand(1)
    t25_band_with_puddles: gdal.Band = t25_with_puddles.GetRasterBand(1)
    t100_band_with_puddles: gdal.Band = t100_with_puddles.GetRasterBand(1)

    t10_band: gdal.Band = t10.GetRasterBand(1)
    t25_band: gdal.Band = t25.GetRasterBand(1)
    t100_band: gdal.Band = t100.GetRasterBand(1)

    memory_ds: ogr.DataSource = VECTOR_DRIVER.CreateDataSource("ds")
    memory_layer: ogr.Layer = memory_ds.CreateLayer("geometry_layer", buildings_layer.GetSpatialRef(), ogr.wkbPolygon)

    raster_bbox = get_extent(t10)

    buildings_layer.SetSpatialFilter(raster_bbox)

    feature: ogr.Feature
    i = 0
    for feature in buildings_layer:
        if qgis_feedback is not None:
            if qgis_feedback.isCanceled():
                break

        delete_all_features_from_layer(memory_layer)

        geom: ogr.Geometry = feature.GetGeometryRef().Buffer(1)

        if not raster_bbox.Intersect(geom):
            continue

        if not geom.Within(raster_bbox):
            geom = geom.Intersection(raster_bbox)

        minX, maxX, minY, maxY = geom.GetEnvelope()

        new_feature: ogr.Feature = ogr.Feature(memory_layer.GetLayerDefn())
        new_feature.SetGeometry(geom)
        memory_layer.SetFeature(new_feature)

        rMinX, rMaxY = raster_coordinates(minX, minY, inv_gt)
        rMaxX, rMinY = raster_coordinates(maxX, maxY, inv_gt, False)

        if int(rMaxX - rMinX) == 0 or int(rMaxY - rMinY) == 0:
            continue

        feature_raster_ds: gdal.Dataset = RASTER_DRIVER.Create(
            "geom_raster",
            int(rMaxX - rMinX),
            int(rMaxY - rMinY),
            bands=1,
            eType=gdal.GDT_Float64,
        )
        t_coords = world_coordinates(rMinX, rMinY, gt)
        feature_raster_ds.SetGeoTransform([t_coords[0], gt[1], gt[2], t_coords[1], gt[4], gt[5]])
        feature_raster_ds.SetProjection(t10.GetProjection())

        gdal.RasterizeLayer(
            feature_raster_ds,
            [1],
            memory_layer,
            burn_values=[1],
            options=["ALL_TOUCHED=TRUE"],
        )

        feature_rasterized = feature_raster_ds.GetRasterBand(1).ReadAsArray()

        t10_water_with_puddles = get_water_height_array(t10_band_with_puddles, rMinX, rMaxX, rMinY, rMaxY)
        t25_water_with_puddles = get_water_height_array(t25_band_with_puddles, rMinX, rMaxX, rMinY, rMaxY)
        t100_water_with_puddles = get_water_height_array(t100_band_with_puddles, rMinX, rMaxX, rMinY, rMaxY)

        t10_water = get_water_height_array(t10_band, rMinX, rMaxX, rMinY, rMaxY)
        t25_water = get_water_height_array(t25_band, rMinX, rMaxX, rMinY, rMaxY)
        t100_water = get_water_height_array(t100_band, rMinX, rMaxX, rMinY, rMaxY)

        wdp_t10_changed = set_field_if_higher(
            feature, wdp_t10_index, float(np.max(t10_water_with_puddles * feature_rasterized))
        )
        wdp_t25_changed = set_field_if_higher(
            feature, wdp_t25_index, float(np.max(t25_water_with_puddles * feature_rasterized))
        )
        wdp_t100_changed = set_field_if_higher(
            feature, wdp_t100_index, float(np.max(t100_water_with_puddles * feature_rasterized))
        )

        wd_t10_changed = set_field_if_higher(feature, wd_t10_index, float(np.max(t10_water * feature_rasterized)))
        wd_t25_changed = set_field_if_higher(feature, wd_t25_index, float(np.max(t25_water * feature_rasterized)))
        wd_t100_changed = set_field_if_higher(feature, wd_t100_index, float(np.max(t100_water * feature_rasterized)))

        if wdp_t10_changed or wd_t10_changed:
            feature.SetField(
                t10_index,
                column_value(
                    np.max(feature_rasterized * t10_water_with_puddles), np.max(feature_rasterized * t10_water)
                ),
            )

        if wdp_t25_changed or wd_t25_changed:
            feature.SetField(
                t25_index,
                column_value(
                    np.max(feature_rasterized * t25_water_with_puddles), np.max(feature_rasterized * t25_water)
                ),
            )

        if wdp_t100_changed or wd_t100_changed:
            feature.SetField(
                t100_index,
                column_value(
                    np.max(feature_rasterized * t100_water_with_puddles), np.max(feature_rasterized * t100_water)
                ),
            )

        feature_set = buildings_layer.SetFeature(feature)
        if feature_set != 0:
            raise RuntimeError(f"Error while inserting Feature: {gdal.GetLastErrorMsg()}, {gdal.GetLastErrorNo()}")

        i += 1

    buildings_layer.SetSpatialFilter(layer_spatial_filter)

    memory_layer = None
    memory_ds = None


def column_value(value_with_puddles: float, value_without_puddles: float) -> str:
    if 0.15 < value_with_puddles and value_without_puddles <= 0.15:
        return "Risico, lokale herkomst"
    elif 0.15 < value_without_puddles:
        return "Risico, regionale herkomst"
    elif value_with_puddles <= 0.15:
        return "Geen risico"

    return "Geen risico"


def classify_area_wide_rain(buildings_path: Path, t10: Path, t25: Path, t100: Path, qgis_feedback=None):
    gdal.UseExceptions()

    buildings_ds: ogr.DataSource = ogr.Open(buildings_path.as_posix(), True)
    tmp_building_layer: ogr.Layer = buildings_ds.GetLayer()

    driver_mem: ogr.Driver = ogr.GetDriverByName("MEMORY")
    source_mem: ogr.DataSource = driver_mem.CreateDataSource("memData")
    buildings_layer: ogr.Layer = source_mem.CopyLayer(
        tmp_building_layer, tmp_building_layer.GetName(), ["OVERWRITE=YES"]
    )

    tmp_building_layer = None

    t10_ds_whole: gdal.Dataset = gdal.Open(t10.as_posix())
    t25_ds_whole: gdal.Dataset = gdal.Open(t25.as_posix())
    t100_ds_whole: gdal.Dataset = gdal.Open(t100.as_posix())

    rasterExtent = Extent.from_gdal_ds(t10_ds_whole)

    tiles = rasterExtent.create_tiles(TILE_SIZE)

    for i, tile in enumerate(tiles):
        buildings_layer.ResetReading()

        if qgis_feedback is None:
            print_progress_bar(i + 1, len(tiles), "Tiles processed.")

        tile.buffer_by(TILE_OVERLAP)

        t10_ds = tile.extract_from(t10_ds_whole)
        t25_ds = tile.extract_from(t25_ds_whole)
        t100_ds = tile.extract_from(t100_ds_whole)

        t10_masked_including_puddles = flood_mask(t10_ds, only_water_height_above=0.02)

        if qgis_feedback:
            if qgis_feedback.isCanceled():
                return

        t25_masked_including_puddles = flood_mask(t25_ds, only_water_height_above=0.02)

        if qgis_feedback:
            if qgis_feedback.isCanceled():
                return

        t100_masked_including_puddles = flood_mask(t100_ds, only_water_height_above=0.02)

        if qgis_feedback:
            if qgis_feedback.isCanceled():
                return

        t10_masked = flood_mask(t10_ds, only_water_height_above=0.02, minimal_area_of_water_pond=200)

        if qgis_feedback:
            if qgis_feedback.isCanceled():
                return

        t25_masked = flood_mask(t25_ds, only_water_height_above=0.02, minimal_area_of_water_pond=200)

        if qgis_feedback:
            if qgis_feedback.isCanceled():
                return

        t100_masked = flood_mask(t100_ds, only_water_height_above=0.02, minimal_area_of_water_pond=200)

        if qgis_feedback:
            if qgis_feedback.isCanceled():
                return

        classify_water_height(
            buildings_layer,
            t10_masked_including_puddles,
            t25_masked_including_puddles,
            t100_masked_including_puddles,
            t10_masked,
            t25_masked,
            t100_masked,
            field_name="gebiedsbreed",
            qgis_feedback=qgis_feedback,
        )

        if qgis_feedback:
            qgis_feedback.setProgress(((i + 1) / len(tiles)) * 100)

    buildings_ds.CopyLayer(buildings_layer, buildings_layer.GetName(), ["OVERWRITE=YES"])

    buildings_layer = None
    buildings_ds = None
    t10_ds = None
    t25_ds = None
    t100_ds = None
    t10_masked_including_puddles = None
    t25_masked_including_puddles = None
    t100_masked_including_puddles = None
    t10_masked = None
    t25_masked = None
    t100_masked = None


if __name__ == "__main__":
    classify_area_wide_rain(
        Path("/home/cahik/Lutra/Floods/New_Data/Overig benodigde data/BAG_panden.gpkg"),
        Path("/home/cahik/Lutra/Floods/New_Data/rasters/T10Compleet.tif"),
        Path("/home/cahik/Lutra/Floods/New_Data/rasters/T25Compleet.tif"),
        Path("/home/cahik/Lutra/Floods/New_Data/rasters/T100Compleet.tif"),
    )
