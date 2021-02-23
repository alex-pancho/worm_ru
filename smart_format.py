import os


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


def html_add_comments():
    for root, dirs, files in os.walk("docs"):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as reader:
                    output = reader.read()
                output = output.replace(
                    '<div class="sphinxsidebar"',
                    '''
                    <div id="octomments"></div>
                    <script>
                      Octomments({
                        debug: true,
                        github: {
                          owner: "alex-pancho",
                          repo: "worm_ru",
                        },
                        issueNumber: 1,
                        renderer: [OctommentsRenderer, "#comments"],
                      }).init();
                    </script>

                    <div class="sphinxsidebar"'''
                    )
                with open(filepath, 'w', encoding='utf-8') as writer:
                    writer.write(output)
    print("octomments added")


if __name__ == '__main__':
    html_add_comments()
