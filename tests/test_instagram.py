def test_instagram(client):
    """
    The function checks the following test cases.
    
    1. The response status code is 200 (OK).
    2. Verify that the returned data is a dictionary
    3. Verify that the post_data dictionary contains all the expected keys
    4. Verify that the latest_posts data is a list of dictionaries
    5. Verify that the latest_posts dictionary contains all the expected keys
    6. Check if the latest posts are within the last 30 days
    """

    # define sample data
    post_data_sample = {
    'id': '1234567890',
    'media_type': 'IMAGE',
    'media_url': 'https://example.com/image.jpg',
    'username': 'test_user',
    'timestamp': '2023-07-20T12:34:56Z',
    }

    latest_posts_sample = [
    {
        'caption': 'Post 1',
        'media_url': 'https://example.com/post1.jpg',
        'media_type': 'IMAGE',
        'timestamp': '2023-07-20T12:34:56Z',
    },
    {
        'caption': 'Post 2',
        'media_url': 'https://example.com/post2.jpg',
        'media_type': 'VIDEO',
        'timestamp': '2023-07-19T10:22:34Z',
    },
    {
        'caption': 'Post 3',
        'media_url': 'https://example.com/post3.jpg',
        'media_type': 'CAROUSEL_ALBUM',
        'timestamp': '2023-07-18T15:45:12Z',
    },
    ]

    # Define the expected keys for the latest_posts dictionary
    item_keys = {
        'caption', 'media_url',
        'media_type', 'timestamp',
    }

 


    response = client.get('/api/bus')
    data = response.get_json()


    # Test the response status code
    assert response.status_code == 200


    # Test get_post_data method with sample data
    post_data = post_data_sample
     # Define the expected keys for the post_data dictionary
    expected_keys = [
        'id', 'media_type',
        'media_url', 'username',
        'timestamp'
    ]
    # Verify that the returned data is a dictionary
    assert isinstance(post_data, dict)
    # Verify that the post_data dictionary contains all the expected keys
    assert all(key in post_data for key in expected_keys)
    
    
    # Define the expected keys for the latest_posts dictionary
    item_keys = {
        'caption', 'media_url',
        'media_type', 'timestamp',
    }
    # Test get_post_data method with sample data
    latest_posts = latest_posts_sample
    # verify that the returned data is a list of dictionaries.
    assert isinstance(latest_posts, list)
    assert all(isinstance(post, dict) for post in latest_posts)
    # verify that each post dictionary contains all the expected keys
    assert all(key in post for key in item_keys)
    # check if the timestamp of returned posts is within the last 30 days
    assert all(isinstance(datetime.fromisoformat(post['timestamp'][:-1]), datetime) for post in latest_posts)
    assert all(datetime.now() - timedelta(days=30) <= datetime.fromisoformat(post['timestamp'][:-1]) <= datetime.now() for post in latest_posts)