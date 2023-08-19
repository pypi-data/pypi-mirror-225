__doc__ = '''Tool Set for Networking Geeks
-------------------------------------------------------------------
JSet, IPv4, IPv6, addressing, Validation,
Default, Container, Numeric, STR, IO, LST, DIC, LOG, DB, IP,
DifferenceDict, DictMethods
-------------------------------------------------------------------
 Juniper      various juniper config operations
 IPv4         IPV4 Object, and its operations
 IPv6         IPV4 Object, and its operations
 addressing   dynamic allocation of IPv4/IPv6 Objects
 Validation   Validate subnet
 Default      default implementations of docstring
 Container    default identical dunder methods implementations
 Numeric      To be implemented later
 STR          String Operations static methods 
 IO           Input/Output of text files Operations static methods 
 LST          List Operations static methods 
 DIC          Dictionary Operations static methods 
 DifferenceDict Differences between dictionaries
 DictMethods  Common Dictionary Methods
 LOG          Logging Operations static methods 
 DB           Database Operations static methods 
 IP           IP Addressing Operations static methods 
 ... and many more
-------------------------------------------------------------------
'''

__all__ = [
	# .juniper
	'Juniper',
	# Jset
	'JSet',
	# .addressing
	'IPv4', 'IPv6', 'addressing', 'Validation', 'get_summaries', 'isSubset',
	'binsubnet', 'bin2dec', 'bin2decmask', 'to_dec_mask', 'bin_mask', 'Routes', 'invmask_to_mask',
	# .gpl
	'Default', 'Container', 'Numeric', 'DifferenceDict', 
	'STR', 'IO', 'LST', 'DIC', 'LOG', 'DB', 'IP', 'XL_READ', 'XL_WRITE', 
	'DictMethods', 'Multi_Execution', 'nslookup', 'standardize_if', 'get_username', 'get_password',
	# .convertdict
	'ConvDict',
	# cpw_cracker
	'encrypt_type7', 'decrypt_type7', 'decrypt_file_passwords', 'mask_file_passwords',
	# jpw_cracker
	'juniper_decrypt', 'juniper_encrypt', 'decrypt_doller9_file_passwords', 'mask_doller9_file_passwords',

	# common
	"remove_domain", "read_file", "get_op", "blank_line", "get_device_manufacturar", "verifid_output", 
	"get_string_part", "get_string_trailing", "standardize_mac", "mac_2digit_separated", "mac_4digit_separated", 
	"flatten", "dataframe_generate",

	#databse
	"write_to_xl", "append_to_xl", "read_xl",

	#batch
	"CreateBatch", "create_batch_file",

	#subnetscan
	"SubnetScan", "compare_ping_sweeps", "get_first_ips", "Ping",

	]

__version__ = "0.0.23"

from .juniper import Juniper
from .jset import JSet

from .addressing import (
	IPv4, IPv6, addressing, Validation, get_summaries, isSubset,
	binsubnet, bin2dec, bin2decmask, to_dec_mask, bin_mask, Routes, invmask_to_mask,
	)

from .gpl import (Default, Container, Numeric, 
	DifferenceDict, DictMethods, DIC,
	STR, IO, LST, LOG, DB, IP, XL_READ, XL_WRITE, 
	Multi_Execution, nslookup, standardize_if,
	get_username, get_password,
	)

from .convertdict import ConvDict
from .cpw_cracker import decrypt_type7, encrypt_type7, decrypt_file_passwords, mask_file_passwords
from .jpw_cracker import juniper_decrypt, juniper_encrypt, decrypt_doller9_file_passwords, mask_doller9_file_passwords

from .common import (
	remove_domain, read_file, get_op, blank_line, get_device_manufacturar, verifid_output, 
	get_string_part, get_string_trailing, standardize_mac, mac_2digit_separated, mac_4digit_separated, 
	flatten, dataframe_generate
	)


from .database import write_to_xl, append_to_xl, read_xl

from .batch import CreateBatch, create_batch_file

from .subnetscan import SubnetScan, compare_ping_sweeps, get_first_ips, Ping
