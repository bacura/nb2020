#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi 0.05b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomi'
@debug = false
@tdiv_set = [ 'breakfast', 'lunch', 'dinner', 'supple', 'memo' ]


#==============================================================================
#DEFINITION
#==============================================================================

####
def sub_menu( lp )
	html = <<-"MENU"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><span class='btn badge rounded-pill bg-info text-dark' onclick="initKoyomi()">#{lp[23]}</span></div>
		<div class='col-2'><span class='btn badge rounded-pill bg-info text-dark' onclick="initKoyomiex()">#{lp[24]}</span></div>
		<div class='col-2'><span class='btn badge rounded-pill bg-secondry' onclick="">#{lp[25]}</span></div>
		<div class='col-2'><span class='btn badge rounded-pill bg-secondry' onclick="">#{lp[26]}</span></div>
		<div class='col-2'></div>
	</div>
</div>

MENU
	puts html
	exit()
end


####
def meals( meal, uname )
	mb_html = '<ul>'
	a = meal.split( "\t" )
	a.each do |e|
		aa = e.split( ':' )
		if /^\?/ =~ aa[0]
			mb_html << "<li style='list-style-type: circle'>#{@something[aa[0]]}</li>"
		elsif /\-m\-/ =~ aa[0]
			puts 'menu' if @debug
			r = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false, @debug )
			if r.first
				mb_html << "<li>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		elsif /\-f\-/ =~ aa[0]
			puts 'fix' if @debug
			r = mdb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false, @debug )
			if r.first
				mb_html << "<li style='list-style-type: circle'>#{r.first['name']}</li>"
			else
				mb_html << "<li class='error'>Error: #{aa[0]}</li>"
			end
		elsif /\-/ =~ aa[0]
			puts 'recipe' if @debug
			r = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false, @debug )
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


####
class Nutrition_calc
	attr_reader :results, :fn_set, :weight_set, :unit_set

	def initialize( uname, fn_set, weight_set, unit_set, fct_item, fct_name, fct_frct )
		@uname = uname
		@fn_set = fn_set
		@weight_set = weight_set
		@unit_set = unit_set
		@results = Hash.new
		@results.default = BigDecimal( 0 )
		@fct_item = fct_item
		@fct_name = fct_name
		@fct_frct = fct_frct
	end

	def load_freeze( fzcode, fct_start, fct_end )
		r = mdb( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{@uname}' AND code='#{fzcode}';", false, false )
		if r.first
			fct_start.upto( fct_end ) do |c| @results[@fct_item[c]] = BigDecimal( r.first[@fct_item[c]] ) end
			return true
		end

		return false
	end

	def load_fix( code, fct_start, fct_end )
		r = mdb( "SELECT * FROM #{$MYSQL_TB_FCS} WHERE user='#{@uname}' AND code='#{code}';", false, false )
		if r.first
			fct_start.upto( fct_end ) do |c|
				@results[@fct_item[c]] += BigDecimal( num_opt( r.first[@fct_item[c]], 100, 1, @fct_frct[@fct_item[c]] + 3 )) unless r.first[@fct_item[c]] == '-'
			end
		end
	end

	def expand_menu( code )
		code_set = []
		r = mdb( "SELECT meal FROM #{$MYSQL_TB_MENU} WHERE user='#{@uname}' AND code='#{code}';", false, false )
		a = r.first['meal'].split( "\t" )
		a.each do |e| code_set << e end

		return code_set
	end

	def expand_recipe( code, rate, unit )
		weight_set_ = []
		recipe_total_weight = BigDecimal( 0 )

		r = mdb( "SELECT sum, dish FROM #{$MYSQL_TB_RECIPE} WHERE user='#{@uname}' AND code='#{code}';", false, false )
		if r.first
			a = r.first['sum'].split( "\t" )
			a.each do |e|
				( sum_no, sum_weight, z, z, z, z, z, sum_ew ) = e.split( ':' )

				if sum_no != '+' && sum_no != '-'
					@fn_set << sum_no
					@unit_set << unit
					sum_ew = sum_weight if sum_ew == nil
					weight_set_ << ( BigDecimal( sum_ew ) / r.first['dish'].to_i )
					recipe_total_weight += ( BigDecimal( sum_ew ) / r.first['dish'].to_i )
				end
			end
		end

		if unit == 99
			weight_set_.map! do |x| x * rate / 100 end
		else
			weight_set_.map! do |x| x * rate / recipe_total_weight end
		end
		@weight_set.concat( weight_set_ )
	end

	def calculate( fct_start, fct_end, fct_frct, fct_item )
		@fn_set.size.times do |c|
			query = ''
			if /^P/ =~ @fn_set[c]
				query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{@fn_set[c]}';"
			elsif /^U/ =~ fn_set[c]
				query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{@fn_set[c]}' AND user='#{@uname}';"
			else
				query = "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{@fn_set[c]}';"
			end

			r = mdb( query, false, false )
			if r.first
				@weight_set[c] = unit_weight( @weight_set[c], @unit_set[c], @fn_set[c] ) if @unit_set[c] != 0 && @unit_set[c] != 99
				fct_start.upto( fct_end ) do |cc|
					t = convert_zero( r.first[@fct_item[cc]] )
					@results[@fct_item[cc]] += BigDecimal( num_opt( t, @weight_set[c], 1, fct_frct[fct_item[cc]] + 3 ))
				end
			end
		end
	end

	def total_html( fc_items )
		html = ''
		fc_items.each do |e|
			if e == 'ENERC_KCAL'
				html << "#{@fct_name[e]}[#{@results[e].to_i}]&nbsp;&nbsp;&nbsp;&nbsp;"
			else
				html << "#{@fct_name[e]}[#{@results[e].to_f}]&nbsp;&nbsp;&nbsp;&nbsp;"
			end
		end

		return html
	end

	def pfc_html()
		html = ''
		pfc_p = ( @results['PROT'] * 4 / @results['ENERC_KCAL'] * 100 ).round( 1 )
		pfc_f = ( @results['FAT'] * 4 / @results['ENERC_KCAL'] * 100 ).round( 1 )
		pfc_c = 100 - pfc_p - pfc_f
		pfc_c = 0 if pfc_c == 100
		html << "<br><span style='color:crimson'>P</span>:<span style='color:green'>F</span>:<span style='color:blue'>C</span> (%) = <span style='color:crimson'>#{pfc_p.to_f}</span> : <span style='color:green'>#{pfc_f.to_f}</span> : <span style='color:blue'>#{pfc_c.to_f}</span>"

		return html
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
sub_menu ( lp ) if command == 'menu'


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
calc_html_set = ['']
fc_items = []
fc_names = []
r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}' AND name='???????????????';", false, @debug )
if r.first
	palette = r.first['palette']
	palette.size.times do |c|
		fc_items << @fct_item[c] if palette[c] == '1'
	end
