from struct import Struct

from ObFileBase import ObFileBase

class ParseAndroidManifest(ObFileBase):
	def __init__(self, file_buf):
		ObFileBase.__init__(self, file_buf)

		self.header_size = 8

		self.str_chunk_stucture = "<7I{0}I{1}I"
		self.resourceid_chunk_structure = "<2I{}I"
		self.namespace_chunk_structure = "<6I"
		self.start_tag_chunk_structure = "<9I{}I"
		self.end_tag_chunk_stucture = "<6I"
		self.text_chunk_structure = "<7I"

		self.start = 0
		self.str_list = []


	def read_magic_flag(self, start):
		print "start looking for magic flag"
		magic_structure = Struct(self.magic_structure)
		magic_tuple = self.read_obinary_file_chunk(start, magic_structure)
		self.start += magic_structure.size
		print map(hex, magic_tuple)
		print
	

	def read_size_flag(self, start):
		print "start looking for androidmanifest filesize"
		file_structure = Struct(self.filesize_structure)
		filesize_tuple = self.read_obinary_file_chunk(start, file_structure)
		self.start += file_structure.size
		print map(hex, filesize_tuple)
		print


	def read_str_chunk_flag(self, start):	
		print "start looking for strings"	
		# read the base information
		str_chunk_top_seven_parsed_tuple = self.read_obinary_file_chunk(start, Struct("<7I"))
		str_chunk_type, str_chunk_size, str_count, style_count, \
			unknown, str_pool_offset,	style_pool_offset = str_chunk_top_seven_parsed_tuple

		self.start += str_chunk_size
		#read the string chunk
		str_chunk_stucture = Struct(self.str_chunk_stucture.format(str_count, style_count))
		str_chunk_top_nine_parsed_tuple = self.read_obinary_file_chunk(start, str_chunk_stucture)

		def inner_read_strings():
			str_off_list = str_chunk_top_nine_parsed_tuple[7: 7 + str_count]
			
			if not style_count :
				str_end_offset = str_chunk_size
			else:
				str_end_offset = style_pool_offset
			
			strs_hex = self.read_obinary_str_content(self.header_size + str_pool_offset, self.header_size + str_end_offset)

			tmp_str = ""
			new_result = []
			for i in strs_hex:
				if i < 30 :
					new_result.append(tmp_str)
					tmp_str = ""
				else:
					tmp_str += chr(i)

			str_result = [i for i in new_result if i]
			self.str_list = str_result
		inner_read_strings()
		print

	def read_resourceid_chunk(self, start):
		print "start looking for resourceid"
		resourceid_chunk_type, resourceid_chunk_size = self.read_obinary_file_chunk(start, Struct("<2I"))
		self.start += resourceid_chunk_size
		resourceid_chunk_tuple = self.read_obinary_file_chunk(start, \
			Struct(self.resourceid_chunk_structure.format(resourceid_chunk_size/4 -2) ) ) 
		print map(hex, resourceid_chunk_tuple)
		print


	def read_namespace_chunk(self, start):
		print "start looking for namespace"
		while True:
			namespace_chunk_tuple = self.read_obinary_file_chunk(start, Struct(self.namespace_chunk_structure))
			print namespace_chunk_tuple
			if namespace_chunk_tuple[0] == 1048832:
				print "start namespace"
				print map(hex, namespace_chunk_tuple)				
				self.start += Struct(self.namespace_chunk_structure).size
				start = self.start
			elif namespace_chunk_tuple[0] == 1048833:
				print "end namespace"				
				print map(hex, namespace_chunk_tuple)
				self.start += Struct(self.namespace_chunk_structure).size
				start = self.start
			else:
				break
		print


	def read_tag_chunk(self, start):
		print "start looking for tag chunk"
		while True:
			chunk_type, chunk_size = self.read_obinary_file_chunk(start, Struct("<2I"))
			if chunk_type == 1048834:
				attr_count = self.read_obinary_file_chunk(self.start, Struct("<8I"))[-1]

				start_tag_chunk_tuple = self.read_obinary_file_chunk(self.start, \
						Struct(self.start_tag_chunk_structure.format(attr_count * 5)))

				print "start tag"
				print start_tag_chunk_tuple
				self.start += chunk_size
				start = self.start
			elif chunk_type == 1048835:
				print "end tag"
				end_tag_chunk_tuple = self.read_obinary_file_chunk(start, \
						Struct(self.end_tag_chunk_stucture))
				chunk_size = end_tag_chunk_tuple[1]
				print end_tag_chunk_tuple
				self.start += chunk_size
				start = self.start
			else:
				print
				break
	
	def read_text_chunk(self, start):
		print "start text chunk"
		while True:
			chunk_type, chunk_size = self.read_obinary_file_chunk(start, Struct("<2I"))
			if chunk_type == 1028836:
				text_chunk_tuple = self.read_obinary_file_chunk(start, \
						Struct(self.text_chunk_structure))
				self.start += Struct( text_chunk_structure )
				start = self.start
			else:
				break


if __name__ == "__main__":
	f = (open("C:\Users\symen\Desktop\crackme02_10_jiagu_sign\AndroidManifest.xml", "rb")).read()
	pam = ParseAndroidManifest(f)
	magic_start = 0
	pam.read_magic_flag(magic_start)

	filesize_start = pam.start
	pam.read_size_flag(filesize_start)

	str_chunk_start = pam.start
	pam.read_str_chunk_flag(str_chunk_start)

	resourceid_chunk_start = pam.start
	pam.read_resourceid_chunk(resourceid_chunk_start)

	namespace_chunk_start = pam.start
	pam.read_namespace_chunk(namespace_chunk_start)

	tag_chunk_start = pam.start
	pam.read_tag_chunk(tag_chunk_start)

	text_chunk_start = pam.start
	pam.read_text_chunk(text_chunk_start)



