#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 plain calc 0.01b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


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
palette = get['palette']
ew_mode = get['ew_mode']
lg = get_data['lg']

ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i
frct_mode = 0 if frct_mode == nil
frct_mode = frct_mode.to_i
frct_accu = 0 if frct_accu == nil
frct_accu = frct_accu.to_i
palette = 0 if palette == nil
palette = palette.to_i
lg = $DEFAULT_LP if lg = '' || lg = nil
lp = lp_init( script, lg )


require "#{$SERVER_PATH}/nb2020-soul-#{lg}"


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


#### Setting palette
palette_sets = []
palette_name = []
r = mdb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false, @debug )
if r.first
	r.each do |e|
		a = e['palette'].split( '' )
		a.map! do |x| x.to_i end
		palette_sets << a
		palette_name << e['name']
	end
end
palette_set = palette_sets[palette]


#### 成分項目の抽出
fct_item = []
@fct_item.size.times do |c|
	fct_item << @fct_item[c] if palette_set[c] == 1
end


#### 食品番号から食品成分と名前を抽出
fct = []
fct_name = []
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

#### 食品成分データの抽出と名前の書き換え
food_no.each do |e|
	fct_tmp = []
	if e == '-'
		fct << '-'
		fct_name << '-'
	elsif e == '+'
		fct << '+'
		fct_name << '+'
	elsif e == '00000'
		fct << '0'
		fct_name << '0'
	else
		if /P|U/ =~ e
			q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
		else
			q = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
		end
		res = db.query( q )
		fct_name << res.first['Tagnames']
		@fct_item.size.times do |c|
			fct_tmp << res.first[@fct_item[c]] if palette_set[c] == 1
		end
		fct << Marshal.load( Marshal.dump( fct_tmp ))
	end
end


#### 名前の書き換え
if false
	food_no.size.times do |c|
 		unless food_no[c] == '+' || food_no[c] == '-' || food_no[c] == '0'
			q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}';"
			q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}' AND ( user='#{uname}' OR user='#{$GM}' );" if /P|U/ =~ food_no[c]
			r = db.query( q )
			fct_name[c] = bind_tags( r ) if r.first
		end
	end
end
db.close


#### データ計算
fct_sum = []
fct_item.size.times do |c| fct_sum << BigDecimal( 0 ) end

food_no.size.times do |fn|
	unless food_no[fn] == '-' || food_no[fn] == '+'
		fct_item.size.times do |fi|
			t = convert_zero( fct[fn][fi] )

			# 通常計算
			fct[fn][fi] = num_opt( t, food_weight[fn], frct_mode, @fct_frct[fct_item[fi]] )
			if frct_accu == 0
				# 通常計算
				fct_sum[fi] += BigDecimal( fct[fn][fi] )
			else
				# 精密計算
				fct_sum[fi] += BigDecimal( num_opt( t, food_weight[fn], frct_mode, @fct_frct[fct_item[fi]] + 3 ))
			end
		end
	end
end


#### 合計値の桁合わせ
fct_sum = adjust_digit( fct_item, fct_sum, frct_mode )


#### HTML食品成分表の生成
fct_txt = ''

# 項目名
fct_txt << lp[8]
fct_item.each do |e|
	if @fct_name[e]
		fct_txt << "#{@fct_name[e]}\t"
	else
		fct_txt << "\t"
	end
end
fct_txt.chop!
fct_txt << "\n"


#### 単位
fct_txt << "\t\tg\t"
fct_item.size.times do |c|
	if @fct_unit[fct_item[c]]
		fct_txt << "#{@fct_unit[fct_item[c]]}\t"
	else
		fct_txt << "\t"
	end
end
fct_txt.chop!
fct_txt << "\n"


#### 各成分値
food_no.size.times do |c|
	unless food_no[c] == '-' || food_no[c] == '+'
		fct_txt << "#{food_no[c]}\t#{fct_name[c]}\t#{food_weight[c].to_f}\t"
		fct_item.size.times do |cc| fct_txt << "#{fct[c][cc]}\t" end
		fct_txt.chop!
		fct_txt << "\n"
	end
end

# 合計値
fct_txt << "\t#{lp[9]}\t#{total_weight.to_f}\t"
fct_item.size.times do |c|
	if fct_item[c] == 'REFUSE' || fct_item[c] == 'WCR' || fct_item[c] == 'Notice'
			fct_txt << "\t"
	else
			fct_txt << "#{fct_sum[c]}\t"
	end
end
fct_txt.chop!
fct_txt << "\n"


#### 食品番号から食品成分を表示
puts "#{lp[10]} #{recipe_name}\t#{lp[11]} #{code}\t#{lp[12]} #{ew_check}\t#{lp[13]} #{frct_select} / #{accu_check}\n".encode( 'Shift_JIS' )
puts fct_txt.encode( 'Shift_JIS' )
