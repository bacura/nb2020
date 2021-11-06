#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 file into koyomi extra 0.01b


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomiex-in'
@debug = true


#==============================================================================
#DEFINITION
#==============================================================================

#### Getting start year
def get_starty( uname )
	start_year = @time_now.year
	r = mdb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, @debug )
	if r.first['koyomiy']
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
	end

	return start_year
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )

#### Guild member check
if user.status < 3
	puts "Guild member error."
	exit
end


#### Getting POST data
command = @cgi['command']
file = @cgi['file']
skip_line1 = @cgi['skip_line1']
overwrite = @cgi['overwrite']
item_solid = @cgi['item_solid']
if @debug
	puts "command:#{command}<br>\n"
	puts "file:#{file}<br>\n"
	puts "skip_line1:#{skip_line1}<br>\n"
	puts "overwrite:#{overwrite}<br>\n"
	puts "item_solid:#{item_solid}<br>\n"
end


puts "Loading config<br>" if @debug
config = Config.new( user.name )
item_nos = []
item_names = []
item_units = []
a = config.koyomiex.split( ':' )
0.upto( @kex_column ) do |c|
	aa = a[c].split( "\t" )
	if aa[0] == "0"
		item_nos << 0
		item_names << ''
		item_units << ''
	elsif aa[0] == "1"
		item_nos << 1
		item_names << aa[1]
		item_units << aa[2]
	else
		item_nos << aa[0].to_i
		item_names << @kex_item[aa[0].to_i]
		item_units << @kex_unit[aa[0].to_i]
	end
end


case command
when 'upload'
	puts 'Upload' if @debug
	file_origin = @cgi['extable'].original_filename
	file_type = @cgi['extable'].content_type
	file_body = @cgi['extable'].read
	file_size = file_body.size.to_i

	puts "<table class='table'>"
	puts "<tr><td>#{lp[2]}</td><td>#{file_origin}</td></tr>"
	puts "<tr><td>#{lp[3]}</td><td>#{file_type}</td></tr>"
	puts "<tr><td>#{lp[4]}</td><td>#{file_size}</td></tr>"
	puts "</table>"

	if file_type == 'text/plain' || file_type == 'text/csv' || file_type == 'application/vnd.ms-excel'
		file_body.gsub!( "\r\n", "\n" )
		file_body.gsub!( "\r", "\n" )
		file_body.gsub!( ',', "\t" )
		file_body.gsub!( '"', '' )

		rows = file_body.split( "\n" )
		line1 = rows[0].split( "\t" )
		line2 = rows[1].split( "\t" )

		puts "temporary file<br>" if @debug
		tmp_file = generate_code( user.name, 't' )
		f = open( "#{$TMP_PATH}/#{tmp_file}", 'w' )
		f.puts file_body
		f.close

		puts "<table class='table table-bordered'>"
		puts "<tr>"
		puts "<td></td>"
		line1.size.times do |c| puts "<th>#{c}</th>" end
		puts "</tr>"
		puts "<tr>"
		puts "<th>#{lp[5]}</th>"
		line1.each do |e| puts "<td>#{e}</td>" end
		puts "</tr>"
		puts "<tr>"
		puts "<th>#{lp[6]}</th>"
		line2.each do |e| puts "<td>#{e}</td>" end
		puts "</tr>"

		puts "<tr>"
		puts "<th>#{lp[7]}</th>"
		line1.size.times do |c|
			puts "<td>"
			puts "<SELECT class='form-select form-select-sm' id='item#{c}'>"
			puts "<OPTION value='0'>#{lp[8]}</OPTION>"
			puts "<OPTION value='99'>#{lp[12]}</OPTION>"
			item_nos.size.times do |cc|
				puts "<OPTION value='#{item_nos[cc]}'>#{item_names[cc]}</OPTION>" if item_nos[cc] != 0
			end
			puts "/<SELECT>"
			puts "</td>"
		end
		puts "</tr>"
		puts "</table>"

		puts "<div class='row'>"
		puts "<div class='col-2'>"
		puts "	<div class='form-check'>"
		puts "	<input class='form-check-input' type='checkbox' id='skip_line1'>"
		puts "	<label class='form-check-label'>#{lp[9]}</label>"
		puts "	</div>"
		puts "</div>"
		puts "<div class='col-2'>"
		puts "	<div class='form-check'>"
		puts "	<input class='form-check-input' type='checkbox' id='overwrite'>"
		puts "	<label class='form-check-label'>#{lp[10]}</label>"
		puts "	</div>"
		puts "</div>"
		puts "<div align='right' class='col-8'>"
		puts "	<button type='button' class='btn btn-sm btn-outline-primary' onclick=\"writekoyomiex( '#{tmp_file}', '#{line1.size}', '#{lp[13]}' )\">#{lp[11]}</button>"
		puts "</div>"
		puts "</div>"

	else
		puts lp[1]
		exit
	end
when 'update'
	puts "Loading temporary file<br>" if @debug
	matrix = []
	d = 0
	f = open( "#{$TMP_PATH}/#{file}", 'r' )
	f.each_line do |l|
		matrix[d] = l.chomp.force_encoding( 'utf-8' ).split( "\t" )
		d += 1
	end
	f.close
	matrix.shift if skip_line1 == '1'

	puts 'Detevting item column<br>' if @debug
	file_item_nos = item_solid.split( ':' )
	date_column = 0
	file_date_column = 0
	file_item_nos.size.times do |c|
		if file_item_nos[c] == '99'
			date_column = c
		end
	end

	item_column_posi = []
	0.upto( @kex_column ) do |c|
		if item_nos[c] != 0
			file_item_nos.size.times do |cc|
				if item_nos[c] == file_item_nos[cc].to_i
					item_column_posi[c] = cc
				end
			end
			item_column_posi[c] = 0 if item_column_posi[c] == nil
		else
			item_column_posi[c] = 0
		end
	end

	puts "date_column:#{date_column}<br>" if @debug
	puts "item_column_posi:#{item_column_posi}<br>" if @debug
	count = 0
	matrix.each do |ea|
		t = ea[date_column]
		t.gsub!( '/', '-' )
		t.gsub!( '.', '-' )
		t.gsub!( '年', '-' )
		t.gsub!( '月', '-' )
		t.gsub!( '日', '' )
		a = t.scan( /\d\d\d\d\-\d\d-\d\d/ )
		yyyymmdd = a[0]

		if yyyymmdd != nil
			sql_set = 'SET '
			r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
			if r.first
				item_column_posi.size.times do |c|
					if item_column_posi[c] != 0 && ( r.first["item#{c}"] == '' || r.first["item#{c}"] == nil ) || overwrite == '1'
						sql_set << "item#{c}='#{ea[item_column_posi[c]]}',"
					end
				end
				sql_set.chop!
				if sql_set != 'SET'
					mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} #{sql_set} WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
					count += 1
				end
			else
				item_column_posi.size.times do |c|
					if item_column_posi[c] != 0
						sql_set << "item#{c}='#{ea[item_column_posi[c]]}',"
					end
				end
				sql_set.chop!
 				if sql_set != 'SET'
					mdb( "INSERT #{$MYSQL_TB_KOYOMIEX} #{sql_set}, user='#{user.name}', date='#{yyyymmdd}';", false, @debug )
					count += 1
				end
			end
		else
			puts lp[15]
			exit
		end
	end

	puts "#{lp[17]}<br>" if skip_line1 == "1"
	if overwrite == "1"
		puts "#{lp[18]} (#{count}/#{matrix.size})<br>"
	else
		puts "#{lp[19]} (#{count}/#{matrix.size})<br>"
	end
	puts lp[16]
end
