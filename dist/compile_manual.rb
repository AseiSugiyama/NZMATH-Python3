# -*- coding: SJIS -*-

require 'fileutils'

def is_win
	return RUBY_PLATFORM.downcase =~ /mswin(?!ce)|mingw|bccwin/
end

# ���ݒ�
$bibtex = is_win ? 'pbibtex' : 'jbibtex'
$rm = is_win ? 'del' : 'rm'
$dev_null = is_win ? 'nul' : '/dev/null'

# convert TeX into PDF
def tex_compile(file)
	print File.basename(Dir.pwd) + '/' + file
	`platex -kanji="sjis" #{file}.tex`
	print "."
	`#{$bibtex} #{file}`
	print "."

	# some system needs three times compiles.
	3.times do
		`platex -kanji="sjis" #{file}.tex`
		print "."
	end

	`dvipdfmx #{file}.dvi > #{$dev_null} 2>&1`
	puts "."
end

# ���ԃt�@�C���폜
def clean
	`#{$rm} *.aux *.bbl *.blg *.dvi *.log *.out *.toc`
end

# compile all TeX files in dir
def compile(dir)
	savedir = Dir.pwd
	Dir.chdir(dir)

	# ���ԃt�@�C���폜
	clean

	# �ʃt�@�C���R���p�C��
	Dir::glob("*.pdf").each do |file|
		next if "nzmath_doc" == file[0...-4]
		tex_compile(file[0...-4])
	end

	header_footer = ["header_overview.tex", "header_basic_util.tex", "header_class.tex",
		"header_function.tex", "footer.tex"]
	header_footer.map!{|file| '../' + file}

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

# 1�s�ڂƍŏI�s (header, footer) �̍폜
def head_foot_del(file)
	data = ""
	open(file, 'r') do |f|
		data = f.readlines
	end

	file_bak = file + ".bak"
	File.rename file, file_bak

	data.shift
	data.pop
	open(file, "w") do |f|
		f.write data
	end

	File.delete(file_bak)
end

def source_compress(dir, olddirrm=false)
	savedir = Dir.pwd
	Dir.chdir(dir)

	srcdir = '../manual_source/'
	if olddirrm then
		# ���f�B���N�g���̍폜
		if File.exists?(srcdir) then
			FileUtils.rm_r(srcdir)
		end
	end

	# �V�����f�B���N�g���̍쐬
	if not File.exists?(srcdir) then
		Dir.mkdir(srcdir)
	end
	srctargetdir = srcdir + File.basename(dir) + '/'
	if not File.exists?(srctargetdir) then
		Dir.mkdir(srctargetdir)
	end

	# �\�[�X�̈ړ�
	Dir::glob("*.tex").each do |file|
		FileUtils.cp(file, srctargetdir)
	end
	FileUtils.cp("../macros.tex", srcdir)
	Dir.chdir(srctargetdir)

	# header, footer �̏���
	Dir::glob("*.tex").each do |file|
		next if "nzmath_doc" == file[0...-4]
		head_foot_del(file)
	end

	Dir.chdir(savedir)
end

compile("../manual/en/")
source_compress("../manual/en/", true)
compile("../manual/ja/")
source_compress("../manual/ja/")
