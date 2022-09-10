#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi extra 0.20b (2022/09/10)


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomiex'
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


puts 'GET POST<br>' if @debug
command = @cgi['command']
yyyy = @cgi['yyyy'].to_i
mm = @cgi['mm'].to_i
yyyy_mm = @cgi['yyyy_mm']
dd = @cgi['dd'].to_i
unless yyyy_mm == ''
	a = yyyy_mm.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
end
dd = 1 if dd == 0
kex_key = @cgi['kex_key']
cell = @cgi['cell']
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "kex_key:#{kex_key}<br>\n"
	puts "cell:#{cell}<br>\n"
	puts "<hr>\n"
end


puts "INITIALIZE Date<br>" if @debug
date = Date.today
date = Date.new( yyyy, mm, dd ) unless yyyy == 0
if yyyy == 0
 	yyyy = date.year
	mm = date.month
	dd = date.day
end
if @debug
	puts "date:#{date.to_time}<br>\n"
end

puts "INITIALIZE calendar<br>" if @debug
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar_td = Calendar.new( user.name, 0, 0, 0 )
calendar.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"


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


puts "HTML Header<br>" if @debug
th_html = '<thead><tr>'
th_html << "<th align='center'></th>"
kexu.each do |k, v|
	th_html << "<th align='center'>#{k} (#{v})</th>" if kexa[k] == '1'
end
th_html << '</tr></thead>'


puts "LOAD date cell<br>" if @debug
cells_day = []
r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND ( date BETWEEN '#{sql_ym}-1' AND '#{sql_ym}-#{calendar.ddl}' );", false, @debug )
r.each do |e|
	if e['cell'] != nil && e['cell'] != ''
		cells_day[e['date'].day] = JSON.parse( e['cell'] )
	end
end


if command == 'update'
	puts "UPDATE cell<br>" if @debug
	if cells_day[dd] == nil || cells_day[dd] == ''
		kexc = Hash.new
		kexu.each do |k, |
			if k == kex_key
				kexc[k] = cell
			else
				kexc[k] = ''
			end
			cells_day[dd] = kexc
		end
	else
		cells_day[dd][kex_key] = cell
	end
end


puts "HTML Cell<br>" if @debug
week_count = calendar.wf
date_html = ''
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( calendar.ddl ) do |c|
	style = ''
	style = "style='color:red;'" if week_count == 0
	date_html << "<tr id='day#{c}'>"
	date_html << "<td #{style}><span>#{c}</span> (#{weeks[week_count]})</td>"
	kexa.each do |k, v|
		if cells_day[c] == nil
			date_html << "<td><input type='text' id='#{k}#{c}' value='' onChange=\"updateKoyomiex( '#{k}', '#{c}' )\"></td>" if v == '1'
		else
			date_html << "<td><input type='text' id='#{k}#{c}' value='#{cells_day[c][k]}' onChange=\"updateKoyomiex( '#{k}', '#{c}' )\"></td>" if v == '1'
		end
	end
	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


####
####
puts "HTML10<br>" if @debug
html[10] = <<-"HTML10"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[8]}</h5></div>
		<div class='col-2 form-inline'>
			<input type='month' class='form-control form-control-sm' id='yyyy_mm' min='#{calendar.yyyyf}-01' max='#{calendar.yyyy + 2}-01' value='#{calendar.yyyy}-#{calendar.mms}' onChange="changeKoyomiex()">
		</div>
		<div class='col-4'>
			<form method='post' enctype='multipart/form-data' id='table_form'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{lp[14]}</label>
				<input type='file' class='form-control' name='extable' onchange="importkoyomiex()">
			</div>
			</form>
		</div>
		<div align='center' class='col-4 joystic_koyomi' onclick="window.location.href='#day#{date.day}';">#{lp[13]}</div>
	</div>
	<div class='row'>
		<div class='col'></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	#{th_html}
	#{date_html}
	</table>

HTML10
####
####

puts html.join


if command == 'update'
	puts "UPDATE cell<br>" if @debug
	cell_ = JSON.generate( cells_day[dd] )
	r = mdb( "SELECT user FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET cell='#{cell_}' WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMIEX} SET cell='#{cell_}', user='#{user.name}', date='#{sql_ymd}';", false, @debug )
	end
end


if command == 'init'
	puts "CLEAN empty cell<br>" if @debug
#	mdb( "DELETE FROM #{$MYSQL_TB_KOYOMIEX} WHERE cell='' OR cell IS NULL;", false, @debug )
end