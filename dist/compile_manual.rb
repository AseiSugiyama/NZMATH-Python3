# -*- coding: SJIS -*-

def is_win
	return RUBY_PLATFORM.downcase =~ /mswin(?!ce)|mingw|bccwin/
end

# 環境設定
$bibtex = is_win ? 'pbibtex' : 'jbibtex'

def tex_compile(file)
	print File.basename(Dir.pwd) + '/' + file
	`platex #{file}.tex`
	print "."
	`#{$bibtex} #{file}.aux`
	print "."
	`platex #{file}.tex`
	print "."
	`platex #{file}.tex`
	print "."
	nul = is_win ? 'nul' : '/dev/null'
	`dvipdfmx #{file}.dvi > #{nul} 2>&1`
	puts "."
end

def clean
	# 中間ファイル削除
	`del *.aux *.bbl *.blg *.dvi *.log *.out *.toc`
end

def compile(dir)
	savedir = Dir.pwd
	Dir.chdir(dir)

	# 個別ファイルコンパイル
	Dir::glob("*.pdf").each do |file|
		next if "nzmath_doc" == file[0...-4]
		tex_compile(file[0...-4])
	end

	header_footer = ["header_basic_util.tex", "header_class.tex",
		"header_function.tex", "footer.tex"]
	header_footer.map!{|file| '../' + file}

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

compile("../manual/en/")
compile("../manual/ja/")
