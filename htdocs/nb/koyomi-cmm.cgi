#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi menu copy / move 0.09b (2023/04/09)


#==============================================================================
# STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
# LIBRARY
#==============================================================================
require './soul'
require './brain'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
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
		'time'		=> "分間",\
		'copy' 		=> "複　製",\
		'move' 		=> "移　動",\
		'inheritance'=> "時間継承",\
		'return' 	=> "<img src='bootstrap-dist/icons/signpost-r.svg' style='height:2em; width:2em;'>",\
		'joystick' 	=> "<img src='bootstrap-dist/icons/geo.svg' style='height:2em; width:2em;'>",\
		'clock'		=> "<img src='bootstrap-dist/icons/clock.svg' style='height:1.5em; width:1.5em;'>",\
		'calendar'	=> "<img src='bootstrap-dist/icons/calendar.svg' style='height:2em; width:2em;'>",\
		'return2'	=> "<img src='bootstrap-dist/icons/signpost.svg' style='height:2em; width:2em;'>"
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


#### Getting POST
command = @cgi['command']
yyyy = @cgi['yyyy'].to_i
mm = @cgi['mm'].to_i
dd = @cgi['dd'].to_i
yyyy_mm_dd = @cgi['yyyy_mm_dd']
unless yyyy_mm_dd == ''
	a = yyyy_mm_dd.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
	dd = a[2].to_i
end
tdiv = @cgi['tdiv'].to_i
hh_mm = @cgi['hh_mm']
meal_time = @cgi['meal_time'].to_i
cm_mode = @cgi['cm_mode']
carry_on = @cgi['carry_on']
carry_on = 1 if @cgi['carry_on'] == ''
carry_on = carry_on.to_i
origin = @cgi['origin']
origin = "#{yyyy}:#{mm}:#{dd}:#{tdiv}" if origin == ''
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "hh_mm:#{hh_mm}<br>\n"
	puts "meal_time:#{meal_time}<br>\n"
	puts "cm_mode:#{cm_mode}<br>\n"
	puts "carry_on:#{carry_on}<br>\n"
	puts "origin:#{origin}<br>\n"
	puts "<hr>\n"
end


puts 'Getting date<br>' if @debug
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar.debug if @debug


puts 'Getting koyomi start year<br>' if @debug
r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	if r.first['koyomi'] != nil && r.first['koyomi'] != ''
		koyomi_cfg = JSON.parse( r.first['koyomi'] )
		start_yesr = koyomi_cfg['start'].to_i
		p koyomi_cfg if @debug
	end
end


puts 'Getting standard meal start & time<br>' if @debug
start_time_set = []
meal_tiems_set = []
r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	if r.first['bio'] != nil && r.first['bio'] != ''
		bio = JSON.parse( r.first['bio'] )
		start_times_set = [bio['bst'], bio['lst'], bio['dst']]
		meal_tiems_set = [bio['bti'].to_i, bio['lti'].to_i, bio['dti'].to_i]

		hh_mm = start_times_set[tdiv] if hh_mm == '' || hh_mm == nil
		meal_time = meal_tiems_set[tdiv] if meal_time == 0
	end
end
hh_mm = '00:00' if hh_mm == nil || hh_mm == ''
meal_time = 20 if meal_time == nil || meal_time == '' || meal_time == 0


yyyy_ = nil
mm_ = nil
dd_ = nil
puts 'Save food<br>' if @debug
if command == 'save'
	( yyyy_, mm_, dd_, tdiv_ ) = origin.split( ':' )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy_}-#{mm_}-#{dd_}' AND tdiv='#{tdiv_}';", false, @debug )
	if r.first
		koyomi_ = r.first['koyomi']
		t = ''
		a = koyomi_.split( "\t" )
		a.each do |e|
			aa = e.split( '~' )
			if /\-z\-/ =~ aa[0]
				rr = mdb( "SELECT name FROM #{$MYSQL_TB_FCZ} WHERE code='#{aa[0]}' AND base='fix' AND user='#{user.name}';", false, @debug )
				if rr.first
					fzcode = generate_code( user.name, 'z' )
					db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
					db.query( "CREATE TEMPORARY TABLE tmp SELECT * FROM #{$MYSQL_TB_FCZ} WHERE code='#{aa[0]}' AND base='fix' AND user='#{user.name}';" )
					db.query( "UPDATE tmp SET code='#{fzcode}', origin='#{yyyy}-#{mm}-#{dd}-#{tdiv}' WHERE base='fix' AND user='#{user.name}';" )
					db.query( "INSERT INTO #{$MYSQL_TB_FCZ} SELECT * FROM tmp;" )
					db.query( "DROP TABLE tmp;" )
					db.close
					t << "#{fzcode}~#{aa[1]}~#{aa[2]}~#{hh_mm}~#{meal_time}\t"
				end
			else
				t << "#{aa[0]}~#{aa[1]}~#{aa[2]}~#{hh_mm}~#{meal_time}\t"
			end
		end
		koyomi_ = t.chop

		rr = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		if rr.first
			koyomi = rr.first['koyomi']
			if koyomi == ''
				koyomi << koyomi_
			else
				koyomi << "\t#{koyomi_}"
			end

			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}', fzcode='' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi_}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug )
		end

		if cm_mode == 'move' && ( yyyy != yyyy_.to_i || mm != mm_.to_i || dd != dd_.to_i || tdiv != tdiv_.to_i )
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='' WHERE user='#{user.name}' AND date='#{yyyy_}-#{mm_}-#{dd_}' AND tdiv='#{tdiv_}';", false, @debug )
			origin = "#{yyyy}:#{mm}:#{dd}:#{tdiv}"
		end
		calendar = Calendar.new( user.name, yyyy, mm, dd )
	end
