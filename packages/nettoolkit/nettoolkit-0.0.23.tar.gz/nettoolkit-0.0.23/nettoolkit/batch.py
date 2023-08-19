""" creates ping script xxxx.bat file for ping test during / after cr
provide prefixes and names of prefixes to it. 
"""

import nettoolkit as nt
import PySimpleGUI as sg
from pprint import pprint
from nettoolkit.formitems import *

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class CreateBatch():
	'''Create Batchfile GUI - Inititates a UserForm asking user inputs.	'''

	header = 'batch file generator'
	version = 'v1.0.0'

	# Object Initializer
	def __init__(self):
		self.dic = {
			# mandatories
			'pfxs':[],
			'names':[],
			'ips':(),
		}
		self.op_folder = '.'
		self.tabs_dic = {
			'Prefixes': self.select_prefixes(),
			'Prefix Names': self.select_names(),
			'ip(s)': self.select_ips(),
			'Output Folder': self.select_file_path(),

		}
		self.create_form()


	def create_form(self):
		"""initialize the form, and keep it open until some event happens.
		"""    		
		layout = [
			banner(self.version), 
			button_pallete(),
			tabs_display(**self.tabs_dic),
		]
		self.w = sg.Window(self.header, layout, size=(700,500))#, icon='data/sak.ico')
		while True:
			event, (i) = self.w.Read()
			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event == 'Cancel': 
				# del(self.dic)
				break
			if event == 'Go': 
				# update self.dic
				for k in self.dic:
					self.dic[k] = get_list(i[k])
				self.op_folder = i['op_folder']
				break
		self.w.Close()
		for ip in self.dic['ips']:
			success = create_batch_file(self.dic['pfxs'], self.dic['names'], ip, self.op_folder)
		if success:
			s = 'batch file creation process complete. please verify'
			print(s)
			sg.Popup(s)
		else:
			s = 'batch file creation process encounter errors. please verify inputs'
			print(s)
			sg.Popup(s)

	def select_file_path(self):
		"""select output files 

		Returns:
			sg.Frame: Frame with input data components
		"""    		
		return sg.Frame(title=None, 
						layout=[
			[sg.Text('output folder:', text_color="yellow"), 
				sg.InputText('', key='op_folder'),  
				sg.FolderBrowse(),
			],
			under_line(80),
			[sg.Text("batch file(s) will be generated at provide output folder path")],
			])


	def select_prefixes(self):
		"""selection of tab display - prefixes

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title=None, 
						layout=[
			[sg.Text("Provide Prefixes", text_color="yellow")],
			[sg.Multiline("", key='pfxs', autoscroll=True, size=(30,10), disabled=False) ],
			under_line(80),
			[sg.Text("Entries can be line(Enter) or comma(,) separated")],
			[sg.Text("Example: \n10.10.10.0/24\n10.10.30.0/24,10.10.50.0/25")],
			under_line(80),
			[sg.Text("Entries of Prefixes and Prefix Names should match exactly")],
			])

	def select_names(self):
		"""selection of tab display - prefixes names

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title=None, 
						layout=[
			[sg.Text("Provide Prefix Names", text_color="yellow")],
			[sg.Multiline("", key='names', autoscroll=True, size=(30,10), disabled=False) ],
			under_line(80),
			[sg.Text("Entries can be line(Enter) or comma(,) separated")],
			[sg.Text("Example: \nVlan-1\nVlan-2,Loopback0")],
			under_line(80),
			[sg.Text("Entries of Prefixes and Prefix Names should match exactly")],
			])

	def select_ips(self):
		"""selection of tab display - ips

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title=None, 
						layout=[
			[sg.Text("Provide ip(s)", text_color="yellow")],
			[sg.Multiline("", key='ips', autoscroll=True, size=(10,5), disabled=False) ],
			under_line(80),
			[sg.Text("Entries can be line(Enter) or comma(,) separated")],
			under_line(80),
			[sg.Text("Example: \n1\n3,4,5")],
			under_line(80),
			[sg.Text("one batch file will generate for each ip")],
			])


# ------------------------------------
def create_batch_file(pfxs, names, ip, op_folder):
	"""creates batch file(s)

	Args:
		pfxs (list): list of prefixes
		names (list): list of prefix names
		ip (list): ip(s) for which batch file(s) to be created
		op_folder (str): output folder where batch file(s) should be created

	Returns:
		bool, None: Result of outcome
	"""	
	if not isinstance(ip, int):
		try:
			ip = int(ip)
		except:
			s = f"incorrect ip detected .`{ip}`, will be skipped"
			sg.Popup(s)
			print(s)
			return None
	if not op_folder:
		s = f'Mandatory argument output folder was missing.\ncould not proceed, check inputs\n'
		sg.Popup(s)
		print(s)
		return None
	op_batch_filename = f"{op_folder}/ping_test-ips-.{ip}.bat"  
	#
	if not isinstance(pfxs, (list, tuple)):
		s = f'Wrong type of prefix list \n{pfxs}, \ncould not proceed, check inputs\nExpected <class "list"> or <class "tuple">, got {type(pfxs)}\n'
		sg.Popup(s)
		print(s)
		return None
	if not isinstance(names, (list, tuple)):
		s = f'Wrong type of name list \n{names}, \ncould not proceed, check inputs\nExpected <class "list"> or <class "tuple">, got {type(names)}\n'
		sg.Popup(s)
		print(s)
		return None
	if len(pfxs) != len(names):
		s = "length of prefixes mismatch with length of names. both should be of same length \ncould not proceed, check inputs"
		sg.Popup(s)
		print(s)
		return None
	#
	# ------------------------------------
	list_of_ips = add_ips_to_lists(pfxs, ip)
	s = create_batch_file_string(list_of_ips, names)
	write_out_batch_file(op_batch_filename, s)
	# ------------------------------------
	return True

def add_ips_to_lists(pfxs, n):
	"""create list of ip addresses for given nth ip from given prefixes 

	Args:
		pfxs (list): list of subnets/prefixes
		n (int): nth ip address

	Returns:
		list: crafted list of ip addresses
	"""	
	list_of_1_ips = []
	for pfx in pfxs:
		subnet = nt.addressing(pfx)
		try:
			ip1 = subnet[n]
			list_of_1_ips.append(ip1)
		except:
			pass
	return list_of_1_ips

def create_batch_file_string(lst, names):
	"""get the output batch file content

	Args:
		lst (list): list of prefixes
		names (list): list of prefix names

	Returns:
		str: output batch file content
	"""	
	s = ''
	for ip, name in zip(lst, names):
		s += f'start "{name}" ping -t {ip}\n'
	return s


def write_out_batch_file(op_batch_filename, s):
	"""write the output batch file.

	Args:
		op_batch_filename (str): output file name
		s (str): mutliline string to write to file
	"""	
	print(f'creating batch file {op_batch_filename}')
	with open(op_batch_filename, 'w') as f:
		f.write(s)

# ------------------------------------

if __name__ == '__main__':
	pass
	# ------------------------------------
	# TEST
	# ------------------------------------
	# u = CreateBatch()
	# del(u)

