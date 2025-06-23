
from typing import Dict, List
import click
import getpass
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

from pkg.instagrapi import InstaClient
from services.unfollower_detector import UnfollowersDetector

console = Console()

def display_not_following_back(users: List[Dict], limit: int = None):
    """Display users who don't follow back"""
    if not users:
        console.print("🎉 [green]Everyone you follow is following you back![/green]")
        return
    
    display_users = users[:limit] if limit else users
    
    table = Table(
        title=f"😤 Users Not Following You Back ({len(users)} total)",
        show_header=True,
        header_style="bold red"
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="white", max_width=25)
    table.add_column("Verified", style="blue", justify="center", width=8)
    table.add_column("Followers", style="green", justify="right")
    
    for i, user in enumerate(display_users, 1):
        verified = "✓" if user.get('is_verified') else ""
        followers = f"{user.get('follower_count', 0):,}" if user.get('follower_count') else "?"
        
        table.add_row(
            str(i),
            f"@{user['username']}",
            user['full_name'][:25],
            verified,
            followers
        )
    
    console.print(table)
    
    if limit and len(users) > limit:
        console.print(f"... and {len(users) - limit} more")

def display_unfollowers(users: List[Dict]):
    """Display users who unfollowed you"""
    if not users:
        console.print("😇 [green]No one unfollowed you since last check![/green]")
        return
    
    table = Table(
        title=f"💔 Recent Unfollowers ({len(users)} total)",
        show_header=True,
        header_style="bold red"
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="white", max_width=25)
    table.add_column("Unfollowed Since", style="yellow")
    
    for i, user in enumerate(users, 1):
        table.add_row(
            str(i),
            f"@{user['username']}",
            user['full_name'][:25],
            user['unfollowed_since']
        )
    
    console.print(table)

def display_new_followers(users: List[Dict]):
    """Display new followers"""
    if not users:
        console.print("📈 [blue]No new followers since last check[/blue]")
        return
    
    table = Table(
        title=f"🎉 New Followers ({len(users)} total)",
        show_header=True,
        header_style="bold green"
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="white", max_width=25)
    table.add_column("Followed Since", style="green")
    
    for i, user in enumerate(users, 1):
        table.add_row(
            str(i),
            f"@{user['username']}",
            user['full_name'][:25],
            user['followed_since']
        )
    
    console.print(table)

def get_authenticated_client(username: str = None, password: str = None) -> InstaClient:
    """Get authenticated Instagram client"""
    if not username:
        username = click.prompt("Enter Instagram username")
    
    if not password:
        password = getpass.getpass("Enter Instagram password: ")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Logging in to Instagram...", total=None)
        
        client = InstaClient()
        success = client.login(username, password)
        
        if success:
            progress.update(task, description="✅ Login successful!")
            return client
        else:
            console.print("❌ [red]Login failed![/red]")
            raise click.Abort()

