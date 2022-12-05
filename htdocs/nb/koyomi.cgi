#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi 0.14b (2022/12/05)


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomi'
@debug = false

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'
require "./language_/#{script}.lp"

#==============================================================================
#DEFINITION
#==============================================================================

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
def meals_html( meal, user )
	mb_html = '<ul>'
	a = meal.split( "\t" )
	a.each do |e|
		aa = e.split( '~' )
		if /^\?/ =~ aa[0]
			mb_html << "<li style='list-style-type: circle'>#{@something[aa[0]]}</li>"
		elsif /\-m\-/ =~ aa[0]
			puts 'menu' if @debug
			r = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE user='#{user.name} AND code='#{aa[0]}';", false, @debug )
			if r.first
				mb_html << "<li>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		elsif /\-z\-/ =~ aa[0]
			puts 'fix' if @debug
			r = mdb( "SELECT name FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND code='#{aa[0]}';", false, @debug )
			if r.first
				mb_html << "<li style='list-style-type: circle'>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		elsif /\-/ =~ aa[0]
			puts 'recipe' if @debug
			r = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' AND code='#{aa[0]}';", false, @debug )
			if r.first
				mb_html << "<li>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		else
			puts 'food' if @debug
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}' AND user='#{uname}';" if /^U/ =~ aa[0]
			r = mdb( q, false, @debug )
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


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )
l = language_pack( user.language )

#### Guild member check
if user.status < 3
	puts "Guild member error."
	exit
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
		r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='1' WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
		else
	   		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', freeze='1', date='#{sql_ymd}';", false, @debug )
		end
	elsif freeze_check == 'false'
		r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='0' WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
		end
	end
when 'freeze_all'
	if freeze_check_all == 'true'
		1.upto( calendar.ddl ) do |c|
			r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
			if r.first
				if r.first['freeze'] != 1
					mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='1' WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
				end
			else
	   			mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', freeze='1', date='#{sql_ym}-#{c}';", false, @debug )
			end
		end
		freeze_all_checked = 'CHECKED'
	elsif freeze_check_all == 'false'
		 mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='0' WHERE user='#{user.name}' AND ( date BETWEEN '#{sql_ym}-1' AND '#{sql_ym}-#{calendar.ddl}' );", false, @debug )
	end
end


puts "Palette setting<br>" if @debug
palette = Palette.new( user.name )
palette.set_bit( $PALETTE_DEFAULT_NAME[user.language][0] )


puts "Multi calc process<br>" if @debug
fct_day_htmls = ['']
visio_htmls = ['']
1.upto( calendar.ddl ) do |c|
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
	fct_day = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
	fct_day.load_palette( palette.bit )
	freeze_flag = false

	r.each do |e|
		if e['tdiv'].to_i < 4 && e['koyomi'] != nil && e['koyomi'] != ''

			fzcode = e['fzcode']
			code_set = []
			rate_set = []
			unit_set = []

			fct_tdiv = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
			fct_tdiv.load_palette( palette.bit )

			if e['freeze'] == 1
				puts "Freeze:#{fzcode}<br>" if @debug
				if fct_tdiv.load_fcz( user.name, fzcode, 'freeze' )
					fct_day.into_solid( fct_tdiv.solid[0] )
					freeze_flag = true
				end
			else
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
						fct_tdiv.into_zero
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
								fns, fws, z = recipe2fns( user.name, e, rate, unit )
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
					fzcode = fct_tdiv.save_fcz( user.name, nil, 'freeze', "#{sql_ym}-#{c}-#{e['tdiv']}" )
					mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{fzcode}' WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}' AND tdiv='#{e['tdiv']}';", false, @debug )
				else
					mdb( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND origin='#{sql_ym}-#{c}-#{e['tdiv']}';", false, @debug )
				end
			end
		end
	end
	puts "Summary#{c} html<br>" if @debug
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
			t << "<br><span style='color:crimson'>P</span>:<span style='color:green'>F</span>:<span style='color:blue'>C</span> (%) = "
			t << "<span style='color:crimson'>#{pfc[0]}</span> : <span style='color:green'>#{pfc[1]}</span> : <span style='color:blue'>#{pfc[2]}</span>"
			t << "&nbsp;&nbsp;<span onclick=\"visionnerz( '#{sql_ym}-#{c}' )\">#{l['visionnerz']}</span>" if user.status >= 5
		end
		fct_day_htmls << t
	end

	unless r.first
 		mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}' AND koyomi='';", false, @debug )
 		0.upto( 3 ) do |i|
 			mdb( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND origin='#{sql_ym}-#{c}-#{i}';", false, @debug )
 		end
	end
end

puts "Day process<br>" if @debug
date_html = ''
week_count = calendar.wf
weeks = [l['sun'], l['mon'], l['tue'], l['wed'], l['thu'], l['fri'], l['sat']]
1.upto( calendar.ddl ) do |c|
	freeze_flag = false
	koyomi_tmp = []

	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
	if r.first
		r.each do |e|
			koyomi_tmp[e['tdiv']] = e['koyomi'] if e['tdiv']
			freeze_flag = true if r.first['freeze'] == 1
		end
	else
		5.times do koyomi_tmp << nil end
	end

	date_html << "<tr id='day#{c}'>"
	style = ''
	style = 'color:red;' if week_count == 0
	date_html << "<td style='#{style}'><span>#{c}</span> (#{weeks[week_count]})</td>"

	onclick = "onclick=\"editKoyomi( 'init', '#{c}' )\""
	4.times do |cc|
		tmp = '-'
		tmp = meals_html( koyomi_tmp[cc], user ) if koyomi_tmp[cc]
		date_html << "<td #{onclick}>#{tmp}</td>"
	end

	tmp = '-'
	tmp = koyomi_tmp[4] if koyomi_tmp[4]
	date_html << "<td #{onclick}>#{tmp}</td>"

	freeze_checked = ''
	freeze_checked = 'CHECKED' if freeze_flag
	date_html << "<td><input type='checkbox' id='freeze_check#{c}' onChange=\"freezeKoyomi( '#{c}' )\" #{freeze_checked}></td>"
	date_html << "</tr>"

	style = ''
	style = 'display:none' if fct_day_htmls[c] == '' || fct_day_htmls[c] == nil
	date_html << "<tr id='nutrition#{c}' class='table-borderless' style='#{style}'>"
	date_html << "<td></td><td colspan='6'>#{fct_day_htmls[c]}</td>"
#	date_html << "<td></td>"
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

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'></th>
     		<th align='center' width='15%'>#{l['breakfast']}</th>
     		<th align='center' width='15%'>#{l['lunch']}</th>
     		<th align='center' width='15%'>#{l['dinner']}</th>
     		<th align='center' width='15%'>#{l['supply']}</th>
     		<th align='center'>#{l['memo']}</th>
     		<th align='center'><input type='checkbox' id='freeze_check_all' onChange="freezeKoyomiAll()" #{freeze_all_checked}>&nbsp;#{l['snow']}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>
HTML

puts html


#### Deleting Empty koyomi
mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE koyomi IS NULL OR koyomi='';", false, @debug )
