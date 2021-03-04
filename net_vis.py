import net
from tkinter import *
from functools import partial

def visualize(root,c,display_x,display_y,n) :
	is_selected = False
	selected_obj = None
	text = None
	def pressed(event, j) :
		nonlocal is_selected 
		nonlocal selected_obj
		nonlocal text
		nonlocal n
		nonlocal c
		nonlocal root
		nonlocal display_y
		nonlocal display_x
		if not is_selected :
			if isinstance(j, net.Out) :
				return
			is_selected = True
			selected_obj = j
			text = c.create_text(display_x//2,display_y-20,text=str("selected object: "+str(j)))
			return
		if is_selected :
			c.delete(text)
			if selected_obj == j :
				is_selected = False
				return
			if position[selected_obj][0] == position[j][0] :
				is_selected = False
				return
			is_selected = False
			if j not in selected_obj.connected :
				selected_obj.append_neuro(j,1)
				visualize(root,c,display_x,display_y,n)
				return
			if j in selected_obj.connected :
				selected_obj.remove_neuro(j) 
				visualize(root,c,display_x,display_y,n)
				return
			#lines[j] = c.create_line(position[selected_obj][0]+20,position[selected_obj][1]+20,position[j][0]+20,position[j][1]+20)
	def lines_weight(event, in_neuro, out_neuro) :
		nonlocal root
		def change_weight(event=None) :
			in_neuro.connected_weight[out_neuro] = int(weight_entry.get())
			lines_weight_root.destroy()
		lines_weight_root = Toplevel(root)
		lines_weight_root.title("Line")
		in_neuro_label = Label(lines_weight_root, text="In neuro: {}".format(str(in_neuro)), )
		out_neuro_label = Label(lines_weight_root, text="Out neuro: {}".format(str(out_neuro)))
		weight_entry = Entry(lines_weight_root, width=25)
		weight_entry.insert(0, in_neuro.connected_weight[out_neuro])
		button = Button(lines_weight_root, text="Change weight", command=change_weight)
		lines_weight_root.bind("<Return>", change_weight)
		in_neuro_label.pack()
		out_neuro_label.pack()
		weight_entry.pack()
		button.pack()
		lines_weight_root.mainloop()
	def configure_neuro(event, neuro) :
		nonlocal root
		if not isinstance(neuro, net.Neuro) : return
		def edit_neuro(event=None) :
			neuro.condition = int(condition_entry.get())
			neuro.max_weight = int(max_weight_entry.get())
			configure_neuro_root.destroy()
		configure_neuro_root = Toplevel(root)
		configure_neuro_root.title("Neuro config")
		name_label = Label(configure_neuro_root, text="Name: {}".format(neuro))
		condition_label = Label(configure_neuro_root, text="Condition: ")
		condition_entry = Entry(configure_neuro_root, width=25)
		condition_entry.insert(0, neuro.condition)
		max_weight_label = Label(configure_neuro_root, text="Max weight: ")
		max_weight_entry = Entry(configure_neuro_root, width=25)
		max_weight_entry.insert(0, neuro.max_weight)
		button = Button(configure_neuro_root, text="Edit", command=edit_neuro)
		name_label.pack()
		condition_label.pack()
		condition_entry.pack()
		max_weight_label.pack()
		max_weight_entry.pack()
		button.pack()
		configure_neuro_root.mainloop()
	position = {}
	circles = []
	lines = []

	x_pos = 0
	y_pos = 0
	x_step = display_x//(2+len(n.layers))
	if n.in_layer : y_step = display_y//len(n.in_layer)
	for i in n.in_layer :
		position[i] = (x_pos+25,y_pos+25)
		y_pos += y_step
	
	for i in n.layers :
		y_pos = 0
		y_step = display_y//len(n.layers[i]) 
		x_pos += x_step
		for j in n.layers[i] :
			position[j] = (x_pos+25,y_pos+25)
			y_pos += y_step
	
	x_pos += x_step
	y_pos = 0
	if n.out_layer : y_step = display_y//len(n.out_layer)
	for i in n.out_layer :
		position[i] = (x_pos+25,y_pos+25)
		y_pos += y_step

	c.delete("all")
	for i in position :
		if i.connected :
			for j in i.connected :
				lines.append(c.create_line(position[i][0]+20,position[i][1]+20,position[j][0]+20,position[j][1]+20,width=2))
				c.tag_bind(lines[len(lines)-1],"<Button-1>", partial(lines_weight, in_neuro=i, out_neuro=j))
		circles.append(c.create_oval(position[i][0],position[i][1],position[i][0]+40,position[i][1]+40,width=2,fill="black",tag="cirlce"))
		c.tag_bind(circles[len(circles)-1],"<Button-1>", partial(pressed, j=i))
		c.tag_bind(circles[len(circles)-1],"<Button-3>", partial(configure_neuro, neuro=i))
		#c.tag_bind(circles[len(circles)-1],"<Button-3>",partial(remove_connection, j=i))
