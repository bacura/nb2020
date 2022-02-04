#! /usr/bin/ruby
#nb2020-clean.rb for modified20211228

#Bacura KYOTO Lab
#Saga Ukyo-ku Kyoto, JAPAN
#https://bacura.jp
#yossy@bacura.jp


#==============================================================================
# MAIN
#==============================================================================

source_file = '20201225-mxt_kagsei-mext_01110-FA-m20211227.txt'
out_file = '20201225-mxt_kagsei-mext_01110-FA-m20211227_clean.txt'

data_solid = []

# 食品成分表データの読み込みと加工
f = open( source_file, 'r' )
f.each_line do |e|
	items = e.force_encoding( 'UTF-8' ).split( "\t" )

	#### 共通
	t = e.force_encoding( 'UTF-8' )
	t.sub!( 'AMMON-E', 'AMMONE' )

	data_solid << t
end
f.close


####
header = data_solid.shift
data_solid_ = []
c = 0
data_solid.each do |e|
	t = e.sub( /\t+\n/, "\n" )
	t.gsub!( '"', '' )
	a = t.split( "\t" )
	if /^\d\d/ =~ e && a.size >= 10
		data_solid_[c] = t
	else
		c -= 1
		data_solid_[c].chomp!
		data_solid_[c] << "<br>#{t}"
	end
	c += 1
end
data_solid_.unshift( header )

# 成分表データの書き込み
f = open( out_file, 'w' )
data_solid_.each do |e| f.puts e end
f.close