def display_analytics(analytics: Dict):
    """Display analytics using rich formatting"""
    table = Table(title="📊 Follower Analytics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="green", justify="right")
    
    table.add_row("👥 Followers", f"{analytics.get('follower_count', 0):,}")
    table.add_row("👤 Following", f"{analytics.get('following_count', 0):,}")
    table.add_row("📷 Posts", f"{analytics.get('posts_count', 0):,}")
    table.add_row("📈 F/F Ratio", f"{analytics.get('follower_following_ratio', 0):.2f}")
    table.add_row("🤝 Mutual Follows", f"{analytics.get('mutual_follows', 0):,}")
    
    console.print(table)

def display_posts(posts: List, limit: int = 10):
    """Display posts using rich formatting"""
    table = Table(title=f"📱 Recent Posts (Top {min(limit, len(posts))})", show_header=True)
    table.add_column("Post #", style="cyan", width=8)
    table.add_column("❤️ Likes", style="red", justify="right")
    table.add_column("💬 Comments", style="blue", justify="right")
    table.add_column("📊 Engagement", style="green", justify="right")
    table.add_column("📅 Date", style="yellow")
    table.add_column("📝 Caption Preview", style="white", max_width=40)
    
    for i, post in enumerate(posts[:limit], 1):
        engagement = post.like_count + post.comment_count
        date_str = post.taken_at.strftime('%m/%d %H:%M')
        caption = post.caption_text or "No caption"
        preview = (caption[:35] + "...") if len(caption) > 35 else caption
        
        table.add_row(
            str(i),
            f"{post.like_count:,}",
            f"{post.comment_count:,}",
            f"{engagement:,}",
            date_str,
            preview
        )
    
    console.print(table)

def export_data(data: Dict, filename: str):
    """Export data to JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.json"
    
    try:
        with open(full_filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        console.print(f"✅ Data exported to [green]{full_filename}[/green]")
    except Exception as e:
        console.print(f"❌ Failed to export data: [red]{e}[/red]")

# CLI App using Click
@click.group(invoke_without_command=True)
@click.option('--username', '-u', help='Instagram username')
@click.option('--password', '-p', help='Instagram password (will prompt if not provided)')
@click.pass_context
def cli(ctx, username, password):
    """Instagram Analytics Tool - Analyze your Instagram profile"""
    if ctx.invoked_subcommand is None:
        console.print(Panel.fit("🚀 Instagram Analytics Tool", style="bold blue"))
        console.print("Use --help to see available commands")
        return
    
    # Store credentials in context
    ctx.ensure_object(dict)
    ctx.obj['username'] = username
    ctx.obj['password'] = password

def get_authenticated_client(username, password):
    """Get authenticated Instagram client"""
    if not username:
        username = Prompt.ask("Enter Instagram username")
    
    if not password:
        password = getpass.getpass("Enter Instagram password: ")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Logging in to Instagram...", total=None)
        
        client = InstaClient()
        success = client.login(username, password)
        
        if success:
            progress.update(task, description="✅ Login successful!")
            return client
        else:
            console.print("❌ [red]Login failed![/red]")
            raise click.Abort()

@cli.command()
@click.option('--export', is_flag=True, help='Export analytics to JSON file')
@click.pass_context
def analytics(ctx, export):
    """Get follower analytics"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Fetching analytics...", total=None)
            analytics_data = client.get_follower_analytics()
        
        display_analytics(analytics_data)
        
        if export:
            export_data(analytics_data, "instagram_analytics")
            
    except Exception as e:
        console.print(f"❌ Error getting analytics: [red]{e}[/red]")
    finally:
        client.logout()

@cli.command()
@click.option('--limit', '-l', default=10, help='Number of posts to retrieve (default: 10)')
@click.option('--export', is_flag=True, help='Export posts data to JSON file')
@click.pass_context
def posts(ctx, limit, export):
    """Get recent posts data"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Fetching {limit} posts...", total=None)
            posts_data = client.get_user_posts(amount=limit)
        
        display_posts(posts_data, limit)
        
        if export:
            posts_dict = [
                {
                    'id': post.id,
                    'likes': post.like_count,
                    'comments': post.comment_count,
                    'date': post.taken_at.isoformat(),
                    'caption': post.caption_text
                }
                for post in posts_data
            ]
            export_data(posts_dict, "instagram_posts")
            
    except Exception as e:
        console.print(f"❌ Error getting posts: [red]{e}[/red]")
    finally:
        client.logout()

@cli.command()
@click.option('--export', is_flag=True, help='Export user info to JSON file')
@click.pass_context
def user_info(ctx, export):
    """Get user profile information"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Fetching user info...", total=None)
            info = client.get_user_info()
        
        if info:
            table = Table(title="👤 User Profile Information", show_header=False)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Username", info.username)
            table.add_row("Full Name", info.full_name or "Not set")
            table.add_row("Bio", (info.biography[:50] + "...") if info.biography and len(info.biography) > 50 else (info.biography or "No bio"))
            table.add_row("Followers", f"{info.follower_count:,}")
            table.add_row("Following", f"{info.following_count:,}")
            table.add_row("Posts", f"{info.media_count:,}")
            table.add_row("Private Account", "Yes" if info.is_private else "No")
            table.add_row("Verified", "Yes" if info.is_verified else "No")
            
            console.print(table)
            
            if export:
                info_dict = {
                    'username': info.username,
                    'full_name': info.full_name,
                    'biography': info.biography,
                    'follower_count': info.follower_count,
                    'following_count': info.following_count,
                    'media_count': info.media_count,
                    'is_private': info.is_private,
                    'is_verified': info.is_verified
                }
                export_data(info_dict, "instagram_user_info")
        else:
            console.print("❌ [red]Failed to get user information[/red]")
            
    except Exception as e:
        console.print(f"❌ Error getting user info: [red]{e}[/red]")
    finally:
        client.logout()
