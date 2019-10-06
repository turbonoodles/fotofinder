'''
Navigate down an arbitrary directory structure and copy photos
Copy into destination directory intelligently based on EXIF data
'''

import exifread as exif
from pathlib import Path
import argparse
import shutil


# Command arguments will be the source and destination folders
parser = argparse.ArgumentParser(description='Copy Images')
parser.add_argument('sourcedir', type=str, help='Source: Input dir to search for photos')
parser.add_argument('destidir', type=str, help='Destination: Dir to put photos in')

args = parser.parse_args()

filetypes = [".DNG", ".JPG", ".NRW"]

#sourcedir = 'C:\\Users\\Craig\\Pictures\\raw_processor_testing'
#destdir = 'noodles'

def process(filename):
    '''
    asdfkl;j
    '''
    img = open(filename, 'rb')
    imgtags = exif.process_file(img, stop_tag='DateTimeOriginal', details=False)
    # Extract date: [Y, m, d]
    date = str(imgtags['EXIF DateTimeOriginal']).split(' ')[0].split(':')
    img.close()
    return date

if __name__ == "__main__":

    counter = 0

    if not Path(args.destidir).exists():
            Path(args.destidir).mkdir()

    for ft in filetypes:
        for file in Path(args.sourcedir).glob(f"**/*{ft}"):

                # Extract date information
                # Skip everything if it doesn't exist
                print(f'processing: {file}')
                try:
                        year, month, day = process(file)

                        # Create year directory, if needed
                        if not Path(f'{args.destidir}\\{year}').exists():
                                print(f'making directory: {year}')
                                Path(f'{args.destidir}\\{year}').mkdir()

                        # Create month directory, if needed
                        if not Path(f'{args.destidir}\\{year}\\{month}').exists():
                                print(f'making directory: {year}\\{month}')
                                Path(f'{args.destidir}\\{year}\\{month}').mkdir()

                        # Create day directory, if needed
                        if not Path(f'{args.destidir}\\{year}\\{month}\\{day}').exists():
                                print(f'making directory: {year}\\{month}\\{day}')
                                Path(f'{args.destidir}\\{year}\\{month}\\{day}').mkdir()

                        # Now that destination dir definitely exists, copy image if it does not exist
                        # in the destination dir
                        fqdest = f'{args.destidir}/{year}/{month}/{day}'
                        imgname = Path(file).name
                        
                        if not Path(f'{fqdest}/{imgname}').exists():
                                print(f'copying: {file}')
                                shutil.copy2(file, fqdest)
                                counter = counter + 1
                        else:
                                print(f'not overwriting: {file}')

                except KeyError:
                        pass

    print(f'copied {counter} images.')