# -*- coding: SJIS -*-

savedir = Dir.pwd
Dir.chdir("../manual/")

begin
	header_footer = ["header_basic_util.tex", "header_class.tex",
		"header_function.tex", "footer.tex"]

	# リネーム
	header_footer.each do |file|
		File::rename(file, file + '_')
	end

	# 空ファイル作成
	header_footer.each do |file|
		open(file, "w") {|f|}
	end

	# コンパイル
	`platex nzmath_doc.tex`
	print "."
	`platex nzmath_doc.tex`
	print "."
	`platex nzmath_doc.tex`
	print "."
	`dvipdfmx nzmath_doc.dvi`
	print "."

	# リネーム
	header_footer.each do |file|
		File::rename(file + '_', file)
	end
ensure
	Dir.chdir(savedir)
end
