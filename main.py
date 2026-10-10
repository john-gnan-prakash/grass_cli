import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from grass_cli.llm import generate_trail_plan
from grass_cli.exporters import export_markdown, export_gpx

app = typer.Typer(help="Grass-CLI: Offline Trail & Adventure Planner")
console = Console()

@app.command()
def plan(
    query: str = typer.Argument(..., help="Query describing your ideal hike/activity"),
    output_dir: str = typer.Option("./output", "--out", "-o", help="Directory to save generated files")
):
    """
    Plan an outdoor activity completely offline using Qwen2.5-Coder.
    """
    console.print(Panel.fit("[bold green]🌲 GRASS-CLI: OFFLINE TRAIL PLANNER[/bold green]", border_style="green"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Inferencing local model via Ollama (qwen2.5-coder)...", total=None)
        try:
            data = generate_trail_plan(query)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1)

    # Render Header Summary
    console.print(f"\n[bold underline]{data.get('trail_name')}[/bold underline]")
    console.print(f"[italic]{data.get('summary')}[/italic]\n")

    # Render Stats Table
    stats_table = Table(show_header=True, header_style="bold cyan")
    stats_table.add_column("Distance")
    stats_table.add_column("Difficulty")
    stats_table.add_column("Est. Duration")
    stats_table.add_column("Elevation Gain")
    
    stats_table.add_row(
        f"{data.get('distance_km')} km",
        f"{data.get('difficulty')}",
        f"{data.get('estimated_duration_mins')} mins",
        f"+{data.get('elevation_gain_m')}m"
    )
    console.print(stats_table)

    # Render Waypoints
    console.print("\n[bold yellow]📍 Waypoint Itinerary[/bold yellow]")
    for wp in data.get("waypoints", []):
        wp_type = wp.get("type", "step").upper()
        console.print(f"  [bold green]{wp.get('step')}. [{wp_type}][/bold green] [bold]{wp.get('name')}[/bold]")
        console.print(f"     {wp.get('description')}")

    # Render Packing List
    console.print("\n[bold yellow]🎒 Recommended Packing List[/bold yellow]")
    for item in data.get("packing_list", []):
        console.print(f"  [ ] {item}")

    # Export Files
    slug = data.get("trail_name", "trail").lower().replace(" ", "_")
    md_path = f"{output_dir}/{slug}.md"
    gpx_path = f"{output_dir}/{slug}.gpx"

    export_markdown(data, md_path)
    export_gpx(data, gpx_path)

    console.print(Panel(
        f"[bold green]Files successfully exported for offline use:[/bold green]\n"
        f"📄 Markdown: [cyan]{md_path}[/cyan]\n"
        f"🗺️ GPX Track: [cyan]{gpx_path}[/cyan]",
        title="Offline Sync Complete",
        border_style="blue"
    ))

if __name__ == "__main__":
    app()