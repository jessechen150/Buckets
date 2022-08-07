from src.item import Item

i = Item("Hello")

print(i.title)
print(i.description)
print(i.last_modified)

i.set_description("This is my description")
print(i.description)