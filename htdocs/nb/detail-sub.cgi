#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 food detail sub 0.00b (2023/4/23)


#==============================================================================
# STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
# LIBRARY
#==============================================================================
require './soul'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'search' 	=> "レシピ検索",\
		'fract' 	=> "端数",\
		'round'		=> "四捨五入",\
		'ceil' 		=> "切り上げ",\
		'floor'		=> "切り捨て",\
		'weight' 	=> "重量",\
		'fn' 		=> "食品番号",\
		'name' 		=> "食品名",\
		'change'	=> "<img src='bootstrap-dist/icons/hammer.svg' style='height:1.2em; width:1.2em;'>",\
		'cboard' 	=> "<img src='bootstrap-dist/icons/card-text.svg' style='height:1.2em; width:1.2em;'>",\
		'calendar'	=> "<img src='bootstrap-dist/icons/calendar-plus.svg' style='height:1.2em; width:1.2em;'>",\
		'unit' 		=> "単",\
		'color' 	=> "色",\
		'shun' 		=> "旬",\
		'dic' 		=> "辞",\
		'allergen' 	=> "ア",\
		'plus' 		=> "<img src='bootstrap-dist/icons/plus-square-fill.svg' style='height:2em; width:2em;'>",\
		'signpost'	=> "<img src='bootstrap-dist/icons/signpost.svg' style='height:2em; width:2em;'>"
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


#### POST
command = @cgi['command']
food_key = @cgi['food_key']
frct_mode = @cgi['frct_mode'].to_i
food_weight = @cgi['food_weight']
food_no = @cgi['food_no']
base = @cgi['base']
base_fn = @cgi['base_fn']
if @debug
	puts "food_key: #{food_key}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "food_weight: #{food_weight}<br>"
	puts "food_no: #{food_no}<br>"
	puts "base: #{base}<br>"
	puts "base_fn: #{base_fn}<br>"
	puts "<hr>"
end


puts 'Key chain<br>' if @debug
food_key = '' if food_key == nil
fg_key, class1, class2, class3, food_name = food_key.split( ':' )

class_name = ''
class_no = 0
unless class1 == nil || class1 == ''
	class_name = class1
	class_no = 1
end
unless class2 == nil || class2 == ''
	class_name = class2
	class_no = 2
end
unless class3 == nil || class3 == ''
	class_name = class3
	class_no = 3
end
if @debug
	puts "fg_key: #{fg_key}<br>"
	puts "class1: #{class1}<br>"
	puts "class2: #{class2}<br>"
	puts "class3: #{class3}<br>"
	puts "class_no: #{class_no}<br>"
	puts "class_name: #{class_name}<br>"
	puts "<hr>"
end


#### 閲覧選択
html = ''
pseudo_button = ''


