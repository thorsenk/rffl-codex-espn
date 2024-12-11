# ESPN Fantasy Football Data Extractor

This project provides tools to extract and analyze data from ESPN Fantasy Football leagues.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your ESPN credentials:
- SWID
- ESPN_S2

## Usage

Basic usage:
```python
python src/espn_fantasy.py
```

## Features

- League Information Retrieval
- Team Rosters
- Matchup History
- Weekly Scores
- Player Statistics

## Project Structure

```
espn_fantasy_football/
├── src/
│   └── espn_fantasy.py      # Main script
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Development

To create a new feature branch:
```bash
git checkout -b feature/your-feature-name
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Create a pull request

## Version History

- v1.0.0 - Initial release with basic functionality
  - League data extraction
  - Team rosters
  - Matchup history 