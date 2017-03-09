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
		self.resourceid_chunk_tuple =()
		self.namespace_chunk_tuple = ()
		self.start_tag_chunk_tuple = ()
		self.end_tag_chunk_tuple = ()


	def read_type_and_size(self):
		return self.read_obinary_file_chunk(self.start, "<2I")

	def read_str_chunk(self):
		# read the base information
		str_chunk_top_seven_parsed_tuple = self.read_obinary_file_chunk(self.start, "<7I")
		str_chunk_type, str_chunk_size, str_count, style_count, \
			unknown, str_pool_offset,	style_pool_offset = str_chunk_top_seven_parsed_tuple

		#read the string chunk
		str_chunk_stucture = self.str_chunk_stucture.format(str_count, style_count)
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
		self.resourceid_chunk_tuple = self.read_obinary_file_chunk(self.start, \
			self.resourceid_chunk_structure.format(chunk_size/4 -2)  ) 
		

	def read_namespace_chunk(self):	
		self.namespace_chunk_tuple = self.read_obinary_file_chunk(self.start, self.namespace_chunk_structure)
		

	def read_start_tag_chunk(self):	
		attr_count = self.read_obinary_file_chunk(self.start, "<8I")[-1]
		self.start_tag_chunk_tuple = self.read_obinary_file_chunk(self.start, \
										self.start_tag_chunk_structure.format(attr_count * 5))
			

	def read_end_tag_chunk(self):
		self.end_tag_chunk_tuple = self.read_obinary_file_chunk(self.start, \
									self.end_tag_chunk_stucture)

	
	def read_text_chunk(self, start):
		text_chunk_tuple = self.read_obinary_file_chunk(start, \
								self.text_chunk_structure)



if __name__ == "__main__":
	f = (open("C:\Users\symen\Desktop\crackme02_10_jiagu_sign\AndroidManifest.xml", "rb")).read()
	pam = ParseAndroidManifest(f)
	magic, am_size = pam.read_type_and_size()
	pam.start += 8

	while pam.start < am_size:
		chunk_type, chunk_size = pam.read_type_and_size()
		if chunk_type == 1835009:
			print "string:", 
			# strings in the self.string_list
			# other information in the  str_chunk_top_nine_parsed_tuple
			# it is easy to find out in the method read_str_chunk
			pam.read_str_chunk()

			print "the number of strings is {} ".format( len(pam.string_list) )
			for string in pam.string_list:
				print "str: {}".format(string)

		elif chunk_type == 524672:
			# resourceid_chunk_tuple store the information of the resource id
			print "resource id :",
			pam.read_resourceid_chunk(chunk_size)
			for resource_id in pam.resourceid_chunk_tuple:
				print "id:{0}, hex:{1}".format(resource_id, hex(resource_id))

		elif chunk_type == 1048832:
			print "start namespace :",
			pam.read_namespace_chunk()
			prefix, uri = pam.namespace_chunk_tuple[4:]
			print "prefix: {0} => {1}, uri:{2} => {3}".format(prefix, pam.string_list[prefix],uri, pam.string_list[uri])


		elif chunk_type == 1048833:
			print "end namespace:",
			pam.read_namespace_chunk()

		elif chunk_type == 1048834:
			pam.read_start_tag_chunk()
			print (pam.start_tag_chunk_tuple[0:])
			print """<{0} """.format(pam.string_list[pam.start_tag_chunk_tuple[5]])

			for i in range(len(pam.start_tag_chunk_tuple[9:]) /5 ):
				attr_list = pam.start_tag_chunk_tuple[8+ 5*i + 1 : 9 + 5+ 5*i]
				print attr_list
				print "{0}  {1}  {2} {3}".format(
					pam.string_list[attr_list[1]],
					pam.string_list[attr_list[2]]
					,attr_list[3], [attr_list[4]])


		elif chunk_type == 1048835:
			pam.read_end_tag_chunk()
			print "namespace_uri:{0}  name:</{1}>".format(
					pam.end_tag_chunk_tuple[4], 
					pam.string_list[pam.end_tag_chunk_tuple[5]])

			

		
		
		elif chunk_type == 1048836:
			print "text :",
			pam.read_text_chunk()
		pam.start += chunk_size



	



