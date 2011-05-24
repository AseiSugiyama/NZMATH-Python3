# -*- coding: SJIS -*-

savedir = Dir.pwd
Dir.chdir("../manual/")

begin
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

	# �R���p�C��
	`platex nzmath_doc.tex`
	print "."
	`platex nzmath_doc.tex`
	print "."
	`platex nzmath_doc.tex`
	print "."
	`dvipdfmx nzmath_doc.dvi`
	print "."

	# ���l�[��
	header_footer.each do |file|
		File::rename(file + '_', file)
	end
ensure
	Dir.chdir(savedir)
end
