from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
import logging
from typing import Dict, List, Optional
import time

class InstaClient:
    def __init__(self, delay_range: tuple = (1, 3)):
        """
        Initialize Instagram client
        
        Args:
            delay_range: Tuple of min/max seconds to wait between requests
        """
        self.cl = Client()
        self.delay_range = delay_range
        self.user_id = None
        self.username = None
        self.is_logged_in = False
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def login(self, username: str, password: str) -> bool:
        """
        Login to Instagram
        
        Args:
            username: Instagram username
            password: Instagram password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            self.cl.login(username, password)
            self.username = username
            self.user_id = self.cl.user_id_from_username(username)
            self.is_logged_in = True
            self.logger.info(f"Successfully logged in as {username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            self.is_logged_in = False
            return False

    def logout(self) -> bool:
        """
        Logout from Instagram
        
        Returns:
            bool: True if logout successful
        """
        try:
            self.cl.logout()
            self.is_logged_in = False
            self.user_id = None
            self.username = None
            self.logger.info("Successfully logged out")
            return True
        except Exception as e:
            self.logger.error(f"Logout failed: {str(e)}")
            return False

    def _check_login(self):
        """Check if user is logged in, raise exception if not"""
        if not self.is_logged_in:
            raise LoginRequired("Please login first")

    def _delay(self):
        """Add random delay between requests to avoid rate limiting"""
        import random
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)

    def get_followers(self, user_id: Optional[str] = None) -> Dict:
        """
        Get followers for a user (defaults to logged-in user)
        
        Args:
            user_id: User ID to get followers for (optional, defaults to self)
            
        Returns:
            Dict: Dictionary of followers {user_id: user_info}
        """
        self._check_login()
        
        try:
            target_user_id = user_id or self.user_id
            self._delay()
            followers = self.cl.user_followers(target_user_id)
            self.logger.info(f"Retrieved {len(followers)} followers")
            return followers
            
        except Exception as e:
            self.logger.error(f"Failed to get followers: {str(e)}")
            return {}

    def get_following(self, user_id: Optional[str] = None) -> Dict:
        """
        Get following list for a user (defaults to logged-in user)
        
        Args:
            user_id: User ID to get following for (optional, defaults to self)
            
        Returns:
            Dict: Dictionary of following {user_id: user_info}
        """
        self._check_login()
        
        try:
            target_user_id = user_id or self.user_id
            self._delay()
            following = self.cl.user_following(target_user_id)
            self.logger.info(f"Retrieved {len(following)} following")
            return following
            
        except Exception as e:
            self.logger.error(f"Failed to get following: {str(e)}")
            return {}

    def get_user_posts(self, user_id: Optional[str] = None, amount: int = 20) -> List:
        """
        Get posts for a user (defaults to logged-in user)
        
        Args:
            user_id: User ID to get posts for (optional, defaults to self)
            amount: Number of posts to retrieve
            
        Returns:
            List: List of media objects
        """
        self._check_login()
        
        try:
            target_user_id = user_id or self.user_id
            self._delay()
            posts = self.cl.user_medias(target_user_id, amount=amount)
            self.logger.info(f"Retrieved {len(posts)} posts")
            return posts
            
        except Exception as e:
            self.logger.error(f"Failed to get posts: {str(e)}")
            return []

    def get_user_info(self, username: Optional[str] = None) -> Optional[Dict]:
        """
        Get user information
        
        Args:
            username: Username to get info for (optional, defaults to self)
            
        Returns:
            Dict: User information dictionary
        """
        self._check_login()
        
        try:
            target_username = username or self.username
            self._delay()
            user_info = self.cl.user_info_by_username(target_username)
            self.logger.info(f"Retrieved user info for {target_username}")
            return user_info
            
        except Exception as e:
            self.logger.error(f"Failed to get user info: {str(e)}")
            return None

    def get_follower_analytics(self) -> Dict:
        """
        Get basic follower analytics
        
        Returns:
            Dict: Follower analytics including count, growth, etc.
        """
        self._check_login()
        
        try:
            user_info = self.get_user_info()
            followers = self.get_followers()
            following = self.get_following()
            
            analytics = {
                'follower_count': user_info.follower_count if user_info else 0,
                'following_count': user_info.following_count if user_info else 0,
                'posts_count': user_info.media_count if user_info else 0,
                'followers_list_size': len(followers),
                'following_list_size': len(following),
                'follower_following_ratio': len(followers) / max(len(following), 1),
                'mutual_follows': len(set(followers.keys()) & set(following.keys()))
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Failed to get follower analytics: {str(e)}")
            return {}