# -*- coding: SJIS -*-

def tex_compile(file)
	print file
	`platex #{file}.tex`
	print "."
	`pbibtex #{file}.tex`
	print "."
	`platex #{file}.tex`
	print "."
	`platex #{file}.tex`
	print "."
	`dvipdfmx #{file}.dvi > nul 2>&1`
	puts "."
end

def clean
	# ���ԃt�@�C���폜
	`del *.aux *.bbl *.blg *.dvi *.log *.out *.toc`
end

def compile
	savedir = Dir.pwd
	Dir.chdir("../manual/")

	# �ʃt�@�C���R���p�C��
	Dir::glob("*.pdf").each do |file|
		next if "nzmath_doc" == file[0...-4]
		tex_compile(file[0...-4])
	end

	header_footer = ["header_basic_util.tex", "header_class.tex",
		"header_function.tex", "footer.tex"]

	# ���l�[��
	header_footer.each do |file|
		File::rename(file, file + '_')
	end

	# ��t�@�C���쐬
	header_footer.each do |file|
		open(file, "w") {|f|}
	end

	begin
		# �R���p�C��
		tex_compile("nzmath_doc")
	ensure
		# ���l�[��
		header_footer.each do |file|
			File::rename(file + '_', file)
		end
	end
ensure
	# ���ԃt�@�C���폜
	clean

	Dir.chdir(savedir)
end

compile
