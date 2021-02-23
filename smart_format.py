

def filename_fixed(filename):
    filename = filename.replace(" ", "_")
    return filename


def content_parser(filepath):
    with open(filepath, 'r', encoding='utf-8') as reader:
        output = reader.readline()
        secline = reader.readline()
        if "#" in secline:
            output = output + secline
        else:
            output = output + "#"*len(output)+"\n" + secline
        for line in reader:
            line = line.replace("\n", "\n\n")
            output = output + line
    with open(filepath, 'w', encoding='utf-8') as writer:
        writer.write(output)
    return None
