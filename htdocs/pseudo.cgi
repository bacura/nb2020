#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 pseudo food editer 0.01b

#==============================================================================
# LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
# STATIC
#==============================================================================
script = 'pseudo'
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

fct_opt = Hash.new

#### POSTデータの取得
command = @cgi['command']
food_key = @cgi['food_key']
code = @cgi['code']
food_name = @cgi['food_name']
food_group = @cgi['food_group']
food_weight = @cgi['food_weight']
class1 = @cgi['class1']
class2 = @cgi['class2']
class3 = @cgi['class3']
tag1 = @cgi['tag1']
tag2 = @cgi['tag2']
tag3 = @cgi['tag3']
tag4 = @cgi['tag4']
tag5 = @cgi['tag5']


food_weight_zero = false
food_weight_zero = true if food_weight == '0'
food_weight = 100 if food_weight == nil || food_weight == ''|| food_weight == '0'
food_weight = BigDecimal( food_weight )

code = '' if code == nil
code = '' unless /P|U\d{5}/ =~ code

fg_key, class1_key, class2_key, class3_key, food_name_key = food_key.split( ':' ) if food_key unless nil
food_group = fg_key unless fg_key == nil
food_group_i = food_group.to_i
class1 = class1_key unless class1_key == nil
class2 = class2_key unless class2_key == nil
class3 = class3_key unless class3_key == nil
food_name = food_name_key unless food_name_key == nil

if @debug
	puts "command: #{command}<br>\n"
	puts "code: #{code}<br>\n"
	puts "food_key: #{food_key}<br>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_group: #{food_group}<br>\n"
	puts "food_weight: #{food_weight}<br>\n"
	puts "class1: #{class1}<br>\n"
	puts "class2: #{class2}<br>\n"
	puts "class3: #{class3}<br>\n"
	puts "tag1: #{tag1}<br>\n"
	puts "tag2: #{tag2}<br>\n"
	puts "tag3: #{tag3}<br>\n"
	puts "tag4: #{tag4}<br>\n"
	puts "tag5: #{tag5}<br>\n"
	puts "<hr>\n"
end


#### 成分読み込み
if command == 'init' && code != ''
	r = mdb( "select * from #{$MYSQL_TB_FCTP} WHERE FN='#{code}' AND ( user='#{user.name}' OR user='#{$GM}' );", false, @debug )
	if r.first
		4.upto( 58 ) do |i| fct_opt[@fct_item[i]] = r.first[@fct_item[i]] end
	end
end


#### クラス・タグ読み込み
tag_user = nil
if command == 'init' && code != ''
	r = mdb( "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND ( user='#{user.name}' OR user='#{$GM}' );", false, @debug )
	if r.first
		tag_user = r.first['user']
		class1 = r.first['class1']
		class2 = r.first['class2']
		class3 = r.first['class3']
		tag1 = r.first['tag1']
		tag2 = r.first['tag2']
		tag3 = r.first['tag3']
		tag4 = r.first['tag4']
		tag5 = r.first['tag5']
	end
