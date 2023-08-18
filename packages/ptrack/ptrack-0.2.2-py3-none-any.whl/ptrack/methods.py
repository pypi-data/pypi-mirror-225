import os
import sys
import requests
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, FileSizeColumn, Task, DownloadColumn, TimeElapsedColumn
from rich.text import Text
from datetime import timedelta
from humanize import naturalsize

console = Console()


def getTotalSize(srcPaths):
    total_size = 0
    for path in srcPaths:
        if os.path.isfile(path):
            total_size += os.path.getsize(path)
        else:
            for r, d, files in os.walk(path):
                for f in files:
                    fp = os.path.join(r, f)
                    total_size += os.path.getsize(fp)
    return total_size


def format_file_size(file_size):
    if file_size >= 1000 ** 4:  # Terabyte
        return f"{round(file_size / (1000 ** 4))} TB"
    elif file_size >= 1000 ** 3:  # Gigabyte
        return f"{round(file_size / (1000 ** 3))} GB"
    elif file_size >= 1000 ** 2:  # Megabyte
        return f"{round(file_size / (1000 ** 2))} MB"
    elif file_size >= 1000:  # Kilobyte
        return f"{round(file_size / 1000)} kB"
    else:  # Byte
        return f"{file_size} bytes"


def regular_copy(src, dst, console, task, progress, file_name):
    operation_cancelled = False
    try:
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                buf = fsrc.read(1024*1024)
                if not buf or operation_cancelled:
                    break
                fdst.write(buf)
                progress.update(task, advance=len(buf))
                progress.refresh()

    except KeyboardInterrupt:
        operation_cancelled = True
        progress.stop()
        return "c"


def verbose_copy(src, dst, console, current, total_files, file_name):
    operation_cancelled = False
    file_size = os.path.getsize(src)

    with Progress(
        BarColumn(bar_width=50),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        "[#ea2a6f][[/#ea2a6f]",
        FileSizeColumn(),
        "[#ea2a6f]/[/#ea2a6f]",
        TextColumn(f"[bold cyan]{format_file_size(file_size)}[/bold cyan]"),
        "[#ea2a6f]][/#ea2a6f]",
        f"({current} of {total_files}) - {file_name}",
        console=console,
        auto_refresh=False
    ) as progress:
        task = progress.add_task("", total=file_size, file_size=format_file_size(file_size))

        try:
            with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                while not progress.finished:
                    buf = fsrc.read(1024*1024)
                    if not buf or operation_cancelled:
                        break
                    fdst.write(buf)
                    progress.update(task, advance=len(buf))
                    progress.refresh()
        except KeyboardInterrupt:
            operation_cancelled = True
            progress.stop()
            return "c"


def hlp():
    print("""
usage: ptrack [-h] [-v] [-c] [-m] [-d] [-V]

A simple CLI utility for asthetically tracking progress when copying or moving files.

options:
  -h, --help      show this help message and exit
  -v, --verbose   verbose output
  -c, --copy      copy files (You can use `ptc` instead of `ptrack -c`)
  -m, --move      move files (You can use `ptm` instead of `ptrack -m`)
  -d, --download  download files (You can use `ptd` instead of `ptrack -d`)
  -V, --version   show program's version number and exit
""")


class CustomFileSizeColumn(FileSizeColumn, TimeElapsedColumn):
    def render(self, task):
        completed = task.completed
        total = task.total
        elapsed = task.elapsed

        if elapsed > 0.0:  # Prevent division by zero
            download_speed = completed / elapsed  # calculate download rate
        else:
            download_speed = 0

        if total:
            size = Text.assemble(
                (f"{self._human_readable_size(completed)}", "green"),  # completed
                (" / ", "none"),  # separator
                (f"{self._human_readable_size(total)}", "red"),  # total
                (" [", "none"),  # opening square bracket
                (f"{self._human_readable_size(download_speed)}/s", "blue"),  # download rate
                ("]", "none"),  # closing square bracket
            )
        else:
            size = Text(str(self._human_readable_size(completed)))
        return size

    def _human_readable_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if abs(size) < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}PB"
