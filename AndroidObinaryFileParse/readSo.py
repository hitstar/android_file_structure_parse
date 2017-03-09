from struct import Struct

from ObFileBase import ObFileBase

class parseSo(ObFileBase):
	def __init__(self, file_buf):
		ObFileBase.__init__(self, file_buf)

		self.start = 0

		self.elf_maybe_type_structure = "<2I"
		self.elf_header_structure = "<16c2H5I6H"
		self.elf_section_header_stucture = "<10I"
		self.elf_program_header_structure = "<8I"

		self.elf_header_tuple = ()
		self.elf_program_header_tuple = ()
		self.elf_section_header_tuple = ()

	def read_elf_maybe_type(self):
		maybe_section_header_type, maybe_program_header_type = self.read_obinary_file_chunk(\
																self.start, self.elf_maybe_type_structure)

	def read_elf_header(self):
		self.elf_header_tuple = self.read_obinary_file_chunk(self.start, self.elf_header_structure)
		elf_header_size= self.elf_header_tuple[23]
		self.start += elf_header_size

	def read_elf_program_header(self):
		self.elf_program_header_tuple = self.read_obinary_file_chunk(self.start, self.elf_program_header_structure)



	def read_elf_section_header(self):
		self.elf_section_header_tuple = self.read_obinary_file_chunk(self.start, self.elf_section_header_stucture)


if __name__ == "__main__":
	f_buf_so = (open("C:\Users\symen\Desktop\crackme02_10_jiagu_sign\lib\\x86\libhello-jni.so", "rb")).read()
	ps = parseSo(f_buf_so)
	ps.read_elf_header()
	print (ps.elf_header_tuple)
	elf_program_headder_off = ps.elf_header_tuple[20]
	elf_program_header_num = ps.elf_header_tuple[25]
	elf_setion_header_off = ps.elf_header_tuple[21]
	elf_section_header_num = ps.elf_header_tuple[27]

	print """elf_program_headder_off: {0}; elf_setion_header_off: {1};\r\
			elf_program_header_num: {2}; elf_segment_header_num: {3}; \r\
			elf_string_header_segment_index: {4}""".format(elf_program_headder_off, \
				elf_program_header_num, elf_setion_header_off, elf_section_header_num,\
					ps.elf_header_tuple[28])

	for i in range(elf_program_header_num):
		ps.start = elf_program_headder_off + i * Struct(ps.elf_program_header_structure).size
		ps.read_elf_program_header()
		print map(hex, ps.elf_program_header_tuple)

	print
	for i in range(elf_section_header_num):
		ps.start = elf_setion_header_off + i* Struct(ps.elf_section_header_stucture).size
		ps.read_elf_section_header()
		print map(hex, ps.elf_section_header_tuple)