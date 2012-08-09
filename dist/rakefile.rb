# coding: UTF-8

require 'rake/clean'

Dir.chdir(File.dirname(__FILE__) + '/../manual')


WINDOWS = (RUBY_PLATFORM =~ /mswin(?!ce)|mingw|bccwin/i)

BIBTEX = WINDOWS ? 'pbibtex' : 'jbibtex'
REMOVE = WINDOWS ? 'del' : 'rm'
DEV_NULL = WINDOWS ? 'nul' : '/dev/null'

TEXS_EN = FileList["en/*.tex"]
TEXS_JA = FileList["ja/*.tex"]
TEXS = TEXS_EN + TEXS_JA
PDFS = TEXS.ext('pdf')

INTERMEDIATE = %w[aux bbl blg dvi log out toc]
INTERMEDIATE.each do |ext|
	CLEAN.include(TEXS.ext(ext))
end
CLOBBER.include(PDFS)


task :default => PDFS

def remove_intermediate(name_without_ext)
	INTERMEDIATE.each do |ext|
		file = name_without_ext + '.' + ext
		if FileTest.file?(file)
			File.delete(file)
		end
	end
end

def compile(target)
	print target + ' '
	name = File.basename(target, '.tex')
	Dir.chdir(File.dirname(target)) do
		remove_intermediate(name)
		print '.'

		`platex -kanji="sjis" #{name}.tex`
		print '.'
		`#{BIBTEX} #{name}`
		print '.'
		3.times do
			`platex -kanji="sjis" #{name}.tex`
			print '.'
		end
#		`dvipdfmx #{name}.dvi > #{DEV_NULL} 2>&1`
		print '.'

		remove_intermediate(name)
		puts '.'
	end
end

%w[en ja].each do |lang|
	file "#{lang}/nzmath_doc.pdf" => Module.const_get('TEXS_' + lang.upcase) do |t|
p t.name
next
		header_footer = %w[header_overview.tex header_basic_util.tex
			header_class.tex header_function.tex footer.tex]

		# rename
		header_footer.each do |file|
			File::rename(file, file + '_')
		end
		# create blank file
		header_footer.each do |file|
			open(file, "w") {|f|}
		end

		begin
			compile(t.source)
		ensure
			# restore
			header_footer.each do |file|
				File::rename(file + '_', file)
			end
		end
	end
end

rule '.pdf' => '.tex' do |t|
	compile(t.source)
end
