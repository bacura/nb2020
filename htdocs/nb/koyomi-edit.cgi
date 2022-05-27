#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi editor 0.17b


#==============================================================================
# LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
# STATIC
#==============================================================================
script = 'koyomi-edit'
@debug = false


#==============================================================================
# DEFINITION
#==============================================================================
def meals( e, lp, user, freeze_flag )
	mb_html = "<table class='table table-sm table-hover'>"
	mb_html << "<thead>"
	mb_html << "<tr>"
	mb_html << "<td>#{lp[8]}</td>"
	mb_html << "<td>#{lp[9]}</td>"
	mb_html << "<td>#{lp[10]}</td>"
	mb_html << "<td>#{lp[21]}</td>"
	mb_html << "<td></td>"
	mb_html << "</tr>"
	mb_html << "</thead>"

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
			rr = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{code}';", false, @debug )
			if rr.first
				item_name = rr.first['name']
			else
				item_name = "<span class='error'>ERROR: #{code}</span>"
			end
			onclick = ""
		elsif /\-z\-/ =~ code
			rr = mdb( "SELECT name FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND code='#{code}' AND base='fix';", false, @debug )
			if rr.first
				item_name = rr.first['name']
				origin = "#{e['date'].year}:#{e['date'].month}:#{e['date'].day}:#{e['tdiv']}:#{c}"
				onclick = " onclick=\"modifysaveKoyomiFC( '#{code}', '#{origin}' )\"" if freeze_flag == 0
				fix_copy_button = "<span onclick=\"modifyKoyomif( '#{code}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{hh_mm}', '#{meal_time}', '#{c}' )\">#{lp[30]}</span>"
			else
				item_name = "<span class='error'>ERROR: #{code}</span>"
				onclick = ''
			end
		elsif /\-/ =~ code
			rr = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';", false, @debug )
			if rr.first
				item_name = rr.first['name']
				onclick = " onclick=\"modifyKoyomi( '#{code}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{hh_mm}', '#{meal_time}', '#{wt}', '#{unit}', '#{c}' )\"" if freeze_flag == 0
				recipe_button = "<span onclick=\"initCB( 'load', '#{code}' )\">#{lp[31]}</span>"
			else
				item_name = "<span class='error'>ERROR: #{code}</span>"
			end
		else
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{user.name}';" if /^U\d{5}/ =~ code
			rr = mdb( q, false, @debug )
			if rr.first
				item_name = rr.first['name']
				onclick = " onclick=\"modifyKoyomi( '#{code}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{hh_mm}', '#{meal_time}', '#{wt}', '#{unit}', '#{c}' )\"" if freeze_flag == 0
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
			food_weight, rate = food_weight_check( wt )
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
			mb_html << "	<span onclick=\"deleteKoyomi( '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{code}', '#{c}' )\">#{lp[27]}</span>"
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
lp = user.load_lp( script )


puts 'Getting koyomi start year<br>' if @debug
r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	if r.first['koyomi'] != nil && r.first['koyomi'] != ''
		koyomi = JSON.parse( r.first['koyomi'] )
		start_yesr = koyomi['start'].to_i
		p koyomi if @debug
	end
end


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
	dd = a[2].to_i
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


if command == 'delete'
	puts 'Deleting food<br>' if @debug
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	a = r.first['koyomi'].split( "\t" )
	new_meal = ''
	a.size.times do |c|
		new_meal << "#{a[c]}\t" if c != order
	end
	new_meal.chop!

	mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{new_meal}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	mdb( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND code='#{code}';", false, @debug ) 	if /\-z\-/ =~ code
end


if command == 'memo'
	puts 'Updating memo<br>' if @debug
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{memo}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET fzcode='', freeze='0', koyomi='#{memo}', user='#{user.name}', date='#{yyyy}-#{mm}-#{dd}', tdiv='4';", false, @debug )
	end
end


if command == 'some'
	puts 'Saving Something<br>' if @debug
	koyomi = "#{some}~0~0~0~0"
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug)
	end
end


puts 'Deleting empty entry<br>' if @debug
mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND freeze=0 AND ( koyomi='' OR koyomi IS NULL OR DATE IS NULL );", false, @debug )


puts 'Setting palette<br>' if @debug
freeze_flag = 0
koyomi_html = []

palette = Palette.new( user.name )
palette.set_bit( nil )


