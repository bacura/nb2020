#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 menul food composition analysis 0.02b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'menu-analysis'


#==============================================================================
#DEFINITION
#==============================================================================

#### Language_pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'koyomi' 	=> "こよみ栄養計算",\
		'palette'	=> "パレット",\
		'signpost'	=> "<img src='bootstrap-dist/icons/signpost.svg' style='height:2em; width:2em;'>",\
		'fromto'	=> "　～　",\
		'calc'		=> "計　算",\
		'no_day'	=> "該当日がありません",\
		'ew'		=> "予想g",\
		'name'		=> "栄養成分",\
		'unit'		=> "単位",\
		'volume'	=> "合計",\
		'breakfast'	=> "朝食",\
		'lunch'		=> "昼食",\
		'dinner'	=> "夕食",\
		'supply'	=> "捕食・間食",\
		'period'	=> "期間総量（",\
		'days'		=> "日間）",\
		'average'	=> "１日平均",\
		'ratio'		=> "割合"
	}

	return l[language]
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


puts 'Getting POST <br>' if @debug
command = @cgi['command']
code = @cgi['code']
ew_mode = @cgi['ew_mode']
ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i
frct_mode = @cgi['frct_mode']
frct_mode = 0 if frct_mode == nil
frct_mode = frct_mode.to_i
frct_accu = @cgi['frct_accu']
frct_accu = 0 if frct_accu == nil
frct_accu = frct_accu.to_i

if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "ew_mode: #{ew_mode}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "frct_accu: #{frct_accu}<br>"
	puts "<hr>"
end


puts 'Checking SELECT & CHECK <br>' if @debug
frct_select = selected( 1, 3, frct_mode )


puts 'Setting palette <br>' if @debug
palette = Palette.new( user.name )
palette_ = @palette_default_name[1] if palette_ == nil || palette_ == '' || palette_ == '0'
palette.set_bit( palette_ )


#### mealからデータを抽出
r = mdb( "SELECT code, name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, @debug )
meal_name = r.first['name']
code = r.first['code']
meal = r.first['meal'].split( "\t" )
recipe_code = []
meal.each do |e| recipe_code << e end


#### 大合計の初期化
fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, frct_accu, frct_mode )
fct.load_palette( palette.bit )

recipe_code.each do |e|
	# RECIPEからデータを抽出
	r = mdb( "SELECT name, sum, dish from #{$MYSQL_TB_RECIPE} WHERE code='#{e}';", false, @debug )
	dish_num = r.first['dish'].to_i
	dish_num = 1 if dish_num == 0
	food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )

	# 食品番号から食品成分と名前を抽出
	fct.set_food( user.name, food_no, food_weight, false )
end
fct.calc
fct.digit


animal_protein = BigDecimal( 0 )
grain_energy = BigDecimal( 0 )
fct.fns.size.times do |c|
	fg = fct.fns[c].sub( /P|U/, '' ).slice( 0, 2 ).to_i
	# 動物性たんぱく質カウント
	animal_protein += fct.solid[c][1] if fg >= 10 && fg <= 13
	# 穀類エネルギーカウント
	grain_energy += fct.solid[c][0] if fg == 1
end


#### 食品構成のカウント
fch = {'01'=>0, '02'=>0, '03'=>0, '04'=>0, '05'=>0, '06'=>0, '07'=>0, '08'=>0, '09'=>0, '10'=>0, '11'=>0, '12'=>0, '13'=>0, '14'=>0, '15'=>0, '16'=>0, '17'=>0, '18'=>0 }
wcv = 0
gycv = 0
milk_liquid = 0
milk_product = 0
salt = 0
miso = 0
shoyu = 0
seasoning = 0

fct.fns.size.times do |c|
	food_group = fct.fns[c].sub( /P|U/, '' ).slice( 0, 2 )
	fch[food_group] += fct.weights[c]
	case food_group
	when '06'
		# 緑黄色野菜の判定
		r = mdb( "SELECT gycv FROM #{$MYSQL_TB_EXT} WHERE FN='#{pseudo_id}#{fct.fns[c]}';", false, @debug )
		if r.first['gycv'] == 1
			gycv += fct.weights[c]
		else
			wcv += fct.weights[c]
		end
	when '13'
		# 牛乳と乳製品の判定
		if fct.fns[c].to_i >= 13001 && fct.fns[c].to_i <= 13006
			milk_liquid += fct.weights[c]
		else
			milk_product += fct.weights[c]
		end
	when '17'
		# 液体だしの乾燥重量化
		if fct.fns[c].to_i >= 17019 && fct.fns[c].to_i <= 17025
			fct.weights[c] = fct.weights[c] / 100 * 1.0
		elsif fct.fns[c].to_i == 17026
			fct.weights[c] = fct.weights[c] / 100 * 2.5
		end
		# 塩の判定
		if ( fct.fns[c].to_i >= 17012 && fct.fns[c].to_i <= 17014 ) || fct.fns[c].to_i == 17089
			salt += fct.weights[c]
		# 味噌の判定
		elsif ( fct.fns[c].to_i >= 17044 && fct.fns[c].to_i <= 17050 ) || fct.fns[c].to_i == 17119 || fct.fns[c].to_i == 17120
			miso += fct.weights[c]
		# 醤油の判定
		elsif ( fct.fns[c].to_i >= 17007 && fct.fns[c].to_i <= 17011 ) || ( fct.fns[c].to_i >= 17086 && fct.fns[c].to_i <= 17088 )
			shoyu += fct.weights[c]
		else
			seasoning += fct.weights[c]
		end
	end
