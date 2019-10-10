#Peter Malinovsky
#605277
#Booz Allen Hamilton
#Summer Games 2019


# Basic tree creator from the custom Node class for use in designing custom RoE profiles that changes the behavior of the main EFOC program.

from menu_tree import Node


root = Node('', '')
current = root
root.importFromFile('save.profile')


while True:

	print('************')
	print('Current Node\n')
	current.printNode()
	print('************\n')

	print('0 - Exit')
	print('1 - Edit menu name')
	print('2 - Edit children label')
	print('3 - Add child')
	print('4 - Print Tree')
	print('5 - Move to child')
	print('6 - Move to parent')
	val = input('Please enter choice: ')
	val = int(val)

	if val == 0:
		#exit()
		break
	elif val == 1:
		name = input('Enter a new title for the current menu: ')
		current.setTitle(name)
	elif val == 2:
		current.printChildLabels()
		index = input('Enter label ID to edit: ')
		label = input('Enter new label: ')
		current.editChildLabel(int(index), label)
	elif val == 3:
		title = input('Enter menu title: ')
		content = input('Enter content for menu: ')
		label = input('Enter label for menu: ')
		current.addChild(title, content, label)
	elif val == 4:
		root.print()
	elif val == 5:
		current.printChildLabels()
		index = input('Enter child to move to: ')
		current = current.getChild(int(index))
	elif val == 6:
		current = current.getParent()


save = root.export()

f = open("save.profile", "w+")
f.write(save)
f.close()
