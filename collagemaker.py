# 2019-03-18 16:10-17:10 60' search files
# 2019-03-18 19-30-20:10 40' resize, combine
# 2019-03-18 20-10

# this app searches all jpegs in subdirectories
# and joins them on 6x6
# requirements

from pathlib import Path
import numpy as np
from PIL import Image

files = []

### scans subdirs, finds all files with ext '.JPG' and adds to list 'files'

def scan(path):
    p = Path(path)
    for x in p.iterdir():
        if x.is_file():
            if x.suffix == '.JPG':
                abs_path = str(x.absolute())
#                print('add=',abs_path)
                files.append(abs_path)

        if x.is_dir():
            new_path = path + '/' + x.name
            scan(new_path)

###


### main()

# step 1: scan all
scan('.')
#scan('./test')

# step 2: 
num_img = len(files)

res = 150
size_x = int(res * 3 / 2.54)
size_y = int(res * 4 / 2.54)
indent = 2

num_pages =  1 + ((num_img - 1) // 36)
total_img = num_pages * 36
while len(files)<total_img:
    files.append('')
a = np.array(files)
b = a.reshape((num_pages,6,6))

for i in range(num_pages):
    img_big = Image.new(mode='RGB', size=(6*size_x + 5*indent, 6*size_y + 5*indent), color=(255,255,255))
   
    for j in range(6):
        for k in range(6):
            filename = b[i,j,k]
            if filename != '':
                im = Image.open(filename)
                im = im.resize((size_x, size_y), resample=Image.BICUBIC)
                #im.show()

                img_big.paste(im, box=(k*(size_x + indent), j*(size_y+indent)))

    img_big_filename = 'Страница ' + str(i+1) + ' из ' + str(num_pages) +'.jpeg'            
    img_big.save(img_big_filename, dpi=(150,150))
