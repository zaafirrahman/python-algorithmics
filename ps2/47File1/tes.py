
# with open("notes.txt", "a", encoding = "utf-8") as file:
#     file.write("\npetani menanam padi di sawah")

with open("notes.txt", "r", encoding = "utf-8") as file:
    data = file.read()
    print(data)