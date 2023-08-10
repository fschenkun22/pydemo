import qrcode
from PIL import Image
import win32print
import win32ui
from PIL import ImageWin


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img


if __name__ == '__main__':
    data = 'hello world'
    img = generate_qr_code(data)
    img.save('qr_code.png')

    # 打印二维码
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    bmp = Image.open('qr_code.png')
    # if bmp.size[0] > bmp.size[1]:
    #     bmp = bmp.rotate(90)
    hDC.StartDoc('qr_code')
    hDC.StartPage()
    dib = ImageWin.Dib(bmp)
    dib.draw(hDC.GetHandleOutput(), (0, 0, 1000, 1000))

    hDC.EndPage()
    hDC.EndDoc()
