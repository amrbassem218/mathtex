# LaTeX Contest to HTML Converter

A command-line tool that converts LaTeX contest files into structured JSON format with HTML problem descriptions. The tool extracts problems from LaTeX files, converts them to HTML using Pandoc, and optionally pushes them to a database.

## Features

- Extract problems from LaTeX contest files
- Convert LaTeX problem descriptions to HTML with MathJax support
- Export problems to JSON format
- Optional database integration for pushing problems to an API
- Support for multiple problem extraction from structured LaTeX files

## Prerequisites

Before installing this tool, ensure you have the following:

1. **Python 3.8+** - Check your version:
   ```bash
   python3 --version
   ```

2. **Pandoc** - Required for LaTeX to HTML conversion
   - **Linux**: 
     ```bash
     sudo apt-get install pandoc  # Debian/Ubuntu
     # or
     sudo yum install pandoc      # RHEL/CentOS
     ```
   - **macOS**: 
     ```bash
     brew install pandoc
     ```
   - **Windows**: Download from [pandoc.org/installing.html](https://pandoc.org/installing.html)
   
   Verify installation:
   ```bash
   pandoc --version
   ```

3. **pip** - Python package manager (usually comes with Python)

## Installation

1. **Clone or download this repository**:
   ```bash
   cd /path/to/mathtex
   ```

2. **Install Python dependencies**:
   ```bash
   pip install requests supabase python-dotenv
   ```
   
   Or if you prefer using a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install requests supabase python-dotenv
   ```

## Configuration

### Environment Variables

If you plan to use the `--push` option to send problems to a database, create a `.env` file in the project root:

```bash
# .env file
API_KEY=your_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
```

The tool will automatically load these variables using `python-dotenv`.

## Usage

### Basic Syntax

```bash
python main.py <input.tex> <source> [options]
```

### Required Arguments

- `input`: Path to the LaTeX contest file (`.tex` format)
- `source`: Source type of the LaTeX file (currently supports: `pandoc`)

### Optional Arguments

- `-o, --output`: Set the output file or directory path (default: `<input_name>.json`)
- `-t, --type`: Problem extraction type - `single` or `multiple` (default: `multiple`)
- `-r, --replace`: Replace existing output file/directory if present
- `-p, --push`: Push the extracted problems to the database via API

### Examples

#### Basic Conversion

Convert a LaTeX file to JSON:

```bash
python main.py pandoc_files/2022.tex pandoc
```

This will create `2022.json` in the current directory with all extracted problems.

#### Specify Output Location

```bash
python main.py pandoc_files/2022.tex pandoc -o output/2022.json
```

#### Output to Directory

If you specify a directory (without file extension), the tool will create the JSON file inside that directory:

```bash
python main.py pandoc_files/2022.tex pandoc -o output/
```

This creates `output/2022.json`.

#### Replace Existing Output

```bash
python main.py pandoc_files/2022.tex pandoc -o output/2022.json --replace
```

#### Push to Database

After extracting problems, push them to the database:

```bash
python main.py pandoc_files/2022.tex pandoc --push
```

This will:
1. Extract problems from the LaTeX file
2. Create a contest in the database
3. Push each problem to the database via API

**Note**: Ensure your `.env` file is configured with the `API_KEY` before using `--push`.

## Output Format

The tool generates a JSON file containing an array of problem objects. Each problem has the following structure:

```json
[
  {
    "name": "A1",
    "description_latex": "LaTeX content of the problem...",
    "description_html": "<p>HTML content with MathJax...</p>"
  },
  {
    "name": "A2",
    "description_latex": "...",
    "description_html": "..."
  }
]
```

## LaTeX File Format

The tool expects LaTeX files with problems formatted using `\item[Label]` syntax within an `itemize` environment:

```latex
\begin{itemize}
\item[A1]
Problem description here...

\item[A2]
Another problem description...
\end{itemize}
```

## Troubleshooting

### Pandoc Not Found

If you get an error that pandoc is not found:
- Ensure pandoc is installed and available in your PATH
- Verify with: `pandoc --version`

### File Not Found

If you get "File doesn't exist" error:
- Check that the input file path is correct
- Use absolute paths if relative paths don't work

### Empty Output

If no problems are extracted:
- Verify your LaTeX file uses the `\item[Label]` format
- Check that problems are within an `itemize` environment
- Ensure the file is not empty

### Database Push Errors

If `--push` fails:
- Verify your `.env` file exists and contains correct values
- Check that the API endpoint is accessible
- Ensure `API_KEY` is set correctly

## Project Structure

```
mathtex/
├── main.py              # Main CLI entry point
├── pandoc.py            # LaTeX problem extraction logic
├── config/
│   └── settings.py      # Configuration settings
├── db/
│   └── client.py        # Database client setup
├── utils/
│   └── database_action.py  # Database operations
└── pandoc_files/        # Example LaTeX files
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines if applicable]
