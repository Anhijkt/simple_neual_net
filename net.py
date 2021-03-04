#so here all main classes and functions

class Neuro() :	 			#this is a single neuron emulation 
	def __init__(self): 	#you can try to build something more complicated then just feed forward net
		self.connected = [] #but i dont think that its gonna work right 
		self.connected_weight = {}
		self.in_weight = 0
		self.max_weight = 1
		self.condition = 1
		self.learn_speed = 0.20
	def learn(self) :
		if self.in_weight >= self.condition :
			for neuro in self.connected :
				neuro.in_weight += self.in_weight * self.connected_weight[neuro]
				if self.connected_weight[neuro] < neuro.max_weight :
					self.connected_weight[neuro] += self.learn_speed
		self.in_weight = 0
	def work(self) :
		if self.in_weight >= self.condition :
			for neuro in self.connected :
				neuro.in_weight += self.in_weight * self.connected_weight[neuro]
		self.in_weight = 0
	def append_neuro(self, neuro,weight) :
		if neuro not in self.connected :
			self.connected.append(neuro)
			self.connected_weight[neuro] = weight
	def remove_neuro(self, neuro) :
		if neuro in self.connected :
			self.connected.remove(neuro)
			del self.connected_weight[neuro]
class Giver() : #this and Out class just to make net input and output layers
	def __init__(self) :
		self.connected = []
		self.connected_weight = {}
	def append_neuro(self, neuro,weight) :
		if neuro not in self.connected :
			self.connected.append(neuro)
			self.connected_weight[neuro] = weight
	def remove_neuro(self, neuro) :
		if neuro in self.connected :
			self.connected.remove(neuro)
			del self.connected_weight[neuro]
	def start(self) :
		if self.connected :
			for child in self.connected :
				child.in_weight += self.connected_weight[child] #if something goes wrong change here
class Out() :
	def __init__(self) :
		self.in_weight = 0
		self.max_weight = 0 #if something goes wrong change here
		self.tmp = 0
		self.connected = []
	def show(self) :
		self.tmp = self.in_weight
		self.in_weight = 0
		#print(self.tmp)
		return self.tmp
class Net() : #this class creates only feed forward networks
	def __init__(self) :
		self.in_layer = []
		self.out_layer = []
		self.layers = {}
		self.output = []
	def create_in_layer(self, n) :#for input it got only number of neurons
		self.in_layer = [Giver() for i in range(n)]
	def create_out_layer(self, n) :#for input it got only number of neurons
		self.out_layer = [Out() for i in range(n)]
	def create_layer(self, name,n) : #for input - name of layer and number of neurons
		self.layers[name] = [Neuro() for i in range(n)] #all secret layers in network got they own names
	def create_connection(self, layer_a,a,layer_b,b,weight) : #ist maybe more complicated
		if layer_a == "in" :								  #layer_a is name of layer,a is number of neuron(like in masssive is starts with 0) 
			self.in_layer[a].append_neuro(self.layers[layer_b][b],weight) #layer_b and b is for neuron that will be connected with neuron a 
		elif layer_b == "out" :											  # weight is for weight of this conection	
			self.layers[layer_a][a].append_neuro(self.out_layer[b],weight)
		else :	
			self.layers[layer_a][a].append_neuro(self.layers[layer_b][b],weight)
	def net_work(self, inp) :#for input - just a massive for input layer
		self.output = []
		if len(inp) != len(self.in_layer) :
			return -1
		for l,j in zip(self.in_layer, inp) :
			if j :
				l.start()
		for l in self.layers :
			for n in self.layers[l] :
				n.work()
		for l in self.out_layer :
			self.output.append(l.show())
		print("Input:")
		print(inp)
		print("Output:")
		print(self.output)
		return ",".join(map(str, self.output))
	def set_learning_speed(self, speed) :
		for l in self.layers :
			for n in self.layers[l] :
				n.learn_speed = speed
	def set_max_weight(self, weight) :
		for l in self.layers :
			for n in self.layers[l] :
				n.max_weight = weight			
	def net_learn(self, n,inp) :# for input n - number of epochs,inp - massive for input layer
		for i in range(n) :
			if len(inp) != len(self.in_layer) :
				return -1
			for l,j in zip(self.in_layer,inp) :
				if j :
					l.start()
			for l in self.layers :
				for n in self.layers[l] :
					n.learn()
			for l in self.out_layer :
				l.show()
