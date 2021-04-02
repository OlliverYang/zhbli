input = open('cvpr2020.md', 'r').read().splitlines()
output = open('cvpr2020_1.xml', 'w')

output.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
output.write('<rss version="2.0">\n\n')
output.write('<channel>\n')
output.write('  <title>CVPR2020</title>\n')
output.write('  <link>https://www.w3schools.com</link>\n')
output.write('  <description>Free web building tutorials</description>\n')


i = 0
for line in input:
    line = line.replace('&', '-')
    line = line.replace('<', '-')
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


