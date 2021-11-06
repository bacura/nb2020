#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser cooking school 0.03b


#==============================================================================
#MEMO
#==============================================================================
#ampm:0->am, 1->pm
#status:0->close, 1->Reserved, 7->No show, 8->Done, 9->Open


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
script = 'school'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

####
def sub_menu( lp )
	html = <<-"MENU"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><span class='badge rounded-pill bg-info text-dark' onclick="initSchool()">#{lp[23]}</span></div>
		<div class='col-2'><span class='badge rounded-pill bg-success' onclick="window.open( 'yoyaku-pc.cgi', 'calendar' )">#{lp[20]}</span></div>
		<div class='col-2'><span class='badge rounded-pill bg-success' onclick="window.open( 'yoyaku-mobi.cgi', 'calendar' );">#{lp[21]}</span></div>
		<div class='col-2'><span class='badge rounded-pill bg-info text-dark' onclick="initSchoolMenu()">#{lp[24]}</span></div>
		<div class='col-2'><span class='badge rounded-pill bg-light text-light' onclick="">#{lp[25]}</span></div>
		<div class='col-2'><span class='badge rounded-pill bg-info text-dark' onclick="initSchoolCustom()">#{lp[32]}</span></div>
		<div class='col-2'></div>
	</div>
</div>

MENU
	puts html
	exit()
end


class Schoolk
	attr_accessor :user, :student, :num, :pass, :menu, :ampm, :date, :status

	def initialize( re )
		@user = re['user']
		@student = re['student']
		@num = re['num'].to_i
		@pass = re['pass']
		@menu = re['menu']
		@ampm = re['ampm'].to_i
		@date = re['date'].to_s
		@status = re['status'].to_i
	end

	def update_status()
		r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLK} WHERE date='#{@date}' AND ampm=#{@ampm};", false, @debug )
		mdb( "UPDATE #{$MYSQL_TB_SCHOOLK} SET status=#{@status} WHERE date='#{@date}' AND ampm=#{@ampm};", false, @debug ) if r.first
	end

	def open()
		r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLK} WHERE date='#{@date}' AND ampm=#{@ampm};", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_SCHOOLK} SET status=9, user=NULL, student=NULL, num=MULL, pass=NULL, menu=NULL WHERE date='#{@date}' AND ampm=#{@ampm};", false, @debug )
		else
			mdb( "INSERT #{$MYSQL_TB_SCHOOLK} SET status=9, date='#{@date}', ampm=#{@ampm};", false, @debug )
		end
	end

	def checked()
		checked = ['checked', '', '', '', '']
		checked = ['', 'checked', '', '', ''] if @status == 9
		checked = ['', '', 'checked', '', ''] if @status == 1
		checked = ['', '', '', 'checked', ''] if @status == 8
		checked = ['', '', '', '', 'checked'] if @status == 7

		return checked
	end

	def checked_bg()
		checked_bg = 'bg-light'
		checked_bg = 'bg-info' if @status == 9
		checked_bg = 'bg-warning' if @status == 1
		checked_bg = 'bg-success' if @status == 8
		checked_bg = 'bg-danger' if @status == 7

		return checked_bg
	end
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )

#### Guild member check
if user.status < 5 && !@debug
	puts "Guild member shun error."
	exit
end


#### Getting POST
command = @cgi['command']
yyyy = @cgi['yyyy'].to_i
mm = @cgi['mm'].to_i
dd = @cgi['dd'].to_i
yyyy_mm = @cgi['yyyy_mm']
ampm = @cgi['ampm']
status = @cgi['status']
unless yyyy_mm == ''
	a = yyyy_mm.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
end
dd = 1 if dd == 0
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy_mm:#{yyyy_mm}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "ampm:#{ampm}<br>\n"
	puts "<hr>\n"
end