end


puts 'Getting PFC rate<br>' if @debug
pfc = fct.calc_pfc


puts 'Animal protein rate<br>' if @debug
animal_protein_rate = ( animal_protein / fct.total[1] * 100 ).round( 1 )


puts 'Grain energy rate<br>' if @debug
grain_energy_rate = ( grain_energy / fct.total[0] * 100 ).round( 1 )


#### ダウンロード名設定
if meal_name != nil && meal_name != ''
	dl_name = "analysis-#{meal_name}"
elsif code != nil && code != ''
	dl_name = "analysis-#{code}"
else
	dl_name = "analysis-table"
end


puts 'HTML <br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{meal_name}</h5></div>
	</div>
	<div class="row">
		<div class='col-4' align='center'>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="frct_accu" value="1" #{checked( frct_accu )} onchange="menuReAnalysis('#{code}')">#{lp[2]}
			</div>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="ew_mode" value="1" #{checked( ew_mode )} onchange="menuReAnalysis('#{code}')">#{lp[3]}
			</div>
		</div>
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="">#{lp[4]}</label>
				<select class="form-select" id="frct_mode" onchange="menuReAnalysis('#{code}')">
					<option value="1"#{frct_select[1]}>#{lp[5]}</option>
					<option value="2"#{frct_select[2]}>#{lp[6]}</option>
					<option value="3"#{frct_select[3]}>#{lp[7]}</option>
				</select>
			</div>
		</div>

		<div class='col-4'></div>
		<div class='col-1'>
			<a href='plain-menu-analysis.cgi?uname=#{user.name}&code=#{code}&ew_mode=#{ew_mode}' download='#{dl_name}.txt'>#{lp[8]}</a>
		</div>
    </div>
</div>
<br>
<div class='table-responsive-sm'>
	<table class="table table-bordered table-sm">
		<tbody>
		<tr><th width="20%" rowspan='24'>#{lp[9]}</th><th width="25%">#{lp[10]}</th><td width="15%">#{fch['01'].to_f}</td></tr>
		<tr><th>#{lp[11]}</th><td>#{fch['02'].to_f}</td></tr>
		<tr><th>#{lp[12]}</th><td>#{fch['03'].to_f}</td></tr>
		<tr><th>#{lp[13]}</th><td>#{fch['04'].to_f}</td></tr>
		<tr><th>#{lp[14]}</th><td>#{fch['05'].to_f}</td></tr>
		<tr><th rowspan="2">#{lp[15]}</th><td rowspan="2">#{fch['06'].to_f}</td><th width="25%">#{lp[16]}</th><td>#{gycv.to_f}</td></tr>
				<tr><th>#{lp[17]}</th><td>#{wcv.to_f}</td></tr>
		<tr><th>#{lp[18]}</th><td>#{fch['07'].to_f}</td></tr>
		<tr><th>#{lp[19]}</th><td>#{fch['08'].to_f}</td></tr>
		<tr><th>#{lp[20]}</th><td>#{fch['09'].to_f}</td></tr>
		<tr><th>#{lp[21]}</th><td>#{fch['10'].to_f}</td></tr>
		<tr><th>#{lp[22]}</th><td>#{fch['11'].to_f}</td></tr>
		<tr><th>#{lp[23]}</th><td>#{fch['12'].to_f}</td></tr>
		<tr><th rowspan="2">#{lp[24]}</th><td rowspan="2">#{fch['13'].to_f}</td><th>#{lp[25]}</th><td>#{milk_liquid.to_f}</td></tr>
				<tr><th>#{lp[26]}</th><td>#{milk_product.to_f}</td></tr>
		<tr><th>#{lp[27]}</th><td>#{fch['14'].to_f}</td></tr>
		<tr><th>#{lp[28]}</th><td>#{fch['15'].to_f}</td></tr>
		<tr><th>#{lp[29]}</th><td>#{fch['16'].to_f}</td></tr>
		<tr><th rowspan="4">#{lp[30]}</th><td rowspan="4">#{fch['17'].to_f}</td><th>#{lp[31]}</th><td>#{miso.to_f}</td></tr>
			<tr><th>#{lp[32]}</th><td>#{shoyu.to_f}</td></tr>
			<tr><th>#{lp[33]}</th><td>#{salt.to_f}</td></tr>
			<tr><th>#{lp[34]}</th><td>#{seasoning.to_f}</td></tr>
		<tr><th>#{lp[35]}</th><td>#{fch['18'].to_f}</td></tr>
		<tr><th>#{lp[36]}</th><td>#{fct.total_weight.to_f}</td></tr>
		<tr><th rowspan='3'>#{lp[37]}</th><th>#{lp[38]}</th><td>#{pfc[0].to_f}</td></tr>
			<th>#{lp[39]}</th><td>#{pfc[1].to_f}</td></tr>
			<th>#{lp[40]}</th><td>#{pfc[2].to_f}</td></tr>
		<tr><th rowspan='2'>#{lp[41]}</th><th>#{lp[42]}</th><td>#{grain_energy_rate.to_f}</td></tr>
			<th>#{lp[43]}</th><td>#{animal_protein_rate.to_f}</td></tr>
		</tbody>
	</table>
</div>
HTML

puts html
puts "<div align='right' class='code'>#{code}</div>"
