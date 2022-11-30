#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi calc 0.00b (2022/11/27)


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomi-calc'
@debug = true

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'
require "./language_/#{script}.lp"

#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )

#### Guild member check
if user.status < 3
	puts "Guild member error."
	exit
end


#### Getting POST
command = @cgi['command']
yyyymmdds = @cgi['yyyymmdds']
yyyymmdde = @cgi['yyyymmdde']
yyyymmdds = @time_now.strftime( "%Y-%m-%d" ) if yyyymmdds == ''
yyyymmdde = @time_now.strftime( "%Y-%m-%d" ) if yyyymmdde == ''
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyymmdds:#{yyyymmdds}<br>\n"
	puts "yyyymmdde:#{yyyymmdde}<br>\n"
	puts "<hr>\n"
end


puts "Multi calc process<br>" if @debug
day_list = []
dtiv0 = Hash.new
dtiv1 = Hash.new
dtiv2 = Hash.new
dtiv3 = Hash.new
koyomi_box = [dtiv0, dtiv1, dtiv2, dtiv3 ]
#r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date BETWEEN '#{yyyymmdds}' AND '#{yyyymmdde}';", false, @debug )
r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}';", false, @debug )
r.each do |e|
	if e['freeze'] == 0
		koyomi_box[e['tdiv'].to_i][e['date'].to_s] = e['koyomi']
		day_list << e['date'].to_s
	end
end
day_list.uniq!
day_count = day_list.size


puts "Palette setting<br>" if @debug
palette = Palette.new( user.name )
palette.set_bit( nil )

fct_day = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct_day.load_palette( palette.bit )

4.times do |c|
	fct_tdiv = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
	fct_tdiv.load_palette( palette.bit )

	koyomi_box[c].each do |k, v|
		code_set = []
		rate_set = []
		unit_set = []

		puts 'Row<br>' if @debug
		a = []
		a = v.split( "\t" ) if v
		a.each do |e|
			( koyomi_code, koyomi_rate, koyomi_unit, z ) = e.split( '~' )
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
	end

	puts 'Start calculation<br>' if @debug
	fct_tdiv.calc
	fct_tdiv.digit
	fct_day.into_solid( fct_tdiv.total )
end


#puts "Summary#{c} html<br>" if @debug
#fct_day.calc
#fct_day.digit

#pfc = fct_day.calc_pfc

#if fct_day.foods.size == 0 && freeze_flag == false
#	fct_day_htmls << ''
#else
#	t = ''
#	fct_day.names.size.times do |i|
#		t << "#{fct_day.names[i]}[#{fct_day.total[i]}]&nbsp;&nbsp;&nbsp;&nbsp;"
#	end

#	if pfc.size == 3
#		t << "<br><span style='color:crimson'>P</span>:<span style='color:green'>F</span>:<span style='color:blue'>C</span> (%) = "
#		t << "<span style='color:crimson'>#{pfc[0]}</span> : <span style='color:green'>#{pfc[1]}</span> : <span style='color:blue'>#{pfc[2]}</span>"
#		t << "&nbsp;&nbsp;<span onclick=\"visionnerz( '#{sql_ym}-#{c}' )\">#{lp[28]}</span>" if user.status >= 5
#	end
#	fct_day_htmls << t
#end




puts "HTML process<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{l['koyomi']}</h5></div>
	</div>
	<div class='row'>
		<div class='col-2 form-inline'>
			<input type='date' class='form-control form-control-sm' id='yyyymmdds' value='#{yyyymmdds}'>
		</div>
		<div class='col-2 form-inline'>
			<input type='date' class='form-control form-control-sm' id='yyyymmdds' value='#{yyyymmdde}'>
		</div>
	</div>
	<div class='row'>
	</div>
HTML

puts html
