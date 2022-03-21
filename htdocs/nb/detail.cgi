#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 detail viewer 0.10b

#==============================================================================
# LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
# STATIC
#==============================================================================
@debug = false
script = 'detail'


#==============================================================================
# DEFINITION
#==============================================================================
#### 検索インデックスの飛ばし処理
def sid_skip( sid, dir )
	r = []
	c = 0
	until r.first
		if dir == 'fwd'
			sid = sid.to_i + 1
			sid = 1 if sid > 2481
		else
			sid = sid.to_i - 1
			sid = 2481 if sid < 1
		end
		r = mdb( "SELECT FN, SID FROM #{$MYSQL_TB_TAG} WHERE SID='#{sid}';", false, @debug )
		c += 1
		break if c > 100
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
lp = user.load_lp( script )


puts 'POST<br>' if @debug
frct_mode = @cgi['frct_mode']
food_weight = @cgi['food_weight']
food_no = @cgi['food_no']
dir = @cgi['dir']
sid = @cgi['sid']
sid_flag = true if sid
selectu = @cgi['selectu'].to_s
if @debug
	puts "frct_mode: #{frct_mode}<br>"
	puts "food_weight: #{food_weight}<br>"
	puts "food_no: #{food_no}<br>"
	puts "dir: #{dir}<br>"
	puts "sid: #{sid}<br>"
	puts "selectu: #{selectu}<br>"
	puts "<hr>"
end


puts 'Unit process<br>' if @debug
unit_set = []
unit_select = []
selectu = 'g' if selectu == ''
uk = BigDecimal( '1' )
r = mdb( "SELECT unit FROM #{$MYSQL_TB_EXT} WHERE FN='#{food_no}';", false, @debug )
if r.first
	unith = JSON.parse( r.first['unit'] )
	unith.each do |k, v|
		unit_set << k
		if k == selectu
			unit_select << 'SELECTED'
			uk = BigDecimal( v.to_s )
		else
			unit_select << ''
		end
	end
end


puts 'Weight process<br>' if @debug
food_volume = BigDecimal( food_weight_check( food_weight ).first )
food_weight = food_volume * uk
frct_select = selected( 0, 3, frct_mode )


puts 'Search index<br>' if @debug
food_no = sid_skip( sid, dir ) if sid != ''


puts 'Load FCT<br>' if @debug
fct_opt = Hash.new
r = mdb( "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no}';", false, @debug )
sid = r.first['SID']
food_no = r.first['FN']
@fct_item.each do |e| fct_opt[e] = num_opt( r.first[e], food_weight, frct_mode, @fct_frct[e] ) end


puts 'Aliase process<br>' if @debug
search_key = ''
r = mdb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{food_no}';", false, @debug )
food_name = r.first['name']

r = mdb( "SELECT alias FROM #{$MYSQL_TB_DIC} WHERE org_name='#{food_name}';", false, @debug )
r.each do |e| search_key << "#{e['alias']}," end
search_key.chop!

alias_button = ''
if user.status > 0
	alias_button << '<div class="input-group input-group-sm">'
	alias_button << "<label class='input-group-text' for='alias'>#{lp[3]}</label>"
	alias_button <<	'<input type="text" class="form-control" id="alias">'
	alias_button <<	"<div class='input-group-prepend'><button class='btn btn-outline-primary' type='button' onclick=\"aliasRequest( '#{food_no}' )\">#{lp[4]}</button></div>"
	alias_button << '</div>'
end


puts 'Add button<br>' if @debug
add_button = ''
add_button = "<spqn onclick=\"addingCB( '#{food_no}', 'detail_weight', '#{food_name}' )\">#{lp[1]}</span>" if user.name


puts 'FCT table HTML<br>' if @debug
energy_html = '<table class="table table-sm table-striped" width="100%">'
energy_html << "<tr>"
@fct_rew.each do |e| energy_html << "<tr><td>#{@fct_name[e]}</td><td align='right'>#{fct_opt[e]} #{@fct_unit[e]}</td></tr>" end
energy_html << '</table>'

pf_html = '<table class="table table-sm table-striped" width="100%">'
@fct_pf.each do |e| pf_html << "<tr><td>#{@fct_name[e]}</td><td align='right'>#{fct_opt[e]} #{@fct_unit[e]}</td></tr>" end
pf_html << '</table>'

cho_html = '<table class="table table-sm table-striped" width="100%">'
@fct_cho.each do |e| cho_html << "<tr><td>#{@fct_name[e]}</td><td align='right'>#{fct_opt[e]} #{@fct_unit[e]}</td></tr>" end
cho_html << '</table>'

