
# -----------------------------------------------------------------------------
import nettoolkit as nt
from nettoolkit import Multi_Execution
import pandas as pd
import PySimpleGUI as sg
from nettoolkit.formitems import *
ping = nt.IP.ping_average
nslookup = nt.nslookup

# -----------------------------------------------------------------------------
def get_first_ips(pfxs, till=5):
	"""selects first (n) ips for each subnets from given prefixes

	Args:
		pfxs (list): list of prefixes
		till (int, optional): how many ips to select. Defaults to 5.

	Returns:
		list: crafted list with first (n) ip addresses from each subnet
	"""	
	new_iplist=[]
	for pfx in pfxs:
		subnet = nt.addressing(pfx)
		try:
			hosts = subnet[1:till+1]
		except:
			hosts =subnet[1:len(subnet)]
		new_iplist.extend([host for host in hosts])
	return new_iplist

# -----------------------------------------------------------------------------
class Ping(Multi_Execution):
	"""Multi Ping class

	Args:
		hosts (str): list of ips to be pinged
		concurrent_connections (int, optional): number of simultaneous pings. Defaults to 1000.
	"""	

	def __init__(self, hosts, concurrent_connections=1000):
		"""instance initializer
		"""		
		self.items = hosts
		self.max_connections = concurrent_connections
		self.ping_results = {}
		self.ping_ms = {}
		self.dns_result = {}
		self.result = {'ping_ms': self.ping_ms, 'dns_result': self.dns_result, 'ping_results': self.ping_results} 
		self.start()

	def execute(self, ip):
		"""executor

		Args:
			ip (str): ip address
		"""		
		self.ping_ms[ip] = ping(ip)
		self.ping_results[ip] = True if self.ping_ms[ip]  else False
		self.dns_result[ip] = nslookup(ip)

	def op_to_xl(self, opfile):
		"""write out result of pings to an output file

		Args:
			opfile (str): output excel file 
		"""		
		df = pd.DataFrame(self.result)
		df.to_excel(opfile, index_label='ip')



def compare_ping_sweeps(first, second):
	"""comparision of two ping result excel files 

	Args:
		first (str): ping result excel file-1
		second (str): ping result excel file-2

	Returns:
		None: Returns None, prints out result on console/screen
	"""	
	#
	df1 = pd.read_excel(first, index_col='ip').fillna('')
	df2 = pd.read_excel(second, index_col='ip').fillna('')
	#
	sdf1 = df1.sort_values(by=['ping_results', 'ip'])
	sdf2 = df2.sort_values(by=['ping_results', 'ip'])
	#
	pinging1 = set(sdf1[(sdf1['ping_results'] == True)].index)
	not_pinging1 = set(sdf1[(sdf1['ping_results'] == False)].index)
	pinging2 = set(sdf2[(sdf2['ping_results'] == True)].index)
	not_pinging2 = set(sdf2[(sdf2['ping_results'] == False)].index)

	# -----------------------------------------------------------------------------

	missing = pinging1.difference(pinging2)
	added = pinging2.difference(pinging1)
	if not missing and not added:
		s = f'All ping responce same, no changes'
		print(s)
		sg.Popup(s)
	else:
		if missing:
			s = f'\n{"="*80}\nips which were pinging, but now not pinging\n{"="*80}\n{missing}\n{"="*80}\n'
			print(s)
			sg.Popup(s)
		if added:
			s = f'\n{"="*80}\nips which were not-pinging, but now it is pinging\n{"="*80}\n{added}\n{"="*80}\n'
			print(s)
			sg.Popup(s)

	return None


# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class SubnetScan():
	'''Subnet Scanner GUI - Inititates a UserForm asking user inputs.	'''

	header = 'Subnet Scanner For First [n] ips of each subnet'
	version = 'v1.0.0'

	# Object Initializer
	def __init__(self):
		self.pfxs = []
		self.op_file = '.'
		self.till = 5
		self.tabs_dic = {
			'Subnet Scan': self.subnet_scanner(),
			'Compare Outputs': self.compare_scanner_outputs(),

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
		self.w = sg.Window(self.header, layout, size=(700,600))#, icon='data/sak.ico')
		while True:
			event, (i) = self.w.Read()
			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event == 'Cancel': 
				break
			if event == 'Go': 

				if i['op_folder'] != '' and i['pfxs'] != "":
					file = 'ping_scan_result_'
					self.op_file = f"{nt.STR.get_logfile_name(i['op_folder'], file, ts=nt.LOG.time_stamp())[:-4]}.xlsx"
					self.pfxs = get_list(i['pfxs'])
					self.till = i['till']
					#
					new_iplist = get_first_ips(self.pfxs, self.till)
					P = Ping(new_iplist)
					P.op_to_xl(self.op_file)

				if i['file1'] != '' and i['file2'] != '':
					self.file1 = i['file1']
					self.file2 = i['file2']
					compare_ping_sweeps(self.file1, self.file2)
				break

		self.w.Close()


	def subnet_scanner(self):
		"""tab display - subnet scanner

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title=None, 
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text('select output folder :',  text_color="yellow"), 
				sg.InputText('', key='op_folder'),   sg.FolderBrowse(),
			],
			under_line(80),
			[sg.Text("Prefixes - enter/comma separated", text_color="yellow")],
			[sg.Multiline("", key='pfxs', autoscroll=True, size=(30,14), disabled=False) ],

			under_line(80),
			[sg.Text('[n]', text_color="yellow"), sg.InputCombo(list(range(1,256)), key='till', size=(20,1))],  
			

			])


	def compare_scanner_outputs(self):
		"""tab display - Compares output of scanner and result

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title=None, 
						relief=sg.RELIEF_SUNKEN, 
						layout=[

			[sg.Text('Select first scanner file :', size=(20, 1), text_color="yellow"), 
				sg.InputText(key='file1'),  
				sg.FileBrowse()],
			under_line(80),

			[sg.Text('Select second scanner file :', size=(20, 1), text_color="yellow"), 
				sg.InputText(key='file2'),  
				sg.FileBrowse()],
			under_line(80),

			])


# -----------------------------------------------------------------------------
# Execute
# -----------------------------------------------------------------------------

if __name__ == '__main__':
	pass
	##

	## 1.
	# pfxs = ['10.10.10.0/24', '10.10.20.0/24']
	# output_file = 'path/filename'
	# ##
	# new_iplist = get_first_ips(pfxs, till)
	# P = Ping(new_iplist)
	# P.op_to_xl(output_file)
	# ##


	## 2.
	# file1 = ''
	# file2 = ''
	# compare_ping_sweeps(first, second)

	# u = SubnetScan()
	# del(u)



	# ----------------------------------------------------------------------