####
school_mode = 3
r = mdb( "SELECT school FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
school_mode = r.first['school'] if r.first


#### Sub menu
sub_menu ( lp ) if command == 'menu'


#### Changing schoolk status
if command == 'changest'
	reservation = Schoolk.new( @cgi )
	reservation.date = "#{yyyy_mm}-#{dd}"
	reservation.update_status
end


#### Open schoolk
if command == 'open'
	reservation = Schoolk.new( @cgi )
	reservation.date = "#{yyyy_mm}-#{dd}"
	reservation.open
end


#### Date & calendar config
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar_td = Calendar.new( user.name, 0, 0, 0 )

calendar.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"


####
date_html = ''
week_count = calendar.wf
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
menu_flag = true;
1.upto( calendar.ddl ) do |c|
	date_html << "<tr id='day#{c}'>"
	if week_count == 0
		date_html << "<td style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</td>"
	elsif week_count == 6
		date_html << "<td style='color:blue;'><span>#{c}</span> (#{weeks[week_count]})</td>"
	else
		date_html << "<td><span>#{c}</span> (#{weeks[week_count]})</td>"
	end




	if school_mode == 3
		if menu_flag
			date_html << "<td><span onclick=\"\">#{lp[29]}</span></td>"
			menu_flag = false
		else
			date_html << "<td>#{lp[30]}</td>"
		end
	elsif school_mode == 2
		if week_count == 1 || menu_flag
			date_html << "<td><span onclick=\"\">#{lp[29]}</span></td>"
			menu_flag = false
		else
			date_html << "<td>#{lp[30]}</td>"
		end
	else
		date_html << "<td><span onclick=\"\">#{lp[29]}</span></td>"
	end






	reservation_am = nil
	reservation_pm = nil
	r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLK} WHERE date='#{sql_ym}-#{c}';", false, @debug )
	if r.first
		r.each do |e|
			if e['ampm'] == 0
				reservation_am = Schoolk.new( e )
			elsif e['ampm'] == 1
				reservation_pm = Schoolk.new( e )
			end
		end

		date_html << "<td>"
		if reservation_am
			rr = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{reservation_am.menu}' AND protect=1;", false, @debug )
			menu_name = lp[14]
			menu_name = rr.first['name'] if rr.first
			menu_name = lp[15] if /sf/ =~ reservation_am.menu

			checked = reservation_am.checked
			checked_bg = reservation_am.checked_bg

			if reservation_am.status != 9 && reservation_am.status != 0
				date_html << "#{reservation_am.student}&nbsp;(#{reservation_am.num})<br>"
				date_html << "#{menu_name} (#{reservation_am.menu})<br>"
				date_html << "#{reservation_am.pass}&nbsp;(#{reservation_am.user})<br><br>"
			end

			date_html << "<div class='#{checked_bg}' align='center'>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='am#{c}' id='status#{c}am0' #{checked[0]} onChange=\"changeSchoolkSt( '#{c}', '0', '0' )\">"
			date_html << "<label class='form-check-label'>#{lp[26]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='am#{c}' id='status#{c}am1' #{checked[1]} onChange=\"changeSchoolkSt( '#{c}', '0', '9' )\">"
			date_html << "<label class='form-check-label'>#{lp[27]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='am#{c}' id='status#{c}am2' #{checked[2]} onChange=\"changeSchoolkSt( '#{c}', '0', '1' )\">"
			date_html << "<label class='form-check-label'>#{lp[16]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='am#{c}' id='status#{c}am3' #{checked[3]} onChange=\"changeSchoolkSt( '#{c}', '0', '8' )\">"
			date_html << "<label class='form-check-label'>#{lp[17]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='am#{c}' id='status#{c}am4' #{checked[4]} onChange=\"changeSchoolkSt( '#{c}', '0', '7' )\">"
			date_html << "<label class='form-check-label'>#{lp[19]}</label>"
			date_html << "</div>"
			date_html << "</div>"
		else
			date_html << "<div onclick=\"openSchoolk( '#{c}', '0' )\">+</div>"
		end
		date_html << "</td>"

		date_html << "<td>"
		if reservation_pm

			rr = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{reservation_pm.menu}' AND protect=1;", false, @debug )
			menu_name = lp[14]
			menu_name = rr.first['name'] if rr.first
			menu_name = lp[15] if /sf/ =~ reservation_pm.menu

			checked = reservation_pm.checked
			checked_bg = reservation_pm.checked_bg

			if reservation_pm.status != 9 && reservation_pm.status != 0
				date_html << "#{reservation_pm.student}&nbsp;(#{reservation_pm.num})<br>"
				date_html << "#{menu_name} (#{reservation_pm.menu})<br>"
				date_html << "#{reservation_pm.pass}&nbsp;(#{reservation_pm.user})<br><br>"
			end

			date_html << "<div class='#{checked_bg}' align='center'>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='pm#{c}' id='status#{c}pm0' #{checked[0]} onChange=\"changeSchoolkSt( '#{c}', '1', '0' )\">"
			date_html << "<label class='form-check-label'>#{lp[26]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='pm#{c}' id='status#{c}pm1' #{checked[1]} onChange=\"changeSchoolkSt( '#{c}', '1', '9' )\">"
			date_html << "<label class='form-check-label'>#{lp[27]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='pm#{c}' id='status#{c}pm2' #{checked[2]} onChange=\"changeSchoolkSt( '#{c}', '1', '1' )\">"
			date_html << "<label class='form-check-label'>#{lp[16]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='pm#{c}' id='status#{c}pm3' #{checked[3]} onChange=\"changeSchoolkSt( '#{c}', '1', '8' )\">"
			date_html << "<label class='form-check-label'>#{lp[17]}</label>"
			date_html << "</div>"
			date_html << "<div class='form-check form-check-inline'>"
			date_html << "<input class='form-check-input' type='radio' name='pm#{c}' id='status#{c}pm4' #{checked[4]} onChange=\"changeSchoolkSt( '#{c}', '1', '7' )\">"
			date_html << "<label class='form-check-label'>#{lp[19]}</label>"
			date_html << "</div>"
			date_html << "</div>"
		else
			date_html << "<div onclick=\"openSchoolk( '#{c}', '1' )\">+</div>"
		end
			date_html << "</td>"
	else
		date_html << "<td><div onclick=\"openSchoolk( '#{c}', '0' )\">+</div></td><td><div onclick=\"openSchoolk( '#{c}', '1' )\">+</div></td>"
	end

	week_count += 1
	week_count = 0 if week_count > 6
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{lp[8]}</h5></div>
		<div class='col-2 form-inline'>
			<input type='month' id='yyyy_mm' min='#{calendar.yyyyf}-01' max='#{calendar.yyyy + 2}-01' value='#{calendar.yyyy}-#{calendar.mms}' onChange="changeSchoolk()">
		</div>
		<div align='center' class='col-7 joystic_koyomi' onclick="window.location.href='#day#{calendar_td.dd}';">#{lp[18]}</div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'></th>
     		<th align='center'>#{lp[28]}</th>
     		<th align='center'>#{lp[12]}</th>
     		<th align='center'>#{lp[13]}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>

HTML

puts html
