#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser magic calc 0.06b (2020/12/01)

#==============================================================================
#STATIC
#==============================================================================
fct_num = 14
@debug = false
script = 'calc'

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
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

r = mdb( "SELECT icalc FROM cfg WHERE user='#{user.name}';", false, @debug )
fct_num = r.first['icalc'].to_i unless r.first['icalc'].to_i == 0


#### Getting POST data
command = @cgi['command']
code = @cgi['code']
ew_mode = @cgi['ew_mode']
frct_mode = @cgi['frct_mode']
frct_accu = @cgi['frct_accu']
palette_ = @cgi['palette']

if ew_mode == nil || ew_mode == ''
	r = mdb( "SELECT calcc FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';",false, @debug )
	if r.first && r.first['calcc'] != nil
		a = r.first['calcc'].split( ':' )
		palette_ = a[0]
		ew_mode = a[1].to_i
		frct_mode = a[2].to_i
		frct_accu = a[3].to_i
	else
		palette_ = nil
		ew_mode = 0
		frct_mode = 1
		frct_accu = 1
	end
end


ew_mode = ew_mode.to_i
frct_mode = frct_mode.to_i
frct_accu = frct_accu.to_i
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "ew_mode: #{ew_mode}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "frct_accu: #{frct_accu}<br>"
	puts "palette_: #{palette_}<br>"
	puts "<hr>"
end


puts 'Extracting SUM data <br>' if @debug
r = mdb( "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
recipe_name = r.first['name']
code = r.first['code']
food_no, food_weight, total_weight = extract_sum( r.first['sum'], r.first['dish'].to_i, ew_mode )


puts 'Checking SELECT & CHECK <br>' if @debug
frct_select = selected( 1, 3, frct_mode )
accu_check = checked( frct_accu )
ew_check = checked( ew_mode )


puts 'Setting palette <br>' if @debug
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


puts 'FCT Calc<br>' if @debug
fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, frct_accu, frct_mode )
fct.load_palette( palette.bit )
fct.set_food( user.name, food_no, food_weight, false )
fct.calc
fct.digit


puts 'HTML食品成分表の生成 <br>' if @debug
fct_html = ''
table_num = fct.items.size / fct_num
table_num += 1 if ( fct.items.size % fct_num ) != 0
fct_width = ( 70 / fct_num ).to_f
table_num.times do |c|
	fct_html << '<table class="table table-striped table-sm">'

	# 項目名
	fct_html << '<tr>'
	fct_html << "	<th align='center' width='6%' class='fct_item'>#{l['food_no']}</th>"
	fct_html << "	<th align='center' width='20%' class='fct_item'>#{l['food_name']}</th>"
	fct_html << "	<th align='center' width='4%' class='fct_item'>#{l['weight']}</th>"
	fct_num.times do |cc|
		fct_no = ( c * fct_num ) + cc
		unless fct.names[fct_no] == nil
			fct_html << "	<th align='center' width='#{fct_width}%' class='fct_item'>#{fct.names[fct_no]}</th>"
		else
			fct_html << "	<th align='center' width='#{fct_width}%' class='fct_item'></th>"
		end
	end
	fct_html << '</tr>'

	# 単位
	fct_html << '<tr>'
	fct_html << '	<td colspan="2" align="center"></td>'
	fct_html << "	<td align='center' class='fct_unit'>( g )</td>"
	fct_num.times do |cc|
		fct_no = ( c * fct_num ) + cc
		fct_html << "	<td align='center' class='fct_unit'>( #{fct.units[fct_no]} )</td>" unless fct.units[fct_no] == nil
	end
	fct_html << '</tr>'

	# 各成分値
	fct.foods.size.times do |cc|
		fct_html << '<tr>'
		fct_html << "	<td align='center'>#{fct.fns[cc]}</td>"
		fct_html << "	<td>#{fct.foods[cc]}</td>"
		fct_html << "	<td align='right'>#{fct.weights[cc].to_f}</td>"
		fct_num.times do |ccc|
			fct_no = ( c * fct_num ) + ccc
			fct_html << "	<td align='right'>#{fct.solid[cc][fct_no]}</td>" unless fct.solid[cc][fct_no] == nil
		end
		fct_html << '</tr>'
	end

	# 合計値
	fct_html << '<tr>'
	fct_html << "	<td colspan='2' align='center' class='fct_sum'>#{l['total']}</td>"
	fct_html << "	<td align='right' class='fct_sum'>#{total_weight.to_f}</td>"
	fct_num.times do |cc|
		fct_no = ( c * fct_num ) + cc
		fct_html << "	<td align='right' class='fct_sum'>#{fct.total[fct_no]}</td>" unless fct.total[fct_no] == nil
	end
	fct_html << '</tr>'
	fct_html << '</table>'
	fct_html << '<br>'
end

puts 'ダウンロード名設定 <br>' if @debug
if recipe_name != nil && recipe_name != ''
	dl_name = "calc-#{recipe_name}"
elsif code != nil && code != ''
	dl_name = "calc-#{code}"
else
	dl_name = "calc-table"
end


puts 'HTML <br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{l['calc']}: #{recipe_name}</h5></div>
	</div>
	<div class="row">
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="palette">#{l['palette']}</label>
				<select class="form-select form-select-sm" id="palette" onchange="recalcView('#{code}')">
					#{palette_html}
				</select>
			</div>
		</div>
		<div class='col-3' align='left'>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="frct_accu" value="1" #{accu_check} onchange="recalcView('#{code}')">#{l['precision']}
			</div>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="ew_mode" value="1" #{ew_check} onchange="recalcView('#{code}')">#{l['ew']}
			</div>
		</div>
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="frct_mode">#{l['fract']}</label>
				<select class="form-select form-select-sm" id="frct_mode" onchange="recalcView('#{code}')">
					<option value="1"#{frct_select[1]}>#{l['round']}</option>
					<option value="2"#{frct_select[2]}>#{l['ceil']}</option>
					<option value="3"#{frct_select[3]}>#{l['floor']}</option>
				</select>
				<span onclick="recalcView('#{code}')">#{l['recalc']}</span>&nbsp;
			</div>
		</div>

		<div class='col-2'></div>
		<div class='col-1'>
			<a href='plain-calc.cgi?uname=#{user.name}&code=#{code}&palette=#{palette_}&ew_mode=#{ew_mode}' download='#{dl_name}.txt'>#{l['raw']}</a>
		</div>
    </div>
</div>
<br>
#{fct_html}
<div align='right' class='code'>#{code}</div>

HTML

puts html

puts 'Updating Calculation option <br>' if @debug
mdb( "UPDATE #{$MYSQL_TB_CFG} SET calcc='#{palette_}:#{ew_mode}:#{frct_mode}:#{frct_accu}' WHERE user='#{user.name}';", false, @debug )
