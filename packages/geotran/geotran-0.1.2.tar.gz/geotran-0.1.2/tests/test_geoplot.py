from geotran import raster

def test_plot():
    assert raster.plot('tests/RGB.byte.tif')