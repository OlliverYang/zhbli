title = 'IJCAI2020'
input_file = title + '.txt'
output_file = title + '.xml'


input = open(input_file, 'r', encoding='UTF-8').read().splitlines()
output = open(output_file, 'w', encoding='UTF-8')

output.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
output.write('<rss version="2.0">\n\n')
output.write('<channel>\n')
output.write('  <title>{}</title>\n'.format(title))
output.write('  <link>https://www.w3schools.com</link>\n')
output.write('  <description>{}</description>\n'.format(title))


i = 0
for line in input:
    line = line.replace('&', '-').replace('<', '-').replace('>', '-').replace('\\', '')  # 非常关键
    if 'Community detection using fast low-cardinality semidefinite programming' in line:
        print('debug')
    i += 1
    if i % 3 == 1:
        output.write('  <item>\n')
        line = line.replace('# ', '')
        line = '    <title>' + line + '</title>\n'
        output.write(line)
    elif i % 3 == 2:
        line = '    <link>' + line + '</link>\n'
        output.write(line)
    elif i % 3 == 0:
        line = '    <description>' + line + '</description>\n'
        output.write(line)
        output.write('  </item>\n')

output.write('</channel>\n\n')
output.write('</rss>\n')
output.close()


