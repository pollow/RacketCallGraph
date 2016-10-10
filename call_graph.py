import sys
import re

def main():
    filename = sys.argv[1]
    f = open(filename)
    line = [x[:-1].strip() for x in f.readlines()] # strip and remove \n
    print("Lines: " + str(len(line)))
    line = [x for x in line if len(x) >= 1 and x[0] != ';'] # filter out empty line and comments

    s = " ".join(line)
    print("Chars: " + str(len(s)))

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
            print("DEBUG: {} @ {}, {} {}".format(s[i:i+10], i, len(st), main))
            if fundef: # previous keyword is define
                fundef = False
                funname = s[i+1: s.find(' ', i)]
                namelist.append(funname)
                print("Function Name: " + funname + " " + str(i))

        elif c == ')': # close an expression
            main = False
            fundef = False 
            tmp = st.pop()
            print("DEBUG: {} @ {}, {} {}".format(s[i-5:i+5], i, len(st), main))
            if not st: # stack is empty, got an complete expression
                if funname is not None: # find a function define
                    funstr = s[s.find(')', tmp)+1: i].strip()
                    # print(funname+ ": ")
                    # print(re.findall('[\w|\d|-]+', funstr))
                    d.append((funname, set(re.findall('[^\s\(\)]+', funstr))))
                    funname = None
        else:
            fundef = False # next keyword of define is not `(`
            if main:
                main = False
                if s[i:i+7] == "define ": # define an function
                    fundef = True
                    i += 6 # skip `define`

        i += 1

    print(namelist)
    f = open("callgraph.dot", "w")

    print("strict digraph {", file=f)
    for key, value in d:
        for v in value:
            if v in namelist:
                print('\t"{0}" -> "{1}"'.format(key, v), file=f)

    print("}", file=f)
        

if __name__ == "__main__":
    main()

