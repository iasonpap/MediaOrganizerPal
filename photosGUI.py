import PySimpleGUI as sg
import utilities as util


sg.theme('DarkAmber')

layout = [
	[sg.Text('Filename')],
	[],
	[],
	[sg.Input(), sg.FileBrowse()],
	[sg.Button('Ok'), sg.Button('Cancel')]
]

window = sg.Window('Photos Organiser', layout)

while True:
	event, values = window.read()
	util.debug(event)
	util.debug(values)
	if event == sg.WIN_CLOSED or event == 'Cancel': 
		break

window.close()