import pytest
from app.main import app
from app.schemas.common import ResponseModel
from app.api.v1.music import get_music_service

def test_identify_music_api(mocker, client, music_service, upload_file):
    # Mock the get_metadata method of the music service
    mock_service = mocker.AsyncMock()
    mock_service.get_metadata.return_value = ResponseModel(code=200, message="Metadata retrieved successfully", data={"artist": "Mock Artist", "title": "Mock Title"})

    
    # Patch the get_metadata method
    app.dependency_overrides[get_music_service] = lambda: mock_service
    
    # Make the API call
    response = client.post("/music/identify", files={"file": (upload_file.filename, upload_file.file, "audio/wav")})
    
    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["code"] == 200
    assert response_data["message"] == "Metadata retrieved successfully"
    assert response_data["data"] == mock_service.get_metadata.return_value.data
    # Clean up the dependency override
    app.dependency_overrides.clear()



    
   