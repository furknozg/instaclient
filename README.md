Instagram Analytics Tool 📊
A comprehensive command-line tool for analyzing your Instagram account, tracking followers, unfollowers, engagement, and generating detailed analytics reports.
✨ Features

👥 Follower Analysis: Track who doesn't follow you back
💔 Unfollower Detection: Monitor who unfollowed you over time
📈 New Follower Tracking: See who recently started following you
📊 Engagement Analytics: Analyze your posts' performance
👻 Low Engagement Detection: Find followers who rarely interact with your content
📱 Complete Profile Analytics: Get comprehensive account insights
📁 Data Export: Export all analytics to JSON files
🎨 Beautiful CLI Interface: Rich, colorful terminal output

🚀 Installation

Clone the repository:

bashgit clone <repository-url>
cd instagram-analytics-tool

Install dependencies:

bashpip install -r requirements.txt
📋 Dependencies

instagrapi - Instagram API client
click - Command line interface framework
rich - Beautiful terminal formatting
httpx - HTTP client for web scraping
pillow - Image processing
jmespath - JSON path expressions

🎯 Usage
Basic Commands
The tool uses a command-line interface with multiple subcommands:
bashpython src/main.py [OPTIONS] COMMAND [ARGS]...
Available Commands
1. Analytics - Get follower analytics
bashpython src/main.py analytics [--export]

Shows follower/following counts, ratios, and mutual follows
Use --export to save data to JSON

2. User Info - Get profile information
bashpython src/main.py user-info [--export]

Displays username, bio, follower counts, verification status
Shows if account is private

3. Posts Analysis - Analyze recent posts
bashpython src/main.py posts [--limit 10] [--export]

Shows likes, comments, engagement for recent posts
--limit sets number of posts to analyze (default: 10)

4. Not Following Back - Find users who don't follow back
bashpython src/main.py not-following-back [--limit 50] [--export] [--sort-by-followers]

Lists users you follow who don't follow you back
--sort-by-followers sorts by follower count (highest first)
--limit controls display count (default: 50)

5. Track Unfollowers - Monitor follower changes
bashpython src/main.py track-unfollowers [--save-snapshot]

Compares current followers with previous snapshot
Shows who unfollowed and who started following
--save-snapshot saves current state for future comparison

6. Low Engagers - Find least engaging followers
bashpython src/main.py low-engagers [--posts 10] [--top 10]

Analyzes who likes/comments least on your posts
--posts sets number of recent posts to analyze
--top shows bottom N engaging followers

7. Full Report - Complete analytics report
bashpython src/main.py full-report [--posts-limit 20] [--export]

Generates comprehensive report with all analytics
Includes user info, follower stats, post performance, and insights

8. Complete Follower Analysis - Combined analysis
bashpython src/main.py full-report-followers [--limit 20]

Combines not-following-back analysis with unfollower tracking
Provides complete follower relationship overview

🔐 Authentication
The tool will prompt for your Instagram credentials:

Username can be provided with -u or --username
Password will be prompted securely (not shown on screen)
Credentials can also be provided via command line (not recommended for security)

Example:
bashpython src/main.py analytics -u your_username
📊 Sample Output
Analytics Report
┌─────────────────── 📊 Follower Analytics ───────────────────┐
│ Metric          │                                    Value │
├─────────────────┼──────────────────────────────────────────┤
│ 👥 Followers    │                                    1,234 │
│ 👤 Following    │                                      567 │
│ 📷 Posts        │                                       89 │
│ 📈 F/F Ratio    │                                     2.18 │
│ 🤝 Mutual       │                                      123 │
└─────────────────┴──────────────────────────────────────────┘
Not Following Back
┌─────────────────────────────────────────────────────────────┐
│           😤 Users Not Following You Back (15 total)        │
├───┬─────────────────┬──────────────────┬──────────┬─────────┤
│ # │ Username        │ Full Name        │ Verified │ Followe │
├───┼─────────────────┼──────────────────┼──────────┼─────────┤
│ 1 │ @example_user   │ Example User     │          │   2,543 │
│ 2 │ @another_user   │ Another Person   │    ✓     │  12,890 │
└───┴─────────────────┴──────────────────┴──────────┴─────────┘
📁 Data Storage
The tool creates an instagram_data/ directory to store:

Snapshots: Follower/following data for comparison over time
Export files: JSON exports with timestamps

Snapshot Files

Format: followers_snapshot_YYYYMMDD_HHMMSS.json
Contains followers and following data for historical comparison
Used for unfollower detection

Export Files

Format: [report_type]_YYYYMMDD_HHMMSS.json
Structured JSON data for external analysis
Includes timestamps and metadata

🔧 Configuration
Delay Settings
The tool includes built-in delays between API requests to avoid rate limiting:

Default: 1-3 seconds between requests
Randomized to appear more natural
Configurable in InstaClient class

Logging

Logs are displayed in the terminal with rich formatting
Error handling for common Instagram API issues
Login/logout status tracking

🛡️ Security & Privacy

Credentials: Never stored permanently
Rate Limiting: Built-in delays prevent account restrictions
Session Management: Proper login/logout handling
Local Storage: All data stored locally on your machine

⚠️ Important Notes

Instagram Terms: Use responsibly and in accordance with Instagram's Terms of Service
Rate Limits: Don't run commands too frequently to avoid temporary restrictions
Private Accounts: Can only analyze accounts you have access to
Large Accounts: Processing may take longer for accounts with many followers
API Changes: Instagram may change their API, which could affect functionality

🐛 Troubleshooting
Common Issues
Login Failed

Check username/password
Try logging in via Instagram app first
Check for two-factor authentication requirements

Rate Limited

Wait a few minutes before retrying
The tool includes delays, but Instagram may still impose limits

Missing Data

Some users may have privacy settings that limit data access
Deleted accounts won't appear in results

Connection Issues

Check internet connection
Instagram servers may be temporarily unavailable

📈 Use Cases

Content Strategy: Analyze which posts perform best
Follower Management: Clean up your following list
Growth Tracking: Monitor follower changes over time
Engagement Analysis: Identify your most engaged followers
Account Insights: Get comprehensive analytics not available in Instagram app

🤝 Contributing
Feel free to submit issues, feature requests, or pull requests to improve the tool.
⚖️ Disclaimer
This tool is for educational and personal use only. Users are responsible for complying with Instagram's Terms of Service and applicable laws. The developers are not responsible for any account restrictions or violations that may result from using this tool.
