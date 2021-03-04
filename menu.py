import net
import net_vis
from tkinter import *
from tkinter import filedialog as fd

def open_net(event=None) :
	net_path = fd.askopenfilename()
	net.load_net(n,net_path)
	net_vis.visualize(root,c,500,500,n)
def save_net(event=None) :
	file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),("All files", "*.*")))
	net.export_net(n, file_name)
def work(event=None) :
	out_text.delete(1.0, END)
	for line in in_text.get(1.0, END).split("\n") :
		if line :
			out_text.insert(END, str(n.net_work(list(map(int,line.split(","))))+"\n"))
def learn() :
	for line in in_text.get(1.0, END).split("\n") :
		if line :
			n.net_learn(4,list(map(int,line.split(","))))
def read(event=None) :
	net.load_net(n,in_text.get(1.0, END),new_net=False)
	net_vis.visualize(root,c,500,500,n)
def clear() :
	global n
	del n
	n = net.Net()
	net_vis.visualize(root,c,500,500,n)

def add_layer(event=None) :
	def process(event=None) :
		global n
		nonlocal layer_name
		nonlocal layer_count
		if layer_name.get() == "in" :
			n.create_in_layer(int(layer_count.get()))
		elif layer_name.get() == "out" :
			n.create_out_layer(int(layer_count.get()))
		else :
			n.create_layer(layer_name.get(),int(layer_count.get()))
		net_vis.visualize(root,c,500,500,n)
		add_layer_root.destroy()
	add_layer_root = Toplevel(root)
	add_layer_root.title("Add layer")
	add_layer_root.focus_set()
	add_layer_root.bind("<Return>", process)
	layer_name_label = Label(add_layer_root, text="Layer name:")
	layer_name = Entry(add_layer_root, width=25)
	layer_count_label = Label(add_layer_root, text="Layer count:")
	layer_count = Entry(add_layer_root, width=25)
	button = Button(add_layer_root, text="add", command=process)
	layer_name_label.pack()
	layer_name.pack()
	layer_count_label.pack()
	layer_count.pack()
	button.pack()
	add_layer_root.mainloop()	
root = Tk()
main_menu = Menu(root)
c = Canvas(root, width=500, height=500, bg='white')
out_text = Text(width=15, height=30)
in_text = Text(width=15, height=30)
n = net.Net()

root.title("Perceptron designer")
c.pack(side=LEFT)
out_text.pack(side=RIGHT)
in_text.pack(side=RIGHT)
root.config(menu=main_menu)

file_menu = Menu(main_menu,tearoff=0)
file_menu.add_command(label="Open", command=open_net)
file_menu.add_command(label="Save", command=save_net)

net_menu = Menu(main_menu,tearoff=0)
net_menu.add_command(label="Read commands", command=read)
net_menu.add_command(label="Add layer", command=add_layer)
net_menu.add_command(label="Learn", command=learn)
net_menu.add_command(label="Work", command=work)
net_menu.add_command(label="Clear", command=clear)

root.bind("<Control-n>", add_layer)
root.bind("<Control-o>", open_net)
root.bind("<Control-s>", save_net)
root.bind("<F5>", read)
root.bind("<F7>", work)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Net", menu=net_menu)



root.mainloop()