case command
when 'init', 'weight'
	puts 'L5 final page<br>' if @debug
	require './brain'

	food_weight = BigDecimal( food_weight_check( food_weight ).first )
	frct_select = selected( 0, 2, frct_mode )

	query = ''
	food_no_list = []
	food_name_list = []
	tag1_list = []
	tag2_list = []
	tag3_list = []
	tag4_list = []
	tag5_list = []
	r = Hash.new

	#### 補助クラスネームの追加処理
	if /\+/ =~ class_name
		class_add = "<span class='tagc'>#{class_name.sub( '+', '' )}</span> "
	else
		class_add = ''
	end


	# 正規食品
	if class_no.to_i == 0
		r = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND name='#{food_name}' AND public='9';", false, @debug )
	else
		r = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND name='#{food_name}' AND public='9';", false, @debug )
	end
	if r.first
		r.each do |e|
			food_no_list << e['FN']
			food_name_list << e['name']
			tag1_list << e['tag1']
			tag2_list << e['tag2']
			tag3_list << e['tag3']
			tag4_list << e['tag4']
			tag5_list << e['tag5']
		end
	end


	# 擬似食品
	if class_no.to_i == 0
		query = "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND name='#{food_name}' AND (( user='#{user.name}' AND public='0' ) OR public='1');"
	else
		query = "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND name='#{food_name}' AND (( user='#{user.name}' AND public='0' ) OR public='1');"
	end
	puts "#{query}<br>" if @debug
	r = mdb( query, false, @debug )
	if r.first
		r.each do |e|
			food_no_list << e['FN']
			food_name_list << e['name']
			tag1_list << e['tag1']
			tag2_list << e['tag2']
			tag3_list << e['tag3']
			tag4_list << e['tag4']
			tag5_list << e['tag5']
		end
	end

 	# 簡易表示の項目
 	fc_items = []
	fc_items_html = ''

	r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}' AND name='簡易表示用';", false, @debug )
	if r.first
		palette = r.first['palette']
		palette.size.times do |c|
			fc_items << @fct_item[c] if palette[c] == '1'
		end
	else
		$PALETTE_DEFAULT[user.language][0].size.times do |c|
			fc_items << @fct_item[c] if $PALETTE_DEFAULT[user.language][0][c] == '1'
		end
	end
	fc_items.each do |e| fc_items_html << "<th align='right'>#{@fct_name[e]}</th>" end


	# 食品ラインの生成
	food_html = ''
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
	food_no_list.size.times do |c|
		pseudo_flag = false
		# 栄養素の一部を取得
		if /U/ =~ food_no_list[c]
			query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{food_no_list[c]}' AND user='#{user.name}';"
			pseudo_flag = true
		elsif /P|C/ =~ food_no_list[c]
			query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{food_no_list[c]}';"
			pseudo_flag = true
		else
			query = "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no_list[c]}';"
		end
		p query if @debug

		res = db.query( query )
		unless res.first
			puts "<span class='error'>[FCTP load]ERROR!!<br>"
			puts "code:#{food_no_list[c]}</span><br>"
			db.query( "DELETE FROM #{$MYSQL_TB_TAG} WHERE FN='#{food_no_list[c]}' AND user='#{user.name}';" )
			db.query( "DELETE FROM #{$MYSQL_TB_EXT} WHERE FN='#{food_no_list[c]}' AND user='#{user.name}';" )
			exit()
		end

		sub_components = ''
		fc_items.each do |e|
			if res.first[e] != nil
				t = num_opt( res.first[e], food_weight, frct_mode, @fct_frct[e] )
				sub_components << "<td align='center'>#{t}</td>"
			else
				sub_components << "<td align='center'><span class='error'>[FCTP load]ERROR!!</td>"
			end
		end

		# 追加・変更ボタン
		if user.name && base == 'cb'
			add_button = "<span onclick=\"changingCB( '#{food_no_list[c]}', '#{base_fn}' )\">#{l['change']}</span>"
		elsif user.name
			add_button = "<span onclick=\"addingCB( '#{food_no_list[c]}', 'weight', '#{food_name}' )\">#{l['cboard']}</span>"
		else
			add_button = ""
		end

		# Koyomi button
		if user.status >= 2 && base != 'cb'
			koyomi_button = "<span onclick=\"addKoyomi( '#{food_no_list[c]}', -5 )\">#{l['calendar']}</span>"
		else
			koyomi_button = ''
		end

		# GM/SGM専用単位変換ボタン
		gm_unitc = ''
		gm_color = ''
		gm_allergen = ''
		gm_shun = ''
		gm_dic = ''

		if user.status >= 8
			res = mdb( "SELECT * FROM #{$MYSQL_TB_EXT} WHERE FN='#{food_no_list[c]}';", false, @debug )
			if res.first
				bc = 'btn-outline-secondary'
				bc = 'btn-outline-danger' if res.first['unit'] != '{"g":1}';
				gm_unitc = "<button type='button' class='btn #{bc} btn-sm' onclick=\"directUnit( '#{food_no_list[c]}' )\">#{l['unit']}</button>"

