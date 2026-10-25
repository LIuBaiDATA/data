import os
import sys
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

# 1. 拦截原本要在终端打印的文字，显示到手机屏幕的文本框里
class PrintLogger:
    def __init__(self, textinput):
        self.textinput = textinput
    def write(self, text):
        if text.strip():
            # Kivy 界面更新必须在主线程，使用 Clock 调度
            Clock.schedule_once(lambda dt: self.append_text(text), 0)
    def flush(self):
        pass
    def append_text(self, text):
        self.textinput.text += text + "\n"
        # 自动滚动到最底部
        self.textinput.cursor = (0, len(self.textinput.text))

# 2. 定义安卓的图形界面
class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.log_area = TextInput(text="程序已启动，正在加载控制器...\n", readonly=True, font_size='12sp')
        self.layout.add_widget(self.log_area)
        
        # 把系统的 print 重定向到我们的界面上
        sys.stdout = PrintLogger(self.log_area)
        sys.stderr = sys.stdout
        
        # 3. 开启一个后台线程运行你的控制器，防止卡死界面
        threading.Thread(target=self.run_controller, daemon=True).start()
        return self.layout

    def run_controller(self):
        # 锁定当前目录，确保控制器能识别同目录的子脚本
        BASE = os.path.dirname(os.path.abspath(__file__))
        os.chdir(BASE)
        sys.path.insert(0, BASE)
        
        try:
            print("正在导入 controller.py ...")
            # 导入你的控制器文件（去掉 .py 后缀）
            import controller
            
            # 如果控制器里有 main 函数，就运行它
            if hasattr(controller, 'main'):
                print("开始执行主控制逻辑...")
                controller.main()
            else:
                print("警告：controller.py 中没有找到 main() 函数。")
                print("如果代码是直接写在文件里的，应该已经自动执行了。")
                
        except Exception as e:
            import traceback
            print("\n❌ 发生致命错误！")
            traceback.print_exc()

if __name__ == '__main__':
    MyApp().run()