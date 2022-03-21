#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi extra 0.12b


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomiex'
@debug = false
item_max = 9	#start from 0


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

#### Guild member check
if user.status < 3
	puts "Guild member error."
	exit
end


#### Getting POST data
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
item_no = @cgi['item_no'].to_i
cell = @cgi['cell']
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "item_no:#{item_no}<br>\n"
	puts "cell:#{cell}<br>\n"
	puts "<hr>\n"
end


#### Getting date
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


puts "Date & calendar config<br>" if @debug
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar_td = Calendar.new( user.name, 0, 0, 0 )
calendar.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"


puts "Loading config<br>" if @debug
kex_select = Hash.new
kex_item = Hash.new
kex_unit = Hash.new
r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	if r.first['koyomi'] != nil && r.first['koyomi'] != ''
		koyomi = JSON.parse( r.first['koyomi'] )
		start = koyomi['start'].to_i
		kex_select = koyomi['kex_select']
		kex_oname = koyomi['kex_oname']
		kex_ounit = koyomi['kex_ounit']
		p koyomi if @debug
	end
end


puts "Updating cell<br>" if @debug
if command == 'update'
	r = mdb( "SELECT user FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET item#{item_no}='#{cell}' WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMIEX} SET item#{item_no}='#{cell}', user='#{user.name}', date='#{sql_ymd}';", false, @debug )
	end
end


puts "Header html<br>" if @debug
th_html = '<thead><tr>'
th_html << "<th align='center'></th>"
0.upto( item_max ) do |c|
	unit= ''
	unit = "(#{kex_ounit[c.to_s]})" if kex_ounit[c.to_s] != ''
	th_html << "<th align='center'>#{kex_oname[c.to_s]} #{unit}</th>" if kex_select[c.to_s] != 'ND'
end
th_html << '</tr></thead>'


puts "Week html<br>" if @debug
date_html = ''
week_count = calendar.wf
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND ( date BETWEEN '#{sql_ym}-1' AND '#{sql_ym}-#{calendar.ddl}' );", false, @debug )
koyomir = []
r.each do |e| koyomir[e['date'].day] = e end


puts "Cell data html<br>" if @debug
1.upto( calendar.ddl ) do |c|
	date_html << "<tr id='day#{c}'>"
	if week_count == 0
		date_html << "<td style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</td>"
	else
		date_html << "<td><span>#{c}</span> (#{weeks[week_count]})</td>"
	end

	if koyomir[c] == nil
		0.upto( item_max ) do |cc|
			date_html << "<td><input type='text' id='id#{c}_#{kex_select[cc.to_s]}' value='' onChange=\"updateKoyomiex( '#{c}', '#{cc}', 'id#{c}_#{kex_select[cc.to_s]}' )\"></td>" if kex_select[cc.to_s] != 'ND'
		end
	else
		0.upto( item_max ) do |cc|
			t = koyomir[c]["item#{cc}"]
			date_html << "<td><input type='text' id='id#{c}_#{kex_select[cc.to_s]}' value='#{t}' onChange=\"updateKoyomiex( '#{c}', '#{cc}', 'id#{c}_#{kex_select[cc.to_s]}' )\"></td>" if kex_select[cc.to_s] != 'ND'
		end
	end

	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


puts "HTML<br>" if @debug
html = <<-"HTML"
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

HTML

puts html
