#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 file into koyomi extra 0.12b


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomiex-in'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


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
kex_select = Hash.new
#kex_item = Hash.new
#kex_unit = Hash.new
r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	if r.first['koyomi'] != nil && r.first['koyomi'] != ''
		koyomi = JSON.parse( r.first['koyomi'] )
		start = koyomi['start'].to_i
		kex_select = koyomi['kex_select']
		kex_oname = koyomi['kex_oname']
		kex_ounit = koyomi['kex_ounit']
		p koyomi if @debug
	end
end


case command
when 'upload'
	puts 'Upload' if @debug
	file_origin = @cgi['extable'].original_filename.force_encoding( 'utf-8' )
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
			puts "<OPTION value='date'>#{lp[12]}</OPTION>"
			0.upto( 9 ) do |cc|
				puts "<OPTION value='#{kex_select[cc.to_s]}'>#{@kex_item[kex_select[cc.to_s]]}</OPTION>" if kex_select[cc.to_s] != 'ND'
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
		if file_item_nos[c] == 'date'
			date_column = c
		end
	end

	item_column_posi = []
	0.upto( 9 ) do |c|
		if kex_select[c.to_s] != 'ND'
			file_item_nos.size.times do |cc|
				if kex_select[c.to_s] == file_item_nos[cc]
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
					if item_column_posi[c] != 0 && ( r.first["item#{c}"] == '' || r.first["item#{c}"] == nil ) || ( overwrite == '1' && item_column_posi[c] != 0 )
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