puts 'Updaing freeze<br>' if @debug
r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
freeze_flag = r.first['freeze'].to_i if r.first
r.each do |e|
	if e['tdiv'] == 4
		koyomi_html[e['tdiv']] = e['koyomi']
	else
		koyomi_html[e['tdiv']] = meals( e, lp, user, freeze_flag )
		fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
		fct.load_palette( palette.bit )
		if freeze_flag == 1
			fct.load_fcz( user.name, e['fzcode'], 'freeze' )
			fct.calc
		else
			code_set = []
			rate_set = []
			unit_set = []

			puts 'Row<br>' if @debug
			a = []
			a = e['koyomi'].split( "\t" ) if e['koyomi']
			a.each do |ee|
				( koyomi_code, koyomi_rate, koyomi_unit, z ) = ee.split( '~' )
				code_set << koyomi_code
				rate_set << koyomi_rate
				unit_set << koyomi_unit
			end

			code_set.size.times do |cc|
				code = code_set[cc]
				z, rate = food_weight_check( rate_set[cc] )
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
							fns, fws, z = recipe2fns( user.name, e, rate, unit )
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
				mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{fzcode}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{e['tdiv']}';", false, @debug )
			else
				mdb( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND origin='#{yyyy}-#{mm}-#{dd}-#{e['tdiv']}';", false, @debug )
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
		cmm_html[c]	<< "<button class='btn btn-sm btn-dark' onclick=\"fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', '#{c}' )\">#{lp[17]}</button>&nbsp;"
	else
		cmm_html[c]	<< "<button class='btn btn-sm btn-secondary'>#{lp[17]}</button>&nbsp;"
	end
	if koyomi_html[c] == nil
		cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{lp[18]}</button>&nbsp;"
		cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{lp[19]}</button>&nbsp;"
	else
		cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'copy', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{lp[18]}</button>&nbsp;"
		cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'move', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{lp[19]}</button>&nbsp;" unless freeze_flag == 1
	end
end


puts 'Setting something<br>' if @debug
some_html = [ '', '', '' ]
if freeze_flag == 0
	0.upto( 2 ) do |c|
		some_html[c] = <<-"SOME"
		<select class='form-select form-select-sm' id='some#{c}' onchange="koyomiSaveSome( '#{yyyy}', '#{mm}', '#{dd}', #{c}, 'some#{c}' )">
			<option value='' selected>#{lp[20]}</option>
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
	form_photo[c] << "<label class='input-group-text'>#{lp[26]}</label>"
	form_photo[c] << "<input type='file' class='form-control' name='photo' onchange=\"koyomiPhotoSave( '#{yyyy}-#{mm}-#{dd}-#{c}', '#photo_form#{c}', '#{dd}' )\" #{disabled}></div>"
	form_photo[c] << '</form>'
end


puts 'photo frame<br>' if @debug
photo_frame = []
disabled = ''
disabled = 'DISABLED' if freeze_flag == 1
0.upto( 3 ) do |c| photo_frame[c] = view_series( user, "#{yyyy}-#{mm}-#{dd}-#{c}", lp[29], 200, dd ) end


####
memo_html = ''
if freeze_flag == 0
	memo_html = <<-"MEMO1"
	<div class='col-10'>
		<textarea class='form-control' id='memo' rows='2'>#{koyomi_html[4]}</textarea>
	</div>
	<div class='col-1'><br>
		<span onclick="memoKoyomi( '#{yyyy}', '#{mm}', '#{dd}' )">#{lp[11]}</span>
	</div>
MEMO1
else
	memo_html = <<-"MEMO2"
	<div class='col-10'>
		#{koyomi_html[4]}
	</div>
MEMO2
end


visionnerz_html = ''
visionnerz_html = "<div align='center' class='col-1 joystic_koyomi' onclick=\"visionnerz( '#{yyyy}-#{mm}-#{dd}' )\">#{lp[22]}</div>" if user.status >= 5


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{yyyy} / #{mm} / #{dd}</h5></div>
		<div align='center' class='col-8 joystic_koyomi' onclick="editKoyomiR( '#{yyyy}', '#{mm}' )">#{lp[7]}</div>
		<div align='center' class='col-1'></div>
		#{visionnerz_html}
	</div>
	<br>

	<div class='row'>
		<h6>#{lp[1]}</h6>
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
		<h6>#{lp[2]}</h6>
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
		<h6>#{lp[3]}</h6>
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
		<h6>#{lp[4]}</h6>
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
		<div class='col-1'><h5>#{lp[28]}</h5></div>
		#{memo_html}
	</div>
</div>

HTML

puts html
