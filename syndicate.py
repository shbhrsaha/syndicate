# this script converts your markdown into a production-ready web site

import os, sys, csv, argparse

# get optional command-line arguments
parser = argparse.ArgumentParser("Turn Markdown files into static web sites.")
parser.add_argument('template_file', metavar='template', nargs='?', default="post.html", help='post template file')
parser.add_argument('--gfm', dest='gfm', action='store_const', const=True, default=False, help='activate github-flavored markdown')
args = parser.parse_args()

# gather template file HTML
templateHTML = file(args.template_file, "rb").read()

# iterate over all markdown files in this directory and subdirectories

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
FILENAME_MATCH = "markdown.txt"

# a list of all the files in ROOT_DIRECTORY that match FILENAME_MATCH
csv_files = [os.path.join(root, name)
             for root, dirs, files in os.walk(ROOT_DIRECTORY)
             for name in files
             if name == FILENAME_MATCH]

# set compilation function
compile_markdown = "ruby gfm.rb %s | perl markdown.pl > temp.txt" if args.gfm else "perl markdown.pl %s > temp.txt"

for file_path in csv_files:

    print "Producing " + file_path

    # determine the current directory
    pathArray = file_path.split("/")
    del(pathArray[-1])
    directory = "/".join(pathArray)

    sys.stdout.flush()

    # extract the title from the markdown
    with open(file_path, 'r') as f:
        title = f.readline()
    while title[0] == "#" or title[0] == " ":
        title = title[1:]

    # run the converter and output to a temp.txt
    os.system(compile_markdown % file_path)

    # now read the output from temp.txt and inject into post.html
    temp_file = open("temp.txt", "rb")
    tempHTML = temp_file.read()

    productionHTML = templateHTML.replace("{{ title }}", title)
    productionHTML = productionHTML.replace("{{ body }}", tempHTML)

    # write that production output to index.html in original directory
    productionFile = open(directory+"/index.html", "w")
    productionFile.write(productionHTML)

if os.path.exists("temp.txt"):
    os.system("rm temp.txt")
print "Production complete."