end


puts 'Save button<br>' if @debug
save_button_txt = l['copy']
save_button_txt = l['move'] if cm_mode == 'move'
save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"cmmSaveKoyomi( '#{cm_mode}', '#{origin}' )\">#{save_button_txt}</button>"


puts 'Date HTML<br>' if @debug
date_html = ''
week_count = calendar.wf
weeks = [l['sun'], l['mon'], l['tue'], l['wed'], l['thu'], l['fri'], l['sat']]
1.upto( calendar.ddl ) do |c|
	date_html << "<tr id='day#{c}'>"
	style = ''
	style = 'color:red;' if week_count == 0
	onclick = "onclick=\"editKoyomi2( 'init', '#{c}' )\""
	date_html << "<td style='#{style}' #{onclick}>#{c} (#{weeks[week_count]})</td>"

	r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{c}' AND freeze='1';", false, @debug )
	unless r.first
		0.upto( 3 ) do |cc|
			koyomi_c = '-'
			rr = mdb( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{c}' AND tdiv='#{cc}';", false, @debug )
			onclick = "onclick=\"cmmSaveKoyomi_direct( '#{cm_mode}', '#{yyyy}', '#{mm}', '#{c}', '#{cc}', '#{origin}' )\""
			if rr.first
				if rr.first['koyomi'] == ''
					date_html << "<td class='table-light' align='center' #{onclick}>#{koyomi_c}</td>"
				else
					koyomi_c = rr.first['koyomi'].split( "\t" ).size
					if dd == c and tdiv == cc
						date_html << "<td class='table-warning' align='center' #{onclick}>#{koyomi_c}</td>"
					else
						date_html << "<td class='table-info' align='center' #{onclick}>#{koyomi_c}</td>"
					end
				end
			else
				date_html << "<td class='table-light' align='center' #{onclick}>#{koyomi_c}</td>"
			end
		end
	else
		4.times do date_html << "<td class='table-secondary'></td>" end
	end

	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


puts 'tdiv HTML<br>' if @debug
tdiv_html = ''
tdiv_set = [ l['breakfast'], l['lunch'], l['dinner'], l['supply'] ]
tdiv_html << "<select id='tdiv_cmm' class='form-select form-select-sm'>"
0.upto( 3 ) do |c| tdiv_html << "<option value='#{c}' #{$SELECT[tdiv == c]}>#{tdiv_set[c]}</option>" end
tdiv_html << "</select>"


puts 'SELECT HH block<br>' if @debug
meal_time_set = [5, 10, 15, 20, 30, 45, 60, 90, 120 ]
eat_time_html = "<div class='input-group input-group-sm'>"
eat_time_html << "<label class='input-group-text btn-info' onclick=\"nowKoyomi( 'hh_mm_cmm' )\">#{l['clock']}</label>"
eat_time_html << "<input type='time' step='60' id='hh_mm_cmm' value='#{hh_mm}' class='form-control' style='min-width:100px;'>"
eat_time_html << "<select id='meal_time_cmm' class='form-select form-select-sm'>"
meal_time_set.each do |e| eat_time_html << "<option value='#{e}' #{$SELECT[meal_time == e]}>#{e}</option>" end
eat_time_html << "</select>"
eat_time_html << "<label class='input-group-text'>#{l['time']}</label>"
eat_time_html << "</div>"


#### carry_on_check
carry_on_html = "<input class='form-check-input' type='checkbox' id='carry_on' #{checked( carry_on )} DISABLED>"
carry_on_html << '<label class="form-check-label">時間継承</label>'


return_button = ''
if yyyy_ == nil
	return_button << "<div align='center' class='col-4 joystic_koyomi' onclick=\"koyomiReturn2KE( '#{yyyy}', '#{mm}', '#{dd}' )\">#{l['return']}</div>"
else
	return_button << "<div align='center' class='col-2 joystic_koyomi' onclick=\"koyomiReturn2KE( '#{yyyy_}', '#{mm_}', '#{dd_}' )\">#{l['return']}</div>"
	return_button << "<div align='center' class='col-2 joystic_koyomi' onclick=\"koyomiReturn2KE( '#{yyyy}', '#{mm}', '#{dd}' )\">#{l['return2']}</div>"
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{yyyy} / #{mm} / #{dd} (#{tdiv_set[tdiv]})</h5></div>
		<div align='center' class='col-2 joystic_koyomi' onclick="window.location.href='#day#{calendar.dd}';">#{l['joystick']}</div>
		<div align='center' class='col-3 joystic_koyomi' onclick="initKoyomi();">#{l['calendar']}</div>
		#{return_button}
	</div>
	<br>
	<div class='row'>
		<div class='col-3 form-inline'>
			<input type='date' class='form-control form-control-sm' id='yyyy_mm_dd' min='#{calendar.yyyyf}-01-01' max='#{calendar.yyyy + 2}-12-31' value='#{calendar.yyyy}-#{calendar.mms}-#{calendar.dds}' onChange="cmmChangeKoyomi( '#{cm_mode}', '#{origin}' )">
		</div>
		<div class='col-3 form-inline'>
			#{tdiv_html}
		</div>
		<div class='col-4 form-inline'>
			#{eat_time_html}
		</div>
		<div class='col-2 form-inline'>
			#{carry_on_html}
		</div>
	</div>
	<br>
	<div class='row'>
		#{save_button}
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'></th>
     		<th align='center'>#{l['breakfast']}</th>
     		<th align='center'>#{l['lunch']}</th>
     		<th align='center'>#{l['dinner']}</th>
     		<th align='center'>#{l['supply']}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>
HTML
puts html
