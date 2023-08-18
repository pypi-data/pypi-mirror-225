import os
import re
import sys
import ptrack
from ptrack.methods import format_file_size, regular_copy, verbose_copy, hlp, getTotalSize, CustomFileSizeColumn
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, FileSizeColumn
from rich.console import Console
from datetime import timedelta
import shutil
import requests
import validators

verbose = ptrack.verbose
argCopy = ptrack.copy
argMove = ptrack.move
argDownload = ptrack.download


def run(process):
    console = Console()

    if len(sys.argv) < 3:
        hlp()
        if process == "Copying":
            console.print("[bold cyan]Usage: ptc [OPTIONS] SOURCE... DESTINATION[/bold cyan]")
        elif process == "Moving":
            console.print("[bold cyan]Usage: ptm [OPTIONS] SOURCE... DESTINATION[/bold cyan]")
        sys.exit(1)

    src_paths = sys.argv[1:-1]
    dst = sys.argv[-1]
    srcPaths = []

    for path in src_paths:
        if path.endswith('/'):
            path = path[:-1]
        srcPaths.append(path)

    if os.path.isdir(dst):
        dst_dir = dst
        new_name = None
    else:
        dst_dir = os.path.dirname(dst)
        new_name = os.path.basename(dst)

    total_files = sum(len(files) for path in srcPaths for r, d, files in os.walk(path) if os.path.isdir(path)) + sum(1 for path in srcPaths if os.path.isfile(path))
    total_size = getTotalSize(srcPaths)

    current_file = 1

    if total_files > 1:
        console.print(f"\n[#ea2a6f]{process}:[/#ea2a6f] [bold cyan]{total_files} files[/bold cyan]\n")
    else:
        for src_path in srcPaths:
            if os.path.isfile(src_path):
                console.print(f"\n[#ea2a6f]{process}:[/#ea2a6f] [bold cyan] {os.path.basename(src_path)} [/bold cyan]\n")

    if verbose:
        for src_path in srcPaths:
            if os.path.isfile(src_path):
                dst_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name)
                terminate = verbose_copy(src_path, dst_path, console, current_file, total_files, file_name=os.path.basename(src_path))
                current_file += 1
                if terminate == 'c':
                    console.print("\n[bold red]\[-][/bold red][bold white] Operation cancelled by user.[/bold white]\n")
                    sys.exit(1)
            else:
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        src_file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(src_file_path, start=src_path)
                        dst_file_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name, relative_path)
                        os.makedirs(os.path.dirname(src_file_path), exist_ok=True)
                        terminate = verbose_copy(src_file_path, dst_file_path, console, current_file, total_files, file_name=file)
                        current_file += 1
                        if terminate == 'c':
                            console.print("\n[bold red]\[-][/bold red][bold white] Operation cancelled by user.[/bold white]\n")
                            sys.exit(1)
    else:
        with Progress(
            BarColumn(bar_width=50),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            "[#ea2a6f][[/#ea2a6f]",
            FileSizeColumn(),
            "[#ea2a6f]/[/#ea2a6f]",
            TextColumn("[bold cyan]{task.fields[total_size]}[/bold cyan]"),
            "[#ea2a6f]][/#ea2a6f]",
            console=console,
            auto_refresh=False
        ) as progress:
            task = progress.add_task("", total=total_size, total_size=format_file_size(total_size))

            for src_path in srcPaths:
                if os.path.isfile(src_path):
                    dst_file_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name)
                    terminate = regular_copy(src_path, dst_file_path, console, task, progress, file_name=os.path.basename(src_path))
                    if terminate == 'c':
                        console.print("\n[bold red]\[-][/bold red][bold white] Operation cancelled by user.[/bold white]\n")
                        sys.exit(1)
                else:
                    for root, dirs, files in os.walk(src_path):
                        for file in files:
                            src_file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(src_file_path, start=src_path)
                            dst_file_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name, relative_path)
                            os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
                            terminate = regular_copy(src_file_path, dst_file_path, console, task, progress, file_name=file)
                            if terminate == 'c':
                                console.print("\n[bold red]\[-][/bold red][bold white] Operation cancelled by user.[/bold white]\n")
                                sys.exit(1)

    return srcPaths


def download():
    console = Console()
    urls = sys.argv[1:]

    if len(urls) == 0:
        console.print("\n[bold red][-][/bold red] No URL provided.\n")
        sys.exit()

    num_urls = len(urls)
    for url in urls:
        if url.startswith('-'):
            num_urls -= 1
        elif not validators.url(url):
            console.print(f"\n[bold red][-][/bold red] Invalid URL: [bold yellow]{url}[/bold yellow]\n")
            sys.exit()

    console.print(f"\n[#ea2a6f]Downloading:[/#ea2a6f] [bold yellow]{num_urls}[/bold yellow] [bold cyan]files[/bold cyan]\n")

    errors = []
    for url in urls:
        try:
            if url.startswith('-'):
                continue

            response = requests.get(url, stream=True, allow_redirects=True)
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                destination_path = re.findall('filename="(.+)"', content_disposition)[0]
            else:
                destination_path = os.path.basename(url)

            with Progress(
                BarColumn(bar_width=50),
                "[progress.percentage]{task.percentage:>3.0f}%",
                TimeRemainingColumn(),
                "[#ea2a6f][[/#ea2a6f]",
                CustomFileSizeColumn(),
                "[#ea2a6f]][/#ea2a6f]",
                f" {destination_path}",  # This line will print the filename at the end
                console=console,
                auto_refresh=True
            ) as progress:
                task_id = progress.add_task("Downloading", total=total_size_in_bytes)
                block_size = 1024  # 1 Kibibyte
                with open(destination_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        file.write(data)
                        progress.update(task_id, advance=block_size)
        except KeyboardInterrupt:
            console.print("\n[bold red]\[-][/bold red][bold white] Operation cancelled by user.[/bold white]\n")
            sys.exit(1)

        except Exception as e:
            console.print(f"\n[bold red]\[-][/bold red][bold white] Could not download file: [bold yellow]{url}[/bold yellow]\n")
            print(e)
            errors.append(url)

    if len(errors) == 0:
        console.print("\n[bold green]Download completed![/bold green]\n")
    else:
        console.print("[bold red]The following files could not be downloaded:[/bold red]\n")
        for error in errors:
            console.print(f"[bold red]   -[/bold red][bold yellow]{error}[/bold yellow]\n")


def copy():
    run('Copying')


def move():
    src_paths = run('Moving')
    for src_path in src_paths:
        if os.path.isfile(src_path):
            os.remove(src_path)
        else:
            shutil.rmtree(src_path)


def main():
    if argMove:
        move()
    elif argCopy:
        copy()
    elif argDownload:
        download()
    else:
        hlp()


if __name__ == "__main__":
    main()
