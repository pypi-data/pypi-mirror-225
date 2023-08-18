import json
import difflib
from rich.prompt import Confirm

def format_tables(source, console, tables_before, tables_after): # source should become a table field eventually, and version should be recieved from a dataset query
    formatted_tables_before = {table.name: {"source": source , "columns": [{column.name: column.graphqlType.upper()} for column in table.columns]} for table in tables_before}
    formatted_tables_after = {table.name: {"source": source , "columns": [{column.name: column.type} for column in table.columns if column.color != "bright_red"]} for table in tables_after}
    json1_obj = json.dumps(formatted_tables_before, sort_keys=True, indent=2).splitlines()
    json2_obj = json.dumps(formatted_tables_after, sort_keys=True, indent=2).splitlines()
    return json1_obj, json2_obj

def generate_diff(console, source, version, dataset_before, dataset_after):
    json1_obj, json2_obj = format_tables(source, console, dataset_before, dataset_after)

    if json1_obj == json2_obj:
        console.print("[red]Error: pat dataset update was run, but no differences in the schema were detected.[/red]")
        return None

    diff_generator = difflib.ndiff(json1_obj, json2_obj)

    for line in diff_generator:
        if line.startswith('+'):
            console.print(f"[green]{line}[/green]")  # Green for additions
        elif line.startswith('-'):
            console.print(f"[red]{line}[/red]")  # Red for deletions
        else:
            console.print(f"[white]{line}[/white]")
    confirmation = Confirm.ask(f"Update dataset to version [blue]{(version + 1)}[/blue]?",
                               console=console)
    return confirmation
