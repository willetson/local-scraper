import os
import zlib

# load configuration
# Enumerate  Systems(Folders)

#   Enumerate Games(files)
#       Calculate CRC/MD5


def main(library):
    for file in os.scandir(library):
        if file.is_dir():
            pass
    pass


def process_system(system):
    pass


def process_game(system, game):

    pass


def process_image(game, url):
    pass


def generate_crc(file):
    x = "filename"
    zlib.crc32(x.encode('ascii'))



zip_name = "test.zip"


def Crc32Hasher(file_path):

    buf_size = 65536
    crc32 = 0

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            crc32 = zlib.crc32(data, crc32)

    return format(crc32 & 0xFFFFFFFF, '08x')


print(Crc32Hasher(zip_name))

import hashlib


zip_name = "test.zip"


def Sha1Hasher(file_path):

    buf_size = 65536
    sha1 = hashlib.sha1()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha1.update(data)

    return format(sha1.hexdigest())


print(Sha1Hasher(zip_name))

import zipfile

zip_name = "test.zip"

if zip_name.lower().endswith(('.zip')):
    z = zipfile.ZipFile(zip_name, "r")

for info in z.infolist():

    print(info.filename,
          format(info.CRC & 0xFFFFFFFF, '08x'))

import zipfile

archive = zipfile.ZipFile(fname)
blocksize = 1024**2  #1M chunks
for fname in archive.namelist():
    entry = archive.open(fname)
    md5 = hashlib.md5()
    while True:
        block = entry.read(blocksize)
        if not block:
            break
        md5.update(block)
    print(fname, md5.hexdigest())

if __name__ == "__main__":
    print("Let's rock and roll")
