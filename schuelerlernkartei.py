import pandas as pd
import os
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import webbrowser

files = []
if len(sys.argv) > 1 and sys.argv[1] == '*': # Search current directory from which script is executed for .csv files and process them all
    for file in os.listdir("."):
        if file.endswith(".csv"):
            files.append(file)
elif len(sys.argv) > 1: # Interpret first argument as file path and process
    for i in range(1, len(sys.argv)):
        if os.path.isfile(sys.argv[i]):
            files.append(sys.argv[i])

if len(files) == 0: # Open file dialog if no csv file was selected until here
    ftypes = [('CSV', '*.csv')]
    Tk().withdraw()
    filenames = askopenfilenames(filetypes=ftypes)
    for filename in filenames:
        files.append(filename)

for file in files:
    data = pd.read_csv(file, delimiter=';')
    klasse = file.rsplit( ".", 1 )[ 0 ]
    print(klasse)
    dictionary = data.to_dict('list')
    
    output = '<html>\n<head><title>'+klasse+'</title>'
    output += '<style>@media print { div { break-inside: avoid; } } @page { margin: 0; } * { box-sizing: border-box; } '
    output += 'table { width: 100%; }'
    output += 'th { text-align: left; } h1 { text-align: center; } body { margin: 0; }</style></head>\n<body>\n'
    
    cols = 6
    height = 187
    
    output += '<div style="page-break-before: always;">'
    output += '<table cellspacing="0" cellpadding="0" width="100%">\n\n'
    for i in dictionary['#']:
        kz = str(dictionary["Schülerkennzahl"][int(i)-1])
        img = "https://www.sokrates-bund.at/SOKB/PupilPicture/92041720250538.jpg" #"https://www.sokrates-bund.at/SOKB/PupilPicture/" + kz + ".jpg"
        if (i-1) % cols == 0:
            output += '<tr>'
        output += '<td width="16.66%" height="'+str(height)+'" valign="center" align="center" style="border: 1px dashed lightgray;">'
        output += '<img src="'+img+'" height="133"></td>'
        if (i-1) % cols == (cols-1):
            output += '</tr>'
    output += '</table></div>\n'
    
    
    output += '<div style="page-break-before: always;">'
    output += '<table cellspacing="0" cellpadding="0" width="100%">\n\n'
    for i in dictionary['#']:
        z = int((i-1) / cols)
        mi = (z+1)*cols - ((i-1) % cols)-1
        vorname = "Maximilian" #dictionary["Vorname"][mi]
        familienname = "Mustermann" #dictionary["Familienname"][mi]
        if (i-1) % cols == 0:
            output += '<tr>'
        output += '<td width="16.66%" height="'+str(height)+'" valign="center" align="center">'
        output += '<h2>'+vorname+'</h2><h3>'+familienname+'</h3><p>'+klasse+'</p></td>'
        if (i-1) % cols == (cols-1):
            output += '</tr>'
    output += '</table></div>\n'
    
    output += '</body></html>'
    #print(output)
    with open(klasse + '.html', 'w', encoding='utf-8') as f:
        f.write(output)
        webbrowser.open('file://' + os.path.realpath(klasse + '.html'))