from geotran import raster

def test_haversine():
    assert raster.haversine(52.370216, 4.895168, 52.520008, 13.404954) == 946.3876221719836