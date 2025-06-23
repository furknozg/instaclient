
from datetime import datetime
import json
from typing import Dict
from pathlib import Path
from pkg.instagrapi import InstaClient
from rich.console import *


class UnfollowersDetector:
    def __init__(self, client: InstaClient):
        self.client = client
        self.data_dir = Path("instagram_data")
        self.data_dir.mkdir(exist_ok=True)
        
    def save_followers_snapshot(self, followers: Dict, following: Dict) -> str:
        """Save current followers/following snapshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.data_dir / f"followers_snapshot_{timestamp}.json"
        
        snapshot = {
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'username': self.client.username,
            'followers': {uid: {'username': user.username, 'full_name': user.full_name} 
                         for uid, user in followers.items()},
            'following': {uid: {'username': user.username, 'full_name': user.full_name} 
                         for uid, user in following.items()},
            'followers_count': len(followers),
            'following_count': len(following)
        }
        
        with open(filename, 'w') as f:
            json.dump(snapshot, f, indent=2)
            
        console.print(f"📸 Snapshot saved: [green]{filename}[/green]")
        return str(filename)
    
    def load_latest_snapshot(self) -> Dict:
        """Load the most recent snapshot"""
        snapshots = list(self.data_dir.glob("followers_snapshot_*.json"))
        if not snapshots:
            return None
            
        latest = max(snapshots, key=lambda x: x.stat().st_mtime)
        
        with open(latest, 'r') as f:
            data = json.load(f)
            
        console.print(f"📂 Loaded snapshot: [blue]{latest.name}[/blue] from {data['datetime'][:19]}")
        return data
    
    def find_not_following_back(self, followers: Dict, following: Dict) -> List[Dict]:
        """Find users you follow who don't follow you back"""
        follower_ids = set(followers.keys())
        following_ids = set(following.keys())
        
        not_following_back = following_ids - follower_ids
        
        return [
            {
                'user_id': uid,
                'username': following[uid].username,
                'full_name': following[uid].full_name or 'No name',
                'is_verified': getattr(following[uid], 'is_verified', False),
                'follower_count': getattr(following[uid], 'follower_count', 0)
            }
            for uid in not_following_back
        ]
    
    def find_unfollowers(self, current_followers: Dict, previous_snapshot: Dict) -> List[Dict]:
        """Find users who unfollowed you since last snapshot"""
        if not previous_snapshot:
            return []
            
        previous_followers = set(previous_snapshot['followers'].keys())
        current_follower_ids = set(current_followers.keys())
        
        unfollowed_ids = previous_followers - current_follower_ids
        
        return [
            {
                'user_id': uid,
                'username': previous_snapshot['followers'][uid]['username'],
                'full_name': previous_snapshot['followers'][uid]['full_name'] or 'No name',
                'unfollowed_since': previous_snapshot['datetime'][:19]
            }
            for uid in unfollowed_ids
        ]
    
    def find_new_followers(self, current_followers: Dict, previous_snapshot: Dict) -> List[Dict]:
        """Find new followers since last snapshot"""
        if not previous_snapshot:
            return []
            
        previous_followers = set(previous_snapshot['followers'].keys())
        current_follower_ids = set(current_followers.keys())
        
        new_follower_ids = current_follower_ids - previous_followers
        
        return [
            {
                'user_id': uid,
                'username': current_followers[uid].username,
                'full_name': current_followers[uid].full_name or 'No name',
                'followed_since': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            for uid in new_follower_ids
        ]