mineral_html = '<table class="table table-sm table-striped" width="100%">'
@fct_m.each do |e| mineral_html << "<tr><td>#{@fct_name[e]}</td><td align='right'>#{fct_opt[e]} #{@fct_unit[e]}</td></tr>" end
mineral_html << '</table>'

fsv_html = '<table class="table table-sm table-striped" width="100%">'
@fct_fsv.each do |e| fsv_html << "<tr><td>#{@fct_name[e]}</td><td align='right'>#{fct_opt[e]} #{@fct_unit[e]}</td></tr>" end
fsv_html << '</table>'

wsv_html = '<table class="table table-sm table-striped" width="100%">'
@fct_wsv.each do |e| wsv_html << "<tr><td>#{@fct_name[e]}</td><td align='right'>#{fct_opt[e]} #{@fct_unit[e]}</td></tr>" end
wsv_html << "<tr><td></td><td></td></tr>"
@fct_as.each do |e| wsv_html << "<tr><td>#{@fct_name[e]}</td><td align='right'>#{fct_opt[e]} #{@fct_unit[e]}</td></tr>" end
wsv_html << '</table>'


puts 'Volume input HTML<br>' if @debug
volume_html = ''
volume_html << "<div class='input-group input-group-sm'>"
volume_html << "	<label class='input-group-text'>#{lp[13]}</label>"
volume_html << "	<input type='text' id='detail_volume' value='#{food_volume.to_f}' class='form-control' onchange=\"detailWeight( '#{food_no}' )\">"
volume_html << "	<select id='detail_unit' class='form-select form-select-sm' onchange=\"detailWeight( '#{food_no}' )\">"
unit_set.size.times do |c| volume_html << "<option value='#{unit_set[c]}' #{unit_select[c]}>#{unit_set[c]}</option>" end
volume_html << "	</select>"
volume_html << "</div>"


puts 'Fract input HTML<br>' if @debug
fract_html = ''
fract_html << '<div class="input-group input-group-sm">'
fract_html << "	<label class='input-group-text'>#{lp[9]}</label>"
fract_html << "	<select class='form-select form-select-sm' id='detail_fraction' onchange=\"detailWeight( '#{food_no}' )\">"
fract_html << "		<option value='1' #{frct_select[1]}>#{lp[10]}</option>"
fract_html << "		<option value='2' #{frct_select[2]}>#{lp[11]}</option>"
fract_html << "		<option value='3' #{frct_select[3]}>#{lp[12]}</option>"
fract_html << '	</select>'
fract_html << '</div>'


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-2">
			<span class='h6'>#{lp[5]}：#{food_no}</span><br>
			<span onclick="detailPage( 'rev', '#{sid}' )">#{lp[7]}</span>
			#{lp[6]}：#{sid}</span>
			<span onclick="detailPage( 'fwd', '#{sid}' )">#{lp[8]}</span>
		</div>
		<div class="col"><h5>#{fct_opt['Tagnames']}</h5></div>
	  	<div class="col"><h5>#{food_volume.to_f} #{selectu}&nbsp;(#{food_weight.to_f} g)</h5></div>
		<div align='center' class='col joystic_koyomi' onclick="detailReturn()">#{lp[15]}</div>

	  </div>
	</div>
	<br>
	<div class="row">
		<div class="col">
			#{volume_html}
		</div>
		<div class="col">
			#{fract_html}
		</div>
		<div class="col" align="right">
			#{add_button}
		</div>
		<div class="col" align="right">
			<a href='plain-text.cgi?food_no=#{food_no}&food_weight=#{food_weight}&frct_mode=#{frct_mode}&lg=#{user.language}' download='detail_#{fct_opt['FN']}.txt'><span>#{lp[14]}</span></a>
		</div>
	</div>
</div>
<br>

<div class='container-fluid'>
	<div class="row">
		<div class="col">
		#{energy_html}
		<div class='notice'>
			#{lp[17]}<br>
			#{fct_opt['Notice']}
		</div>
		</div>

		<div class="col">
			#{pf_html}
		</div>

		<div class="col">
			#{cho_html}
		</div>
	</div>

	<div class="row">
		<div class="col">
			#{mineral_html}
		</div>

		<div class="col">
			#{fsv_html}
		</div>

		<div class="col-4">
			#{wsv_html}
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
HTML
puts html


#### 登録ユーザーで直接参照の場合は履歴に追加
add_his( user.name, food_no ) unless sid_flag || user.status == 0
