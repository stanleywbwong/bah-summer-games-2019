#Peter Malinovsky
#605277
#Booz Allen Hamilton
#Summer Games 2019


import json


# Node class the contains the data parameters of the menu options in the dynamic RoE
# Once an inital note is created, multiple child nodes can be created representing difference choices and their respective properties. These children nodes can then contain children and so on.
# A tree can be both imported and exported from a file, in the context of the RoE they are .profile files. The format follows the JSON standard and can be edited from a text editor to create or modify the properties of a tree.

# Data Structure
#     Parent
#      -Title
#      -Message content
#      -Menu ID (Auto-generated)
#      -List of children nodes
#      -List of labels to get to children nodes, user's choice

#     Node 0 - Content [Question 1]
#       Children [Node 01, Node 02]
#       Children Labels [Answer 1(goes to Node 01), Answer 2(goes to Node 02)]
#
#         Node 01 - Content [Statement]
#           Children []
#           Children Label []
#         Node 02 - Content [Statement]
#           Children []
#           Children Labels []

class Node:
	def __init__(self, title, content, menuID = '0', parent = None):

		if parent == None:
			self.parent = self
		else:
			self.parent = parent

		self.children = []
		self.children_label = []
		self.childcount = 0
		self.title = title
		self.content = content
		self.menuID = menuID


	def setTitle(self, new_title):
		self.title = new_title


	def setContent(self, content):
		self.content = content


	def editChildLabel(self, childID, new_label):
		self.children_label[childID] = new_label


	def addChild(self, title, content, label):
		self.childcount += 1
		self.children.append(Node(title, content, self.menuID + str(self.childcount), self))
		self.children_label.append(label)
		return self.children[-1]


	def getChild(self, index):
		print(index)
		return self.children[index]


	def getParent(self):
		return self.parent


	def getTitle(self):
		return self.title


	def getContent(self):
		return self.content


	def getChildLabel(self, index):
		return self.children_label[index]


	def getChildren(self):
		return self.children_label


	def getChildCount(self):
		return self.childcount


	def printNode(self):
		print(self.menuID)
		print(self.title)
		print(self.content)
		print()


	def print(self):
		self.printNode()
		for elem in self.children:
			elem.print()


	def printChildLabels(self):
		for i in range(len(self.children_label)):
			print(str(i) + ' - ' + self.children_label[i])


	def export(self):
		s = '\n{\n' + \
			'\"title\": \"' + self.title + '\",\n\"content\": \"' + self.content + '\",\n'\
			'\"children_label\": ' + self.exportChildrenLabel() + ',\n' + \
			'\"children\": ' + self.exportChildren() + '\n}'
		return s


	def exportChildren(self):
		s = '['
		for elem in self.children:
			s += elem.export() + ','
		if s != '[':
			s = s[0:-1] + '\n]'
		else:
			s += ']'
		return s


	def exportChildrenLabel(self):
		s = '['
		for elem in self.children_label:
			s += '\n{\"label\":\"' + elem + '\"},'
		if s != '[':
			s = '\n' + s
			s = s[0:-1] + '\n]'
		else:
			s += ']'
		return s


	def importFromFile(self, filename):

		with open(filename, "r") as read_file:
			data = json.load(read_file)

			title = data['title']
			content = data['content']
			children_label = data['children_label']
			children = data['children']

			self.setTitle(title)
			self.setContent(content)
			self.importChildren(children_label, children)


	def importChildren(self, children_label, children):
		for i in range(len(children_label)):
			label = children_label[i]['label']
			title = children[i]['title']
			content = children[i]['content']
			c_l = children[i]['children_label']
			c = children[i]['children']

			new = self.addChild(title, content, label)
			new.importChildren(c_l, c)