else
 	fc_items = ['ENERC_KCAL', 'PROT', 'FAT', 'CHO', 'NACL_EQ']
end
fc_items.each do |e| fc_names << @fct_name[e] end

puts "Multi calc process<br>" if @debug
1.upto( calendar.ddl ) do |c|
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
	if r.first && r.first['koyomi'] != nil
		calc = Nutrition_calc.new( user.name, [], [], [], @fct_item, @fct_name, @fct_frct )
		some_set = ''
		fzcode = r.first['fzcode']

		freeze_flag = false
		r.each do |e|
			break if freeze_flag

			if e['tdiv'] != 4
				code_set = []
				rate_set = []
				unit_set = []
				if e['freeze'] == 1
					puts 'Freeze<br>' if @debug
					freeze_flag = calc.load_freeze( fzcode, @fct_start, @fct_end )
				else
					puts 'Row<br>' if @debug
					a = []
					a = e['koyomi'].split( "\t" ) if e['koyomi']
					a.each do |ee|
						( koyomi_code, koyomi_rate, koyomi_unit, z ) = ee.split( ':' )
						code_set << koyomi_code
						rate_set << koyomi_rate
						unit_set << koyomi_unit
					end

					puts 'Recipe<br>' if @debug
					code_set.size.times do |cc|
						code = code_set[cc]
						food_weight, rate = food_weight_check( rate_set[cc] )
						unit = unit_set[cc].to_i

						if /\?/ =~ code
						elsif /\-f\-/ =~ code
							puts 'FIX<br>' if @debug
							rr = mdb( "SELECT * FROM #{$MYSQL_TB_FCS} WHERE user='#{user.name}' AND code='#{code}';", false, @debug )
							calc.load_fix( code, @fct_start, @fct_end ) if rr.first
						else
							recipe_set = []
							recipe_set = calc.expand_menu( code ) if /\-m\-/ =~ code

							recipe_set << code if recipe_set.size == 0
							recipe_set.size.times do |ccc|
								if /\-r\-/ =~ recipe_set[ccc] || /\w+\-\h{4}\-\h{4}/ =~ recipe_set[ccc]
									calc.expand_recipe( recipe_set[ccc], rate, unit )
								end
							end

							# food
							if /\-/ !~ code
								puts 'Food<br>' if @debug
								calc.fn_set << code
								calc.weight_set << rate
								calc.unit_set << unit
							end
						end
					end
				end

			end
		end
		puts 'Start calculation<br>' if @debug
		calc.calculate( @fct_start, @fct_end, @fct_frct, @fct_item )

		puts "freeze process:#{freeze_flag}<br>" if @debug
		unless freeze_flag
			sub_query = ''
			calc.results.each do |k, v|
				t = v.round( @fct_frct[k] )
				calc.results[k] = t
				sub_query << " #{k}='#{t}',"
			end
			sub_query.chop!

			rr = mdb( "SELECT code FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND code='#{fzcode}';", false, @debug )
			if sub_query == ''
			elsif rr.first && fzcode != ''
				puts "UPDATE(#{fzcode})<br>" if @debug
				mdb( "UPDATE #{$MYSQL_TB_FCZ} SET #{sub_query} WHERE user='#{user.name}' AND code='#{fzcode}';", false, @debug )
				mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{fzcode}' WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
			else
				new_fzcode = generate_code( user.name, 'z' )
				puts "INSERT(#{new_fzcode})<br>" if @debug
				mdb( "INSERT INTO #{$MYSQL_TB_FCZ} SET user='#{user.name}', code='#{new_fzcode}', #{sub_query};", false, @debug )
				mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{new_fzcode}' WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
			end
		end
		calc_html = ''
		calc_html << calc.total_html( fc_items )
		calc_html << calc.pfc_html()
		calc_html_set << calc_html
	else
		calc_html_set << ''
		mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}' AND koyomi='';", false, @debug ) if r.first
	end
