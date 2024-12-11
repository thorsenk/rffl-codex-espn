# RFFL Codex ESPN

A specialized ESPN Fantasy Football data extraction and analysis tool for the RFFL (Redneck Fantasy Football League). This project provides comprehensive tools to extract and analyze league data, team rosters, matchup history, and detailed statistics.

## Features

- **League Information**
  - Team standings
  - Weekly matchups
  - League settings
  - Scoring rules

- **Team Data**
  - Complete rosters
  - Player statistics
  - Team performance metrics
  - Owner information

- **Matchup Analysis**
  - Head-to-head records
  - Weekly scoring
  - Historical matchup data
  - Playoff scenarios

## Project Structure

```
rffl-codex-espn/
├── src/
│   ├── config/
│   │   └── settings.py         # Configuration settings
│   ├── utils/
│   │   └── espn_api.py        # API utility functions
│   ├── models/                 # Data models
│   └── espn_fantasy.py        # Main script
├── tests/                      # Test files
├── docs/                       # Documentation
├── examples/                   # Example scripts
├── requirements.txt           # Project dependencies
└── README.md                 # This file
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rffl-codex-espn.git
cd rffl-codex-espn
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your ESPN credentials:
   - SWID: Your ESPN SWID token
   - ESPN_S2: Your ESPN S2 token

   You can find these values in your browser cookies when logged into ESPN Fantasy Football.

## Usage

### Basic Usage

```python
python src/espn_fantasy.py
```

### Advanced Usage

```python
from src.utils.espn_api import get_league_data, get_team_name_map

# Get league data
league_data = get_league_data(league_id=323196, season=2024)

# Get team information
team_map = get_team_name_map(league_data)
```

## Development

### Creating Feature Branches

For new features or experiments:

```bash
# Create a new feature branch
git checkout -b feature/enhanced-scoring

# Make your changes
# Test your changes
# Commit your changes
git add .
git commit -m "Added enhanced scoring features"

# Push to GitHub
git push origin feature/enhanced-scoring
```

### Example Feature Branches

1. `feature/enhanced-scoring`
   - Detailed scoring breakdowns
   - Historical scoring trends
   - Position-specific scoring analysis

2. `feature/playoff-analysis`
   - Playoff scenarios calculator
   - Strength of schedule analysis
   - Playoff odds calculator

3. `feature/data-export`
   - CSV export functionality
   - Excel report generation
   - Custom data formatting

4. `feature/historical-data`
   - Multi-season data analysis
   - Historical team performance
   - Dynasty league tools

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Version History

- v1.0.0 - Initial release
  - Basic league data extraction
  - Team roster information
  - Matchup history
  - Weekly scoring data

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ESPN Fantasy Football API
- RFFL League Members
- Fantasy Football community
- Contributors and testers