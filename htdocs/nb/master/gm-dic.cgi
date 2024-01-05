#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM food alias dictionary editor 0.33b (2023/07/17)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require '../soul'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'fg' 	=> "食品群",\
		'fn' 	=> "食品名",\
		'alias' => "別名",\
		'linkno' => "リンク食品番号",\
		'fg00' 	=> "特・その他",\
		'fg01' 	=> "穀",\
		'fg02' 	=> "芋",\
		'fg03' 	=> "甘",\
		'fg04' 	=> "豆",\
		'fg05' 	=> "種",\
		'fg06' 	=> "菜",\
		'fg07' 	=> "果",\
		'fg08' 	=> "茸",\
		'fg09' 	=> "藻",\
		'fg10' 	=> "魚",\
		'fg11' 	=> "肉",\
		'fg12' 	=> "卵",\
		'fg13' 	=> "乳",\
		'fg14' 	=> "油",\
		'fg15' 	=> "菓",\
		'fg16' 	=> "飲",\
		'fg17' 	=> "調",\
		'fg18' 	=> "調",\
		'dic_edit' => "辞書エディタ"
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
db = Db.new( user, @debug, false )


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### POST
command = @cgi['command']
sg = @cgi['sg']
sg = '01' if command == 'init'
org_name = @cgi['org_name'].to_s
aliases = @cgi['aliases'].to_s
dfn = @cgi['dfn'].to_s
if @debug
	puts "command:#{command}<br>\n"
	puts "sg:#{sg}<br>\n"
	puts "org_name:#{org_name}<br>\n"
	puts "aliases:#{aliases}<br>\n"
	puts "dfn:#{dfn}<br>\n"
	puts "<hr>\n"
end

list_html = ''
case command
when 'menu'
	html_sub = <<-"HTML_SUB"
<span class="badge rounded-pill bg-info text-dark" id="category1" onclick="changeDic( '01' )">#{l['fg01']}</span>
<span class="badge rounded-pill bg-info text-dark" id="category2" onclick="changeDic( '02' )">#{l['fg02']}</span>
<span class="badge rounded-pill bg-info text-dark" id="category3" onclick="changeDic( '03' )">#{l['fg03']}</span>
<span class="badge rounded-pill bg-danger" id="category4" onclick="changeDic( '04' )">#{l['fg04']}</span>
<span class="badge rounded-pill bg-warning text-dark" id="category5" onclick="changeDic( '05' )">#{l['fg05']}</span>
<span class="badge rounded-pill bg-success" id="category6" onclick="changeDic( '06' )">#{l['fg06']}</span>
<span class="badge rounded-pill bg-info text-dark" id="category7" onclick="changeDic( '07' )">#{l['fg07']}</span>
<span class="badge rounded-pill bg-success" id="category8" onclick="changeDic( '08' )">#{l['fg08']}</span>
<span class="badge rounded-pill bg-success" id="category9" onclick="changeDic( '09' )">#{l['fg09']}</span>
<span class="badge rounded-pill bg-danger" id="category10" onclick="changeDic( '10' )">#{l['fg10']}</span>
<span class="badge rounded-pill bg-danger" id="category11" onclick="changeDic( '11' )">#{l['fg11']}</span>
<span class="badge rounded-pill bg-danger" id="category12" onclick="changeDic( '12' )">#{l['fg12']}</span>
<span class="badge rounded-pill bg-light text-dark" id="category13" onclick="changeDic( '13' )">#{l['fg13']}</span>
<span class="badge rounded-pill bg-warning text-dark" id="category14" onclick="changeDic( '14' )">#{l['fg14']}</span>
<span class="badge rounded-pill bg-secondary" id="category15" onclick="changeDic( '15' )">#{l['fg15']}</span>
<span class="badge rounded-pill bg-primary" id="category16" onclick="changeDic( '16' )">#{l['fg16']}</span>
<span class="badge rounded-pill bg-light text-dark" id="category17" onclick="changeDic( '17' )">#{l['fg17']}</span>
<span class="badge rounded-pill bg-secondary" id="category18" onclick="changeDic( '18' )">#{l['fg18']}</span>
<span class="badge rounded-pill bg-light text-dark" id="category0" onclick="changeDic( '00' )">#{l['fg00']}</span>
HTML_SUB
	puts html_sub
	exit

