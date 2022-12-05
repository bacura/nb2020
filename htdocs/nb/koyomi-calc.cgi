#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 koyomi calc 0.00b (2022/11/27)


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomi-calc'
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
palette_ = @cgi['palette']
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
r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date BETWEEN '#{yyyymmdds}' AND '#{yyyymmdde}';", false, @debug )
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
palette_ = @palette_default_name[1] if palette_ == nil || palette_ == '' || palette_ == '0'
palette.set_bit( palette_ )

puts 'HTMLパレットの生成 <br>' if @debug
palette_html = ''
palette.sets.each_key do |k|
	s = ''
	s = 'SELECTED' if palette_ == k
	palette_html << "<option value='#{k}' #{s}>#{k}</option>"
end


fct_total = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct_total.load_palette( palette.bit )

fct_tdiv = []
4.times do |c|
	fct_tdiv[c] = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
	fct_tdiv[c].load_palette( palette.bit )

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
				fct_tdiv[c].into_zero
			elsif /\-z\-/ =~ code
				puts 'FIX<br>' if @debug
				fct_tdiv[c].load_fcz( user.name, code, 'fix' )
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
				fct_tdiv[c].set_food( user.name, food_nos, food_weights, false )
			end
		end
	end

	puts 'Start calculation<br>' if @debug
	fct_tdiv[c].calc
	fct_tdiv[c].digit
	fct_total.into_solid( fct_tdiv[c].total )
end


puts "Summary html<br>" if @debug
fct_total.calc
fct_total.digit


fct_table = ''
if day_count >= 1
	fct_table << '<table class="table table-sm table-striped">'
	fct_table << "<tr><td><h5>#{l['period']}#{day_count}#{l['days']}</h5></td></tr>"
	fct_table << '<tr>'
	fct_table << "<th class='fct_item'>#{l['name']}</th>"
	fct_table << "<th class='fct_item'>#{l['unit']}</th>"
	fct_table << "<th class='fct_item'>#{l['volume']}</th>"
	fct_table << "<th class='fct_item'>#{l['breakfast']}</th>"
	fct_table << "<th class='fct_item'>#{l['lunch']}</th>"
	fct_table << "<th class='fct_item'>#{l['dinner']}</th>"
	fct_table << "<th class='fct_item'>#{l['supply']}</th>"
	fct_table << '<tr>'

	fct_total.names.size.times do |i|
		fct_table << '<tr>'
		fct_table << "<td>#{fct_total.names[i]}</td>"
		fct_table << "<td>#{fct_total.units[i]}</td>"
		fct_table << "<td>#{fct_total.total[i]}</td>"
		fct_table << "<td>#{fct_tdiv[0].total[i]}</td>"
		fct_table << "<td>#{fct_tdiv[1].total[i]}</td>"
		fct_table << "<td>#{fct_tdiv[2].total[i]}</td>"
		fct_table << "<td>#{fct_tdiv[3].total[i]}</td>"
		fct_table << '</tr>'
	end

	fct_table << "<tr><td><h5>#{l['average']}</h5></td></tr>"
	fct_table << '<tr>'
	fct_table << "<th class='fct_item'>#{l['name']}</th>"
	fct_table << "<th class='fct_item'>#{l['unit']}</th>"
	fct_table << "<th class='fct_item'>#{l['volume']}</th>"
	fct_table << "<th class='fct_item'>#{l['breakfast']}</th>"
	fct_table << "<th class='fct_item'>#{l['lunch']}</th>"
	fct_table << "<th class='fct_item'>#{l['dinner']}</th>"
	fct_table << "<th class='fct_item'>#{l['supply']}</th>"
	fct_table << '<tr>'

	fct_total.names.size.times do |i|
		fct_table << '<tr>'
		fct_table << "<td>#{fct_total.names[i]}</td>"
		fct_table << "<td>#{fct_total.units[i]}</td>"
		fct_table << "<td>#{( fct_total.total[i] / day_count ).round( fct_total.frcts[i] )}</td>"
		fct_table << "<td>#{( fct_tdiv[0].total[i] / day_count ).round( fct_tdiv[0].frcts[i] )}</td>"
		fct_table << "<td>#{( fct_tdiv[1].total[i] / day_count ).round( fct_tdiv[1].frcts[i] )}</td>"
		fct_table << "<td>#{( fct_tdiv[2].total[i] / day_count ).round( fct_tdiv[2].frcts[i] )}</td>"
		fct_table << "<td>#{( fct_tdiv[3].total[i] / day_count ).round( fct_tdiv[3].frcts[i] )}</td>"
		fct_table << '<tr>'
	end
	fct_table << '</table>'
else
	fct_table << "<h5>#{l['no_day']}</h5>"
end

puts "HTML process<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{l['koyomi']}</h5></div>
	</div>
	<div class='row'>
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{l['palette']}</label>
				<select class="form-select form-select-sm" id="palette">
					#{palette_html}
				</select>
			</div>

		</div>
		<div class='col-2 form-inline'>
			<input type='date' class='form-control form-control-sm' id='yyyymmdds' value='#{yyyymmdds}'>
		</div>
		<div align='center' class='col-1'>
			#{l['fromto']}
		</div>
		<div class='col-2 form-inline'>
			<input type='date' class='form-control form-control-sm' id='yyyymmdde' value='#{yyyymmdde}'>
		</div>
	</div>
	<br>
	<div class='row'>
		<button class='btn btn-sm btn-info' onclick='calcKoyomiCalc()'>#{l['calc']}</buttnon>
	</div>
	<br>
	#{fct_table}
HTML

puts html
