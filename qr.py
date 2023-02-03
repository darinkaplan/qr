from PIL import Image
import cv2
import pyzbar.pyzbar as pyzbar
from pdf2image import convert_from_path
import glob, os
import magic
import pyheif



def find_qr(file_path, debug=False):
    datatype = magic.from_file(file_path).split(' ')[0]
    results = []
    print(f"FILE DATATYPE: {datatype}") if debug else None
    if datatype == 'PDF':
        # Open the PDF
        images = convert_from_path(file_path)
        # Iterate over the images
        for image in images:
            # Use the pyzbar library to detect and decode QR codes in the image
            decoded_objects = pyzbar.decode(image)
            # Print the data of each QR code found
            for obj in decoded_objects:
                print("Data:", obj.data.decode("utf-8")) if debug else None
                results.append(obj)
    elif datatype in ['JPEG', 'SVG', 'PNG', 'BMP', 'data']:
        # Load the image
        image = cv2.imread(file_path)
        # Find and decode QR codes in the image
        decoded_objects = pyzbar.decode(image)
        # Print the data of each QR code found
        for obj in decoded_objects:
            print("Data:", obj.data.decode("utf-8")) if debug else None
            results.append(obj)
    elif datatype == 'ISO':
        heif_file = pyheif.read(file_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        fname = f"images/tmpFile_heif.png"
        image.save(fname, "PNG")
        results = find_qr(fname)
        os.remove(fname)
    else:
        print(f"{file_path}: Not a Supported FileType")
    return results


if __name__ == '__main__':
    final = []
    for imagePath in glob.glob("images/*.*"):
        print(f"Analyzing file: {imagePath}")
        final.extend(find_qr(imagePath))
    print(f"{len(final)} QR codes identified")
    print(final)

