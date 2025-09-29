# !uv pip install sqlparse

from IPython.display import display, HTML, Markdown
import sqlparse

def display_sql(sql_string, title="SQL Query"):
    "Display SQL with beautiful formatting in Jupyter"
    # Format SQL with proper indentation
    formatted_sql = sqlparse.format(
        sql_string, 
        reindent=True, 
        keyword_case='upper',
        identifier_case='lower'
    )
    
    # Create markdown display
    markdown_content = f"""
### {title}
```sql
{formatted_sql}
```
"""
    display(Markdown(markdown_content))
    return formatted_sql