@cli.command()
@click.option('--limit', '-l', default=50, help='Limit number of results shown (default: 50)')
@click.option('--export', is_flag=True, help='Export results to JSON file')
@click.option('--sort-by-followers', is_flag=True, help='Sort by follower count (highest first)')
@click.pass_context
def not_following_back(ctx, limit, export, sort_by_followers):
    """Find users who don't follow you back"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Get followers and following
            task = progress.add_task("Fetching followers...", total=None)
            followers = client.get_followers()
            
            progress.update(task, description="Fetching following...")
            following = client.get_following()
            
            progress.update(task, description="Analyzing relationships...")
            detector = UnfollowersDetector(client)
            not_following = detector.find_not_following_back(followers, following)
        
        # Sort by follower count if requested
        if sort_by_followers:
            not_following.sort(key=lambda x: x.get('follower_count', 0), reverse=True)
        
        # Display results
        console.print(f"\n📊 Analysis complete!")
        console.print(f"👥 You follow: [blue]{len(following)}[/blue] users")
        console.print(f"👥 Following you: [green]{len(followers)}[/green] users")
        console.print(f"😤 Not following back: [red]{len(not_following)}[/red] users")
        
        display_not_following_back(not_following, limit)
        
        if export:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"not_following_back_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump({
                    'generated_at': datetime.now().isoformat(),
                    'username': client.username,
                    'total_following': len(following),
                    'total_followers': len(followers),
                    'not_following_back_count': len(not_following),
                    'not_following_back': not_following
                }, f, indent=2)
            console.print(f"📁 Results exported to [green]{filename}[/green]")
            
    except Exception as e:
        console.print(f"❌ Error: [red]{e}[/red]")
    finally:
        client.logout()

@cli.command()
@click.option('--save-snapshot', is_flag=True, help='Save current state as snapshot for future comparison')
@click.pass_context
def track_unfollowers(ctx, save_snapshot):
    """Track who unfollowed you since last check"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])
    
    try:
        detector = UnfollowersDetector(client)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Fetching current data...", total=None)
            followers = client.get_followers()
            following = client.get_following()
            
            progress.update(task, description="Loading previous snapshot...")
            previous_snapshot = detector.load_latest_snapshot()
            
            progress.update(task, description="Analyzing changes...")
        
        if previous_snapshot:
            # Find unfollowers and new followers
            unfollowers = detector.find_unfollowers(followers, previous_snapshot)
            new_followers = detector.find_new_followers(followers, previous_snapshot)
            
            console.print(f"\n📊 Changes since {previous_snapshot['datetime'][:19]}:")
            console.print(f"📉 Unfollowers: [red]{len(unfollowers)}[/red]")
            console.print(f"📈 New followers: [green]{len(new_followers)}[/green]")
            console.print(f"📊 Net change: [{'green' if len(new_followers) >= len(unfollowers) else 'red'}]{len(new_followers) - len(unfollowers):+d}[/]")
            
            display_unfollowers(unfollowers)
            console.print()
            display_new_followers(new_followers)
            
        else:
            console.print("📸 [yellow]No previous snapshot found. This will be your first snapshot.[/yellow]")
        
        # Save new snapshot
        if save_snapshot or not previous_snapshot:
            if not previous_snapshot or Confirm.ask("Save current state as new snapshot?"):
                detector.save_followers_snapshot(followers, following)
                
    except Exception as e:
        console.print(f"❌ Error: [red]{e}[/red]")
    finally:
        client.logout()