#				gm_color = "<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"directColor( '#{food_no_list[c]}' )\">#{l['color']}</button>"

				bc = 'btn-outline-secondary'
				bc = 'btn-outline-danger' if res.first['allergen'].to_i > 0;
				gm_allergen = "<button type='button' class='btn btn #{bc} btn-sm' onclick=\"directAllergen( '#{food_no_list[c]}' )\">#{l['allergen']}</button>"

				bc = 'btn-outline-danger'
				bc = 'btn-outline-secondary' if res.first['shun1s'] == 0 || res.first['shun1s'] == ''|| res.first['shun1s'] == nil;
				gm_shun = "<button type='button' class='btn #{bc} btn-sm' onclick=\"directShun( '#{food_no_list[c]}' )\">#{l['shun']}</button>"

				gm_dic = "<button type='button' class='btn btn-outline-info btn-sm' onclick=\"initDic( 'direct', '#{fg_key}', '#{food_name}', '#{food_no_list[c]}' )\">#{l['dic']}</button>"
			end
		end

		tags = "<span class='tag1'>#{tag1_list[c]}</span> <span class='tag2'>#{tag2_list[c]}</span> <span class='tag3'>#{tag3_list[c]}</span> <span class='tag4'>#{tag4_list[c]}</span> <span class='tag5'>#{tag5_list[c]}</span>"
		if pseudo_flag
			food_html << "<tr class='fct_value'><td>#{food_no_list[c]}</td><td class='link_cursor' onclick=\"pseudoAdd( 'init', '#{fg_key}:#{class1}:#{class2}:#{class3}:#{food_name}', '#{food_no_list[c]}' )\">#{class_add}#{food_name_list[c]} #{tags}</td><td>#{add_button}&nbsp;#{koyomi_button}&nbsp;&nbsp;#{gm_unitc}&nbsp;#{gm_allergen}&nbsp;#{gm_shun}&nbsp;#{gm_dic}</td>#{sub_components}</tr>\n"
		else
			food_html << "<tr class='fct_value'><td>#{food_no_list[c]}</td><td class='link_cursor' onclick=\"detailView( '#{food_no_list[c]}' )\">#{class_add}#{food_name_list[c]} #{tags}</td><td>#{add_button}&nbsp;#{koyomi_button}&nbsp;&nbsp;#{gm_unitc}&nbsp;#{gm_allergen}&nbsp;#{gm_shun}&nbsp;#{gm_dic}</td>#{sub_components}</tr>\n"
		end
	end
	db.close

	# 擬似食品ボタンの作成
 	pseudo_button = "<apan onclick=\"pseudoAdd( 'init', '#{fg_key}:#{class1}:#{class2}:#{class3}:#{food_name}', '' )\">#{l['plus']}</span>\n" if user.status > 0

 	# Recipe search badge
 	recipe_search = "&nbsp;&nbsp;<span class='badge bbg' onclick=\"searchDR( '#{food_name}' )\">#{l['search']}</span><br><br>"

 	#
	return_button = ''
	return_button = "<div align='center' class='joystic_koyomi' onclick=\"returnCB( '', '' )\">#{l['signpost']}</div><br>" if base == 'cb'


	html = <<-"HTML"
	<div class='container-fluid'>#{return_button}<div class="row">
  		<div class="col-3"><span class='h5'>#{food_name}</span>#{recipe_search}</div>
  		<div class="col-3"><h5>#{food_weight.to_f} g</h5></div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="fraction">#{l['fract']}</label>
				<select class="form-select" id="fraction" onchange="changeDSWeight( 'weight', '#{food_key}', '#{food_no}' )">
					<option value="1"#{frct_select[1]}>#{l['round']}</option>
					<option value="2"#{frct_select[2]}>#{l['ceil']}</option>
					<option value="3"#{frct_select[3]}>#{l['floor']}</option>
				</select>
			</div>
		</div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="weight">#{l['weight']}</label>
				<input type="number" min='0' class="form-control" id="weight" value="#{food_weight.to_f}">
				<button class="btn btn-outline-primary" type="button" onclick="changeDSWeight( 'weight', '#{food_key}', '#{food_no}' )">g</button>
			</div>
		</div>
	</div></div>
	<br>

	<table class="table table-sm table-hover">
		<thead>
			<tr>
	  			<th>#{l['fn']}</th>
	  			<th>#{l['name']}</th>
				<th></th>
				#{fc_items_html}
    		</tr>
  		</thead>

		#{food_html}
	</table>
	#{pseudo_button}
HTML

end

puts html
