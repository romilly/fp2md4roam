# Mind Map to Markdown for Roam import

Got a Mind Map  with contents you'd like to import into Roam?

This Python application might do what just you want.

It will take a Freeplane `.mm` Mind Map file and convert it into Markdown ready for manual import into Roam.

I *think* Freemind mind maps should also work, but I have not yet tested them.

It's currently in early beta. 

## Features

The generated markdown file will have a hierarchy of bullet points
that match the branches of the Mind Map.

For each branch that has a *description*, the text of the description
will be appended to the branch title, starting on the line below.

If a branch has a link to a web page a link will be generated in the markdown
file.

Rich text is supported in branch titles and descriptions.

## Requirements

You need Python >= 3.8 and a recent version of pip3.

## Installation

`pip3 install fp2md4roam`

## Use

From a command line, run
`convert_map <path_to_mind_map> <target_directory>`

So, if you have a mind map file `my_map.mm`, and type
`convert_map my_map.mm foo` with a root node called `My Smart Mind Map`
this will create a file called `MySmartMindMap.md` in the output directory `foo`.

You can then import the `MySmartMap.md` into Roam in the usual way.

When Roam imports a Markdown file it will ask you what
name you want for the page after import.

Since this application will remove spaces and punctuation for the generated file name
you may want to alter the page name before you import it.

### Example:




