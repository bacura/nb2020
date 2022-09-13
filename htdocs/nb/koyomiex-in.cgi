#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 file into koyomi extra 0.21b (2022/09/12)


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
item_solid = @cgi['item_solid']
if @debug
	puts "command:#{command}<br>\n"
	puts "file:#{file}<br>\n"
	puts "item_solid:#{item_solid}<br>\n"
end


puts "LOAD config<br>" if @debug
start = Time.new.year
kexu = Hash.new
kexa = Hash.new
kexc = Hash.new
skip_line1 = nil
overwrite = nil

r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	if r.first['koyomi'] != nil && r.first['koyomi'] != ''
		koyomi = JSON.parse( r.first['koyomi'] ) if r.first['koyomi'] != ''
		start = koyomi['start'].to_i
		kexu = koyomi['kexu']
		kexa = koyomi['kexa']
		kexin = koyomi['kexin']
	end
end


case command
when 'upload'
	puts 'Upload' if @debug
	file_origin = @cgi['extable'].original_filename.force_encoding( 'utf-8' )
	file_type = @cgi['extable'].content_type
	file_body = @cgi['extable'].read
	file_size = "#{( file_body.size / 1000 ).to_i} kbyte"

	unless kexin == nil
		overwrite = kexin['overwrite']
		skip_line1 = kexin['skip_line1']
	end

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

		rows = file_body.force_encoding( 'utf-8' ).split( "\n" )
		line1 = rows[0].split( "\t" )
		line2 = rows[1].split( "\t" )

		puts "temporary file<br>" if @debug
		tmp_file = generate_code( user.name, 't' )
		f = open( "#{$TMP_PATH}/#{tmp_file}", 'w' )
		f.puts file_body
		f.close

		col_no_html = ''
		line1.size.times do |c| col_no_html << "<th align='center'>#{c}</th>" end

		line1_html = ''
		line1.each do |e| line1_html << "<td style='font-size:0.5rem'>#{e}</td>" end

		line2_html = ''
		line2.each do |e| line2_html << "<td style='font-size:1rem'>#{e}</td>" end

		line_select = ''
		line1.size.times do |c|
			line_select << "<td>"
			line_select << "<SELECT class='form-select form-select-sm' id='item#{c}'>"
			line_select << "<OPTION value='ND'>ND</OPTION>"
			line_select << "<OPTION value='date'>#{lp[12]}</OPTION>"
			kexu.each do |k, v| line_select << "<OPTION value='#{k}'>#{k}</OPTION>" end
			line_select << "/<SELECT>"
			line_select << "</td>"
		end


		skip_line1_checked = ''
		skip_line1_checked = 'CHECKED' if skip_line1 == '1'

		overwrite_checked = ''
		overwrite_checked = 'CHECKED' if overwrite == '1'


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
		#{line1_html}
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
			<input class='form-check-input' type='checkbox' id='skip_line1' #{skip_line1_checked}>
			<label class='form-check-label'>#{lp[9]}</label>
		</div>
	</div>
	<div class='col-2'>
		<div class='form-check'>
			<input class='form-check-input' type='checkbox' id='overwrite'  #{overwrite_checked}>
			<label class='form-check-label'>#{lp[10]}</label>
		</div>
	</div>
</div>
<div class='row'>
	<button type='button' class='btn btn-sm btn-warning' onclick=\"writekoyomiex( '#{tmp_file}', '#{line1.size}', '#{lp[13]}' )\">#{lp[11]}</button>
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
	skip_line1 = @cgi['skip_line1']
	overwrite = @cgi['overwrite']

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
	kex_key = item_solid.split( ':' )
	kex_posi = Hash.new
	c = 0
	kex_key.each do |e|
		kex_posi['date'] = c if e == 'date'
		kex_posi[e] = c if e != nil && e != '' && e != 'ND'
		c += 1
	end


	puts "kex_posi:#{kex_posi}<br>" if @debug
	count = 0
	matrix.each do |ea|
		t = ea[kex_posi['date']]
		t.gsub!( '/', '-' )
		t.gsub!( '.', '-' )
		t.gsub!( '年', '-' )
		t.gsub!( '月', '-' )
		t.gsub!( '日', '' )
		a = t.scan( /\d\d\d\d\-\d\d-\d\d/ )
		yyyymmdd = a[0]

		if yyyymmdd != nil
			puts "LOAD date cell<br>" if @debug
			r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
			kexc = Hash.new
			count_flag = false
			if r.first
				kexc = JSON.parse( r.first['cell'] ) if r.first['cell'] != nil && r.first['cell'] != ''
				kex_posi.each do |k, v|
					unless k == 'date'
						if kexc[k] == '' || kexc[k] == nil || overwrite == '1'
							kexc[k] = ea[v]
							count_flag = true
						end
					end
				end
				cell_ = JSON.generate( kexc )
				mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET cell='#{cell_}' WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
				count += 1 if count_flag

			else
				kex_posi.each do |k, v|
					kexc[k] = ea[v] unless k == 'date'
				end
				cell_ = JSON.generate( kexc )
				mdb( "INSERT INTO #{$MYSQL_TB_KOYOMIEX} SET cell='#{cell_}', user='#{user.name}', date='#{yyyymmdd}';", false, @debug )
				count += 1
			end
		else
			puts lp[15]
			exit
		end
	end

	puts "Infom result<br>" if @debug
	html[30] = ''
	html[30] << "#{lp[17]}<br>" if skip_line1 == '1'
	if overwrite == '1'
		html[30] << "#{lp[18]} (#{count}/#{matrix.size})<br>"
	else
		html[30] << "#{lp[19]} (#{count}/#{matrix.size})<br>"
	end
end

puts html.join


if command == 'update'
	puts 'UPDATE config<br>' if @debug

	kexin = { 'skip_line1'=>skip_line1, 'overwrite'=>overwrite }
	koyomi_ = JSON.generate( { "start"=>start,  "kexu"=>kexu, "kexa"=>kexa, "kexin"=>kexin } )
	mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomi='#{koyomi_}' WHERE user='#{user.name}';", false, @debug )
end
