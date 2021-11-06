#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe to pseudo food 0.03b

#==============================================================================
# LIBRARY
#==============================================================================
require './probe'


#==============================================================================
# STATIC
#==============================================================================
script = 'pseudo_r2f'
@debug = false


#==============================================================================
# DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### POSTデータの取得
command = @cgi['command']
code = @cgi['code']
food_name = @cgi['food_name']
food_group = @cgi['food_group']
class1 = @cgi['class1']
class2 = @cgi['class2']
class3 = @cgi['class3']
tag1 = @cgi['tag1']
tag2 = @cgi['tag2']
tag3 = @cgi['tag3']
tag4 = @cgi['tag4']
tag5 = @cgi['tag5']
if @debug
	puts "command: #{command}<br>\n"
	puts "code: #{code}<br>\n"
	puts "<hr>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_group: #{food_group}<br>\n"
	puts "class1: #{class1}<br>\n"
	puts "class2: #{class2}<br>\n"
	puts "class3: #{class3}<br>\n"
	puts "tag1: #{tag1}<br>\n"
	puts "tag2: #{tag2}<br>\n"
	puts "tag3: #{tag3}<br>\n"
	puts "tag4: #{tag4}<br>\n"
	puts "tag5: #{tag5}<br>\n"
end


puts 'SUMからデータを抽出<br>' if @debug
r = mdb( "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
code = r.first['code']
dish_num = r.first['dish'].to_i
food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, 0 )

if command == 'form'
	# 食品群オプション html
	food_group_option = ''
	19.times do |c|
		cc = c
		cc = "0#{c}" if c < 10
		food_group_option << "<option value='#{cc}'>#{c}.#{@category[c]}</option>"
	end

	html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_name">#{lp[1]}</label>
				<input type="text" class="form-control form-control-sm" id="food_name" value="#{food_name}">
			</div>
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_group">#{lp[2]}</label>
				<select class="form-select form-select-sm" id="food_group">
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-3"></div>
		<div class="col-1">
			<button class="btn btn-outline-primary btn-sm" type="button" onclick="savePseudo_R2F( '#{code}' )">#{lp[3]}</button>
		</div>
	</div>

	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class1" placeholder="class1" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class2" placeholder="class2" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class3" placeholder="class3" value=""></div>
	</div>
	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag1" placeholder="tag1" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag2" placeholder="tag2" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag3" placeholder="tag3" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag4" placeholder="tag4" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag5" placeholder="tag5" value=""></div>
		<div class="col-1"></div>
	</div>
</div>

HTML
end


if command == 'save'
	fct_opt = Hash.new

	puts '食品番号から食品成分と名前を抽出<br>' if @debug
	fct = []
	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
	food_no.each do |e|
		fct_tmp = []
		if e == '-'
			fct << '-'
		elsif e == '+'
			fct << '+'
		elsif e == '00000'
			fct << '0'
		else
			if /P|U/ =~ e
				query = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{user.name}' OR user='#{$GM}' );"
			else
				query = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
			end
			res = db.query( query )
			@fct_item.each do |e| fct_tmp << res.first[e] end
			fct << Marshal.load( Marshal.dump( fct_tmp ))
		end
	end
	db.close

	puts 'データ計算<br>' if @debug
	fct_sum = []
	@fct_item.each do fct_sum << BigDecimal( 0 ) end
	food_no.size.times do |fn|
		unless food_no[fn] == '-' || food_no[fn] == '+'
			@fct_start.upto( @fct_end ) do |fi|
				t = convert_zero( fct[fn][fi] )
				fct[fn][fi] = num_opt( t, food_weight[fn], 0, @fct_frct[@fct_item[fi]] )
				fct_sum[fi] += BigDecimal( num_opt( t, food_weight[fn], 0, @fct_frct[@fct_item[fi]] + 3 ))
			end
		end
	end

	puts '100 g当たりに換算と合計値の桁合わせ<br>' if @debug
	@fct_start.upto( @fct_end ) do |i| fct_sum[i] = fct_sum[i] / ( total_weight / 100 ) end
	fct_sum = adjust_digit( @fct_item, fct_sum, 0 )
	@fct_start.upto( @fct_end ) do |i|	fct_opt[@fct_item[i]] = fct_sum[i] end

	#計算除外値
	fct_opt['REFUSE'] = 0
	fct_opt['Notice'] = code


	class1_new = ''
	class2_new = ''
	class3_new = ''
	tag1_new = ''
	tag2_new = ''
	tag3_new = ''
	tag4_new = ''
	tag5_new = ''
	class1_new = "＜#{class1}＞" unless class1 == ''
	class2_new = "（#{class2}）" unless class2 == ''
	class3_new = "［#{class3}］" unless class3 == ''
	tag1_new = "　#{tag1}" unless tag1 == ''
	tag2_new = "　#{tag2}" unless tag2 == ''
	tag3_new = "　#{tag3}" unless tag3 == ''
	tag4_new = "　#{tag4}" unless tag4 == ''
	tag5_new = "　#{tag5}" unless tag5 == ''
	tagnames_new = "#{class1_new}#{class2_new}#{class3_new}#{food_name}#{tag1_new}#{tag2_new}#{tag3_new}#{tag4_new}#{tag5_new}"

	puts '擬似食品成分表テーブルに追加<br>' if @debug
	fct_set = ''
	( @fct_start - 1 ).upto( @fct_end + 1 ) do |i| fct_set << "#{@fct_item[i]}='#{fct_opt[@fct_item[i]]}'," end
	fct_set.chop!

	puts '新規食品番号の合成<br>' if @debug
	code = ''
	if user.status >= 8
		puts '公開<br>' if @debug
		public_bit = 1
		r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public='3';", false, @debug )

		if r.first
			code = r.first['FN']
			puts "リサイクル:#{code}<br>" if @debug
		else
			rr = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public=1)", false, @debug )
			if rr.first
				puts "検出:#{rr.first['FN']}<br>" if @debug
				last_code = rr.first['FN'][-3,3].to_i
				code = "P#{food_group}%#03d" % ( last_code + 1 )
			else
				code = "P#{food_group}001"
			end
			puts "新規:#{code}<br>" if @debug
		end
	else
		puts 'プライベート<br>' if @debug
		r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}' AND public='2';", false, @debug )
		if r.first
			code = r.first['FN']
		else
			rr = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}' AND public=0);", false, @debug )
			if rr.first
				last_code = rr.first['FN'][-3,3].to_i
				code = "U#{food_group}%#03d" % ( last_code + 1 )
			else
				code = "U#{food_group}001"
			end
		end
	end

	puts '食品番号のチェック<br>' if @debug
	r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE user='#{user.name}' AND FN='#{code}';", false, @debug )
	if r.first
		# 擬似食品テーブルの更新
		mdb( "UPDATE #{$MYSQL_TB_FCTP} SET FG='#{food_group}',Tagnames='#{tagnames_new}',#{fct_set} WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
		mdb( "UPDATE #{$MYSQL_TB_TAG} SET FG='#{food_group}',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='#{public_bit}' WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
		mdb( "UPDATE #{$MYSQL_TB_EXT} SET user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0' WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{code}',user='#{user.name}',Tagnames='#{tagnames_new}',#{fct_set};", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{code}',SID='',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',user='#{user.name}',public='#{public_bit}';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{code}', user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0';", false, @debug )
	end
end

puts html

puts '\(^q^)/' if @debug
