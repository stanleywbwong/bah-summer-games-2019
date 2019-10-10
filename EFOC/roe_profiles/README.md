<!-- language: lang-none -->

# RoE Profiles 

The Rules of Engagement Profiles dictates the behavior of the EFOC, allowing a
user to create their own custom behavior. To add additional profiles, you can
either use the tree_creator script found in the menu_tree folder, or you can
write a text file containing the RoE. To add it to the EFOC program, simply
place the .profile file in this roe_profile folder and start the program.

## RoE Format 

The format used to store the RoE profiles is an attempt to store a tree in a
json format. The structure is as follows: 

    {
    "title": "",
    "content": "",
    "children_label": [],
    "children": []
    }
    
The number of elements in children_label must match the number of children in
each node of the tree, a child must have an associated label. There is no limit
to the size of the tree that can be created from this structure. 

There is no error handling in the format while importing the .profile, so make
sure the format matches the format of the other profiles in this folder.
