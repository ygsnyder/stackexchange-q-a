
import os
import re
import locale
import ast
import time

stream = os.popen('echo Returned output')
output =  stream.read()
print(output)


def is_valid_python(code):
   try:
       ast.parse(code)
   except SyntaxError:
       return False
   return True

#add Python snippets to file for transpiling
with open ('./initialPythonIntents.txt','r', encoding='utf-8') as initialIntents, open ('./initialPythonSnippets.txt','r', encoding='utf-8') as initialSnippets:
    with open ('./preTransProcessedIntents.txt', 'w') as processedIntents, open('./preTransProcessedSnippets.txt', 'w') as processedSnippets:
        initialIntentLine = initialIntents.readline()
        initialSnippetLine = initialSnippets.readline()
        count = 0
        while initialSnippetLine:
            print(initialIntentLine)
            print(initialSnippetLine)
            print('processing snippet %s: ' %count + initialSnippetLine)
            #
            # Check for invalid/non-ascii characters
            #
            try:
                mynewstring = initialSnippetLine.encode('ascii')
                print('is ascii')
            except UnicodeEncodeError:
                print("there are non-ascii characters in there - ommitting line %s in output file" %count)
                initialIntentLine = initialIntents.readline()
                initialSnippetLine = initialSnippets.readline()
                count += 1
                continue
            #
            # Remove in-line comments
            #
            initialSnippetLine = re.sub('#SPACE#',' ',initialSnippetLine)
            initialSnippetLine = re.sub('#NEWLINE#','\n', initialSnippetLine)
            initialSnippetLine = re.sub('#INDENT#','    ', initialSnippetLine)

            #
            # Removes 'return'  & 'del' for lines beginning with return and del statements
            #
            if (initialSnippetLine.startswith('return')):
                initialSnippetLine = initialSnippetLine.replace('return ', '', 1)
            
            if (initialSnippetLine.startswith('del ')):
                initialSnippetLine = initialSnippetLine.replace('del ', 'delete', 1)

            #
            # Checks for valid Python Syntax
            #
            if (is_valid_python(initialSnippetLine)):
                print('valid')
                
                processedSnippets.write('delimiter\n')
                processedSnippets.write('%s' %initialSnippetLine)
                processedIntents.write('%s' %initialIntentLine)
                
            else:
                print('invalid') 
            
            
            # next line
            initialIntentLine = initialIntents.readline()
            initialSnippetLine = initialSnippets.readline()
            count += 1
    

# Create the Py file with filtered snippets
with open('./preTransProcessedSnippets.txt','r', encoding='utf-8') as infile, open('./P2JSnippets.py','w') as P2J:
    line = infile.readline()
    while line:
        P2J.write('%s' %line)
        
        line = infile.readline()

#
# Trancrypt Python to JavaScript
#
print(locale.getpreferredencoding())
os.system('transcrypt -n ./P2JSnippets.py')


while not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)))):
    print('not ready')
    time.sleep(10)

print('#######################################################')
#
# Parse the transpiled JavaScript to create the final .snippet file (Output.txt) that corresponds to preTransProccessedIntent.txt
#
with open (os.path.join(os.path.dirname(os.path.abspath(__file__)), '__target__\P2JSnippets.js'), 'r') as infile, open('Output.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace('\r','').replace('\n','').replace('export ','').split('delimiter;')

    data.pop(0)
    print(data[-1])
    data[-1] = data[-1].replace('//# sourceMappingURL=P2JSnippets.map', '')
    print(data[-1])

    for line in data:
        outfile.write(line + "\n")
    print('done')

#
# Log Errors with JSLint to lintederrors.txt
#
print(locale.getpreferredencoding())
os.system('node .\jslinter.js')