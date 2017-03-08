from struct import Struct

class ObFileBase(object):
	def __init__(self, file_buf):
		self.f = file_buf 

	def read_obinary_file_chunk(self, start, format_struct):
		# unpack -> string to obinary according to the base file format
		#return a tuple match format struct 
		
		return format_struct.unpack((self.f[start:start + format_struct.size]))

	def read_obinary_str_content(self, start, end):
		# pass
		# # print self.f
		# # print map(hex, self.f[start:end])
		# print self.f[start:end]
		print (end - start)
		return  Struct("<{}H".format((end - start)/2)).unpack(self.f[start:end])
