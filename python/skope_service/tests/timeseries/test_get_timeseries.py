'''Test the /timeseries endpoint.'''
import pytest

from skope_service import app

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def client():
    '''Return the Flask client instance to test against.'''
    return app.test_client()

@pytest.fixture(scope='module')
def response(client):
    '''Invoke the timeseries service and return the response.'''
    return client.get('/timeseries/annual_5x5x5_dataset/uint16_variable' +
                      '?longitude=-123.0&latitude=45.0&start=0&end=4')

@pytest.fixture(scope='module')
def response_json(response):
    '''Return the JSON body of response.'''
    return response.get_json()

# pylint: disable=redefined-outer-name, missing-docstring

def test_response_status_is_success(response):
    assert response.status == '200 OK'
    assert response.status_code == 200

def test_response_body_is_json(response):
    assert response.is_json
    assert response.mimetype == 'application/json'

def test_dataset_id_should_match_request(response_json):
    assert response_json['datasetId'] == 'annual_5x5x5_dataset'

def test_variable_name_should_match_request(response_json):
    assert response_json['variableName'] == 'uint16_variable'

def test_boundary_geometry_type_should_be_default_value_of_point(response_json):
    assert response_json['boundaryGeometry']['type'] == 'Point'

def test_boundary_geometry_coordinates_should_match_query_parameters(response_json):
    assert response_json['boundaryGeometry']['coordinates'] == [-123, 45]

def test_range_start_and_in_response_json_should_match_query_parameters(response_json):
    assert response_json['start'] == '0'
    assert response_json['end'] == '4'

def test_values_array_in_response_json_and_should_match_series_for_pixel_0_0(response_json):
    assert response_json['values'] == [100, 200, 300, 400, 500]
