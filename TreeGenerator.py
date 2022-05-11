import sys
import os

NATIVE = '\033[m'
DARK_GRAY = '\033[90'
DARK_BLUE = '\033[34m'
CYAN = '\033[96'

USE_COLOR = False

def ForegroundColor(color):
    if (USE_COLOR):
        sys.stdout.write(color)

def ResetColor():
    if (USE_COLOR):
        sys.stdout.write(NATIVE)

def IsDirectory(node, source):
    os.path.isdir(os.path.join(source, node))

def GetChildren(node, source):
    if (os.path.isfile(os.path.join(source, node))):
        return []

    fullpath = node
    if (source != None and source != ""):
        fullpath = os.path.join(source, fullpath)

    files = [f for f in os.listdir(fullpath) if os.path.isfile(os.path.join(fullpath, f))]
    dirs = [d for d in os.listdir(fullpath) if os.path.isdir(os.path.join(fullpath, d))]

    return dirs + files

def PrintTree(writer, node, source = "", indent = "", isLast = True, depth = None, curDepth = 0):
    isConsoleOut = writer == sys.stdout

    if (isConsoleOut):
        ForegroundColor(DARK_GRAY)

    marker = None

    if (isLast):
        marker = "└─"
    else:
        marker = "├─"

    writer.write(f"{indent}{marker}")

    if (isConsoleOut):
        if (IsDirectory(node, source)):
            ForegroundColor(DARK_BLUE)
        else:
            ForegroundColor(CYAN)

    writer.write(f"{node}\n")

    if (isConsoleOut):
        ResetColor()

    if (isLast):
        indent += "  "
    else:
        indent += "│ "

    if (curDepth == depth):
        return

    children = GetChildren(node, source)
    lastChild = None

    if (len(children) > 0):
        if (source == None or source == ""):
            source = node
        else:
            source = os.path.join(source, node)

        lastChild = children[-1]

    for child in children:
        PrintTree(writer, child, source, indent, child == lastChild, depth, curDepth + 1)

def Main():
    PrintTree(sys.stdout, "./")

if __name__ == "__main__":
    Main()
