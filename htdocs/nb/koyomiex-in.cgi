#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 file into koyomi extra 0.20b (2022/09/10)


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
html = []


puts 'CHECK membership<br>' if @debug
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


puts "LOAD config<br>" if @debug
start = Time.new.year
kexu = Hash.new
kexa = Hash.new
r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	if r.first['koyomi'] != nil && r.first['koyomi'] != ''
		koyomi = JSON.parse( r.first['koyomi'] ) if r.first['koyomi'] != ''
		start = koyomi['start'].to_i
		kexu = koyomi['kexu']
		kexa = koyomi['kexa']
	end
end


case command
when 'upload'
	puts 'Upload' if @debug
	file_origin = @cgi['extable'].original_filename.force_encoding( 'utf-8' )
	file_type = @cgi['extable'].content_type
	file_body = @cgi['extable'].read
	file_size = "#{( file_body.size / 1000 ).to_i} kbyte"

	####
####
html[10] = <<-"HTML10"
<table class='table'>
	<tr><td>#{lp[2]}</td><td>#{file_origin}</td></tr>
	<tr><td>#{lp[3]}</td><td>#{file_type}</td></tr>
	<tr><td>#{lp[4]}</td><td>#{file_size}</td></tr>
</table>
HTML10
####
	####

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

		col_no_html = ''
		line1.size.times do |c| col_no_html << "<th align='center'>#{c}</th>" end

		lin = ''
		line1.each do |e|
			lin << "#{e}"
		end
puts lin
#		line1.each do |e| line1_html << "<td style='font-size:0.5rem'></td>" end
		line2_html = ''
		line2.each do |e| line2_html << "<td style='font-size:1rem'>#{e}</td>" end

		line_select = ''
		line1.size.times do |c|
			line_select << "<td>"
			line_select << "<SELECT class='form-select form-select-sm' id='item#{c}'>"
			line_select << "<OPTION value='date'>#{lp[12]}</OPTION>"
			kexu.each do |k, v| line_select << "<OPTION value='#{k}'>#{k}</OPTION>" end
			line_select << "/<SELECT>"
			line_select << "</td>"
		end

		########
########
html[20] = <<-"HTML20"
<table class='table table-bordered'>
	<tr>
		<td></td>
		#{col_no_html}
	</tr>
	<tr>
		<th>#{lp[5]}</th>
		#{lin}
	</tr>
	<tr>
		<th>#{lp[6]}</th>
		#{line2_html}
	</tr>

	<tr>
		<th>#{lp[7]}</th>
		#{line_select}
	</tr>
</table>

<div class='row'>
	<div class='col-2'>
		<div class='form-check'>
			<input class='form-check-input' type='checkbox' id='skip_line1'>
			<label class='form-check-label'>#{lp[9]}</label>
		</div>
	</div>
	<div class='col-2'>
		<div class='form-check'>
			<input class='form-check-input' type='checkbox' id='overwrite'>
			<label class='form-check-label'>#{lp[10]}</label>
		</div>
	</div>
	<div align='right' class='col-8'>
		<button type='button' class='btn btn-sm btn-outline-primary' onclick=\"writekoyomiex( '#{tmp_file}', '#{line1.size}', '#{lp[13]}' )\">#{lp[11]}</button>
	</div>
</div>
HTML20
########
		########

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

puts html.join
