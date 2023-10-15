page_error =  """
[red]● Frontend Error ({type})[/]

Error:    {name}
Message:  {mesg}
Cause:    {caus}
"""

class PageError(Exception):
    """Represents a page (frontend) error."""
    def __init__(self, d: dict):
        super().__init__(
           page_error.format(**d)
        )
