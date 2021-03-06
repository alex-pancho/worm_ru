import os
from transliterate import translit

filename_list = [
        ["[Изменено]", ""],
        ["(правка)", ""], ["(правка,", ""],
        ["(правки)", ""], ["правки)", ""],
        ["(кавычки)", ""], ["(кавычки,", ""], ["кавычки)", ""],
        ["(перевыложено)", ""],
        [" ", ""],
        ]
text_list = [
        ["<b>", "**"],
        ["</b>", "**"],
        ["<i>", "*"],
        ["</i>", "*"],
        ["\n", "\n\n"],
        # ["", ""], #
        ]


def replace_me(filename, replace_list=filename_list, transliter=False):
    for r in replace_list:
        filename = filename.replace(r[0], r[1])
    if transliter:
        filename = translit(filename, 'ru', reversed=True)
    return filename


def content_parser(filepath):
    with open(filepath, 'r', encoding='utf-8') as reader:
        output = reader.readline()
        secline = reader.readline()
        if "#" in secline:
            output = output + secline
        else:
            output = output + "#"*len(output)+"\n" + replace_me(secline, text_list)
        for line in reader:
            line = line.strip(" ")
            line = replace_me(line, text_list)
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
                    '''</div>


            <div class="clearer"></div>''',
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
                        renderer: [OctommentsRenderer, "#octomments"],
                      }).init();
                    </script>
</div>


            <div class="clearer"></div>'''
                    )
                with open(filepath, 'w', encoding='utf-8') as writer:
                    writer.write(output)
    print("octomments added")


if __name__ == '__main__':
    html_add_comments()
