#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 menu basic analysis 0.02b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'plain-menu-analysis'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### Language init
def lp_init( script, language_set )
  f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{language_set}", "r" )
  lp = [nil]
  f.each do |line|
    lp << line.chomp.force_encoding( 'UTF-8' )
  end
  f.close

  return lp
end


#### 予想重量チェック
def ew_check( ew_mode, lp )
  ew_check = lp[6]
  ew_check = lp[7] if ew_mode == 1

  return ew_check
end


#==============================================================================
# Main
#==============================================================================
puts "Content-type: text/text\n\n"

#### GETデータの取得
get = get_data()
uname = get['uname']
code = get['code']
ew_mode = get['ew_mode']
lg = get_data['lg']

ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i

lg = $DEFAULT_LP if lg = '' || lg = nil
lp = lp_init( script, lg )


#### チェック設定
ew_check = ew_check( ew_mode, lp )


puts 'Setting palette' if @debug
palette = Palette.new( uname )
palette_ = @palette_default_name[1] if palette_ == nil || palette_ == '' || palette_ == '0'
palette.set_bit( palette_ )


puts 'Extracting recipe from meal' if @debug
r = mdb( "SELECT code, name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false, @debug )
meal_name = r.first['name']
code = r.first['code']
meal = r.first['meal'].split( "\t" )
recipe_code = []
meal.each do |e| recipe_code << e end


puts 'FCT init' if @debug
fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct.load_palette( palette.bit )

recipe_code.each do |e|
	# RECIPEからデータを抽出
	r = mdb( "SELECT name, sum, dish from #{$MYSQL_TB_RECIPE} WHERE code='#{e}';", false, @debug )
	dish_num = r.first['dish'].to_i
	dish_num = 1 if dish_num == 0
	food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )

	# 食品番号から食品成分と名前を抽出
	fct.set_food( uname, food_no, food_weight, false )
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


puts 'Counting food group' if @debug
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


puts 'Getting PFC rate' if @debug
pfc = fct.calc_pfc


puts 'Animal protein rate' if @debug
animal_protein_rate = ( animal_protein / fct.total[1] * 100 )


puts 'Grain energy rate' if @debug
grain_energy_rate = ( grain_energy / fct.total[0] * 100 )


#### ダウンロード名設定
if meal_name != nil && meal_name != ''
	dl_name = "calc-#{meal_name}"
elsif code != nil && code != ''
	dl_name = "calc-#{code}"
else
	dl_name = "calc-table"
end


#### テキスト成形
analysis_text = ''
analysis_text << "#{lp[8]}\t#{lp[9]}\t#{fch['01'].to_f}\n"
analysis_text << "\t#{lp[10]}\t#{fch['02'].to_f}\n"
analysis_text << "\t#{lp[11]}\t#{fch['03'].to_f}\n"
analysis_text << "\t#{lp[12]}\t#{fch['04'].to_f}\n"
analysis_text << "\t#{lp[13]}\t#{fch['05'].to_f}\n"
analysis_text << "\t#{lp[14]}\t#{fch['06'].to_f}\n"
analysis_text << "\t#{lp[15]}\t#{gycv.to_f}\n"
analysis_text << "\t#{lp[16]}\t#{wcv.to_f}\n"
analysis_text << "\t#{lp[17]}\t#{fch['07'].to_f}\n"
analysis_text << "\t#{lp[18]}\t#{fch['08'].to_f}\n"
analysis_text << "\t#{lp[19]}\t#{fch['09'].to_f}\n"
analysis_text << "\t#{lp[20]}\t#{fch['10'].to_f}\n"
analysis_text << "\t#{lp[21]}\t#{fch['11'].to_f}\n"
analysis_text << "\t#{lp[22]}\t#{fch['12'].to_f}\n"
analysis_text << "\t#{lp[23]}\t#{fch['13'].to_f}\n"
analysis_text << "\t#{lp[24]}\t#{milk_liquid.to_f}\n"
analysis_text << "\t#{lp[25]}\t#{milk_product.to_f}\n"
analysis_text << "\t#{lp[26]}\t#{fch['14'].to_f}\n"
analysis_text << "\t#{lp[27]}\t#{fch['15'].to_f}\n"
analysis_text << "\t#{lp[28]}\t#{fch['16'].to_f}\n"
analysis_text << "\t#{lp[29]}\t#{fch['17'].to_f}\n"
analysis_text << "\t#{lp[30]}\t#{miso.to_f}\n"
analysis_text << "\t#{lp[31]}\t#{shoyu.to_f}\n"
analysis_text << "\t#{lp[32]}\t#{salt.to_f}\n"
analysis_text << "\t#{lp[33]}\t#{seasoning.to_f}\n"
analysis_text << "\t#{lp[34]}\t#{fch['18'].to_f}\n"
analysis_text << "\t#{lp[35]}\t#{fct.total_weight.to_f}\n"
analysis_text << "#{lp[36]}\t#{lp[37]}\t#{pfc[0].to_f}\n"
analysis_text << "\t#{lp[38]}\t#{pfc[1].to_f}\n"
analysis_text << "\t#{lp[39]}\t#{pfc[2].to_f}\n"
analysis_text << "#{lp[40]}\t#{lp[41]}\t#{grain_energy_rate.to_f}\n"
analysis_text << "\t#{lp[42]}\t#{animal_protein_rate.to_f}\n"

#### 食品番号から食品成分を表示
puts "#{lp[43]} #{meal_name}\t#{lp[44]} #{code}\t#{lp[45]} #{ew_check}\n"
puts analysis_text
