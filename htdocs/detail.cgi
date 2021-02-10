#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 detail viewer 0.00

#==============================================================================
# LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
# STATIC
#==============================================================================
@debug = false
script = 'detail'


#==============================================================================
# DEFINITION
#==============================================================================
#### 端数処理の設定
def frct_check( frct_mode )
	frct_mode = 1 if frct_mode == nil
	fs = []
	0.upto( 3 ) do |c|
		if frct_mode.to_i == c
			fs << 'selected'
		else
			fs << ''
		end
	end

	return frct_mode, fs
end


#### 検索インデックスの飛ばし処理
def sid_skip( sid, dir )
	r = []
	c = 0
	until r.first
		if dir == 'fwd'
			sid = sid.to_i + 1
			sid = 1 if sid > 2198
		else
			sid = sid.to_i - 1
			sid = 2198 if sid < 1
		end
		r = mdb( "SELECT FN, SID FROM #{$MYSQL_TB_TAG} WHERE SID='#{sid}';", false, @debug )
		c += 1
		break if c > 10
	end
	food_no = r.first['FN']

	return food_no
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.language( script )


#### GETデータの取得
get_data = get_data()
frct_mode = get_data['frct_mode']
food_weight = CGI.unescape( get_data['food_weight'] ) if get_data['food_weight'] != '' && get_data['food_weight'] != nil
food_no = get_data['food_no']
dir = get_data['dir']
sid = get_data['sid']
sid_flag = true if sid
if @debug
	puts "frct_mode: #{frct_mode}<br>"
	puts "food_weight: #{food_weight}<br>"
	puts "food_no: #{food_no}<br>"
	puts "dir: #{dir}<br>"
	puts "sid: #{sid}<br>"
	puts "<hr>"
end


#### 食品重量の決定
food_weight = BigDecimal( food_weight_check( food_weight ).first )


#### 端数処理の設定
frct_mode, frct_select = frct_check( frct_mode )


#### 検索インデックスの処理
food_no = sid_skip( sid, dir ) if sid


#### 全ての栄養素を取得
fct_opt = Hash.new
r = mdb( "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no}';", false, @debug )
sid = r.first['SID']
food_no = r.first['FN']
@fct_item.each do |e| fct_opt[e] = num_opt( r.first[e], food_weight, frct_mode, @fct_frct[e] ) end


#### 検索キーの生成
search_key = ''
r = mdb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{food_no}';", false, @debug )
food_name = r.first['name']

r = mdb( "SELECT alias FROM #{$MYSQL_TB_DIC} WHERE org_name='#{food_name}';", false, @debug )
r.each do |e| search_key << "#{e['alias']}," end
search_key.chop!


#### 追加ボタンの生成
add_button = ''
add_button = "<spqn onclick=\"addingCB( '#{food_no}', 'detail_weight', '#{food_name}' )\">#{lp[1]}</span>" if user.name


#### 別名リクエストボタンの生成
alias_button = ''
if user.status > 0
	alias_button << '<div class="input-group input-group-sm">'
	alias_button << "<label class='input-group-text' for='alias'>#{lp[3]}</label>"
	alias_button <<	'<input type="text" class="form-control" id="alias">'
	alias_button <<	"<div class='input-group-prepend'><button class='btn btn-outline-primary' type='button' onclick=\"aliasRequest( '#{food_no}' )\">#{lp[4]}</button></div>"
	alias_button << '</div>'
end

energy_html = '<table class="table table-sm table-striped" width="100%">'
for c in 4..7 do energy_html << "<tr><td>#{@fct_name[@fct_item[c]]}</td><td align='right'>#{fct_opt[@fct_item[c]]} #{@fct_unit[@fct_item[c]]}</td></tr>" end
energy_html << '</table>'

pfc_html = '<table class="table table-sm table-striped" width="100%">'
for c in 8..19 do pfc_html << "<tr><td>#{@fct_name[@fct_item[c]]}</td><td align='right'>#{fct_opt[@fct_item[c]]} #{@fct_unit[@fct_item[c]]}</td></tr>" end
pfc_html << '</table>'

