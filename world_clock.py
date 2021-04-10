from datetime import datetime
from time import sleep

from pytz import timezone

from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.live import Live

from numstrings import get_matching_str, combine_number_str

import yaml
import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "clocks.yaml"
abs_file_path = os.path.join(script_dir, rel_path)

clocks = {}
with open(abs_file_path) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    clocks = yaml.load(file, Loader=yaml.FullLoader)


def get_time_string(
    zone='Europe/Paris', 
    render_secs = False,
    render_ms = False   ):
    
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


for clock_name, params in clocks.items():
    print(params) 



layout = Layout()
layout.split_row(
    Layout(name="paris",minimum_size=72), Layout(name="tokyo")#, Layout(name="london")
) 
with Live(layout, refresh_per_second=20, screen=True):
    try:
        while(True):
            paris = Panel(get_time_string(render_secs=True, render_ms=True), title="Paris, France", width=72, height=8)
            tokyo = Panel("[yellow]"+get_time_string('Asia/Tokyo')+"[/yellow]", title="Tokyo, Japan", width=37, height=8)
            #london = Panel(get_time_string('Europe/London'), title="London, United Kingdom", width=35, height=8)
            layout["paris"].update(paris)
            layout["tokyo"].update(tokyo)
            #layout["london"].update(london)
            sleep(0.05)
    except KeyboardInterrupt:
        pass
