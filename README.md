# RFFL Codex ESPN

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/thorsenk/rffl-codex-espn/ci.yml?branch=main)](https://github.com/thorsenk/rffl-codex-espn/actions)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive data extraction and analysis tool for using ESPN's Fantasy Football API. This project provides tools for historical data collection, analysis, and insights generation.

## Table of Contents
- [RFFL Codex ESPN](#rffl-codex-espn)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Quick Start](#quick-start)
    - [Clone the Repository](#clone-the-repository)
    - [Set Up Environment](#set-up-environment)
    - [Configure ESPN Credentials](#configure-espn-credentials)
    - [Run Data Collection](#run-data-collection)
  - [Project Structure](#project-structure)
  - [Configuration](#configuration)
    - [ESPN Authentication](#espn-authentication)
    - [League Configuration](#league-configuration)
  - [Data Storage](#data-storage)
  - [Usage Examples](#usage-examples)
    - [Basic Data Collection](#basic-data-collection)
    - [Advanced Analysis](#advanced-analysis)
  - [Development](#development)
    - [Setting Up Development Environment](#setting-up-development-environment)
    - [Contributing](#contributing)
  - [Testing](#testing)
  - [Error Handling](#error-handling)
  - [Performance Considerations](#performance-considerations)
  - [FAQ](#faq)
  - [Roadmap](#roadmap)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  - [Contact](#contact)

## Overview

RFFL Codex ESPN is designed to:
- Extract and store historical fantasy football data from ESPN
- Track league performance metrics over time
- Generate insights about team and player performance
- Support data-driven decision making for fantasy football

## Prerequisites

Before you begin, ensure you have met the following requirements:
- **Operating System:** Windows, macOS, or Linux
- **Python Version:** 3.8 or higher
- **Git:** Installed and configured
- **ESPN Account:** Access to ESPN Fantasy Football with necessary credentials
- **Storage:** Sufficient disk space for historical data storage

## Quick Start

### Clone the Repository
```bash
git clone https://github.com/thorsenk/rffl-codex-espn.git
cd rffl-codex-espn
```

### Set Up Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure ESPN Credentials

1. **Copy Example Credentials File**
```bash
cp set_credentials.sh.example set_credentials.sh
```

2. **Edit `set_credentials.sh`**
Open `set_credentials.sh` in your preferred text editor and add your ESPN credentials:
```bash
export SWID="your-swid-token"  # Example: {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
export ESPN_S2="your-espn-s2-token"
```

3. **Load Credentials**
```bash
source set_credentials.sh
```

### Run Data Collection
```bash
python src/espn_fantasy.py
```

## Project Structure

```
rffl-codex-espn/
├── data/                    # Data storage directory
│   └── seasons/            # Season-specific data
│       └── YYYY/           # Year-specific directories
│           ├── rosters/    # Team roster data
│           ├── matchups/   # Weekly matchup data
│           ├── standings/  # League standings
│           └── raw/        # Raw API responses
├── src/
│   ├── config/            # Configuration settings
│   ├── utils/             # Utility functions
│   ├── models/            # Data models
│   └── espn_fantasy.py    # Main script
├── tests/                 # Test files
├── docs/                  # Documentation
└── examples/              # Example scripts
```

## Configuration

### ESPN Authentication
To access your league's data, you need two authentication tokens from ESPN:

1. **Find Your Credentials:**
   - Log into ESPN Fantasy Football
   - Open browser developer tools (F12)
   - Go to Application/Storage > Cookies
   - Find and copy:
     - `SWID` token
     - `ESPN_S2` token

2. **Configure Credentials:**
   - Add tokens to `set_credentials.sh`
   - Keep these tokens secure and never commit them

### League Configuration
Update `src/config/settings.py` with your league details:
```python
LEAGUE_ID = YOUR_LEAGUE_ID  # Found in your league's URL
SEASON_YEAR = CURRENT_SEASON
```

## Data Storage

Data is organized by season and type:
- `rosters/`: Weekly team rosters
- `matchups/`: Weekly matchup results
- `standings/`: League standings
- `transactions/`: Trades and other transactions
- `raw/`: Raw API responses

Each file is timestamped for historical tracking.

## Usage Examples

### Basic Data Collection
```python
from utils.data_storage import store_season_data, load_season_data

# Store current roster data for week 1 of 2024
store_season_data(roster_data, year=2024, data_type="rosters", filename="week1")

# Load most recent standings as a pandas DataFrame
standings = load_season_data(2024, "standings", "week1", as_dataframe=True)
print(standings.head())
```

### Advanced Analysis
```python
from utils.analysis import analyze_team_performance, calculate_playoff_odds

# Analyze team performance
performance = analyze_team_performance(team_name="Gypsy PCX", year=2024)
print(performance.summary())

# Calculate playoff odds
odds = calculate_playoff_odds(team_name="Gypsy PCX", week=10)
print(f"Playoff Probability: {odds.probability:.2%}")
```

## Development

### Setting Up Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Code Style
- Pull Request Process
- Development Workflow
- Testing Requirements

## Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_data_storage.py
```

## Error Handling

The system includes robust error handling for:
- API connection issues
- Rate limiting
- Data validation
- Authentication errors

Errors are logged to `data/logs/` with timestamps and context.

## Performance Considerations

- Implements caching to reduce API calls
- Respects ESPN's rate limits
- Batches requests when possible
- Stores raw responses for reprocessing

## FAQ

**Q:** How do I update my ESPN credentials?  
**A:** Edit `set_credentials.sh` with new tokens and run `source set_credentials.sh`

**Q:** How often is data collected?  
**A:** By default, data is collected daily during the season

**Q:** Can I analyze historical seasons?  
**A:** Yes, specify the season year in your API calls

## Roadmap

- [ ] Real-time data syncing
- [ ] Web dashboard for visual analytics
- [ ] Machine learning for player performance prediction
- [ ] Multi-league support
- [ ] Advanced statistical analysis tools

## License

This project is licensed under the [MIT License](LICENSE). You are free to:
- Use the code commercially
- Modify the code
- Distribute the code
- Use the code privately

## Acknowledgments

- [ESPN Fantasy Football API](https://www.espn.com/fantasy/football/)
- [Pandas](https://pandas.pydata.org/) for data analysis
- [Requests](https://docs.python-requests.org/) for API integration
- RFFL League Members for testing and feedback
- All contributors who have helped improve this project

## Contact

- **Project Maintainer:** Kyle Thorsen
- **GitHub Issues:** [Report a Bug](https://github.com/thorsenk/rffl-codex-espn/issues)
- **Email:** [147131161+thorsenk@users.noreply.github.com](mailto:147131161+thorsenk@users.noreply.github.com)
