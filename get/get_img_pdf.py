import time, re, os
import fitz

def pdf2pic(path, pic_path):

    t0 = time.perf_counter()

    checkXO = r"/Type(?= */XObject)"
    checkIM = r"/Subtype(?= */Image)"

    doc = fitz.open(path)
    imgcount = 0
    lenXREF = doc.xref_length()

    print("foldname:{}, totalpage:{}, target:{}".format(path, len(doc), lenXREF-1))

    for i in range(1, lenXREF):
        text = doc.xref_object(i)
        isXObject = re.search(checkXO, text)

        isImage = re.search(checkIM, text)
        if not isXObject or not isImage:
            continue
        imgcount += 1

        pix = fitz.Pixmap(doc, i)

        new_name = path.replace('\\', '_') + "_img{}.png".format(imgcount)
        new_name = new_name.replace(':', '')

        if pix.n < 5:
            pix.writePNG(os.path.join(pic_path, new_name))
        else:
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(os.path.join(pic_path, new_name))
            pix0 = None

        pix = None
        t1 = time.perf_counter()
        print("run in {}s".format(t1 - t0))
        print("get {} figs".format(imgcount))

if __name__ == "__main__":
    path = r'regional.pdf'
    pic_path = r'images'

    m = pdf2pic(path, pic_path)
