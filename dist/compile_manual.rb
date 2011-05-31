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
	# 中間ファイル削除
	`del *.aux *.bbl *.blg *.dvi *.log *.out *.toc`
end

def compile
	savedir = Dir.pwd
	Dir.chdir("../manual/")

	# 個別ファイルコンパイル
	Dir::glob("*.pdf").each do |file|
		next if "nzmath_doc" == file[0...-4]
		tex_compile(file[0...-4])
	end

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

	begin
		# コンパイル
		tex_compile("nzmath_doc")
	ensure
		# リネーム
		header_footer.each do |file|
			File::rename(file + '_', file)
		end
	end
ensure
	# 中間ファイル削除
	clean

	Dir.chdir(savedir)
end

compile
