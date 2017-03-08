from struct import Struct

from ObFileBase import ObFileBase

class ParseAndroidManifest(ObFileBase):
	def __init__(self, file_buf):
		ObFileBase.__init__(self, file_buf)

		self.header = 8

		self.magic_structure = "<I"

		self.filesize_structure = "<I"

		self.str_chunk_stucture = "<4I1I2I{0}I{1}I"
		self.resourceid_chunk_structure = "<2I{rs_id_count}I"


		self.start_namespace_chunk_structure = "<3I1I2I"
		self.end_namespace_chunk_structure = "<3I1I2I"

		self.start_tag_chunk = "<3I1I5I{attr_count_fifth}I"
		self.end_tag_chunk = "<3I1I2I"

		self.text_chunk = "<3I1I1I2I"

		self.start = 0



	def read_magic_flag(self, start):
		magic_structure = Struct(self.magic_structure)
		magic_tuple = self.read_obinary_file_chunk(start, magic_structure)
		self.start += magic_structure.size
		print map(hex, magic_tuple)
	

	def read_size_flag(self, start):
		file_structure = Struct(self.filesize_structure)
		filesize_tuple = self.read_obinary_file_chunk(start, file_structure)
		self.start += file_structure.size
		print map(hex, filesize_tuple)

	def read_str_chunk_flag(self, start):		
		# read the base information
		str_chunk_top_seven_parsed_tuple = self.read_obinary_file_chunk(start, Struct("<7I"))
		str_chunk_type, str_chunk_size, str_count, style_count, \
			unknown, str_pool_offset,	style_pool_offset = str_chunk_top_seven_parsed_tuple

		#read the string chunk
		str_chunk_stucture = Struct(self.str_chunk_stucture.format(str_count, style_count))
		str_chunk_top_nine_parsed_tuple = self.read_obinary_file_chunk(start, str_chunk_stucture)
		print map(hex, str_chunk_top_nine_parsed_tuple)

		def read_strings():
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
			print str_result


		read_strings()


if __name__ == "__main__":
	f = (open("C:\Users\symen\Desktop\crackme02_10_jiagu_sign\AndroidManifest.xml", "rb")).read()
	pam = ParseAndroidManifest(f)
	magic_start = 0
	pam.read_magic_flag(magic_start)

	filesize_start = pam.start
	pam.read_size_flag(filesize_start)

	str_chunk_start = pam.start
	pam.read_str_chunk_flag(str_chunk_start)



