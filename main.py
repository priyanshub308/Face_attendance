import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image,ImageTk
import os
import subprocess
import datetime



                        #    Util starts here
def get_button(window, text, color, command, fg='white'):
    button=tk.Button(window,
                     text=text,
                     activebackground="black",
                     activeforeground="white",
                     fg=fg,
                     bg=color,
                     command=command,
                     height=2,
                     width=20,
                     font=('Helvetica bold', 20)
    )

    return button


def get_img_label(window):
    label=tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label=tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt= tk.Text(window,
                      height=2,
                      width=15, font=("Ariel", 22))
    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)


                # Util ends here
    


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+300+100")

        self.login_button_main_window = get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_newuser_button_main_window = get_button(self.main_window, 'register new user', 'gray', self.register_newuser, fg='black')
        self.register_newuser_button_main_window.place(x=750, y=400)

        self.webcam_label = get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir= './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)


        self.log_path='./log.txt'



    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label=label
        self.process_webcam()


    def process_webcam(self):
        ret, frame= self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)




    def login(self):
        unknown_img_path= './.tmp.jpg'
        
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output= str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        print(output)
        name = output.split(',')[1][:-5]

        
        if name in ['unknown_person', 'no_persons_found']:
            msg_box('Oops....', 'Unknown user, Please register new user or try again.')

        else:
            msg_box('Welcome Back !', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name,datetime.datetime.now()))
                f.close()

        os.remove(unknown_img_path)


    def register_newuser(self):
        self.register_newuser_window = tk.Toplevel(self.main_window)
        self.register_newuser_window.geometry("1200x520+320+120")

        self.accept_button_register_newuser_window = get_button(self.register_newuser_window, 'Accept', 'green', self.accept_register_newuser)
        self.accept_button_register_newuser_window.place(x=750, y=300)


        self.tryagain_button_register_newuser_window = get_button(self.register_newuser_window, 'Try Again', 'red', self.tryagain_register_newuser)
        self.tryagain_button_register_newuser_window.place(x=750, y=400)

        self.capture_label = get_img_label(self.register_newuser_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        
        self.add_img_to_label(self.capture_label)

        self.entry_text_register_newuser= get_entry_text(self.register_newuser_window)
        self.entry_text_register_newuser.place(x=750,y=100)


        self.text_label_register_newuser =get_text_label(self.register_newuser_window ,"Plese, \nInput username: ")
        self.text_label_register_newuser.place(x=750,y=20)




    def tryagain_register_newuser(self):
        self.register_newuser_window.destroy()



    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_newuser_capture = self.most_recent_capture_arr.copy()




    def start(self):
        self.main_window.mainloop()



    def accept_register_newuser(self):
        name=self.entry_text_register_newuser.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_newuser_capture)

        msg_box('Success!', 'User was register Successfully !')

        self.register_newuser_window.destroy()



if __name__ == "__main__":
    app= App()
    app.start()
