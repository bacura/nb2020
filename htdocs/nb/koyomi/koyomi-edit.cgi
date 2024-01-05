#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi editor 0.22b (2023/10/04)


#==============================================================================
# STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
# LIBRARY
#==============================================================================
require '../soul'
require '../brain'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'breakfast' => "朝食",\
		'lunch' 	=> "昼食",\
		'dinner' 	=> "夕食",\
		'supply'	=> "間食 / 補食",\
		'control'	=> "操作",\
		'meal'		=> "食事内容",\
		'volume'	=> "摂取量",\
		'start'		=> "開始時刻",\
		'period'	=> "食事時間",\
		'some'		=> "何か食べた",\
		'some-'		=> "小盛",\
		'some='		=> "並盛",\
		'some+'		=> "大盛",\
		'some--'	=> "微盛",\
		'some++'	=> "特盛",\
		'somep'		=> "写真",\
		'plus'		=> "＋",\
		'copy'		=> "複製",\
		'move'		=> "移動",\
		'memo'		=> "メモ",\
		'clear'		=> "お片付け",\
		'return'	=> "<img src='bootstrap-dist/icons/signpost-r.svg' style='height:2em; width:2em;'>",\
		'visionnerz'=> "<img src='bootstrap-dist/icons/graph-up.svg' style='height:2em; width:2em;'>",\
		'write'		=> "<img src='bootstrap-dist/icons/pencil-square.svg' style='height:3em; width:3em;'>",\
		'recipe'	=> "<img src='bootstrap-dist/icons/card-text.svg' style='height:1.2em; width:1.2em;'>",\
		'camera'	=> "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>",\
		'trashf'	=> "<img src='bootstrap-dist/icons/trash-fill.svg' style='height:1.2em; width:1.2em;'>",\
		'trash'		=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.2em; width:1.2em;'>"
		}

	return l[language]
end

