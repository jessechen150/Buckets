from datetime import datetime

class Item:
    """
    Representing an item in a bucket list.
    """
    def __init__(self, title):
        self.title = title
        self.date_format = "%B %d %Y, %I:%M %p"
        self.last_modified = datetime.now().strftime(self.date_format)

        # Properties
        self.description = None

    def set_description(self, desc):
        if len(desc) > 1000:
            self.description = desc[:1000]
        else:
            self.description = desc
        self.last_modified = datetime.now().strftime(self.date_format)