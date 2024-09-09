#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 menu calc 0.0.4.AI (2024/09/08)

#==============================================================================
#STATIC
#==============================================================================
fct_num = 14
@debug = false
script = 'menu-calc'

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'


#==============================================================================
#DEFINITION
#==============================================================================
# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		:food_no	=> "食品番号",\
		:food_name	=> "食品名",\
		:weight 	=> "重量",\
		:sub_total	=> "小計",\
		:palette 	=> "パレット",\
		:frct		 => "端数",\
		:frct_accu	=> "精密合計",\
		:ew 		=> "予想g",\
		:round	 	=> "四捨五入",\
		:round_up	 => "切り上げ",\
		:round_down	 => "切り捨て",\
		:calculator	=> "<img src='bootstrap-dist/icons/calculator.svg' style='height:2em; width:2em;'>",\
		:download	=> "Raw<img src='bootstrap-dist/icons/download.svg' style='height:1.5em; width:1.5em;'>",\
		:total	 	=> "合計"
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
db = Db.new( user, @debug, false )


r = db.query( "SELECT icalc FROM cfg WHERE user='#{user.name}';", false )
fct_num = r.first['icalc'].to_i unless r.first['icalc'].to_i == 0


#### Getting POST data
command = @cgi['command']
menu_code = @cgi['code']
ew_mode = @cgi['ew_mode']
frct_mode = @cgi['frct_mode']
frct_accu = @cgi['frct_accu']
palette_ = @cgi['palette']


if ew_mode.nil? || ew_mode.empty?
	r = db.query( "SELECT calcc FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false )
	if r.first && r.first['calcc'] != nil
		a = r.first['calcc'].split( ':' )
		palette_ = a[0]
		ew_mode = a[1].to_i
		frct_mode = a[2].to_i
		frct_accu = a[3].to_i
	else
		palette_ = nil
		ew_mode = 0
		frct_mode = 0
		frct_accu = 0
	end
end


puts 'Setting palette <br>' if @debug
palette = Palette.new( user.name )
palette_ = @palette_default_name[1] if palette_.nil? || palette_.empty?
palette.set_bit( palette_ )


puts 'Palette HTML <br>' if @debug
palette_html = ''
palette.sets.each_key do |k|
	palette_html << "<option value='#{k}' #{$SELECT[palette_ == k]}>#{k}</option>"
end


puts 'Extract recipe from Meal <br>' if @debug
r = db.query( "SELECT code, name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false )
meal_name = r.first['name']
meal_code = r.first['code']
meal = r.first['meal'].split( "\t" )
recipe_codes = r.first['meal'].split( "\t" )


#### 大合計の初期化
total_fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, frct_accu, frct_mode )
total_fct.load_palette( palette.bit )


puts 'Each FCT Calc<br>' if @debug
rc = 0
recipe_name = []
fct_html = []
total_total_weight = 0
fct_width = ( 70 / fct_num ).to_f
recipe_codes.each do |e|
	p e if @debug
	r = db.query( "SELECT name, sum, dish from #{$MYSQL_TB_RECIPE} WHERE code='#{e}';", false )
	recipe_name[rc] = r.first['name']
	dish_num = r.first['dish'].to_i
	dish_num = 1 if dish_num == 0
	food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )
	total_total_weight += total_weight

	fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, frct_accu, frct_mode )
	fct.load_palette( palette.bit )
	fct.set_food( user.name, food_no, food_weight, false )
	fct.calc
	fct.digit

	total_fct.into_solid( fct.total )

	#### HTML食品成分表の生成
	fct_html[rc] = ''
	table_num = fct.items.size / fct_num
	table_num += 1 if ( fct.items.size % fct_num ) != 0
	table_num.times do |c|
		fct_html[rc] << "<h6>#{recipe_name[rc]}</h6>"
		fct_html[rc] << '<table class="table table-striped table-sm">'

		# 項目名
		fct_html[rc] << '	<tr>'
		fct_html[rc] << "	<th align='center' width='6%' class='fct_item'>#{l[:food_no]}</th>"
		fct_html[rc] << "	<th align='center' width='20%' class='fct_item'>#{l[:food_name]}</th>"
		fct_html[rc] << "	<th align='center' width='4%' class='fct_item'>#{l[:weight]}</th>"
		fct_num.times do |cc|
			fct_no = ( c * fct_num ) + cc
			unless fct.names[fct_no] == nil
				fct_html[rc] << "	<th align='center' width='#{fct_width}%' class='fct_item'>#{fct.names[fct_no]}</th>"
			else
				fct_html[rc] << "	<th align='center' width='#{fct_width}%' class='fct_item'></th>"
			end
		end
		fct_html[rc] << '    </tr>'

		# 単位
		fct_html[rc] << '	<tr>'
		fct_html[rc] << '	<td colspan="2" align="center"></td>'
		fct_html[rc] << "	<td align='center' class='fct_unit'>( g )</td>"
		fct_num.times do |cc|
			fct_no = ( c * fct_num ) + cc
			fct_html[rc] << "	<td align='center' class='fct_unit'>( #{fct.units[fct_no]} )</td>" unless fct.units[fct_no] == nil
		end
		fct_html[rc] << '    </tr>'

		# 各成分値
		fct.foods.size.times do |cc|
			fct_html[rc] << '	<tr>'
			fct_html[rc] << "	<td align='center'>#{fct.fns[cc]}</td>"
			fct_html[rc] << "	<td>#{fct.foods[cc]}</td>"
			fct_html[rc] << "	<td align='right'>#{fct.weights[cc].to_f}</td>"
			fct_num.times do |ccc|
				fct_no = ( c * fct_num ) + ccc
				fct_html[rc] << "	<td align='right'>#{fct.solid[cc][fct_no]}</td>" unless fct.solid[cc][fct_no] == nil
			end
			fct_html[rc] << '    </tr>'
		end

		# 合計値
		fct_html[rc] << '	<tr>'
		fct_html[rc] << "	<td colspan='2' align='center' class='fct_sum'>#{l[:subtotal]}</td>"
		fct_html[rc] << "	<td align='right' class='fct_sum'>#{total_weight.to_f}</td>"
		fct_num.times do |cc|
			fct_no = ( c * fct_num ) + cc
			fct_html[rc] << "      <td align='right' class='fct_sum'>#{fct.total[fct_no].to_f}</td>" unless fct.total[fct_no] == nil
		end
		fct_html[rc] << '    </tr>'

		fct_html[rc] << '</table>'
		fct_html[rc] << '<br>'
	end
	rc += 1