elsif command == 'save' && code != ''
	r = mdb( "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
	tag_user = r.first['user'] if r.first
end


#### 保存部分
if command == 'save'
	# 廃棄率
	if @cgi['REFUSE'] == '' || @cgi['REFUSE'] == nil
		fct_opt['REFUSE'] = 0
	else
		fct_opt['REFUSE'] = @cgi['REFUSE'].to_i
	end

	# エネルギー補完
	if  @cgi['ENERC_KCAL'].to_f != 0 && @cgi['ENERC'].to_f == 0
		fct_opt['ENERC_KCAL'] = @cgi['ENERC_KCAL']
		fct_opt['ENERC'] = (( @cgi['ENERC_KCAL'].to_i * 4184 ) / 1000 ).to_i
	elsif @cgi['ENERC_KCAL'].to_f == 0 && @cgi['ENERC'].to_f != 0
		fct_opt['ENERC_KCAL'] = ( @cgi['ENERC'] / 4.184 ).to_i
		fct_opt['ENERC'] = @cgi['ENERC']
	elsif @cgi['ENERC_KCAL'].to_f == 0 && @cgi['ENERC'].to_f == 0
		fct_opt['ENERC_KCAL'] = 0
		fct_opt['ENERC'] = 0
	else
		fct_opt['ENERC_KCAL'] = @cgi['ENERC_KCAL']
		fct_opt['ENERC'] = @cgi['ENERC']
	end


	# 重量影響成分
	fct_opt['ENERC_KCAL'] = ( BigDecimal( fct_opt['ENERC_KCAL'].to_s ) / ( food_weight / 100 )).round( @fct_frct[@fct_item[5]] )
	fct_opt['ENERC'] = ( BigDecimal( fct_opt['ENERC'].to_s ) / ( food_weight / 100 )).round( @fct_frct[@fct_item[6]] )
	7.upto( 57 ) do |i|
		if @cgi[@fct_item[i]] == '' || @cgi[@fct_item[i]] == nil || @cgi[@fct_item[i]] == '-'
			fct_opt[@fct_item[i]] = '-'
		else
			fct_opt[@fct_item[i]] = ( BigDecimal( @cgi[@fct_item[i]] ) / ( food_weight / 100 )).round( @fct_frct[@fct_item[i]] )
		end
	end

	# 重量変化率
	if @cgi['WCR'] == '' || @cgi['WCR'] == nil
		fct_opt['WCR'] = '-'
	else
		fct_opt['WCR'] = @cgi['WCR'].to_i
	end

	# 備考
	fct_opt['Notice'] = @cgi['Notice']

	# ゼロ重量戻し
	food_weight = 0 if food_weight_zero

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


	# 擬似食品成分表テーブルに追加
	fct_set = ''
	4.upto( 58 ) do |i| fct_set << "#{@fct_item[i]}='#{fct_opt[@fct_item[i]]}'," end
	fct_set.chop!

	# タグテーブルに追加
	public_bit = 0
	public_bit = 1 if user.status == 9

	# 新規食品番号の合成
	r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}' AND public='2';", false, @debug )
	if r.first && public_bit == 0
		code = r.first['FN']
	elsif r.first && /P/ =~ r.first['FN']
		code = r.first['FN']
	else
		rr = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}');", false, @debug )
		if rr.first
			last_FN = rr.first['FN'][-3,3].to_i
			if public_bit == 1
				@new_FN = "P#{food_group}%#03d" % ( last_FN + 1 )
			else
				@new_FN = "U#{food_group}%#03d" % ( last_FN + 1 )
			end
		else
			if public_bit == 1
				@new_FN = "P#{food_group}001"
			else
				@new_FN = "U#{food_group}001"
			end
		end
	end

	# 食品番号のチェック
	unless code == ''
		r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE user='#{user.name}' AND FN='#{code}';", false, @debug )
	else
		r = []
	end

	if r.first
		# 擬似食品テーブルの更新
		mdb( "UPDATE #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{code}',Tagnames='#{tagnames_new}',#{fct_set} WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )

		# タグテーブルの更新
		mdb( "UPDATE #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{code}',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='#{public_bit}' WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )

		# 拡張タグテーブルに追加
		mdb( "UPDATE #{$MYSQL_TB_EXT} SET FN='#{code}', user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0' WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
	else
		# 擬似食品テーブルに追加
		mdb( "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{@new_FN}',user='#{user.name}',Tagnames='#{tagnames_new}',#{fct_set};", false, @debug )

		# タグテーブルに追加
		mdb( "INSERT INTO #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{@new_FN}',SID='',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',user='#{user.name}',public='#{public_bit}';", false, @debug )

		# 拡張タグテーブルに追加
		mdb( "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{@new_FN}', user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0';", false, @debug )

		code = @new_FN
	end

	food_weight = 100
end


#### 削除部分
if command == 'delete'
	mdb( "UPDATE #{$MYSQL_TB_TAG} SET public='2' WHERE user='#{user.name}' AND FN='#{code}';", false, @debug )
	code = ''
end


#### debug
if @debug
	puts "fct_opt: #{fct_opt}<br>\n"
	puts "<hr>\n"
end


#### food group html
food_group_option = ''
19.times do |c|
	cc = c
	cc = "0#{c}" if c < 10
	if food_group_i == c
		food_group_option << "<option value='#{cc}' SELECTED>#{c}.#{@category[c]}</option>"
	else
		food_group_option << "<option value='#{cc}'>#{c}.#{@category[c]}</option>"
	end
end


#### disable option
disabled_option = ''
disabled_option = 'disabled' if tag_user != user.name && tag_user != nil


#### html_fct_block
html_fct_block1 = '<table class="table-sm table-striped" width="100%">'
4.upto( 7 ) do |i| html_fct_block1 << "<tr><td>#{@fct_name[@fct_item[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{@fct_item[i]}' value=\"#{fct_opt[@fct_item[i]].to_f}\" #{disabled_option}></td><td>#{@fct_unit[@fct_item[i]]}</td></tr>\n" end
html_fct_block1 << '</table>'

html_fct_block2 = '<table class="table-sm table-striped" width="100%">'
8.upto( 19 ) do |i| html_fct_block2 << "<tr><td>#{@fct_name[@fct_item[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{@fct_item[i]}' value=\"#{fct_opt[@fct_item[i]].to_f}\" #{disabled_option}></td><td>#{@fct_unit[@fct_item[i]]}</td></tr>\n" end
html_fct_block2 << '</table>'

html_fct_block3 = '<table class="table-sm table-striped" width="100%">'
20.upto( 33 ) do |i| html_fct_block3 << "<tr><td>#{@fct_name[@fct_item[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{@fct_item[i]}' value=\"#{fct_opt[@fct_item[i]].to_f}\" #{disabled_option}></td><td>#{@fct_unit[@fct_item[i]]}</td></tr>\n" end
html_fct_block3 << '</table>'

html_fct_block4 = '<table class="table-sm table-striped" width="100%">'
34.upto( 45 ) do |i| html_fct_block4 << "<tr><td>#{@fct_name[@fct_item[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{@fct_item[i]}' value=\"#{fct_opt[@fct_item[i]].to_f}\" #{disabled_option}></td><td>#{@fct_unit[@fct_item[i]]}</td></tr>\n" end
html_fct_block4 << '</table>'

html_fct_block5 = '<table class="table-sm table-striped" width="100%">'
46.upto( 55 ) do |i| html_fct_block5 << "<tr><td>#{@fct_name[@fct_item[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{@fct_item[i]}' value=\"#{fct_opt[@fct_item[i]].to_f}\" #{disabled_option}></td><td>#{@fct_unit[@fct_item[i]]}</td></tr>\n" end
html_fct_block5 << '</table>'

html_fct_block6 = '<table class="table-sm table-striped" width="100%">'
56.upto( 57 ) do |i| html_fct_block6 << "<tr><td>#{@fct_name[@fct_item[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{@fct_item[i]}' value=\"#{fct_opt[@fct_item[i]].to_f}\" #{disabled_option}></td><td>#{@fct_unit[@fct_item[i]]}</td></tr>\n" end
html_fct_block6 << '</table>'


#### save button
save_button = ''
save_button = "<button class=\"btn btn-outline-primary btn-sm\" type=\"button\" onclick=\"pseudoSave( '#{code}' )\">#{lp[1]}</button>" if tag_user == user.name || code == ''


#### delete button
delete_button = ''
delete_button = "<button class='btn btn-outline-danger btn-sm' type='button' onclick=\"pseudoDelete( '#{code}' )\">#{lp[2]}</button>" if code != '' && tag_user == user.name


#### html part
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="food_name" placeholder="#{lp[3]}" value="#{food_name}">
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_group">#{lp[4]}</label>
				<select class="form-select" id="food_group">
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_weight">#{lp[5]}</label>
				<input type="text" class="form-control form-control-sm" id="food_weight" placeholder="100" value="#{food_weight.to_f}">&nbsp;g
			</div>

		</div>

		<div class="col-1"></div>

		<div class="col-1">
			#{save_button}
		</div>
	</div>

	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class1" placeholder="class1" value="#{class1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class2" placeholder="class2" value="#{class2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class3" placeholder="class3" value="#{class3}"></div>
	</div>
	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag1" placeholder="tag1" value="#{tag1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag2" placeholder="tag2" value="#{tag2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag3" placeholder="tag3" value="#{tag3}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag4" placeholder="tag4" value="#{tag4}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag5" placeholder="tag5" value="#{tag5}"></div>
		<div class="col-1"></div>
		<div class="col-1">#{delete_button}</div>
	</div>
	<hr>
	<div class="row">
		<div class="col-4">
			#{html_fct_block1}

			<div style='border: solid gray 1px; margin: 0.5em; padding: 0.5em;'>
				備考：<br>
				<textarea rows="6" cols="32" id="Notice" #{disabled_option}>#{fct_opt['Notice']}</textarea>
			</div>
		</div>

		<div class="col-4">
			#{html_fct_block2}
		</div>

		<div class="col-4">
			#{html_fct_block3}
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="col-4">
			#{html_fct_block4}
		</div>

		<div class="col-4">
			#{html_fct_block5}
		</div>

		<div class="col-4">
			#{html_fct_block6}
		</div>
	</div>
</div>

HTML

puts html
