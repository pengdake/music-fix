async def test_get_metadata_cache_hit(mocker, cache, music_service, upload_file):
    cache_value = {"artist": "Test Artist", "title": "Test Title"}
    await cache.set(f"music_metadata:{upload_file.filename}", cache_value)
    # Call the get_metadata method
    response = await music_service.get_metadata(upload_file)
    
    # Assert the response (you can adjust this based on your expected output)
    assert response.code == 200
    assert response.message == "Metadata retrieved successfully"
    assert response.data == cache_value

async def test_get_metadata_cache_miss(mocker, music_service, upload_file):    
    # Mock the get_metadata function to return a specific value
    mock_metadata = {"artist": "Mock Artist", "title": "Mock Title"}
    mocker.patch('app.services.music.get_metadata', return_value=mock_metadata)
    
    # Call the get_metadata method
    response = await music_service.get_metadata(upload_file)
    
    # Assert the response (you can adjust this based on your expected output)
    assert response.code == 200
    assert response.message == "Metadata retrieved successfully"
    assert response.data == mock_metadata

async def test_get_metadata_not_found(mocker, music_service, upload_file):    
    # Mock the get_metadata function to return None
    mocker.patch('app.services.music.get_metadata', return_value=None)
    
    # Call the get_metadata method
    response = await music_service.get_metadata(upload_file)
    
    # Assert the response (you can adjust this based on your expected output)
    assert response.code == 404
    assert response.message == "Could not identify the music file."
    assert response.data is None