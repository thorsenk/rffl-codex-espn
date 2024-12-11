# RFFL Codex ESPN

A comprehensive data extraction and analysis tool for the Redneck Fantasy Football League (RFFL) using ESPN's Fantasy Football API. This project provides tools for historical data collection, analysis, and insights generation.

## Overview

RFFL Codex ESPN is designed to:
- Extract and store historical fantasy football data from ESPN
- Track league performance metrics over time
- Generate insights about team and player performance
- Support data-driven decision making for fantasy football

## Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/thorsenk/rffl-codex-espn.git
cd rffl-codex-espn
```

2. **Set Up Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure ESPN Credentials**
```bash
cp set_credentials.sh.example set_credentials.sh
# Edit set_credentials.sh with your ESPN SWID and ESPN_S2 tokens
source set_credentials.sh
```

4. **Run Data Collection**
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
1. `SWID`: Your ESPN SWID token
2. `ESPN_S2`: Your ESPN S2 token

To find these:
1. Log into ESPN Fantasy Football
2. Open browser developer tools (F12)
3. Go to Application/Storage > Cookies
4. Find and copy the SWID and ESPN_S2 values
5. Add them to your `set_credentials.sh` file

### League Configuration
Update `src/config/settings.py` with your league details:
```python
LEAGUE_ID = YOUR_LEAGUE_ID
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

# Store current roster data
store_season_data(roster_data, year=2024, data_type="rosters", filename="week1")

# Load most recent standings
standings = load_season_data(2024, "standings", "week1", as_dataframe=True)
```

### List Available Data
```python
from utils.data_storage import list_season_data

# List all data for 2024
files = list_season_data(2024)

# List only roster data
roster_files = list_season_data(2024, "rosters")
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
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Testing

Run tests with:
```bash
python -m pytest tests/
```

## Error Handling

The system includes robust error handling for:
- API connection issues
- Rate limiting
- Data validation
- Authentication errors

Errors are logged and can be found in `data/logs/`.

## Performance Considerations

- Implements caching to reduce API calls
- Respects ESPN's rate limits
- Batches requests when possible
- Stores raw responses for reprocessing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- ESPN Fantasy Football API
- RFFL League Members
- Fantasy Football community
- Contributors and testers