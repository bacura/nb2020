#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi 0.22b (2023/12/24)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require '../soul'
require '../brain'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'koyomi' 	=> "こよみ:食事",\
		'sun' 		=> "日",\
		'mon' 		=> "月",\
		'tue' 		=> "火",\
		'wed' 		=> "水",\
		'thu' 		=> "木",\
		'fri' 		=> "金",\
		'sat' 		=> "土",\
		'year' 		=> "年",\
		'breakfast' => "朝食",\
		'lunch' 	=> "昼食",\
		'dinner' 	=> "夕食",\
		'supply'	=> "間食 / 補食",\
		'memo' 		=> "メモ",\
		'foodrec' 	=> "食事記録",\
		'exrec'		=> "拡張記録",\
		'calc' 		=> "栄養計算",\
		'compo' 	=> "食品構成",\
		'g100' 		=> "100 g相当",\
		'food_n' 	=> "食品名",\
		'food_g'	=> "食品群",\
		'weight'	=> "重量(g)",\
		'palette'	=> "パレット",\
		'snow'		=> "<img src='bootstrap-dist/icons/snow2.svg' style='height:1.2em; width:1.2em;'>",\
		'visionnerz'=> "<img src='bootstrap-dist/icons/graph-up.svg' style='height:2em; width:1.0em;'>",\
		'return'	=> "<img src='bootstrap-dist/icons/geo.svg' style='height:2em; width:2em;'>"
	}

	return l[language]
end

####
def sub_menu( l )
	html = <<-"MENU"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><span class='btn badge rounded-pill ppill' onclick="initKoyomi()">#{l['foodrec']}</span></div>
		<div class='col-2'><span class='btn badge rounded-pill ppill' onclick="initKoyomiex()">#{l['exrec']}</span></div>
		<div class='col-2'><span class='btn badge rounded-pill ppill' onclick="initKoyomiCalc()">#{l['calc']}</span></div>
		<div class='col-2'><span class='btn badge rounded-pill ppill' onclick="initKoyomiCompo()">#{l['compo']}</span></div>
		<div class='col-2'></div>
	</div>
</div>

MENU
	puts html
	exit()
end