end
total_fct.calc
total_fct.digit


#### ダウンロード名設定
if meal_name != nil && meal_name != ''
	dl_name = "calc-#{meal_name}"
elsif meal_code != nil && meal_code != ''
	dl_name = "calc-#{meal_code}"
else
	dl_name = "calc-table"
end


#### 食品番号から食品成分を抽出
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{meal_name}</h5></div>
	</div>
	<div class="row">
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="palette">#{l[:palette]}</label>
				<select class="form-select" id="palette" onchange="menuRecalcView('#{meal_code}')">
					#{palette_html}
				</select>
			</div>
		</div>

		<div class='col-3' align='center'>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="frct_accu" value="1" #{$CHECK[frct_accu]} onchange="menuRecalcView('#{meal_code}')">#{l[:frct_accu]}
			</div>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="ew_mode" value="1" #{$CHECK[ew_mode]} onchange="menuRecalcView('#{meal_code}')">#{l[:ew]}
			</div>
		</div>

		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{l[:frct]}</label>
				<select class="form-select" id="frct_mode" onchange="menuRecalcView('#{meal_code}')">
					<option value="1"#{$SELECT[frct_mode == 1]}>#{l[:round]}</option>
					<option value="2"#{$SELECT[frct_mode == 2]}>#{l[:round_up]}</option>
					<option value="3"#{$SELECT[frct_mode == 3]}>#{l[:round_down]}</option>
				</select>
				<span onclick="menuRecalcView('#{meal_code}')">#{l[:calculator]}</span>&nbsp;
			</div>
		</div>
		<div class='col-2'></div>
		<div class='col-1'>
			<a href='plain-menu-calc.cgi?uname=#{user.name}&code=#{meal_code}&palette=#{palette_}&ew_mode=#{ew_mode}' download='#{dl_name}.txt'>#{l[:download]}</a>
		</div>
    </div>
</div>
<br>
HTML


#### HTML食品成分全合計
fct_html_sum = ''
table_num = total_fct.items.size / fct_num
table_num += 1 if ( total_fct.items.size % fct_num ) != 0
table_num.times do |c|
	fct_html_sum << '<table class="table table-striped table-sm">'

	# 項目名
	fct_html_sum << '	<tr>'
	fct_html_sum << '	<th align="center" width="6%" class="fct_item"></th>'
	fct_html_sum << '	<th align="center" width="20%" class="fct_item"></th>'
	fct_html_sum << "	<th align='center' width='4%' class='fct_item'>#{l[:weight]}</th>"
	fct_num.times do |cc|
		fct_no = ( c * fct_num ) + cc
		unless total_fct.names[fct_no] == nil
			fct_html_sum << "	<th align='center' width='#{fct_width}%' class='fct_item'>#{total_fct.names[fct_no]}</th>"
		else
			fct_html_sum << "	<th align='center' width='#{fct_width}%' class='fct_item'></th>"
		end
	end
	fct_html_sum << '	</tr>'

	# 単位
	fct_html_sum << '	<tr>'
	fct_html_sum << '	<td colspan="2" align="center"></td>'
	fct_html_sum << "	<td align='center' class='fct_unit'>( g )</td>"
	fct_num.times do |cc|
		fct_no = ( c * fct_num ) + cc
		fct_html_sum << "	<td align='center' class='fct_unit'>( #{total_fct.units[fct_no]} )</td>" unless total_fct.units[fct_no] == nil
	end
	fct_html_sum << '    </tr>'

	# 合計値
	fct_html_sum << '	<tr>'
	fct_html_sum << "	<td colspan='2' align='center' class='fct_sum'>#{l[:total]}</td>"
	fct_html_sum << "	<td align='right' class='fct_sum'>#{total_total_weight.to_f}</td>"
	fct_num.times do |cc|
		fct_no = ( c * fct_num ) + cc
		fct_html_sum << "	<td align='right' class='fct_sum'>#{total_fct.total[fct_no].to_f}</td>" unless total_fct.total[fct_no] == nil
	end
	fct_html_sum << '    </tr>'
	fct_html_sum << '</table>'
end


puts html
puts fct_html_sum

fct_html.each do |e| puts e end

puts "<div align='right' class='code'>#{meal_code}</div>"

#### Updating Calculation option
db.query( "UPDATE #{$MYSQL_TB_CFG} SET calcc='#{palette_}:#{ew_mode}:#{frct_mode}:#{frct_accu}' WHERE user='#{user.name}';", false )
