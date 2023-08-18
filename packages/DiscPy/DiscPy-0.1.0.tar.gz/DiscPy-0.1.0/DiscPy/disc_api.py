import logging, requests
from rest_adapter import RestAdapter
from models import *

class DiscuitAPI:
    def __init__(self, hostname: str = 'discuit.net/api', ssl_verify: bool = True,
                 logger: logging.Logger = None):
        
        self._rest_adapter = RestAdapter(hostname, ssl_verify, logger)
        self._session = requests.Session()

    def authenticate(self, username:str, password:str):
        try:
            result = self._session.get('https://discuit.net/api/_initial')
        except requests.exceptions.RequestException as e:
            raise DiscuitAPIException("Request for login headers failed") from e

        headers = {
            'Cookie' : result.headers['Set-Cookie'],
            'X-Csrf-Token' : result.headers['Csrf-Token'],
            'Content-Type' : 'application/json'
        }

        data = {
            'username' : username,
            'password' : password
        }

        try:
            response = self._session.post('http://discuit.net/api/_login', 
                                     headers=headers, json=data)
        except requests.exceptions.RequestException as e:
            raise DiscuitAPIException("Login request failed") from e
    
    def get_all_posts(self) -> Posts:
        """Gets most recent posts, site-wide.

        Returns:
            Posts: A list of Post objects.
        """
        result = self._rest_adapter.get(endpoint='posts')
        posts = Posts(**result.data)
        return posts
    
    def get_community_posts(self, community_id: str) -> Posts:
        """Gets most recent posts by Community ID

        Args:
            community_id (str): The ID of the community to get posts from.

        Returns:
            Posts: A list of Post objects.
        """
        result = self._rest_adapter.get(endpoint=f'posts?communityID={community_id}')
        posts = Posts(**result.data)
        return posts
    
    def get_post_by_id(self, post_id: str) -> Post:
        """Get a Post object by Public ID
        Currently returns list of posts, even though its one.

        Args:
            post_id (str): The Public ID of the post (discuit.com/postId)

        Returns:
            Posts: List of Post objects.
        """
        # post ID should be the public ID
        # currently broken, as models are weird
        result = self._rest_adapter.get(endpoint=f'posts/{post_id}')
        post = Post(**result.data)
        return post
    
    def get_post_comments(self, post_id:str) -> Comments: 
        """Get comments on a post by Public ID

        Args:
            post_id (str): The Public ID of the post.

        Returns:
            Comments: A list of Comment objects
        """
        result = self._rest_adapter.get(endpoint=f'posts/{post_id}/comments')
        comments = Comments(**result.data)
        return comments

    def fetch_link_data(self, link: Link):
        link.data = self._rest_adapter.fetch_data(url=link.url)

    def get_communites(self) -> List[Community]:
        """Returns a list of all communities, sitewide

        Returns:
            List[Community]: A list of community objects
        """
        results = self._rest_adapter.get(endpoint='communities')
        communities_list = [Community(**datum) for datum in results.data]
        return communities_list

    def get_community_by_id(self, community_id: str) -> Community:
        """Returns a community object by ID.

        Args:
            community_id (str): The community ID.

        Returns:
            Community: A Community object
        """
        result = self._rest_adapter.get(endpoint=f'communities/{community_id}')
        community = Community(**result.data)
        return community

    def get_community_rules(self, community_id: str) -> List[CommunityRule]:
        """Returns a list of CommunityRule objects for the community ID

        Args:
            community_id (str): ID of community.

        Returns:
            List[CommunityRule]: A List of CommunityRule objects
        """
        result = self._rest_adapter.get(endpoint=f"communities/{community_id}/rules")
        rules_list = [CommunityRule(**datum) for datum in result.data]
        return rules_list

    def get_community_mods(self, community_id: str) -> List[User]:
        """Returns a list of User objects that moderate the community.

        Args:
            community_id (str): Community ID

        Returns:
            List[User]: A list of user objects.
        """
        result = self._rest_adapter.get(endpoint=f"communities/{community_id}/mods")
        mods_list = [User(**datum) for datum in result.data]
        return mods_list

    def get_user_by_username(self, username: str) -> User:
        """Returns a User object by username

        Args:
            username (str): the username of the user

        Returns:
            User: A User object
        """
        result = self._rest_adapter.get(endpoint=f"users/{username}")
        user = User(**result.data)
        return user

    def get_user_feed(self, username:str):
        pass

#res = api.get_community_posts(test_comm_id)        Returns diff community posts