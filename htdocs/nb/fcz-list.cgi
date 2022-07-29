#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 fcz edit list 0.00b ()


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'



#==============================================================================
#STATIC
#==============================================================================
script = 'fcz-list'
page_limit = 50
@debug = false
reserves = %W( fix freeze recipe )


#==============================================================================
#DEFINITION
#==============================================================================


#### ページングパーツ
def pageing_html( page, page_start, page_end, page_max, lp )
	html = ''
	html << '<ul class="pagination pagination-sm justify-content-end">'
	if page == 1
		html << "<li class='page-item disabled'><span class='page-link'>#{lp[5]}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"baseFCZlist( #{page - 1} )\">#{lp[5]}</span></li>"
	end
	html << "<li class='page-item'><a class='page-link' onclick=\"baseFCZlist( 1 )\">1…</a></li>" unless page_start == 1

	page_start.upto( page_end ) do |c|
		active = ''
		active = ' active' if page == c
		html << "<li class='page-item#{active}'><a class='page-link' onclick=\"fczListP( #{c} )\">#{c}</a></li>"
	end

	html << "<li class='page-item'><a class='page-link' onclick=\"baseFCZlist( #{page_max} )\">…#{page_max}</a></li>" unless page_end == page_max
	if page == page_max
		html << "<li class='page-item disabled'><span class='page-link'>#{lp[6]}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"baseFCZlist( #{page + 1} )\">#{lp[6]}</span></li>"
	end
	html << '  </ul>'

	return html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### POST
command = @cgi['command']
page = @cgi['page'].to_i
base = @cgi['base'].to_s
fcz_code = @cgi['fcz_code'].to_s

fcze_cfg = Hash.new
r = mdb( "SELECT fcze FROM cfg WHERE user='#{user.name}';", false, @debug )
if r.first
	fcze_cfg = JSON.parse( r.first['fcze'] )
	puts fcze_cfg if @debug
	page = fcze_cfg['page'].to_i if page == 0
	base = fcze_cfg['base'] if base == ''
end
base = 'general' if base == nil || base == ''
puts command, base, page, '<hr>' if @debug


protect_flag = false
reserves.each do |e|
	protect_flag = true if e == base
end


case command
when 'delete'
	puts "Deleting FCZ<br>" if @debug
	mdb( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}' AND code='#{fcz_code}';", false, @debug )
end


puts "Paging parts<br>" if @debug
r = mdb( "SELECT COUNT(code) FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}';", false, @debug )
fcz_num = r.first['COUNT(code)']

page_max = fcz_num / page_limit + 1
page_start = 1
page_end = page_max
if page_end > 5
	if page > 3
		page_start = page - 3
		page_start = page_max - 6 if page_max - page_start < 7
	end
	if page_end - page < 3
		page_end = page_max
	else
		page_end = page + 3
		page_end = 7 if page_end < 7
	end
else
	page_end = page_max
end
html_paging = pageing_html( page, page_start, page_end, page_max, lp )


puts "Base select parts<br>" if @debug
base_select = "<SELECT class='form-select form-select-sm' id='base_select' onchange=\"baseFCZlist( #{page} )\">"
r = mdb( "SELECT DISTINCT base FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}';", false, @debug )
base_select << "<OPTION value='general'>general</OPTION>"
r.each do |e|
	s = ''
	s = 'SELECTED' if e['base'] == base
	base_select << "<OPTION value='#{e['base']}' #{s}>#{e['base']}</OPTION>"
end
base_select << '</SELECT>'


puts "FCZ list<br>" if @debug
fcz_html = ''
offset = ( page - 1 ) * page_limit
r = mdb( "SELECT code, origin, base, name FROM #{$MYSQL_TB_FCZ} WHERE base='#{base}' ORDER BY name LIMIT #{offset}, #{page_limit};", false, @debug )
r.each do |e|
	fcz_html << '<tr style="font-size:medium;">'
	fcz_html << "<td>#{e['code']}</td>"
	fcz_html << "<td>#{e['name']}</td>"
	fcz_html << "<td>#{e['origin']}</td>"
	fcz_html << "<td><span onclick=\"initFCZedit( '#{e['code']}' )\">#{lp[8]}</span></td>"
	fcz_html << "<td>"
	unless protect_flag
		fcz_html << "<td><input class='form-check-input' type='checkbox' id='#{e['code']}'>"
		fcz_html << "&nbsp;<span onclick=\"deleteFCZlist( '#{e['code']}', '#{page}' )\">#{lp[9]}</span></td>"
	end
	fcz_html << "</td>"
	fcz_html << '</tr>'
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-7'><h5>#{base} (#{fcz_num})</h5></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
	<br>


	<div class='row'>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">Base</label>
				#{base_select}
			</div>
			</div>
		<div class='col-3'><button class="btn btn-outline-primary btn-sm" type="button" onclick="initFCZedit( 'new' )">#{lp[7]}</button></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead class='cb_header'>
		<tr>
			<td>#{lp[1]}</td>
			<td>#{lp[2]}</td>
			<td>#{lp[3]}</td>
			<td>#{lp[4]}</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
	</thead>

		#{fcz_html}
	</table>

	<div class='row'>
		<div class='col-7'></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
</div>
HTML

puts html

#### 検索設定の保存
fcze_ = JSON.generate( { "page" => page, "base" => base } )
mdb( "UPDATE #{$MYSQL_TB_CFG} SET fcze='#{fcze_}' WHERE user='#{user.name}';", false, @debug )
