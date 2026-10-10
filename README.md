# Grass CLI

Grass CLI is a local-first trail planning utility that turns a natural-language hiking prompt into a structured outdoor itinerary. It uses Ollama running on your machine to generate a trail plan and then exports the result as both Markdown and GPX so the trip can be saved and used offline.

## What it does

The app accepts a prompt such as:

- "Create an easy 5 km forest loop with a creek crossing"
- "Plan a moderate weekend hike with scenic overlooks"
- "Generate a family-friendly trail with water and rest stops"

It then produces a trail object with:

- trail name and summary
- difficulty rating
- estimated duration
- distance and elevation gain
- waypoint list with coordinates
- packing checklist

The generated data is exported to:

- Markdown summary for reading and sharing
- GPX track for navigation apps or offline device use

## Project structure

- `main.py` - CLI entry point
- `grass_cli/llm.py` - calls the local Ollama model and parses the JSON output
- `grass_cli/exporters.py` - writes Markdown and GPX files
- `output/` - sample generated trail exports

## Requirements

Before running the app, make sure you have:

- Python 3.13+
- Ollama installed and running locally
- The model pulled locally:

```bash
ollama pull qwen2.5-coder:14b
```

The app expects Ollama to be available at:

```text
http://localhost:11434
```

## Installation

From the project root:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Usage

Run the CLI with a prompt:

```bash
python main.py plan "Easy 5 km loop through a forest with a creek crossing" --out ./output
```

Or with PowerShell:

```powershell
py .\main.py plan "Easy 5 km loop through a forest with a creek crossing" --out .\output
```

The command will:

1. send the request to Ollama
2. parse the JSON trail plan
3. print a rich summary to the terminal
4. save files to the output directory

## Example output

The repository includes sample generated files in the `output/` directory, such as:

- `output/forest_loop_by_the_creek.md`
- `output/forest_loop_by_the_creek.gpx`

These are example trail plans generated from a prompt and can be used as a reference for the expected format.

## Notes

- The project is designed for fully local inference, so no cloud API key is required.
- The model must return valid JSON for the itinerary schema.
- Output is saved under the chosen directory and can be opened in a browser, text editor, or hiking app.

## License

This project does not currently include a license file. Add one if you plan to distribute or publish the project.
