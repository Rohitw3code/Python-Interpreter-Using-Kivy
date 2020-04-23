from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.codeinput  import CodeInput
from kivy.modules import keybinding
from kivy.core.window import Window
from pygments.lexers import CythonLexer
from kivy.extras.highlight import KivyLexer
import os
import threading
import subprocess

p = None
root=Builder.load_string('''
GridLayout:
    cols:1
    rows:3
    TextInput:
        id:l1
        text:'Output---Here'
        markup:True

    CodeInput:
        id:inpt
        on_text:app.indent(self)
        text:'a=input("enter please : ")'
        auto_indent:True

    Button:
        id:b1
        text:'compile'
        on_press:app.frezz_prevent(self)
        background_color:0.1,0.2,0.8,0.9
        size_hint_y:0.1

''')
class main(Widget):
    pass
class compiler(App):
    def build(self):
        self.p=''
        return root
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if len(modifiers) > 0 and modifiers[0] == 'ctrl' and text == 'a':  # Ctrl+a
            print("\nThe key", keycode, "have been pressed")
            print(" - text is %r" % text)
            print(" - modifiers are %r" % modifiers)
            self.menu.add_menu()
    def process(self):
            self.p = subprocess.Popen(['python', 'program.py'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     shell=True
                     )
            
    def comp(self):
        file=open('program.py','w')
        file.write(self.root.ids.inpt.text)
        file.close()
        file=open('program.py','a')
        file.close()
        self.process()
        out=[]
        pro=threading.Thread(target=self.process)
        pro.start()
        for line in self.p.stdout:
            if 'input(' in str(line)[2::]:
                print(1)
                pass
            else:
                st=str(line)[2:-5:]
                out.append(st)
        string=''
        for i in out:
            string=string+i+'\n'
        self.root.ids.l1.text=string

    def frezz_prevent(self,button):
        x=threading.Thread(target=self.comp)
        x.start()

    def indent(self,button):
      try:
        if root.ids.inpt.text[-1]==':':
            root.ids.inpt.text=root.ids.inpt.text+'\n   '
      except: 
            pass
compiler().run()
