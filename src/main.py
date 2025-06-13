import os
import shutil
from textnode import TextNode, TextType
from convert import *

def create_dir(destination):
    if not os.path.exists(destination):
        print(f"- Creating directory {destination}")
        os.mkdir(destination)
        if os.path.exists(destination):
            print(f"- Directory {destination} created.")
        else:
            raise Exception(f"Could not create directory {destination}!")

def copy_from_dir_to_dir(source, destination):
    # delete all from destination, file and dir
    if os.path.exists(destination):
        print(f"- Found directory {destination}. Deleting content")
        shutil.rmtree(destination)
        if os.path.exists(destination):
            raise Exception(f"Could not delete directory {destination}!")
        create_dir(destination)
    # or create dir that does not exist
    else:
        create_dir(destination)

    # copy all file from source to destination
    for filename in os.listdir(source):
        if os.path.isfile(f"{source}/{filename}"):
            print(f"- Copying file {source}/{filename} into {destination}")
            shutil.copy(f"{source}/{filename}", f"{destination}/")
        elif os.path.isdir(f"{source}/{filename}"):
            print(f"- Found directory {source}/{filename}")
            copy_from_dir_to_dir(f"{source}/{filename}", f"{destination}/{filename}")
        else:
            raise Exception(f"Unkown file/dir {source}/{filename} found")


def extract_title(markdown):
        if markdown.split("\n")[0][0:2] == "# ":
            return markdown.split("\n")[0][2:]
        else:
            raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"\n- Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as content_file:
        markdown = content_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    with open(dest_path, "w") as dest_html:
        dest_html.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        create_dir(dest_dir_path)
    for filename in os.listdir(dir_path_content):
        if os.path.isfile(f"{dir_path_content}/{filename}"):
            print(f"- Generating file {dir_path_content}/{filename} into {dest_dir_path}")
            generate_page(f"{dir_path_content}/{filename}", template_path, f"{dest_dir_path}/{filename.replace('.md','.html')}")
        elif os.path.isdir(f"{dir_path_content}/{filename}"):
            print(f"- Found directory {dir_path_content}/{filename}")
            generate_pages_recursive(f"{dir_path_content}/{filename}", template_path, f"{dest_dir_path}/{filename}")
        else:
            raise Exception(f"Unkown file/dir {dir_path_content}/{filename} found")

def main():
    #Node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(Node)
    print("## STARTING PROGRAM ##")
    source_dir = "static"
    destination_dir = "public"
    copy_from_dir_to_dir(source_dir, destination_dir)

    generate_pages_recursive("content", "template.html", "public")
 
if __name__ == "__main__":
    main()