####
def meals_html( meal, db )
	mb_html = '<ul>'
	a = meal['koyomi'].split( "\t" )
	a.each do |e|
		aa = e.split( '~' )
		if /^\?/ =~ aa[0]
			mb_html << "<li style='list-style-type: circle'>#{@something[aa[0]]}</li>"
		elsif /\-m\-/ =~ aa[0]
			puts 'menu' if @debug
			r = db.query( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE user='#{db.user.name} AND code='#{aa[0]}';", false )
			if r.first
				mb_html << "<li>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		elsif /\-z\-/ =~ aa[0]
			puts 'fix' if @debug
			r = db.query( "SELECT name FROM #{$MYSQL_TB_FCZ} WHERE user='#{db.user.name}' AND base='fix' AND code='#{aa[0]}';", false )
			if r.first
				mb_html << "<li style='list-style-type: circle'>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		elsif /\-/ =~ aa[0]
			puts 'recipe' if @debug
			r = db.query( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE user='#{db.user.name}' AND code='#{aa[0]}';", false )
			if r.first
				mb_html << "<li>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		else
			puts 'food' if @debug
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}' AND user='#{db.user.name}';" if /^U/ =~ aa[0]
			r = db.query( q, false )
			if r.first
				mb_html << "<li style='list-style-type: square'>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		end
	end
	mb_html << '</ul>'

	return mb_html
end


def media_html( yyyy, mm, dd, tdiv, db )
	html = ''
	r = db.query( "SELECT mcode, zidx FROM #{$MYSQL_TB_MEDIA} WHERE user='#{db.user.name}' AND code='#{yyyy}-#{mm}-#{dd}-#{tdiv}' AND type='jpg' ORDER BY zidx;", false )
	r.each do |e|
		html << "<a href='#{$PHOTO}/#{e['mcode']}.jpg' target='media'><img src='#{$PHOTO}/#{e['mcode']}-tns.jpg' class='photo_tns'></a>"
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

#### Guild member check
if user.status < 3
	puts "Guild member error."
#	exit
end


#### Getting POST
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
dd = 1 if dd == 0
freeze_check = @cgi['freeze_check']
freeze_check_all = @cgi['freeze_check_all']
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "freeze_check:#{freeze_check}<br>\n"
	puts "freeze_check_all:#{freeze_check_all}<br>\n"
	puts "<hr>\n"
end


#### Sub menu
sub_menu ( l ) if command == 'menu'


puts "Date & calendar config<br>" if @debug
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar_td = Calendar.new( user.name, 0, 0, 0 )

calendar.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"


puts "Freeze process<br>" if @debug
freeze_all_checked = ''
case command
when 'freeze'
	if freeze_check == 'true'
		db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='1' WHERE user='#{user.name}' AND date='#{sql_ymd}';", true )
	elsif freeze_check == 'false'
		db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='0' WHERE user='#{user.name}' AND date='#{sql_ymd}';", true )
	end
when 'freeze_all'
	if freeze_check_all == 'true'
		db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='1' WHERE user='#{user.name}' AND ( date BETWEEN '#{sql_ym}-1' AND '#{sql_ym}-#{calendar.ddl}' );", true )
		freeze_all_checked = 'CHECKED'
	elsif freeze_check_all == 'false'
		 db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='0' WHERE user='#{user.name}' AND ( date BETWEEN '#{sql_ym}-1' AND '#{sql_ym}-#{calendar.ddl}' );", true )
	end
end


puts "Palette setting<br>" if @debug
palette = Palette.new( user.name )
palette.set_bit( $PALETTE_DEFAULT_NAME[user.language][0] )


puts "koyomi matrix<br>" if @debug
koyomi_mx = []
31.times do |i| koyomi_mx[i + 1] = Array.new end
r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND koyomi!='' AND koyomi IS NOT NULL AND date BETWEEN '#{sql_ym}-1' AND '#{sql_ym}-31';", false )
r.each do |e| koyomi_mx[e['date'].day][e['tdiv']] = e end

puts "html parts<br>" if @debug
fct_day_htmls = ['']

fct_day = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct_day.load_palette( palette.bit )

fct_tdiv = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct_tdiv.load_palette( palette.bit )

puts "koyomi matrix calc<br>" if @debug
1.upto( calendar.ddl ) do |day|
	if koyomi_mx[day] != nil
		freeze_flag = false
		code_set = []
		rate_set = []
		unit_set = []

		fct_day.flash

		4.times do |tdiv|
			kmre = koyomi_mx[day][tdiv]
			fct_tdiv.flash
			code_set = []
			rate_set = []
			unit_set = []

			if kmre != nil
				fzcode = kmre['fzcode']
				if kmre['freeze'] == 1

					puts "Freeze:#{fzcode}<br>" if @debug
					if fzcode != ''
						if fct_tdiv.load_fcz( user.name, fzcode, 'freeze' )
							fct_day.into_solid( fct_tdiv.solid[0] )
						end
					end
					freeze_flag = true
				else
					puts 'Row<br>' if @debug
					a = []
					a = kmre['koyomi'].split( "\t" )
					a.each do |e|
						koyomi_code, koyomi_rate, koyomi_unit = e.split( '~' )[0..2]
						code_set << koyomi_code
						rate_set << koyomi_rate
						unit_set << koyomi_unit
					end

					code_set.size.times do |c|
						code = code_set[c]
						rate = food_weight_check( rate_set[c] ).last
						unit = unit_set[c]

						if /\?/ =~ code
							fct_day.into_zero
						elsif /\-z\-/ =~ code
							puts 'FIX<br>' if @debug
							fct_tdiv.load_fcz( user.name, code, 'fix' )
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
							fct_tdiv.set_food( user.name, food_nos, food_weights, false )
						end
					end

					puts 'Start calculation<br>' if @debug
					fct_tdiv.calc
					fct_tdiv.digit

					fct_day.into_solid( fct_tdiv.total )

					if fct_tdiv.foods.size != 0
						puts "freeze process<br>" if @debug

						fzcode = fct_tdiv.save_fcz( user.name, nil, 'freeze', "#{sql_ym}-#{day}-#{tdiv}" )
						db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{fzcode}' WHERE user='#{user.name}' AND date='#{sql_ym}-#{day}' AND tdiv='#{tdiv}';", true )
					else
						db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND origin='#{sql_ym}-#{day}-#{tdiv}';", true )
					end
				end
			end
		end
		
		puts "Summary#{day} html<br>" if @debug
		fct_day.calc
		fct_day.digit
		pfc = fct_day.calc_pfc

		if fct_day.foods.size == 0 && freeze_flag == false
			fct_day_htmls << ''
		else
			t = ''
			fct_day.names.size.times do |i|
				t << "#{fct_day.names[i]}[#{fct_day.total[i]}]&nbsp;&nbsp;&nbsp;&nbsp;"
			end

			if pfc.size == 3
				t << "&nbsp;&nbsp;<span style='color:crimson'>P</span>:<span style='color:green'>F</span>:<span style='color:blue'>C</span> (%) = "
				t << "<span style='color:crimson'>#{pfc[0]}</span> : <span style='color:green'>#{pfc[1]}</span> : <span style='color:blue'>#{pfc[2]}</span>"
				t << "&nbsp;&nbsp;<span onclick=\"visionnerz( '#{sql_ym}-#{day}' )\">#{l['visionnerz']}</span>" if user.status >= 5
			end
			fct_day_htmls << t
		end
		
		if koyomi_mx[day][4] != nil
		end
	end
end


puts "Day process<br>" if @debug
date_html = ''
week_count = calendar.wf
weeks = [l['sun'], l['mon'], l['tue'], l['wed'], l['thu'], l['fri'], l['sat']]
1.upto( calendar.ddl ) do |day|
	puts "Day #{day}<br>" if @debug
	freeze_flag = false
	active_flag = true
	kmrd = koyomi_mx[day]
	onclick = "onclick=\"editKoyomi( 'init', '#{day}' )\""

	tmp_html = ''
	if kmrd.size != 0
		5.times do |tdiv|
			tmp = '-'
			if kmrd[tdiv] != nil
				if tdiv < 4
					tmp = meals_html( kmrd[tdiv], db )
					tmp << media_html( calendar.yyyy, calendar.mm, day, tdiv, db  )
				else
					tmp = kmrd[4]['koyomi']
				end

				freeze_flag = true if kmrd[tdiv]['freeze'] == 1
			end
			tmp_html << "<td #{onclick}>#{tmp}</td>"
		end
	else
		5.times do tmp_html << "<td #{onclick}>-</td>" end
		active_flag = false
	end

	style = ''
	style = 'color:red;' if week_count == 0
	date_html << "<tr id='day#{day}'>"
	date_html << "<td align='center' rowspan=2 style='#{style}'><span>#{day}</span> (#{weeks[week_count]})"
	date_html << "<br><br><input type='checkbox' id='freeze_check#{day}' onChange=\"freezeKoyomi( '#{day}' )\" #{$CHECK[freeze_flag]}>" if active_flag
	date_html << "</td>"
	date_html << tmp_html
	date_html << "</tr>"

	date_html << "<tr>"
	date_html << "<td colspan='5' #{onclick}>#{fct_day_htmls[day]}</td>" if fct_day_htmls[day] != nil
	date_html << "</tr>"

	week_count += 1
	week_count = 0 if week_count > 6
end


joystic_goto = calendar_td.dd - 1
joystic_goto = 1 if joystic_goto < 1


puts "HTML process<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{l['koyomi']}</h5></div>
		<div class='col-2 form-inline'>
			<input type='month' class='form-control form-control-sm' id='yyyy_mm' min='#{calendar.yyyyf}-01' max='#{calendar.yyyy + 2}-01' value='#{calendar.yyyy}-#{calendar.mms}' onChange="changeKoyomi()">
		</div>
		<div align='center' class='col-8 joystic_koyomi' onclick="window.location.href='#day#{joystic_goto}';">#{l['return']}</div>
	</div>
	<br>

	<table class="table table-sm">
	<thead class="table-light">
    	<tr>
     		<th align='center'>
     			<div class="form-check">
     				<input class="form-check-input" type='checkbox' id='freeze_check_all' onChange="freezeKoyomiAll()" #{freeze_all_checked}>
					<label class="form-check-label">#{l['snow']}</label>
				</div>
     		</th>
     		<th align='center' width='15%'>#{l['breakfast']}</th>
     		<th align='center' width='15%'>#{l['lunch']}</th>
     		<th align='center' width='15%'>#{l['dinner']}</th>
     		<th align='center' width='15%'>#{l['supply']}</th>
     		<th align='center'>#{l['memo']}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>
HTML

puts html

#==============================================================================
# POST PROCESS
#==============================================================================

#### Deleting Empty koyomi
db.query( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE koyomi IS NULL OR koyomi='';", true )
