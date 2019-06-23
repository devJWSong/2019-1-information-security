import struct, hashlib, time
import binascii
import os
from Crypto.Cipher import AES
from PIL import Image

def make_pass():
    timekey = int(time.time())
    return str(timekey)

def encrypt_image(file_path, key, outpath = "./encrypt.png", chunksize=1024):
    im, im_arr = load_image(file_path)
    x_size, y_size = im.size

    # iv = b'initialvector123'
    encryptor = AES.new(key, AES.MODE_ECB)
    # encryptor = AES.new(key, AES.MODE_CBC, iv)
    # encryptor = AES.new(key, AES.MODE_CTR, iv)

    depth = len(im_arr[0,0])

    image_data = ''

    # get pixel data
    for x in range(x_size):
        for y in range(y_size):
            for i in range(depth):
                image_data += chr(im_arr[x,y][i])
                # print(image_data)

    encdata = ''

    BLOCK_SIZE = 16

    start = time.time()

    # encrypt image
    for i in range(len(image_data)//chunksize):
        chunk = b''
        chunk = image_data[i*chunksize:(i+1)*chunksize]

        if len(chunk) == 0:
            break

        elif len(chunk) % BLOCK_SIZE != 0:
            pad_len = BLOCK_SIZE - len(chunk) % BLOCK_SIZE

        encdata += encryptor.encrypt(chunk)

    end = time.time()

    print('elpased time: ' + str(end - start))

    # change pixel data
    for x in range(x_size-1):
        for y in range(y_size-1):
            im_arr[x,y] = (ord(encdata[x*y_size*depth+y*depth]), ord(encdata[x*y_size*depth+y*depth+1]), ord(encdata[x*y_size*depth+y*depth+2]))    

    save_image(outpath, im)


def load_image(file_path):
    im = Image.open(file_path, 'r')
    arr = im.load()
    print("Image loaded")
    return im, arr

def save_image(file_path, im):
    im.save(file_path)
    print("Image saved")

def main():
    password = make_pass()
    key = hashlib.sha256(password.encode('utf-8')).digest()
    
    print('key: ' + binascii.hexlify(bytearray(key)))

    encrypt_image("./linux.png", key)

if __name__ == "__main__":
    main()