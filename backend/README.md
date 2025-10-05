# Gakumas Share Backend

FastAPI backend for the Gakumas memory set sharing platform.

## Features

- FastAPI with async/await support
- MongoDB with Motor (async driver)
- Pydantic models with validation
- Discord OAuth2 + SuperTokens session management
- Automated game data pipeline
- Comprehensive test suite

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern, fast web framework
- **MongoDB** - Document database
- **uv** - Ultra-fast Python package manager
- **Pydantic** - Data validation and settings
- **Motor** - Async MongoDB driver
- **SuperTokens** - Session management
- **Authlib** - OAuth2 client
- **pytest** - Testing framework

## Setup

### Prerequisites

- Python 3.11+
- uv package manager
- MongoDB instance

### Installation

```bash
cd backend

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Download and generate game data
uv run python scripts/update_data.py
```

### Environment Variables

```bash
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=gakumas_share

# Discord OAuth2
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret

# SuperTokens
SUPERTOKENS_CONNECTION_URI=your_supertokens_uri
SUPERTOKENS_API_KEY=your_api_key
```

## Data Pipeline

The backend includes an automated data pipeline that downloads and processes game data from the community-maintained Google Sheets.

### Data Sources

- **Game Data**: https://docs.google.com/spreadsheets/d/19E3wGFhnmcK9jdP8dTIFo0_XUx1jCqYGvzzGAXQqaq4/
- **Structure**: Based on [gakumas-tools](https://github.com/surisuririsu/gakumas-tools)
- **License**: BSD 3-Clause (see ATTRIBUTION.md)

### Pipeline Commands

```bash
# Update all game data (download CSV + convert to JSON)
uv run python scripts/update_data.py

# Download CSV files only
uv run python scripts/download_csv.py

# Convert CSV to JSON only
uv run python scripts/csv_to_json.py

# Discover sheet GIDs (for debugging)
uv run python scripts/discover_sheet_gids.py
```

### Data Structure

```
backend/data/
├── csv/          # Downloaded CSV files (generated, not in repo)
│   ├── idols.csv
│   ├── p_idols.csv
│   ├── p_items.csv
│   ├── skill_cards.csv
│   ├── stages.csv
│   └── customizations.csv
└── json/         # Generated JSON files (generated, not in repo)
    ├── idols.json
    ├── p_idols.json
    ├── p_items.json
    ├── skill_cards.json
    ├── stages.json
    └── customizations.json
```

## Project Structure

```
backend/
├── app/
│   ├── models/          # Pydantic models
│   │   ├── user.py      # User models
│   │   └── memory.py    # Memory set models
│   ├── routers/         # API routes
│   ├── tests/           # Test suite
│   ├── constants.py     # Game data constants
│   ├── config.py        # App configuration
│   └── main.py          # FastAPI app
├── scripts/             # Data pipeline scripts
├── data/               # Game data files
└── pyproject.toml      # Dependencies & config
```

## Development

### Running the Server

```bash
# Development server with hot reload
uv run uvicorn app.main:app --reload

# Production server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest app/tests/test_memory_models.py -v
```

### Code Quality

```bash
# Format code
uv run ruff format app/

# Lint code
uv run ruff check app/

# Type checking (if using mypy)
uv run mypy app/
```

## API Documentation

Once the server is running, visit:

- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Game Data Models

### Memory Set Structure

```python
MemorySetCreate(
    title="編成名",
    stage_type="contest",         # contest | event
    stage_plan="sense",          # free | sense | logic | anomaly
    p_idol_id=1,                 # P-Idol ID from data
    clear_rank="S+",             # A+ | S | S+
    p_items=[],                  # Array of P-Items (can be empty)
    skill_cards=[SkillCard(...)], # Array of skill cards (min 1)
    notes="メモ"
)
```

### Validation Rules

- ✅ `p_items` can be empty array
- ✅ `skill_cards` requires at least 1 item
- ✅ `enhancement_level` must be 1-10
- ✅ All IDs validated against game data

## Contributing

1. Ensure tests pass: `uv run pytest`
2. Format code: `uv run ruff format app/`
3. Update data if needed: `uv run python scripts/update_data.py`

## License

BSD 3-Clause License - see [LICENSE](../LICENSE) and [ATTRIBUTION.md](../ATTRIBUTION.md)

Game data and images courtesy of [gakumas-tools](https://github.com/surisuririsu/gakumas-tools) project.