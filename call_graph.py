import sys
import re

def main():
    filename = sys.argv[1]
    f = open(filename)
    line = [x[:-1].strip() for x in f.readlines()] # strip and remove \n
    line = [x for x in line if len(x) >= 1 and x[0] != ';'] # filter out empty line and comments

    s = " ".join(line)

    # process block comment
    while True:
        l = s.find("#|")
        if l != -1 :
            r = s.find("|#")
            s = s[:l] + s[r+2:]
        else:
            break

    # process function comment
    while True:
        l = s.find("#;")
        if l != -1:
            r = l + 2
            stack = []
            while r < len(s):
                if s[r] == '(':
                    stack.append(s[r])
                elif s[r] == ')':
                    stack.pop()
                    if not stack:
                        break;
                r += 1

            s = s[:l] + s[r+1:]
        else:
            break

    st = []
    main = False
    fundef = False
    funname = None
    namelist = []
    i = 0
    d = []
    while i < len(s):
        c = s[i]
        if c == '(': # open an expression
            if not st: # open an expression
                main = True
            st.append(i)
            if fundef: # previous keyword is define
                fundef = False
                funname = s[i+1: s.find(' ', i)]
                namelist.append(funname)

        elif c == ')': # close an expression
            main = False
            fundef = False 
            tmp = st.pop()
            if not st: # stack is empty, got an complete expression
                if funname is not None: # find a function define
                    funstr = s[s.find(')', tmp)+1: i].strip()
                    print(funname + ": ")
                    print(set(re.findall('[^\s\(\)\[\]]+', funstr)))
                    d.append((funname, set(re.findall('[^\s\(\)\[\]]+', funstr))))
                    funname = None
        else:
            fundef = False # next keyword of define is not `(`
            if main:
                main = False
                if s[i:i+7] == "define ": # define an function
                    fundef = True
                    i += 6 # skip `define`

        i += 1

    f = open("callgraph.dot", "w")

    print("strict digraph {", file=f)
    for key, value in d:
        for v in value:
            if v in namelist:
                print('\t"{0}" -> "{1}"'.format(key, v), file=f)

    print("}", file=f)

    print("Done ^_^.")

if __name__ == "__main__":
    main()

