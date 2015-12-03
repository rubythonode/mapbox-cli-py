from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group


@responses.activate
def test_cli_surface():
    body = """{"results":[{"id":0,"latlng":{"lat":36.05322,"lng":-112.084004},"ele":2186.361304424316},{"id":1,"latlng":{"lat":36.053573,"lng":-112.083914},"ele":2187.6233827411997},{"id":2,"latlng":{"lat":36.053845,"lng":-112.083965},"ele":2163.921475128245}],"attribution":"&lt;a href='https://www.mapbox.com/about/maps/' target='_blank'&gt;&amp;copy; Mapbox&lt;/a&gt;"}"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/surface/mapbox.mapbox-terrain-v1.json?access_token=bogus&points=-112.084004%2C36.053220%3B-112.083914%2C36.053573%3B-112.083965%2C36.053845&geojson=true&fields=ele&layer=contour&zoom=14&interpolate=true',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'surface',
         'mapbox.mapbox-terrain-v1',
         'contour',
         'ele',
         "[-112.084004, 36.05322]",
         "[-112.083914, 36.053573]",
         "[-112.083965, 36.053845]"])
    assert result.exit_code == 0