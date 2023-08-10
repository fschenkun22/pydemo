# coding: utf-8" 

import qrcode
from PIL import Image
import win32print
import win32ui
import win32con
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

    # 获取当前打印机纸张大小
    page_size = hDC.GetDeviceCaps(
        win32con.PHYSICALWIDTH), hDC.GetDeviceCaps(win32con.PHYSICALHEIGHT)
    print('page size: {} x {}'.format(page_size[0], page_size[1]))

    bmp = Image.open('qr_code.png')
    hDC.StartDoc('qr_code')
    hDC.StartPage()

    hDC.MoveTo(0, 100)
    hDC.LineTo(page_size[0], 100)
    
    font = win32ui.CreateFont({
        # 'name': 'Arial',
        'height': 100,
    })
    hDC.SelectObject(font)
    hDC.TextOut(350, 0, '开始的内容说明')


    font = win32ui.CreateFont({
        # 'name': 'Arial',
        'height': 90,
    })
    hDC.SelectObject(font)
    hDC.TextOut(350, 150, '第二行的内容说明第二行的内容说明第第二行')


    font = win32ui.CreateFont({
        # 'name': 'Arial',
        'height': 50,

    })
    hDC.SelectObject(font)
    hDC.TextOut(350, 250, '第三行的内容说明')



    dib = ImageWin.Dib(bmp)
    # 参数是一个元组，表示绘制的位置和大小。元组中的四个数字分别代表左上角的x坐标、左上角的y坐标、右下角的x坐标和右下角的y坐标
    dib.draw(hDC.GetHandleOutput(), (0, 0, bmp.size[0], bmp.size[1]))

    hDC.EndPage()
    hDC.EndDoc()