@cli.command()
@click.option("--posts", default=10, show_default=True, help="Number of recent posts to analyze")
@click.option("--top", default=10, show_default=True, help="Show bottom N engaging followers")
@click.pass_context
def low_engagers(ctx, posts, top):
    """📉 Find followers who engage least (likes/comments)"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])

    console.print(f"🔍 Fetching last {posts} posts...")
    media_list = client.get_user_posts(amount=posts)
    if not media_list:
        console.print("[red]No posts found.[/red]")
        return

    followers = client.get_followers()
    engagement_count = {uid: 0 for uid in followers.keys()}

    for media in media_list:
        try:
            likers = client.cl.media_likers(media.pk)
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to fetch likers for post {media.pk}: {e}[/yellow]")
            likers = []

        try:
            raw_comments = client.cl.media_comments(media.pk)
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to fetch comments for post {media.pk}: {e}[/yellow]")
            raw_comments = []

        # Count likes
        for user in likers:
            if user.pk in engagement_count:
                engagement_count[user.pk] += 1

        # Count comments (safely)
        for comment in raw_comments:
            try:
                if comment.user and comment.user.pk in engagement_count:
                    engagement_count[comment.user.pk] += 1
            except AttributeError:
                console.print(f"[yellow]Skipping malformed comment[/yellow]")

    # Sort by lowest engagement
    least_engagers = sorted(engagement_count.items(), key=lambda x: x[1])[:top]

    table = Table(title=f"🚨 Least Engaging Followers (Out of {len(followers)} followers)")
    table.add_column("Username", style="cyan")
    table.add_column("Full Name")
    table.add_column("Engagements", justify="right")

    for uid, count in least_engagers:
        user = followers[uid]
        table.add_row(user.username, user.full_name or "—", str(count))

    console.print(table)
    client.logout()

@cli.command()
@click.option('--posts-limit', '-l', default=20, help='Number of posts to include in report (default: 20)')
@click.option('--export', is_flag=True, help='Export full report to JSON file')
@click.pass_context
def full_report(ctx, posts_limit, export):
    """Generate a complete analytics report"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])
    
    try:
        console.print(Panel.fit("📊 Generating Full Instagram Analytics Report", style="bold blue"))
        
        report_data = {}
        
        # Get all data
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # User info
            task1 = progress.add_task("Fetching user info...", total=None)
            user_data = client.get_user_info()
            report_data['user_info'] = user_data
            
            # Analytics
            progress.update(task1, description="Fetching analytics...")
            analytics_data = client.get_follower_analytics()
            report_data['analytics'] = analytics_data
            
            # Posts
            progress.update(task1, description=f"Fetching {posts_limit} posts...")
            posts_data = client.get_user_posts(amount=posts_limit)
            report_data['posts'] = posts_data
            
            progress.update(task1, description="✅ Report generated!")
        
        # Display all data
        console.print("\n" + "="*60)
        if user_data:
            console.print(f"📱 Account: @{user_data.username} ({user_data.full_name or 'No name'})")
        
        display_analytics(analytics_data)
        console.print()
        display_posts(posts_data, min(10, posts_limit))
        
        # Calculate additional insights
        if posts_data:
            avg_likes = sum(post.like_count for post in posts_data) / len(posts_data)
            avg_comments = sum(post.comment_count for post in posts_data) / len(posts_data)
            total_engagement = sum(post.like_count + post.comment_count for post in posts_data)
            
            insights_table = Table(title="📈 Content Insights", show_header=True)
            insights_table.add_column("Metric", style="cyan")
            insights_table.add_column("Value", style="green", justify="right")
            
            insights_table.add_row("Average Likes per Post", f"{avg_likes:.0f}")
            insights_table.add_row("Average Comments per Post", f"{avg_comments:.0f}")
            insights_table.add_row("Total Engagement", f"{total_engagement:,}")
            insights_table.add_row("Engagement Rate", f"{(total_engagement / max(analytics_data.get('follower_count', 1), 1)) * 100:.2f}%")
            
            console.print()
            console.print(insights_table)
        
        if export:
            # Prepare export data
            export_report = {
                'generated_at': datetime.now().isoformat(),
                'user_info': {
                    'username': user_data.username if user_data else None,
                    'full_name': user_data.full_name if user_data else None,
                    'follower_count': user_data.follower_count if user_data else 0,
                    'following_count': user_data.following_count if user_data else 0,
                    'media_count': user_data.media_count if user_data else 0,
                } if user_data else {},
                'analytics': analytics_data,
                'posts': [
                    {
                        'id': post.id,
                        'likes': post.like_count,
                        'comments': post.comment_count,
                        'date': post.taken_at.isoformat(),
                        'caption': post.caption_text,
                        'engagement': post.like_count + post.comment_count
                    }
                    for post in posts_data
                ],
                'insights': {
                    'avg_likes': avg_likes if posts_data else 0,
                    'avg_comments': avg_comments if posts_data else 0,
                    'total_engagement': total_engagement if posts_data else 0,
                } if posts_data else {}
            }
            export_data(export_report, "instagram_full_report")
        
    except Exception as e:
        console.print(f"❌ Error generating report: [red]{e}[/red]")
    finally:
        client.logout()

