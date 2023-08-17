import pytest

from src.resources import instagram


class TestInstagram:

    @pytest.fixture(scope='class')
    def tracker(self):
        return instagram.InstagramTracker()

    @pytest.mark.parametrize(
        'media_id',
        ['18231215743226312', '17861579396985953', '17893044365851471'],
    )
    def test_get_post_data(self, tracker, media_id):
        json = tracker.get_post_data(media_id)

        assert isinstance(json, dict)
        assert all(
            key in json for key in [
                'id', 'media_type', 'media_url',
                'username', 'timestamp',
            ]
        )
        assert json['id'] == media_id
        assert json['username'] == 'wirtschaftsinformatik_wwu'

    def test_get_user_posts(self, tracker):
        json = tracker.get_user_posts()

        assert isinstance(json, dict)
        assert all(key in json for key in ['data', 'paging'])
        assert isinstance(json['data'], list)
        assert all(isinstance(post, dict) for post in json['data'])
        assert all(
            key in post for key in [
                'id', 'caption',
            ] for post in json['data']
        )

    @pytest.mark.parametrize('amount', [3, 5, 10])
    def test_get_latest_posts(self, tracker, amount):
        json = tracker.get_latest_posts(int(amount))

        assert isinstance(json, list)
        assert all(isinstance(post, dict) for post in json)
        assert all(
            key in post for key in ['caption', 'media_url', 'media_type', 'timestamp']
            for post in json
        )
        assert len(json) == amount

        for post in json:
            assert post.get('media_type') in [
                'IMAGE', 'VIDEO', 'CAROUSEL_ALBUM',
            ]

    def test_instagram_endpoint(self, client):
        response = client.get('/api/instagram')
        json = response.get_json()

        assert isinstance(json, list)
        assert all(isinstance(post, dict) for post in json)
        assert all(
            key in post for key in ['caption', 'media_url', 'media_type', 'timestamp']
            for post in json
        )
        assert len(json) == 5

        for post in json:
            assert post.get('media_type') in [
                'IMAGE', 'VIDEO', 'CAROUSEL_ALBUM',
            ]
