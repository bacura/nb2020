#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 plain calc 0.02b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'plain-calc'
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

#### 端数処理の選択
def frct_select( frct_mode, lp )
	frct_select = ''
	case frct_mode
	when 3
		frct_select = lp[1]
	when 2
		frct_select = lp[2]
	else
		frct_select = lp[3]
	end

	return frct_select
end


#### 合計精密チェック
def accu_check( frct_accu, lp )
  accu_check = lp[4]
  accu_check = lp[5] if frct_accu == 1

  return accu_check
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
frct_mode = get['frct_mode']
frct_accu = get['frct_accu']
palette_ = get['palette']
ew_mode = get['ew_mode']
lg = get_data['lg']

ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i
frct_mode = 0 if frct_mode == nil
frct_mode = frct_mode.to_i
frct_accu = 0 if frct_accu == nil
frct_accu = frct_accu.to_i
lg = $DEFAULT_LP if lg = '' || lg = nil
lp = lp_init( script, lg )


puts 'Extracting SUM data <br>' if @debug
r = mdb( "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{uname}';", false, @debug )
recipe_name = r.first['name']
code = r.first['code']
dish_num = r.first['dish'].to_i
food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )


puts 'Checking SELECT & CHECK <br>' if @debug
frct_select = frct_select( frct_mode, lp )
accu_check = accu_check( frct_accu, lp )
ew_check = ew_check( ew_mode, lp )


puts 'Setting palette <br>' if @debug
palette = Palette.new( uname )
palette_ = @palette_default_name[1] if palette_ == nil || palette_ == ''
palette.set_bit( palette_ )


puts 'FCT Calc<br>' if @debug
fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct )
fct.load_palette( palette.bit )
fct.set_food( uname, food_no, food_weight, false )
fct.calc( frct_accu, frct_mode )
fct.digit( frct_mode )


puts 'FCT TEXT<br>' if @debug
fct_txt = ''

# 項目名
fct_txt << lp[8]
fct.names.each do |e|
	fct_txt << "#{e}\t"
end
fct_txt.chop!
fct_txt << "\n"

#### 単位
fct_txt << "\t\tg\t"
fct.units.each do |e|
	fct_txt << "#{e}\t"
end
fct_txt.chop!
fct_txt << "\n"


#### 各成分値
fct.foods.size.times do |c|
	fct_txt << "#{fct.fns[c]}\t#{fct.names[c]}\t#{fct.weights[c].to_f}\t"
	fct.items.size.times do |cc| fct_txt << "#{fct.solid[c][cc].to_f}\t" end
	fct_txt.chop!
	fct_txt << "\n"
end


# 合計値
fct_txt << "\t#{lp[9]}\t#{total_weight.to_f}\t"
fct.total.each do |e|
		fct_txt << "#{e}\t"
end
fct_txt.chop!
fct_txt << "\n"


#### 食品番号から食品成分を表示
puts "#{lp[10]} #{recipe_name}\t#{lp[11]} #{code}\t#{lp[12]} #{ew_check}\t#{lp[13]} #{frct_select} / #{accu_check}\n".encode( 'Shift_JIS' )
puts fct_txt.encode( 'Shift_JIS' )
