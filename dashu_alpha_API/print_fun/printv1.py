
import qrcode
from PIL import Image
import win32print
import win32ui
import win32con
from PIL import ImageWin
from configparser import ConfigParser


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img


def get_setting(s):
    cfg = ConfigParser()
    cfg.read('./config.ini')
    return cfg.get('print_settings', s)


def print_full(qr_code='', text1='', text2='', text3=''):

    # 生成打印图片
    data = qr_code
    img = generate_qr_code(data)
    img.save('qr_code.png')

    # 打印二维码 获取默认打印机
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    if qr_code == 'test':
        return {
            'code': 201,
            'status': True,
            'msg': 'printer has been found : ' + printer_name
        }

    # 获取当前打印机纸张大小
    page_size = hDC.GetDeviceCaps(
        win32con.PHYSICALWIDTH), hDC.GetDeviceCaps(win32con.PHYSICALHEIGHT)
    print('page size: {} x {}'.format(page_size[0], page_size[1]))

    # 打印图片
    bmp = Image.open('qr_code.png')
    hDC.StartDoc('qr_code')
    hDC.StartPage()

    # 打印分割线
    hDC.MoveTo(0, int(get_setting('cut_line_pos_0')))
    hDC.LineTo(page_size[0]-200, int(get_setting('cut_line_pos_0')))

    hDC.MoveTo(0, int(get_setting('cut_line_pos_1')))  # 第二条分割线 第二个值要相等
    hDC.LineTo(page_size[0]-0, int(get_setting('cut_line_pos_1')))  # 第二条分割线

    # 右上角  左下角角标
    hDC.MoveTo(0, page_size[1]-100)
    hDC.LineTo(100, page_size[1]-100)
    hDC.MoveTo(0, page_size[1]-100)
    hDC.LineTo(0, page_size[1]-200)

    hDC.MoveTo(page_size[0]-100, 0)
    hDC.LineTo(page_size[0]-100, 100)
    hDC.MoveTo(page_size[0]-100, 0)
    hDC.LineTo(page_size[0]-200, 0)

    # 打印文字1行
    font = win32ui.CreateFont({
        # 'name': 'Arial',
        'height': int(get_setting('line_height_0')),
        'weight': int(get_setting('line_weight_0')),
    })
    hDC.SelectObject(font)
    hDC.TextOut(int(get_setting('line_pos_x_0')),
                int(get_setting('line_pos_y_0')), text1)

    # 打印文字2行
    font = win32ui.CreateFont({
        # 'name': 'Arial',
        'height': int(get_setting('line_height_1')),
        'weight': int(get_setting('line_weight_1')),
    })
    hDC.SelectObject(font)
    hDC.TextOut(int(get_setting('line_pos_x_1')),
                int(get_setting('line_pos_y_1')), text2)

    # 打印文字3行
    font = win32ui.CreateFont({
        # 'name': 'Arial',
        'height': int(get_setting('line_height_2')),
        'weight': int(get_setting('line_weight_2')),
    })
    hDC.SelectObject(font)
    hDC.TextOut(int(get_setting('line_pos_x_2')),
                int(get_setting('line_pos_y_2')), text3)

    # 结束输出区

    dib = ImageWin.Dib(bmp)
    # 参数是一个元组，表示绘制的位置和大小。元组中的四个数字分别代表左上角的x坐标、左上角的y坐标、右下角的x坐标和右下角的y坐标
    dib.draw(hDC.GetHandleOutput(), (0, 0, bmp.size[0], bmp.size[1]))

    hDC.EndPage()
    hDC.EndDoc()
    return '打印成功'


if __name__ == '__main__':
    print('先到这')

    print_full('321', '内容1', '内容2', '内容3')
    exit(0)

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
    hDC.LineTo(page_size[0]-200, 100)

    hDC.MoveTo(0, 500)  # 第二条分割线 第二个值要相等
    hDC.LineTo(page_size[0]-0, 500)  # 第二条分割线

    # 右上角  左下角角标
    hDC.MoveTo(0, page_size[1]-100)
    hDC.LineTo(100, page_size[1]-100)
    hDC.MoveTo(0, page_size[1]-100)
    hDC.LineTo(0, page_size[1]-200)

    hDC.MoveTo(page_size[0]-100, 0)
    hDC.LineTo(page_size[0]-100, 100)
    hDC.MoveTo(page_size[0]-100, 0)
    hDC.LineTo(page_size[0]-200, 0)

    font = win32ui.CreateFont({
        # 'name': 'Arial',
        'height': 100,
        'weight': 800,
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
