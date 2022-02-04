#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 plain menu calc 0.03b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'plain-menu-calc'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### Language init
def lp_init( script, language_set )
  f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{language_set}", "r" )
  lp = [nil]
  f.each do |line| lp << line.chomp.force_encoding( 'UTF-8' ) end
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
ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i

palette_ = ''
if get['palette'] == nil
	palette_ = @palette_default_name[1]
else
	palette_ = CGI.unescape( get['palette'] )
end

lg = get_data['lg']
lg = $DEFAULT_LP if lg = '' || lg = nil
lp = lp_init( script, lg )
if @debug
	puts "uname: #{uname}\n"
	puts "code: #{code}\n"
	puts "ew_mode: #{ew_mode}\n"
	puts "palette_: #{palette_}\n"
	puts "<hr>"
end


puts "Checking CHECK\n" if @debug
ew_check = ew_check( ew_mode, lp )


puts "Setting palette\n" if @debug
palette = Palette.new( uname )
palette_ = @palette_default_name[1] if palette_ == nil || palette_ == ''
palette.set_bit( palette_ )


puts "Extract recipe from Meal\n" if @debug
recipe_code = []
r = mdb( "SELECT code, name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false, @debug )
meal_name = r.first['name']
code = r.first['code']
meal = r.first['meal'].split( "\t" )
meal.each do |e| recipe_code << e end


#### 大合計の初期化
total_fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
total_fct.load_palette( palette.bit )


puts 'Each FCT Calc<br>' if @debug
rc = 0
recipe_name = []
fct_txt = []
total_total_weight = 0
recipe_code.each do |e|
	r = mdb( "SELECT name, sum, dish from #{$MYSQL_TB_RECIPE} WHERE code='#{e}';", false, @debug )
	recipe_name[rc] = r.first['name']
	dish_num = r.first['dish'].to_i
	dish_num = 1 if dish_num == 0
	food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )
	total_total_weight += total_weight

	fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
	fct.load_palette( palette.bit )
	fct.set_food( uname, food_no, food_weight, false )
	fct.calc
	#fct.digit

	total_fct.into_solid( fct.total )

	#### HTML食品成分表の生成
	fct_txt[rc] = ''
	fct_txt[rc] << "#{recipe_name[rc]}\n"

	# 項目名
	fct_txt[rc] << "\t#{lp[8]}\t#{lp[16]}\t#{lp[17]}"
	fct.names.each do |ee| fct_txt[rc] << "\t#{ee}" end
	fct_txt[rc] << "\n"

	# 単位
	fct_txt[rc] << "\t\t\t( g )"
	fct.units.each do |ee| fct_txt[rc] << "\t( #{ee} )" end
	fct_txt[rc] << "\n"

	# 各成分値
	fct.foods.size.times do |c|
			fct_txt[rc] << "\t#{fct.fns[c]}\t#{fct.names[c]}\t#{fct.weights[c].to_f}"
			fct.items.size.times do |cc|
				fct_txt[rc] << "\t#{fct.solid[c][cc].to_f}"
			end
			fct_txt[rc] << "\n"
	end

	# 合計値
	fct_txt[rc] << "\t\t#{lp[9]}\t#{total_weight.to_f}"
	fct.total.each do |e| fct_txt[rc] << "\t#{e.to_f}" end
	fct_txt[rc] << "\n\n"

	rc += 1
end
total_fct.calc
#total_fct.digit


#### HTML食品成分全合計
fct_txt_sum = ''

# 項目名
fct_txt_sum << "\t\t\t#{lp[10]}\t"
total_fct.names.each do |e| fct_txt_sum << "#{e}\t" end
fct_txt_sum.chop!
fct_txt_sum << "\n"

# 単位
fct_txt_sum << "\t\t\t(g)\t"
total_fct.units.each do |e| fct_txt_sum << "(#{e})\t" end
fct_txt_sum.chop!
fct_txt_sum << "\n"

# 合計値
fct_txt_sum << "\t\t#{lp[11]}\t#{total_total_weight.to_f}\t"
total_fct.total.each do |e| fct_txt_sum << "#{e.to_f}\t" end
fct_txt_sum.chop!
fct_txt_sum << "\n"


#### 食品番号から食品成分を表示
puts "#{lp[12]} #{meal_name}\t#{lp[13]} #{code}\t#{lp[14]} #{ew_check}\n"
fct_txt.each do |e| puts e end
puts fct_txt_sum
