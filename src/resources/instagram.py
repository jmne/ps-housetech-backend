import json
import os

from flask import abort

from .tracker import Tracker

INSTAGRAM_KEY = os.getenv('INSTAGRAM_KEY')


class InstagramTracker(Tracker):
    """InstagramTracker class using the Instagram API.

    Use of the Instagram Basic Display API.
    """

    def __init__(self):
        """
        Initialization of InstagramTracker class.

        Args:
            self.
        """
        super().__init__()

    def get_post_data(self, media_id):
        """
        Get post data from Instagram API.

        Args:
            self.
            media_id (str): Instagram media id.

        Returns:
            dict: Post data.
        """
        url = (f''' https://graph.instagram.com/
                    {media_id}?fields=id,media_type,media_url,username,timestamp
                    &access_token={INSTAGRAM_KEY}''')
        response = self.session.get(url)
        if response.status_code != 200:
            abort(404, description='Could not request data from Instagram.')
        return json.loads(response.text)

    def get_user_posts(self):
        """Get all user post ids + captions from Instagram API.

        Args:
            self.

        Returns:
            dict: all user post ids + captions.
        """
        url = f'''  https://graph.instagram.com/
                    me/media?fields=id,caption
                    &access_token={INSTAGRAM_KEY}'''
        response = self.session.get(url)
        if response.status_code != 200:
            abort(404, description='Could not request data from Instagram.')
        return json.loads(response.text)

    def get_latest_posts(self, amount):
        """
        Get latest posts from Instagram API.

        Args:
            self.
            amount (int): Amount of posts to be returned.

        Returns:
            dict: Latest posts.
        """
        latest_posts = []
        user_posts = self.get_user_posts()['data']
        if amount > len(user_posts):
            amount = len(user_posts)
        for entry in user_posts[0:amount]:  # not sure if this works
            post = self.get_post_data(entry['id'])
            latest_posts.append(
                {
                    'caption': entry['caption'],
                    'media_url': post['media_url'],
                    'media_type': post['media_type'],
                    'timestamp': post['timestamp'],
                },
            )
        return latest_posts
