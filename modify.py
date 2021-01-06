import os

path = "/home/rfaccount/ctf/write-ups/picoCTF"


dirname = [f for f in os.listdir(path) if not f.endswith("py")]

md_file_path = []
for i in dirname:
    print([f for f in os.listdir(os.path.join(path, i)) if f.endswith(".md")])
    md_file_path.extend([os.path.join(os.path.join(path, i), f) for f in os.listdir(os.path.join(path, i)) if f.endswith(".md")])

print(md_file_path)

md_file = {}

for mdpath in md_file_path:
    with open(mdpath, 'r') as f:
        md_file[mdpath] = f.readlines()

for key in md_file:
    value = md_file[key]
    for i, line in enumerate(value):
        # if line.startswith("+++"):
        #     value[i] = '---\n'
        # if line.startswith("title = "):
        #     value[i] = line.replace("title = ", "title: ")
        # if line.startswith("title: "):
        #     value[i] = line[:7] + '-'.join(line[7:].split(' '))
        # if line.startswith("date = "):
        #     value[i] = line.replace("date = ", "date: ")
        # if line.startswith("author = "):
        #     value[i] = line.replace("author = ", "author: ")
        # if line.startswith("description = "):
        #     value[i] = line.replace("description = ", "description: ")
        if line.startswith("description: "):
            print(line[:line.find("?category")])
            value[i] = line[:line.find("?category")] + '"\n'
            print(value[i])

for path in md_file:
    value = md_file[path]
    print(path)
    with open(path, 'w') as f:
        f.writelines(value) 