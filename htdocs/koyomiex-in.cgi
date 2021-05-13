#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi extra 0.01b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'
require 'fileutils'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomiex-in'
@debug = false


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


#### Order check
def array_no( solid, delimiter )
	list = solid.split( delimiter )
	date_column = 0
	posi = []
	list.size.times do |c|
		if list[c] == '99'
			posi << 0
			date_column = c
		else
			posi << list[c].to_i
		end
	end

	return date_column, posi
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


#### Loading config
puts "Loading config<br>" if @debug
kex_select_set = []
item_set = []
unit_set = []
r = mdb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	a = r.first['koyomiex'].split( ':' )
	0.upto( 9 ) do |c|
		aa = a[c].split( "\t" )
		if aa[0] == "0"
		elsif aa[0] == "1"
			kex_select_set << aa[0].to_i
			item_set << aa[1]
			unit_set << aa[2]
		else
			kex_select_set << aa[0].to_i
			item_set << @kex_item[aa[0].to_i]
			unit_set << @kex_unit[aa[0].to_i]
		end
	end
end


case command
when 'upload'
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

		puts "Loading config<br>" if @debug
		item_set = []
		name_set = []
		r = mdb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first
			a = r.first['koyomiex'].split( ':' )
			a.each do |e|
				aa = e.split( "\t" )
				if aa[0] == "1"
					item_set << aa[0].to_i
					name_set << aa[1]
				elsif aa[0] != "0"
					item_set << aa[0].to_i
					name_set << @kex_item[aa[0].to_i]
				end
			end
		end

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
			item_set.size.times do |cc|
				puts "<OPTION value='#{item_set[cc]}'>#{name_set[cc]}</OPTION>"
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

	date_column, posi = array_no( item_solid, ':' )
	puts "date_column:#{date_column}<br>" if @debug
	puts "posi:#{posi}<br>" if @debug

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
			ea.size.times do |c|
				if posi[c] != 0
					sql_set << "item#{posi[c]}='#{ea[c]}',"
				end
			end
			sql_set.chop!

			if sql_set != 'SET'
				r = mdb( "SELECT date FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
				if r.first
					if overwrite == '1'
						mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} #{sql_set} WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
						count += 1
					end
				else
					mdb( "INSERT #{$MYSQL_TB_KOYOMIEX} #{sql_set}, user='#{user.name}', date='#{yyyymmdd}';", false, @debug )
					count += 1
				end
			else
				puts lp[14]
				exit
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