def load_net(n, file_name,new_net=True) :
	if new_net :
		n.in_layer = []
		n.layers = {}
		n.out_layer = []
	if "\n" in file_name :
		code = file_name.split("\n")
	else :						   #with this feature you can load your nets from a text files 
		code = open(file_name,"r") #and use it in your code
	for line in code :		   #for input is has n - for net object,file_name - for file	
		line = line.split()
		if "#" in line or "//" in line :
			continue
		if "in_layer" in line :
			n.create_in_layer(int(line[1]))
		if "out_layer" in line :
			n.create_out_layer(int(line[1]))
		if "layer" in line :
			n.create_layer(line[1],int(line[2]))
		if len(line) == 5 :
			n.create_connection(line[0],int(line[1]),line[2],int(line[3]),int(line[4]))
		if "set_condition" in line :
			n.layers[line[1]][int(line[2])].condition = int(line[3])
		if "set_weight" in line :
			n.layers[line[1]][int(line[2])].connected_weight[n.layers[line[3]][int(line[4])]] = int(line[5])
			continue
		if "set_max-weight" in line :
			n.layers[line[1]][int(line[2])].max_weight = int(line[3])
		if "all_learning_speed" in line :
			n.set_learning_speed(line[1])
		if "all_max_weight" in line :
			n.set_max_weight(line[1])
		if "all_to_all" in line :
			layers_name = [i for i in n.layers]
			for i in n.in_layer :
				for j in n.layers[layers_name[0]] :
					i.append_neuro(j,1)
			if len(layers_name) >= 2 :
				for i in layers_name :
					if i != layers_name[len(layers_name)-1] :
						for j in n.layers[i] :
							for l in n.layers[layers_name[layers_name.index(i)+1]] :
								j.append_neuro(l,int(line[1]))
			for i in n.layers[layers_name[len(layers_name)-1]] :
				for j in n.out_layer :
					i.append_neuro(j,1)
	if "\n" not in file_name :
		code.close()
def export_net(n, file_name) :
	f = open(file_name, "w")
	if n.in_layer :
		f.write("in_layer {}".format(len(n.in_layer)))
		f.write("\n")
	for i in n.layers :
		f.write("layer {} {}".format(i,len(n.in_layer)))
		f.write("\n")
	if n.out_layer :
		f.write("out_layer {}".format(len(n.out_layer)))
		f.write("\n")
	for i in n.in_layer :
		for j in i.connected :
			f.write(find_neuro(n,i)+" "+find_neuro(n,j)+" "+str(i.connected_weight[j]))
			f.write("\n")
	for layer in n.layers :
		for i in n.layers[layer] :
			for j in i.connected :
				f.write(find_neuro(n,i)+" "+find_neuro(n,j)+" "+str(i.connected_weight[j]))
				f.write("\n")
	f.close()
def find_neuro(n, neuro) :
	if isinstance(neuro, Giver) :
		for i in range(len(n.in_layer)) :
			if n.in_layer[i] == neuro :
				return "in {}".format(i) 
	if isinstance(neuro, Out) :
		for i in range(len(n.out_layer)) :
			if n.out_layer[i] == neuro :
				return "out {}".format(i)
	if isinstance(neuro, Neuro) :
		for i in n.layers :
			for j in range(len(n.layers[i])) :
				if n.layers[i][j] == neuro :
					return "{} {}".format(i,j)