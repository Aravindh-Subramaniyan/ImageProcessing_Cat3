from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog as tkFileDialog,simpledialog,messagebox
import cv2
import main
import os

def show(result_im=None):
    global panelA, panelB, path
    image = cv2.imread(path)
    # print(path)
    if result_im is None:
        result_im = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    edged = cv2.cvtColor(result_im, cv2.COLOR_BGR2RGB) #cv2.Canny(gray, 50, 100)
    image = Image.fromarray(image)
    edged = Image.fromarray(edged)
    image = ImageTk.PhotoImage(image)
    edged = ImageTk.PhotoImage(edged)
    if panelA is None or panelB is None:
        panelA = Label(image=image)
        panelA.image = image
        panelA.pack(side="left", padx=10, pady=10)
        panelB = Label(image=edged)
        panelB.image = edged
        panelB.pack(side="right", padx=10, pady=10)
    else:
        # update the pannels
        panelA.configure(image=image)
        panelB.configure(image=edged)
        panelA.image = image
        panelB.image = edged

def savefile(edge):
    edge = cv2.cvtColor(edge, cv2.COLOR_BGR2RGB)
    edge = Image.fromarray(edge)
    # edge = ImageTk.PhotoImage(edge)
    filename = tkFileDialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    edge.save(filename)
    return filename.name

def pp(i,colours_):
    # messagebox.showinfo("# WARNING: ", "Please save this Pointlist image to paint it..")
    d = savefile(i)
    os.system("python paint.py "+d)

def dialog():
    global root, path, btn3
    palette = simpledialog.askinteger("Input", "Enter palette size?",
                                parent=root,minvalue=0, maxvalue=40)
    if palette is not None:
        palette = 20

    stroke_scale = simpledialog.askinteger("Input", "Enter stroke scale?",
                                     parent=root,
                                     minvalue=0, maxvalue=100)
    if stroke_scale is not None:
        stroke_scale = 0

    g_s_radius = simpledialog.askinteger("Input", "Enter gradient smoothing radius?",
                                   parent=root,
                                   minvalue=0, maxvalue=100)
    if g_s_radius is not None:
        g_s_radius = 0

    l_image_size = simpledialog.askinteger("Input", "Enter image size?",
                                   parent=root,
                                   minvalue=0, maxvalue=1080)
    if l_image_size is not None:
        l_image_size = 0

    result_im, colours_ = main.point(path,palette,l_image_size,stroke_scale,g_s_radius)
    # cv2.imshow("res2", result_im)
    show(result_im)
    btn3 = Button(root, text="Save Pointlist ART", command=lambda: savefile(result_im))
    btn3.pack(side="right",fill="both", expand="yes", padx="20", pady="20")
    # btn4 = Button(root, text="Paint the Pointlists", command=lambda: pp(result_im,colours_))
    # btn4.pack(side="right",fill="both", expand="yes", padx="20", pady="20")


def select_image():
    # grab a reference to the image panels
    global path,btn3
    # open a file chooser dialog and allow the user to select an input
    # image
    path = tkFileDialog.askopenfilename()
    # ensure a file path was selected
    if len(path) > 0:
        show()
        btn2.pack(side="top", fill="both", expand="yes", padx="20", pady="20")


# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None
panelB = None
path = None
btn3 = None
# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Choose image", bg="white", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes",padx="100", pady="100")
btn2 = Button(root, text="Select poinlist values", command=dialog)
# btn2.pack(side="top", fill="both", expand="no", padx="20", pady="20")
# kick off the GUI
root.mainloop()