end


puts "Day process<br>" if @debug
date_html = ''
week_count = calendar.wf
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( calendar.ddl ) do |c|
	freeze_flag = false
	koyomi_tmp = []
	freeze_checked = ''

	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}';", false, @debug )
	if r.first
		r.each do |e|
			koyomi_tmp[e['tdiv']] = e['koyomi'] if e['tdiv'] != nil
			freeze_flag = true if r.first['freeze'] == 1
		end
	else
		5.times do koyomi_tmp << nil end
	end

	freeze_checked = 'CHECKED' if freeze_flag
	onclick = "onclick=\"editKoyomi( 'init', '#{c}' )\""

	date_html << "<tr id='day#{c}'>"
	if week_count == 0
		date_html << "<td style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</td>"
	else
		date_html << "<td><span>#{c}</span> (#{weeks[week_count]})</td>"
	end
	4.times do |cc|
		if koyomi_tmp[cc] == nil
			date_html << "<td #{onclick}>-</td>"
		else
			meal_block = meals( koyomi_tmp[cc], user.name )

			date_html << "<td #{onclick}>#{meal_block}</td>"
		end
	end
	if koyomi_tmp[4] == nil
		date_html << "<td #{onclick}>-</td>"
	else
		date_html << "<td #{onclick}>#{koyomi_tmp[4]}</td>"
	end

	date_html << "<td><input type='checkbox' id='freeze_check#{c}' onChange=\"freezeKoyomi( '#{c}' )\" #{freeze_checked}></td>"
	date_html << "</tr>"

	if calc_html_set[c] == '' || calc_html_set[c] == nil
		date_html << "<tr id='nutrition#{c}' class='table-borderless' style='display:none'>"
	else
		date_html << "<tr id='nutrition#{c}' class='table-borderless'>"
	end
	date_html << "<td></td>"
	date_html << "<td colspan='6'>#{calc_html_set[c]}</td>"
	date_html << "<td></td>"
	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end

puts "HTML process<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[8]}</h5></div>
		<div class='col-2 form-inline'>
			<input type='month' class='form-control form-control-sm' id='yyyy_mm' min='#{calendar.yyyyf}-01' max='#{calendar.yyyy + 2}-01' value='#{calendar.yyyy}-#{calendar.mms}' onChange="changeKoyomi()">
		</div>
		<div align='center' class='col-8 joystic_koyomi' onclick="window.location.href='#day#{calendar_td.dd}';">#{lp[18]}</div>
	</div>
	<div class='row'>
		<div class='col'></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'></th>
     		<th align='center' width='15%'>#{lp[12]}</th>
     		<th align='center' width='15%'>#{lp[13]}</th>
     		<th align='center' width='15%'>#{lp[14]}</th>
     		<th align='center' width='15%'>#{lp[15]}</th>
     		<th align='center'>#{lp[16]}</th>
     		<th align='center'><input type='checkbox' id='freeze_check_all' onChange="freezeKoyomiAll()" #{freeze_all_checked}>&nbsp;#{lp[17]}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>
HTML

puts html


#### Deleting Empty koyomi
mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE koyomi IS NULL;", false, @debug )