@cli.command()
@click.option('--limit', '-l', default=20, help='Limit number of results shown (default: 20)')
@click.pass_context
def full_report_followers(ctx, limit):
    """Complete analysis: not following back + unfollowers tracking"""
    client = get_authenticated_client(ctx.obj['username'], ctx.obj['password'])
    
    try:
        console.print(Panel.fit("🔍 Complete Follower Analysis", style="bold blue"))
        
        detector = UnfollowersDetector(client)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Fetching all data...", total=None)
            followers = client.get_followers()
            following = client.get_following()
            
            progress.update(task, description="Loading previous data...")
            previous_snapshot = detector.load_latest_snapshot()
            
            progress.update(task, description="Running analysis...")
            not_following = detector.find_not_following_back(followers, following)
            
            unfollowers = []
            new_followers = []
            if previous_snapshot:
                unfollowers = detector.find_unfollowers(followers, previous_snapshot)
                new_followers = detector.find_new_followers(followers, previous_snapshot)
        
        # Display comprehensive results
        console.print(f"\n📊 [bold]COMPLETE ANALYSIS RESULTS[/bold]")
        console.print(f"👥 Following: [blue]{len(following):,}[/blue] | Followers: [green]{len(followers):,}[/green]")
        console.print(f"😤 Not following back: [red]{len(not_following)}[/red]")
        
        if previous_snapshot:
            console.print(f"💔 Recent unfollowers: [red]{len(unfollowers)}[/red]")
            console.print(f"🎉 New followers: [green]{len(new_followers)}[/green]")
        
        console.print("\n" + "="*60)
        display_not_following_back(not_following, limit)
        
        if previous_snapshot:
            console.print()
            display_unfollowers(unfollowers)
            console.print()
            display_new_followers(new_followers)
        
        # Offer to save snapshot
        if Confirm.ask("\nSave current state as snapshot for future tracking?"):
            detector.save_followers_snapshot(followers, following)
            
    except Exception as e:
        console.print(f"❌ Error: [red]{e}[/red]")
    finally:
        client.logout()

if __name__ == "__main__":
    cli()