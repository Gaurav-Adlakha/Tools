from dialoghelper import *
import fasthtml.common as ft
from IPython.display import Markdown
from  monsterui.all import *
from fastcore.all import *
from fasthtml.jupyter import render_ft
import contextkit.read as rd
from typing import List, Dict, Any, Union

import json
render_ft()

_flag_counter = 0

def add_flag(name="🚩", use_counter=False):
    "Add a flag marker to the dialog with optional global counter"
    global _flag_counter
    if use_counter: _flag_counter += 1; content = f"# heading{_flag_counter} {name}"
    else: content = name
    add_msg(content=content, msg_type="note")

def get_msgs_between_flags(flag="🏁"):
    "Get all message IDs between two instances of a flag"
    flag_msgs = find_msgs(re_pattern=f"^{re.escape(flag)}$")
    if len(flag_msgs) < 2: return []
    start_idx, end_idx = msg_idx(flag_msgs[0]['id']), msg_idx(flag_msgs[1]['id'])
    return [read_msg(n=i, relative=False)['id'] for i in range(start_idx + 1, end_idx)]

def get_flag_ids(flag="🚩"):
    "Get message IDs for all flag messages"
    flag_msgs = find_msgs(re_pattern=f"^(# heading\\d+ )?{re.escape(flag)}$")
    return [msg['id'] for msg in flag_msgs]

def delete_flags(flag="🚩"):
    "Delete all flag messages"
    flag_ids = get_flag_ids(flag)
    for msg_id in flag_ids: del_msg(msg_id)
    return f"Deleted {len(flag_ids)} flags"

from typing import List, Dict, Any, Union
import contextkit.read as rd
def get_markdown_contexts(urls: Union[str, List[str]]) -> Dict[str, Any]:
    """Get markdown content from one or more URLs. Returns tuple for unpacking."""
    if len(urls) == 1: return rd.read_url(urls[0])
    return tuple(rd.read_url(url) for url in urls)