mineral_html = '<table class="table table-sm table-striped" width="100%">'
for c in 20..33 do mineral_html << "<tr><td>#{@fct_name[@fct_item[c]]}</td><td align='right'>#{fct_opt[@fct_item[c]]} #{@fct_unit[@fct_item[c]]}</td></tr>" end
mineral_html << '</table>'

vitis_html = '<table class="table table-sm table-striped" width="100%">'
for c in 34..45 do vitis_html << "<tr><td>#{@fct_name[@fct_item[c]]}</td><td align='right'>#{fct_opt[@fct_item[c]]} #{@fct_unit[@fct_item[c]]}</td></tr>" end
vitis_html << '</table>'

vits_html = '<table class="table table-sm table-striped" width="100%">'
for c in 46..55 do vits_html << "<tr><td>#{@fct_name[@fct_item[c]]}</td><td align='right'>#{fct_opt[@fct_item[c]]} #{@fct_unit[@fct_item[c]]}</td></tr>" end
vits_html << '</table>'

etc_html = '<table class="table table-sm table-striped" width="100%">'
for c in 56..57 do etc_html << "<tr><td>#{@fct_name[@fct_item[c]]}</td><td align='right'>#{fct_opt[@fct_item[c]]} #{@fct_unit[@fct_item[c]]}</td></tr>" end
etc_html << '</table>'


#### html部分
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-2" align='center'>
			<span class='h6'>#{lp[5]}：#{food_no}<br>
			<span onclick="detailPage( 'rev', '#{sid}' )">#{lp[7]}</span>
			#{lp[6]}：#{sid}</span>
			<span onclick="detailPage( 'fwd', '#{sid}' )">#{lp[8]}</span>
		</div>
	  	<div class="col-2"><h5>#{food_weight.to_f} g</h5></div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="detail_fraction">#{lp[9]}</label>
				<select class="form-select form-select-sm" id="detail_fraction" onchange="detailWeight( '#{food_no}' )">
					<option value="1"#{frct_select[1]}>#{lp[10]}</option>
					<option value="2"#{frct_select[2]}>#{lp[11]}</option>
					<option value="3"#{frct_select[3]}>#{lp[12]}</option>
				</select>
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="weight">#{lp[13]}</label>
				<input type="number" min='0' class="form-control" id="detail_weight" value="#{food_weight.to_f}" onchange="detailWeight( '#{food_no}' )">
				<button class="btn btn-outline-primary" type="button" onclick="detailWeight( '#{food_no}' )">g</button>
			</div>
		</div>
		<div class="col-1">
		</div>
		<div class="col-1">
			#{add_button}
		</div>
		<div class="col-1">
			<a href='plain-text.cgi?food_no=#{food_no}&food_weight=#{food_weight}&frct_mode=#{frct_mode}' download='detail_#{fct_opt['FN']}.txt'><span>#{lp[14]}</span></a>
		</div>
		<div class="col-1" align='right'>
			<span onclick='detailReturn()'>#{lp[15]}</span>
		</div>
	</div>
</div>
<br>

<div class='container-fluid'>
	<div class="row">
		<div class="col-7"><h5 onclick='detailReturn()'>#{fct_opt['Tagnames']}</h5></div>
	</div>
	<br>

	<div class="container-fluid">
		<div class="row">
			<div class="col">
			#{energy_html}
			<div class='notice'>
				#{lp[17]}<br>
				#{fct_opt['Notice']}
			</div>
			</div>

			<div class="col">
				#{pfc_html}
			</div>

			<div class="col">
				#{mineral_html}
			</div>
		</div>

		<div class="row">
			<div class="col">
				#{vitis_html}
			</div>

			<div class="col">
				#{vits_html}
			</div>

			<div class="col-4">
				#{etc_html}
			</div>
		</div>
	</div>

	<div class="row">
		<div class="col-8">
			#{lp[16]}：#{search_key}
		</div>
		<div class="col-4">
			#{alias_button}
		</div>
	</div>
</div>
HTML
puts html


#### 登録ユーザーで直接参照の場合は履歴に追加
add_his( user.name, food_no ) unless sid_flag || user.status == 0