def meals( e, l, db, freeze_flag )
	mb_html = "<table class='table table-sm table-hover'>"
	mb_html << '<thead class="table-light">'
	mb_html << '<tr>'
	mb_html << "<td>#{l['meal']}</td>"
	mb_html << "<td>#{l['volume']}</td>"
	mb_html << "<td>#{l['start']}</td>"
	mb_html << "<td>#{l['period']}</td>"
	mb_html << '<td></td>'
	mb_html << '</tr>'
	mb_html << '</thead>'

	a = e['koyomi'].split( "\t" )
	c = 0
	a.each do |ee|
		aa = ee.split( '~' )
		code = aa[0]
		wt = aa[1]
		unit = aa[2]
		hh_mm = aa[3]
		meal_time = aa[4]
		item_name = ''
		onclick = ''
		fix_copy_button = ''
		recipe_button = ''

		if /^\?/ =~ code
			item_name = @something[code]
		elsif /\-m\-/ =~ code
			rr = db.query( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{code}';", false )
			if rr.first
				item_name = rr.first['name']
			else
				item_name = "<span class='error'>ERROR: #{code}</span>"
			end
			onclick = ""
		elsif /\-z\-/ =~ code
			rr = db.query( "SELECT name FROM #{$MYSQL_TB_FCZ} WHERE user='#{db.user.name}' AND code='#{code}' AND base='fix';", false )
			if rr.first
				item_name = rr.first['name']
				origin = "#{e['date'].year}:#{e['date'].month}:#{e['date'].day}:#{e['tdiv']}:#{c}"
				onclick = " onclick=\"modifyKoyomif( '#{code}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{hh_mm}', '#{meal_time}', '#{c}' )\"" if freeze_flag == 0
				fix_copy_button = "<span onclick=\"modifysaveKoyomiFC( '#{code}', '#{origin}' )\">#{l['move']}</span>"
			else
				item_name = "<span class='error'>ERROR: #{code}</span>"
				onclick = ''
			end
		elsif /\-/ =~ code
			rr = db.query( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';", false )
			if rr.first
				item_name = rr.first['name']
				onclick = " onclick=\"modifyKoyomi( 'modify', '#{code}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{hh_mm}', '#{meal_time}', '#{wt}', '#{unit}', '#{c}' )\"" if freeze_flag == 0
				recipe_button = "<span onclick=\"initCB( 'load', '#{code}' )\">#{l['recipe']}</span>"
			else
				item_name = "<span class='error'>ERROR: #{code}</span>"
			end
		else
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{db.user.name}';" if /^U\d{5}/ =~ code
			rr = db.query( q, false )
			if rr.first
				item_name = rr.first['name']
 				if freeze_flag == 0
 					onclick = " onclick=\"modifyKoyomi( 'modify', '#{code}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{hh_mm}', '#{meal_time}', '#{wt}', '#{unit}', '#{c}' )\""
 				else
 					onclick = " onclick=\"modifyKoyomi( 'fzc_mode', '#{code}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{hh_mm}', '#{meal_time}', '#{wt}', '#{unit}', '#{c}' )\""
 				end
			else
				item_name = "<span class='error'>ERROR: #{code}</span>"
			end
		end
		mb_html << "<tr>"
		mb_html << "<td#{onclick}>#{item_name}</td>"

		if /\-z\-/ =~ code ||  /^\?/ =~ code
			mb_html << "<td#{onclick}>-</td>"
		elsif /\-m\-/ =~ code || /\-/ =~ code
			mb_html << "<td#{onclick}>#{wt}&nbsp;#{unit}</td>"
		else
			uw = ''
			rate = food_weight_check( wt ).last
			uw = "&nbsp;(#{unit_weight( rate, unit, code ).to_f} g)" if unit != 'g'
			mb_html << "<td#{onclick}>#{wt}&nbsp;#{unit}#{uw}</td>"
		end

		mb_html << "<td#{onclick}>#{aa[3]}</td>"
		mb_html << "<td#{onclick}>#{aa[4]}</td>"

		if freeze_flag == 0
			mb_html << "<td>"
			mb_html << "<div class='row'>"

			mb_html << "	<div class='col-6'>"
			mb_html << fix_copy_button unless fix_copy_button == ''
			mb_html << recipe_button unless recipe_button == ''
			mb_html << "	</div>"

			mb_html << "<div class='col-6'>"
			mb_html << "	<span onclick=\"deleteKoyomi( '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{code}', '#{c}' )\">#{l['trash']}</span>"
			mb_html << "</div>"

			mb_html << "</div>"
			mb_html << "</td>"
		else
			mb_html << "<td></td>"
		end
		mb_html << '</tr>'
		c += 1
	end
	mb_html << '</table>'

	return mb_html
end


#### View photos series
def view_series( user, code, del_icon, size, dd )
	media = Media.new( user )
	media.code = code
	media.load_series()

	html = ''
	if media.series.size > 0
		html << "<div class='row'>"
		media.series.each do |e|
			html << "<div class='col'>"
			html << "<span onclick=\"koyomiPhotoDel( '#{code}', '#{e}', '#{dd}' )\">#{del_icon}</span><br>"
			html << "<a href='#{$PHOTO}/#{e}.jpg' target='photo'><img src='#{$PHOTO}/#{e}-tn.jpg' width='#{size}px' class='img-thumbnail'></a>"
			html << "</div>"
		end
		html << "</div>"
	else
		html << 'No photo'
	end

	return html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )

puts 'Getting POST' if @debug
command = @cgi['command']
yyyy = @cgi['yyyy'].to_i
mm = @cgi['mm'].to_i
dd = @cgi['dd'].to_i
yyyy_mm = @cgi['yyyy_mm']
unless yyyy_mm == ''
	a = yyyy_mm.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
end

yyyy_mm_dd = @cgi['yyyy_mm_dd']
unless yyyy_mm_dd == ''
	a = yyyy_mm_dd.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
	dd = a[2].to_i if dd == 0
end

tdiv = @cgi['tdiv'].to_i
code = @cgi['code']
memo = @cgi['memo']
order = @cgi['order'].to_i
some = @cgi['some']
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "code:#{code}<br>\n"
	puts "memo:#{memo}<br>\n"
	puts "order:#{order}<br>\n"
	puts "some: #{some}<br>\n"
	puts "<hr>\n"
end


case command
when 'delete'
	puts 'Deleting food<br>' if @debug
	r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
	a = r.first['koyomi'].split( "\t" )
	new_meal = ''
	a.size.times do |c|
		new_meal << "#{a[c]}\t" if c != order
	end
	new_meal.chop!

	db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{new_meal}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", true )
	db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND code='#{code}';", true ) 	if /\-z\-/ =~ code

when 'memo'
	puts 'Updating memo<br>' if @debug
	r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false )
	if r.first
		db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{memo}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", true )
	else
		db.query( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET fzcode='', freeze='0', koyomi='#{memo}', user='#{user.name}', date='#{yyyy}-#{mm}-#{dd}', tdiv='4';", true )
	end

when 'some'
	puts 'Saving Something<br>' if @debug
	koyomi = "#{some}~0~0~0~0"
	r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
	if r.first
		db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", true )
	else
		db.query( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", true )
	end

when 'clear'
	puts 'Clear koyomi<br>' if @debug
	r = db.query( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}';", true )
	codes = []
	r.each do |e|
		a = e['koyomi'].split( "\t" ) if e['koyomi']
		a.each do |ee|
			code = ee.split( '~' )[0]
			codes << "'#{code}'" if /\-z\-/ =~ code
		end
	end
	if codes.size != 0
		code_in = codes.join( ',' )
		db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND code IN(#{code_in});", true )
	end
	db.query( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}';", true )
end


puts 'Deleting empty entry<br>' if @debug
db.query( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND freeze=0 AND ( koyomi='' OR koyomi IS NULL OR DATE IS NULL );", true )


puts 'Setting palette<br>' if @debug
freeze_flag = 0
koyomi_html = []

palette = Palette.new( user.name )
palette.set_bit( $PALETTE_DEFAULT_NAME[user.language][0] )


puts 'Updaing media<br>' if @debug
4.times do |tdiv|
	r = db.query( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND code='#{yyyy}-#{mm}-#{dd}-#{tdiv}';", false )
	if r.first
		rr = db.query( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
		db.query( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}', koyomi='?P';", true ) unless rr.first
	else
		rr = db.query( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
		if rr.first
			db.query( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", true ) if rr.first['koyomi'] == '?P'
		end
	end
end


puts 'Updaing freeze<br>' if @debug
r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
freeze_flag = r.first['freeze'].to_i if r.first
r.each do |e|
	if e['tdiv'] == 4
		koyomi_html[e['tdiv']] = e['koyomi']
	else
		koyomi_html[e['tdiv']] = meals( e, l, db, freeze_flag )
		fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
		fct.load_palette( palette.bit )

		if freeze_flag == 1
			if e['fzcode'] != ""
				fct.load_fcz( user.name, e['fzcode'], 'freeze' )
				fct.calc
			end
		else
			code_set = []
			rate_set = []
			unit_set = []

			puts 'Raw<br>' if @debug
			a = []
			a = e['koyomi'].split( "\t" ) if e['koyomi']
			a.each do |ee|
				koyomi_code, koyomi_rate, koyomi_unit = ee.split( '~' )[0..2]
				code_set << koyomi_code
				rate_set << koyomi_rate
				unit_set << koyomi_unit
			end

			code_set.size.times do |cc|
				code = code_set[cc]
				rate = food_weight_check( rate_set[cc] ).last
				unit = unit_set[cc]

				if /\?/ =~ code



				elsif /\-z\-/ =~ code
					puts 'FIX<br>' if @debug
					fct.load_fcz( user.name, code, 'fix' )
				else
					puts 'Recipe<br>' if @debug
					recipe_codes = []
					if /\-m\-/ =~ code
						recipe_codes = menu2rc( user.name, code )
					else
						recipe_codes << code
					end

					food_nos = []
					food_weights = []
					recipe_codes.each do |e|
						if /\-r\-/ =~ e || /\w+\-\h{4}\-\h{4}/ =~ e
							fns, fws = recipe2fns( user.name, e, rate, unit, 1 )[0..1]
							food_nos.concat( fns )
							food_weights.concat( fws )
						else
							food_nos << code
							food_weights << unit_weight( rate, unit, code )
						end
					end

					puts 'Foods<br>' if @debug
					fct.set_food( user.name, food_nos, food_weights, false )
				end
			end

			puts 'Start calculation<br>' if @debug
			fct.calc
			fct.digit

			if fct.foods.size != 0
				puts "freeze process<br>" if @debug
				fzcode = fct.save_fcz( user.name, nil, 'freeze', "#{yyyy}-#{mm}-#{dd}-#{e['tdiv']}" )
				db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{fzcode}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{e['tdiv']}';", true )
			else
				db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND origin='#{yyyy}-#{mm}-#{dd}-#{e['tdiv']}';", true )
			end
		end

		total_html = ''
		fct.total.size.times do |i| total_html << "#{fct.names[i]}[#{fct.total[i].to_f}]&nbsp;&nbsp;&nbsp;&nbsp;" end
		koyomi_html[e['tdiv']] << total_html
	end
end


####
cmm_html = [ '', '', '', '' ]
0.upto( 3 ) do |c|
	unless freeze_flag == 1
		cmm_html[c]	<< "<button class='btn btn-sm btn-dark' onclick=\"fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', '#{c}' )\">#{l['plus']}</button>&nbsp;"
	else
		cmm_html[c]	<< "<button class='btn btn-sm btn-secondary'>#{l['plus']}</button>&nbsp;"
	end
	if koyomi_html[c] == nil
		cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{l['copy']}</button>&nbsp;"
		cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{l['move']}</button>&nbsp;"
	else
		cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'copy', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{l['copy']}</button>&nbsp;"
		cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'move', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{l['move']}</button>&nbsp;" unless freeze_flag == 1
	end
end


puts 'Setting something<br>' if @debug
some_html = [ '', '', '' ]
if freeze_flag == 0
	0.upto( 2 ) do |c|
		some_html[c] = <<-"SOME"
		<select class='form-select form-select-sm' id='some#{c}' onchange="koyomiSaveSome( '#{yyyy}', '#{mm}', '#{dd}', #{c}, 'some#{c}' )">
			<option value='' selected>#{l['some']}</option>
			<option value='?--'>#{@something['?--']}</option>
			<option value='?-'>#{@something['?-']}</option>
			<option value='?='>#{@something['?=']}</option>
			<option value='?+'>#{@something['?+']}</option>
			<option value='?++'>#{@something['?++']}</option>
			<option value='?0'>#{@something['?0']}</option>
		</select>
SOME
	end
end


puts 'photo upload form<br>' if @debug
form_photo = []
disabled = ''
disabled = 'DISABLED' if freeze_flag == 1
0.upto( 3 ) do |c|
	form_photo[c] = "<form method='post' enctype='multipart/form-data' id='photo_form#{c}'>"
	form_photo[c] << '<div class="input-group input-group-sm">'
	form_photo[c] << "<label class='input-group-text'>#{l['camera']}</label>"
	form_photo[c] << "<input type='file' class='form-control' name='photo' onchange=\"koyomiPhotoSave( '#{yyyy}-#{mm}-#{dd}-#{c}', '#photo_form#{c}', '#{dd}' )\" #{disabled}></div>"
	form_photo[c] << '</form>'
end


puts 'photo frame<br>' if @debug
photo_frame = []
disabled = ''
disabled = 'DISABLED' if freeze_flag == 1
0.upto( 3 ) do |c| photo_frame[c] = view_series( user, "#{yyyy}-#{mm}-#{dd}-#{c}", l['trashf'], 200, dd ) end


####
memo_html = ''
if freeze_flag == 0
	memo_html = <<-"MEMO1"
	<div class='col-10'>
		<textarea class='form-control' id='memo' rows='2'>#{koyomi_html[4]}</textarea>
	</div>
	<div class='col-1'><br>
		<span onclick="memoKoyomi( '#{yyyy}', '#{mm}', '#{dd}' )">#{l['write']}</span>
	</div>
MEMO1
else
	memo_html = <<-"MEMO2"
	<div class='col-10'>
		#{koyomi_html[4]}
	</div>
MEMO2
end





html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{yyyy} / #{mm} / #{dd}</h5></div>
		<div align='center' class='col-8 joystic_koyomi' onclick="editKoyomiR( '#{yyyy}', '#{mm}' )">#{l['return']}</div>
		<div align='center' class='col-2'>
			<input type='checkbox' id='check_kc'>&nbsp;
			<span class='badge rounded-pill npill' onclick="clearKoyomi( '#{yyyy}', '#{mm}', '#{dd}' )">#{l['clear']}</span>
		</div>

	</div>
	<br>

	<div class='row'>
		<h6>#{l['breakfast']}</h6>
		<div class='col-4'>
			<div class="input-group">
				#{cmm_html[0]}
				#{some_html[0]}
			</div>
		</div>
		<div class='col-3'></div>
		<div class='col-5'>#{form_photo[0]}</div>
	</div>
	<div class='row'>
		<div class='col-7'>#{koyomi_html[0]}</div>
		<div class='col-5'>#{photo_frame[0]}</div>
	</div>
	<hr>

	<div class='row'>
		<h6>#{l['lunch']}</h6>
		<div class='col-4'>
			<div class="input-group">
				#{cmm_html[1]}
				#{some_html[1]}
			</div>
		</div>
		<div class='col-3'></div>
		<div class='col-5'>#{form_photo[1]}</div>
	</div>
	<div class='row'>
		<div class='col-7'>#{koyomi_html[1]}</div>
		<div class='col-5'>#{photo_frame[1]}</div>
	</div>
	<hr>

	<div class='row'>
		<h6>#{l['dinner']}</h6>
		<div class='col-4'>
			<div class="input-group">
				#{cmm_html[2]}
				#{some_html[2]}
			</div>
		</div>
		<div class='col-3'></div>
		<div class='col-5'>#{form_photo[2]}</div>
	</div>
	<div class='row'>
		<div class='col-7'>#{koyomi_html[2]}</div>
		<div class='col-5'>#{photo_frame[2]}</div>
	</div>
	<hr>

	<div class='row'>
		<h6>#{l['supply']}</h6>
		<div class='col-4'>
			<div class="input-group">
				#{cmm_html[3]}
				#{some_html[3]}
			</div>
		</div>
		<div class='col-3'></div>
		<div class='col-5'>#{form_photo[3]}</div>
	</div>
	<div class='row'>
		<div class='col-7'>#{koyomi_html[3]}</div>
		<div class='col-5'>#{photo_frame[3]}</div>
	</div>
	<br><br>

	<div class='row'>
		<div class='col-1'><h5>#{l['memo']}</h5></div>
		#{memo_html}
	</div>
</div>

HTML

puts html
