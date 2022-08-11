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
        self.status = 0
        self.description = None

    def set_title(self, title):
        if len(title) > 100:
            self.title = title[:100]
        else:
            self.title = title
        self.last_modified = datetime.now().strftime(self.date_format)

    def set_description(self, desc):
        if len(desc) > 1000:
            self.description = desc[:1000]
        else:
            self.description = desc
        self.last_modified = datetime.now().strftime(self.date_format)

    def set_status(self, status):
        if status in range(3):
            # 0 = Not Started
            # 1 = In Progress
            # 2 = Completed
            self.status = status
        else:
            raise ValueError("Please input a status between 0 and 2.")


class BucketList:
    """
    Representing a bucket list.
    """
    def __init__(self, title):
        self.title = title
        self.date_format = "%B %d %Y, %I:%M %p"
        self.last_modified = datetime.now().strftime(self.date_format)
        self.items = []

    def add_item(self, title):
        item = Item(title)
        self.items.append(item)
        return item

    def remove_index(self, index):
        self.items.pop(index)

    def __len__(self):
        return len(self.items)