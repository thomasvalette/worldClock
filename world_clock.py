import os
from datetime import datetime
from time import sleep

from pytz import timezone
import yaml
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
from rich.style import Style
from rich.align import Align

from numstrings import get_matching_str, combine_number_str

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "clocks.yaml"
abs_file_path = os.path.join(script_dir, rel_path)

clocks = {}
with open(abs_file_path) as file:
    clocks = yaml.load(file, Loader=yaml.FullLoader)


def get_time_string(
    zone='Europe/Paris', 
    render_secs = False,
    render_ms = False,
    color="white"):
    
    now = datetime.now(timezone(zone))

    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    microsec = str(now.microsecond)

    hour = hour.zfill(2)
    minute = minute.zfill(2)
    second = second.zfill(2)
    microsec = microsec.zfill(6)

    to_render = "{}{}:{}{}".format(
        hour[0],
        hour[1],
        minute[0],
        minute[1])

    if render_secs:
        to_render += ":{}{}".format(
            second[0],
            second[1])

    if render_ms:
        to_render += ":{}".format(
            microsec[0])

    return "\n" + combine_number_str(to_render)


sub_layouts = []
sub_params = {}
high_refresh_rate = False # is enabled if milliseconds are displayed
for clock_name, params in clocks.items():
    minimum_size=37
    if params['seconds']:
        minimum_size += 21   #58
    if params['milliseconds']:
        minimum_size += 16   #72
        high_refresh_rate = True

    sub_layouts.append(Layout(name=clock_name,minimum_size=minimum_size))
    sub_params.update({clock_name : params})

console = Console()
layout = Layout()

def create_layout():
    # determining the total number of rows
    total_width = 0
    row_layouts = []
    row_layout = []
    for sub_layout in sub_layouts:
        if total_width + sub_layout.minimum_size >= console.size[0]:
            row_layouts.append(row_layout)
            row_layout = [sub_layout]
            total_width = 0
        else:
            row_layout.append(sub_layout)
            total_width += sub_layout.minimum_size
    row_layouts.append(row_layout)

    to_split_col = []
    for row in row_layouts:
        tmp_layout = Layout()
        tmp_layout.split_row(*row)
        to_split_col.append(tmp_layout)

    layout.split_column(
        *to_split_col
    )


def get_panel(title, width, zone, render_secs, render_ms, color):
    return Panel(
        Align.center(
            get_time_string(zone=zone, render_secs=render_secs, render_ms=render_ms, color=color),
            #vertical="middle",
        ),
        title=title,
        #width=width,
        height=8,
        highlight=True,
        style=Style(color=color))


if high_refresh_rate:
    refresh_rate = 40
else:
    refresh_rate = 2
sleep_time = 1/refresh_rate

screen_size = 0
with Live(layout, refresh_per_second=refresh_rate, screen=True):
    try:
        while(True):
            # detect screen resizing
            if screen_size != console.size[0]:
                screen_size = console.size[0]
                create_layout()
            for sub_layout in sub_layouts:
                params = sub_params[sub_layout.name]
                layout[sub_layout.name].update(
                    get_panel(
                        "[b]"+params["title"]+"[/b]",
                        sub_layout.minimum_size,
                        params["timezone"],
                        params["seconds"],
                        params["milliseconds"],
                        params["color"]
                    )
                )
            sleep(sleep_time)
    except KeyboardInterrupt:
        pass
