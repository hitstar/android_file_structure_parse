from struct import Struct

from ObFileBase import ObFileBase

class ParseAndroidManifest(ObFileBase):
	def __init__(self, file_buf):
		ObFileBase.__init__(self, file_buf)

		self.header = 8

		self.magic_filesize_structure = "<2I"
		self.filesize_structure = "<I"
		self.type_and_size = "<2I"
		self.str_chunk_stucture = "<7I{0}I{1}I"
		self.resourceid_chunk_structure = "<2I{}I"
		self.namespace_chunk_structure = "<6I"
		self.start_tag_chunk_structure = "<9I{}I"
		self.end_tag_chunk_stucture = "<6I"
		self.text_chunk_structure = "<7I"

		self.start = 0
		self.string_list = []


	def read_type_and_size(self):
		return self.read_obinary_file_chunk(self.start, Struct("<2I"))

	def read_str_chunk(self):
		# read the base information
		str_chunk_top_seven_parsed_tuple = self.read_obinary_file_chunk(self.start, Struct("<7I"))
		str_chunk_type, str_chunk_size, str_count, style_count, \
			unknown, str_pool_offset,	style_pool_offset = str_chunk_top_seven_parsed_tuple

		#read the string chunk
		str_chunk_stucture = Struct(self.str_chunk_stucture.format(str_count, style_count))
		str_chunk_top_nine_parsed_tuple = self.read_obinary_file_chunk(self.start, str_chunk_stucture)

		def inner_read_strings():
			str_off_list = str_chunk_top_nine_parsed_tuple[7: 7 + str_count]
			
			if not style_count :
				str_end_offset = str_chunk_size
			else:
				str_end_offset = style_pool_offset
			
			strs_hex = self.read_obinary_str_content(self.header + str_pool_offset, self.header + str_end_offset)

			tmp_str = ""
			new_result = []
			for i in strs_hex:
				if i < 30 :
					new_result.append(tmp_str)
					tmp_str = ""
				else:
					tmp_str += chr(i)

			str_result = [i for i in new_result if i]
			self.string_list = str_result
		inner_read_strings()
		print


	def read_resourceid_chunk(self, chunk_size):	
		resourceid_chunk_tuple = self.read_obinary_file_chunk(self.start, \
			Struct(self.resourceid_chunk_structure.format(chunk_size/4 -2) ) ) 
		print map(hex, resourceid_chunk_tuple)


	def read_namespace_chunk(self):	
		namespace_chunk_tuple = self.read_obinary_file_chunk(self.start, Struct(self.namespace_chunk_structure))
		print namespace_chunk_tuple	
		
		


	def read_start_tag_chunk(self):	
		attr_count = self.read_obinary_file_chunk(self.start, Struct("<8I"))[-1]
		start_tag_chunk_tuple = self.read_obinary_file_chunk(self.start, \
										Struct(self.start_tag_chunk_structure.format(attr_count * 5)))
		print start_tag_chunk_tuple
	
	def read_end_tag_chunk(self):
		end_tag_chunk_tuple = self.read_obinary_file_chunk(self.start, \
									Struct(self.end_tag_chunk_stucture))
		print end_tag_chunk_tuple

	
	def read_text_chunk(self, start):
		text_chunk_tuple = self.read_obinary_file_chunk(start, \
								Struct(self.text_chunk_structure))



if __name__ == "__main__":
	f = (open("C:\Users\symen\Desktop\crackme02_10_jiagu_sign\AndroidManifest.xml", "rb")).read()
	pam = ParseAndroidManifest(f)
	magic, am_size = pam.read_type_and_size()
	pam.start += 8

	while pam.start < am_size:
		chunk_type, chunk_size = pam.read_type_and_size()
		if chunk_type == 1835009:
			print "string:", 
			pam.read_str_chunk()
		elif chunk_type == 524672:
			print "resource id :",
			pam.read_resourceid_chunk(chunk_size)
		elif chunk_type == 1048832:
			print "start namespace :",
			pam.read_namespace_chunk()
		elif chunk_type == 1048833:
			print "end namespace:",
			pam.read_namespace_chunk()
		elif chunk_type == 1048834:
			print "start tag:",
			pam.read_start_tag_chunk()
		elif chunk_type == 1048835:
			print "end tag:",
			pam.read_end_tag_chunk()
		elif chunk_type == 1048836:
			print "text :",
			pam.read_text_chunk()
		pam.start += chunk_size



	



