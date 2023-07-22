#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 file into koyomi extra 0.30b (2023/01/21)


#==============================================================================
#LIBRARY
#==============================================================================
require '../soul'
require '../brain'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )


#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'msg_err' 	=> "このタイプのファイルは受け付けておりません。",\
		'file_name' => "ファイル名：",\
		'file_type'	=> "ファイルタイプ：",\
		'file_size'	=> "ファイルサイズ：",\
		'line1'		=> "1行目",\
		'line2'		=> "2行目",\
		'field'		=> "項目設定",\
		'nd'		=> "未設定",\
		'ignore1'	=> "1行目を無視",\
		'ow'		=> "上書き",\
		'record'	=> "記録する",\
		'date'		=> "日付",\
		'msg_err1'	=> "日付の選択は必須! (>_<)",\
		'msg_err2'	=> "日付項目が読み込めない形式です。",\
		'msg_res1'	=> "1行目のデータを無視しました。",\
		'msg_res2'	=> "全項目を更新しました。",\
		'msg_res3'	=> "空白の項目のみ更新しました。"
	}

	return l[language]
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
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
selecteds = ''

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
		selecteds = kexin['selecteds']
	end

	####
####
html[10] = <<-"HTML10"
<table class='table'>
	<tr><td>#{l['file_name']}</td><td>#{file_origin}</td></tr>
	<tr><td>#{l['file_type']}</td><td>#{file_type}</td></tr>
	<tr><td>#{l['file_size']}</td><td>#{file_size}</td></tr>
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
			if selecteds
				sc = selecteds[c, 1].to_i
				line_select << "<td>"
				line_select << "<SELECT class='form-select form-select-sm' id='item#{c}'>"
				line_select << "<OPTION value='ND'>#{l['nd']}</OPTION>"
				s = ''
				s = 'SELECTED' if sc == 1
				line_select << "<OPTION value='date' #{s}>#{l['date']}</OPTION>"

				kexa.each.with_index( 2 ) do |( k, v ), i|
					s = ''
					s = 'SELECTED' if sc == i
					line_select << "<OPTION value='#{k}' #{s}>#{k}</OPTION>" if v == '1'
				end
				line_select << "/<SELECT>"
				line_select << "</td>"
			else
				line_select << "<td>"
				line_select << "<SELECT class='form-select form-select-sm' id='item#{c}'>"
				line_select << "<OPTION value='ND'>#{l['nd']}</OPTION>"
				line_select << "<OPTION value='date'>#{l['date']}</OPTION>"
				kexa.each do |k, v|
					line_select << "<OPTION value='#{k}'>#{k}</OPTION>" if v == '1'
				end
				line_select << "/<SELECT>"
				line_select << "</td>"
			end
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
	<th>#{l['line1']}</th>
		#{line1_html}
	</tr>

	<tr>
		<th>#{l['line2']}</th>
		#{line2_html}
	</tr>

	<tr>
		<th>#{l['field']}</th>
		#{line_select}
	</tr>
</table>

<div class='row'>
	<div class='col-2'>
		<div class='form-check'>
			<input class='form-check-input' type='checkbox' id='skip_line1' #{skip_line1_checked}>
			<label class='form-check-label'>#{l['ignore1']}</label>
		</div>
	</div>
	<div class='col-2'>
		<div class='form-check'>
			<input class='form-check-input' type='checkbox' id='overwrite'  #{overwrite_checked}>
			<label class='form-check-label'>#{l['ow']}</label>
		</div>
	</div>
</div>
<div class='row'>
	<button type='button' class='btn btn-sm btn-warning' onclick=\"writekoyomiex( '#{tmp_file}', '#{line1.size}', '#{l['msg_err1']}' )\">#{l['record']}</button>
</div>
HTML20
########
		########

	else
		puts l['msg_err']
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
	kex_key.each.with_index( 0 ) do |e, i|
		kex_posi['date'] = i if e == 'date'
		kex_posi[e] = i if e != nil && e != '' && e != 'ND'
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
			puts l['msg_err2']
			exit
		end
	end

	puts "Infom result<br>" if @debug
	html[30] = ''
	html[30] << "#{l['msg_res1']}<br>" if skip_line1 == '1'
	if overwrite == '1'
		html[30] << "#{l['msg_res2']} (#{count}/#{matrix.size})<br>"
	else
		html[30] << "#{l['msg_res3']} (#{count}/#{matrix.size})<br>"
	end
end

puts html.join


if command == 'update'
	puts 'UPDATE config<br>' if @debug
	selecteds_ = ''
	a = item_solid.split( ':' )
	a.each do |e|
		if e == 'ND'
			selecteds_ << '0'
		elsif e == 'date'
			selecteds_ << '1'
		else
			kexu.each.with_index( 2 ) do |( k, v ), i|
				selecteds_ << i.to_s if e == k
			end
		end
	end

	kexin = { 'skip_line1'=>skip_line1, 'overwrite'=>overwrite, 'selecteds'=>selecteds_ }
	koyomi_ = JSON.generate( { "start"=>start,  "kexu"=>kexu, "kexa"=>kexa, "kexin"=>kexin } )
	mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomi='#{koyomi_}' WHERE user='#{user.name}';", false, @debug )
end
