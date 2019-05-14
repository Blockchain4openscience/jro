import nbformat as nbf
import pip

#Install libraries

pip.main(['install', '-r', 'requirements.txt'])


#Build Jupyter Notebook

nb = nbf.v4.new_notebook()

f = open('README.md', 'r')

text = f.read()

f.close()

cells = text.split('```')

nb['cells'] = []

for index, cell in enumerate(cells):
    if index%2:
        nb['cells'].append(nbf.v4.new_code_cell(cell))
    else:
        nb['cells'].append(nbf.v4.new_markdown_cell(cell))


nbf.write(nb, 'test.ipynb')
