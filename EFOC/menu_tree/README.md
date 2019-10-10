# RoE Profile Menu Tree 

To create the different profiles for the RoE behavior, a tree was used to encode
decisions to actions. The tree is composed of Nodes found in the menu_tree file
which each contain a title, content, a list of child labels and a list of the
child nodes. The list of child labels and child nodes is a one to one mapping,
so they must be the same length and in the same order. The node title is the
title of the popup window and the content is the message that is displayed
inside the popup window. If the operator should have the ability to choose
certain responses to narrow down the scope of their action, each response is
stored as a child label. When the child label is selected on the parent window,
the child node is pulled out of the node list and becomes the current active
node. This is how the tree is traversed. The back button moves you back up the
tree until you reach the root node.

## Creating New Profiles 

To get started, you can either copy and modify an existing profile or use the
tree_creator to create or modify a tree. The tree_creator can import and export
trees and allows you to modify, print, and view the structure of your RoE tree
before loading it into the main GUI.