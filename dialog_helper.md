```
def hide_messages(search_term: str, summary: str = None):
    """Hides all messages matching the search term and adds a summary note"""
    msgs_to_hide = find_msgs(search_term)
    
    if not msgs_to_hide:
        return "No messages found matching that search term"
    
    # Skip each message
    for msg in msgs_to_hide:
        update_msg(msg['id'], skipped=1)
    
    # Create summary if not provided
    if summary is None:
        summary = f"# Summary: {len(msgs_to_hide)} messages about '{search_term}' hidden"
    
    # Add summary before the first message
    add_msg(content=summary, placement='add_before', msgid=msgs_to_hide[0]['id'])
    
    return f"Summarized and hid {len(msgs_to_hide)} messages"
```