when 'update', 'new'
	aliases.gsub!( "\s", ',' )
	aliases.gsub!( '　', ',' )
	aliases.gsub!( '、', ',' )
	aliases.gsub!( '，', ',' )
	aliases.gsub!( ',,', ',' )
	a = aliases.split( ',' )
	a.uniq!

	db.query( "DELETE FROM #{$MYSQL_TB_DIC} WHERE org_name='#{org_name}' AND FG ='#{sg}' AND ( def_fn='#{dfn}' OR def_fn='' OR def_fn IS NULL);", true )
	a.each do |e|
		db.query( "INSERT INTO #{$MYSQL_TB_DIC} SET alias='#{e}', org_name='#{org_name}', def_fn='#{dfn}', FG ='#{sg}', user='#{user.name}';", true )
	end

	exit
else
	r = db.query( "SELECT DISTINCT org_name, def_fn FROM #{$MYSQL_TB_DIC} WHERE FG ='#{sg}' ORDER BY org_name ASC;", false )
	r.each do |e|
		list_html << "<div class='row'>"
		list_html << "<div class='col-2'>"
		list_html << "#{e['org_name']}"
		list_html << '</div>'
		list_html << "<div class='col-9'>"

		alias_value = ''
		def_fn = ''
		rr = db.query( "SELECT DISTINCT * from #{$MYSQL_TB_DIC} WHERE org_name='#{e['org_name']}' AND FG ='#{sg}' AND ( def_fn='#{e['def_fn']}' OR def_fn='' OR def_fn IS NULL);", false )
		rr.each do |ee|
			alias_value << "#{ee['alias']},"
			def_fn = ee['def_fn']
		end
		alias_value.chop!

		list_html << "<input type='text' class='form-control' id=\'#{e['org_name']}' value='#{alias_value}' onchange=\"saveDic( '#{e['org_name']}', '#{sg}' )\">"
		list_html << '</div>'
		list_html << "<div class='col-1'>"
		list_html << "<input type='text' class='form-control' id=\'dfn_#{e['org_name']}' value='#{def_fn}' onchange=\"saveDic( '#{e['org_name']}', '#{sg}' )\">"
		list_html << '</div>'
		list_html << '</div>'
	end
end


select_html = "<select id='new_fg' class='form-control'>"
1.upto( 18 ) do |c|

	fg = c
	fg = "0#{fg}" if c < 10
	s = ''
	s = 'SELECTED' if fg.to_s == sg
	select_html << "<option value='#{fg}' #{s}>#{@category[c]}</option>"
end
select_html << "<option value='00'>#{@category[0]}</option>"
select_html << '</select>'

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{l['dic_edit']}: </h5></div>
	</div>
	<br>
	<div class='row'>
		<div class='col-2'>
			<div class="input-group input-group-sm">
				<span class="input-group-text">#{l['fg']}</span>
				#{select_html}
			</div>
		</div>

		<div class='col-3'>
			<div class="input-group input-group-sm">
				<span class="input-group-text">#{l['fn']}</span>
				<input type='text' id='new_org_name' value='#{org_name}' class='form-control'>
			</div>
		</div>

		<div class='col-3'>
			<div class="input-group input-group-sm">
				<span class="input-group-text">#{l['alias']}</span>
				<input type='text' id='new_alias' class='form-control'>
			</div>
		</div>

		<div class='col-3'>
			<div class="input-group input-group-sm">
				<span class="input-group-text">#{l['linkno']}</span>
				<input type='text' id='dic_def_fn' value='#{dfn}' class='form-control'>
			</div>
		</div>

		<div class='col-1'><button type='button' class='btn btn-outline-primary btn-sm btn-sm' onclick="newDic()">追加</button></div>
	</div>
	<br>
	#{list_html}
HTML

puts html
