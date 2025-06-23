# Instagram Analytics Tool 📊

A comprehensive **command-line tool** for analyzing your Instagram account, tracking followers, unfollowers, engagement, and generating detailed analytics reports.

---

## ✨ Features

- 👥 **Follower Analysis**: Track who doesn't follow you back  
- 💔 **Unfollower Detection**: Monitor who unfollowed you over time  
- 📈 **New Follower Tracking**: See who recently started following you  
- 📊 **Engagement Analytics**: Analyze your posts' performance  
- 👻 **Low Engagement Detection**: Find followers who rarely interact with your content  
- 📱 **Complete Profile Analytics**: Get comprehensive account insights  
- 📁 **Data Export**: Export all analytics to JSON files  
- 🎨 **Beautiful CLI Interface**: Rich, colorful terminal output  

---

## 🚀 Installation

1. **Clone the repository**:

```bash
git clone <repo-url>
cd instagram-analytics-tool
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## 📋 Dependencies

- `instagrapi` – Instagram API client  
- `click` – Command line interface framework  
- `rich` – Beautiful terminal formatting  
- `httpx` – HTTP client for web scraping  
- `pillow` – Image processing  
- `jmespath` – JSON path expressions  

---

## 🎯 Usage

The tool uses a CLI with multiple subcommands:

```bash
python src/main.py [OPTIONS] COMMAND [ARGS]...
```

### 🔍 Available Commands

#### 📊 Analytics – Get follower analytics

```bash
python src/main.py analytics [--export]
```

- Shows follower/following counts, ratios, and mutual follows  
- `--export`: Save data to JSON  

---

#### 👤 User Info – Get profile information

```bash
python src/main.py user-info [--export]
```

- Displays username, bio, follower counts, verification status  
- Indicates if account is private  

---

#### 🖼️ Posts Analysis – Analyze recent posts

```bash
python src/main.py posts [--limit 10] [--export]
```

- Shows likes, comments, engagement for recent posts  
- `--limit`: Number of posts to analyze (default: 10)  

---

#### 🚫 Not Following Back

```bash
python src/main.py not-following-back [--limit 50] [--export] [--sort-by-followers]
```

- Lists users you follow who don't follow you back  
- `--sort-by-followers`: Sort by follower count (descending)  
- `--limit`: Max number of users to display  

---

#### 🔁 Track Unfollowers

```bash
python src/main.py track-unfollowers [--save-snapshot]
```

- Compares current followers with previous snapshot  
- `--save-snapshot`: Save current follower state  

---

#### 💤 Low Engagers – Find least engaging followers

```bash
python src/main.py low-engagers [--posts 10] [--top 10]
```

- Analyzes followers who least engage (likes/comments)  
- `--posts`: Number of recent posts to analyze  
- `--top`: Show bottom N engaging followers  

---

#### 📘 Full Report – Complete analytics report

```bash
python src/main.py full-report [--posts-limit 20] [--export]
```

- Generates a full report with all analytics  
- Includes user info, follower stats, post performance  

---

#### 🔍 Complete Follower Analysis

```bash
python src/main.py full-report-followers [--limit 20]
```

- Combines not-following-back and unfollower tracking  
- Offers a complete follower relationship overview  

---

## 🔐 Authentication

- Prompted at runtime for **username/password**  
- Provide username via:

```bash
python src/main.py analytics -u your_username
```

- Password will be entered securely (not shown on screen)  
- *Avoid providing credentials via command line for security*  

---

## 📊 Sample Output

### Follower Analytics

```
┌────────────── 📊 Follower Analytics ───────────────┐
│ Metric       │ Value                              │
├──────────────┼─────────────────────────────────────┤
│ 👥 Followers │ 1,234                               │
│ 👤 Following │ 567                                 │
│ 📷 Posts     │ 89                                  │
│ 📈 F/F Ratio │ 2.18                                │
│ 🤝 Mutual    │ 123                                 │
└──────────────┴─────────────────────────────────────┘
```

### Not Following Back

```
┌─────────────── Users Not Following You Back ───────────────┐
│ # │ Username      │ Full Name      │ Verified │ Followers │
├───┼───────────────┼────────────────┼──────────┼───────────┤
│ 1 │ @example_user │ Example User   │          │ 2,543     │
│ 2 │ @another_user │ Another Person │ ✓        │ 12,890    │
└───┴───────────────┴────────────────┴──────────┴───────────┘
```

---

## 📁 Data Storage

### Snapshot Files

- Format: `followers_snapshot_YYYYMMDD_HHMMSS.json`  
- Used to track historical follower/following changes  

### Export Files

- Format: `[report_type]_YYYYMMDD_HHMMSS.json`  
- Structured JSON files with timestamps and metadata  

---

## 🔧 Configuration

### Delay Settings

- Random delays (1–3 seconds) between requests  
- Prevents Instagram rate-limiting  
- Configurable in `InstaClient` class  

### Logging

- Rich terminal logs  
- Tracks login/logout, API issues, and errors  

---

## 🛡️ Security & Privacy

- **Credentials** are never stored permanently  
- **Rate limiting** safeguards built-in  
- **Session management** ensures clean logins/logouts  
- All data stored **locally**  

---

## ⚠️ Important Notes

- Use in accordance with **Instagram's Terms of Service**  
- Avoid frequent usage to prevent **rate limiting**  
- Private accounts and deleted users may **limit data**  
- **Instagram API changes** could break functionality  

---

## 📈 Use Cases

- 📌 Content Strategy  
- 📌 Follower Management  
- 📌 Growth Tracking  
- 📌 Engagement Analysis  
- 📌 Account Insights  

---

## 🤝 Contributing

Submit issues, feature requests, or pull requests to contribute!

---

## ⚖️ Disclaimer

> This tool is for **educational and personal use only**.  
> Users are responsible for complying with **Instagram's Terms** and **local laws**.  
> Developers are **not responsible** for any account restrictions resulting from usage.
