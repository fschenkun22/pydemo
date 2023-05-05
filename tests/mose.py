import pyautogui
import time
import keyboard
import threading
import mouse
import os

# 定义一个函数来处理“修复问题”和“删除”的点击事件
def click_buttons(fix_button_pos, delete_button_pos):
    # 移动鼠标到“修复”按钮的位置并点击
    pyautogui.moveTo(fix_button_pos[0], fix_button_pos[1], duration=0)
    pyautogui.click()
    # 等待弹出窗口
    time.sleep(0.1)
    # 移动鼠标“删除”按钮的位置并点击
    pyautogui.moveTo(delete_button_pos[0], delete_button_pos[1], duration=0)
    pyautogui.click()
    # 等待操作完成
    time.sleep(0.2)

# 定义一个函数来处理键盘事件
def handle_keyboard():
    while True:
        if keyboard.is_pressed('c'):
            os._exit(0)

# 创建一个线程来处理键盘事件
keyboard_thread = threading.Thread(target=handle_keyboard)
keyboard_thread.start()

# 等待用户点击鼠标左键来获取“修复问题”按钮的位置
print("请点击鼠标左键来获取“修复问题”按钮的位置")
while True:
    if keyboard.is_pressed('c'):
        os._exit(0)
    if keyboard.is_pressed('esc'):
        break
    if mouse.is_pressed(button='left'):
        break
fix_button_pos = pyautogui.position()
print("“修复问题”按钮的位置为：", fix_button_pos)

# 等待用户点击鼠标左键来获取“删除”按钮的位置
print("请点击鼠标左键来获取“删除”按钮的位置")
while True:
    if keyboard.is_pressed('c'):
        os._exit(0)
    if keyboard.is_pressed('esc'):
        break
    if mouse.is_pressed(button='left'):
        break
delete_button_pos = pyautogui.position()
print("“删除”按钮的位置为：", delete_button_pos)

# 循环点击“修复问题”和“删除”按钮
while True:
    # 处理“修复问题”和“删除”按钮的点击事件
    click_buttons(fix_button_pos, delete_button_pos)
