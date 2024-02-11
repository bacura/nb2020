#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 media list 0.00b (2024/02/06)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )
page_limit = 50
reserves = %W( general reference fix freeze recipe )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'code' 	=> "Code",\
		'mcode' 	=> "mcode",\
		'cap' 	=> "Caption",\
		'origin' 	=> "Origin",\
		'type' 	=> "Type",\
		'date' => "Date",\
		'zidx' => "zidx",\
		'base' => "Base",\
		'list' => "<img src='bootstrap-dist/icons/list-task.svg' style='height:1.8em; width:1.8em;'>",\
		'tile' => "<img src='bootstrap-dist/icons/grid-3x3-gap.svg' style='height:1.8em; width:1.8em;'",\

		'datedele' 	=> "起源",\
		'pad' 		=> "<img src='bootstrap-dist/icons/dpad.svg' style='height:1.8em; width:1.2em;'>&nbsp;操作",\
		'pre' 		=> "前項",\
		'next' 		=> "次項",\
		'text'		=> "<img src='bootstrap-dist/icons/filetype-txt.svg' style='height:1.8em; width:1.2em;'>",\
		'trash'		=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.8em; width:1.2em;'>",\
		'cp2words'	=> "<img src='bootstrap-dist/icons/eyedropper.svg' style='height:1.2em; width:1.2em;'>"


	}

	return l[language]
end

#### ページングパーツ
def pageing_html( page, page_start, page_end, page_max, l )
	html = ''
	html << '<ul class="pagination pagination-sm justify-content-end">'
	if page == 1
		html << "<li class='page-item disabled'><span class='page-link'>#{l['pre']}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"baseFCZlist( #{page - 1} )\">#{l['pre']}</span></li>"
	end
	html << "<li class='page-item'><a class='page-link' onclick=\"baseFCZlist( 1 )\">1…</a></li>" unless page_start == 1

	page_start.upto( page_end ) do |c|
		active = ''
		active = ' active' if page == c
		html << "<li class='page-item#{active}'><a class='page-link' onclick=\"fczListP( #{c} )\">#{c}</a></li>"
	end
	html << "<li class='page-item active'><a class='page-link' onclick=\"fczListP( 1 )\">1</a></li>" if page_end == 0

	html << "<li class='page-item'><a class='page-link' onclick=\"baseFCZlist( #{page_max} )\">…#{page_max}</a></li>" unless page_end == page_max
	if page == page_max
		html << "<li class='page-item disabled'><span class='page-link'>#{l['next']}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"baseFCZlist( #{page + 1} )\">#{l['next']}</span></li>"
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
l = language_pack( user.language )
db = Db.new( user, @debug, false )


#### POST
command = @cgi['command']
page = @cgi['page'].to_i
base = @cgi['base'].to_s
type = @cgi['type'].to_s
mode = @cgi['type'].to_i
mcode = @cgi['mcode'].to_s

media_cfg = Hash.new
r = db.query( "SELECT media FROM cfg WHERE user='#{user.name}';", false )
if r.first
	if r.first['media'] != nil
		media_cfg = JSON.parse( r.first['media'] )
		puts media_cfg if @debug
		page = media_cfg['page'].to_i if page == 0
		base = media_cfg['base'] if base == ''
	end
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
	db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}' AND code='#{fcz_code}';", true )
end


puts "Paging parts<br>" if @debug
r = db.query( "SELECT COUNT(mcode) FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}';", false )
item_num = r.first['COUNT(mcode)']

page_max = item_num / page_limit
page_start = 1
page_max += 1 if ( item_num % page_limit ) != 0
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
html_paging = pageing_html( page, page_start, page_end, page_max, l )


puts "base html<br>" if @debug
base_html = ''
base_html << "<option value='all'>All</option>"
r = db.query( "SELECT DISTINCT base FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}';", false )
r.each do |e|
	base_html << "<option value='#{e['base']}'>#{e['base']}</option>"
end


puts "media list<br>" if @debug
media_html = ''
offset = ( page - 1 ) * page_limit
offset = 0 if offset < 0
r = db.query( "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' ORDER BY date LIMIT #{offset}, #{page_limit};", false )
r.each do |e|
	media_html << '<tr style="font-size:medium;">'
	media_html << "<td><img src='#{$PHOTO}/#{e['mcode']}-tns.jpg'></td>"
	media_html << "<td>#{e['caption']}</td>"
	media_html << "<td>#{e['origin']}</td>"
	media_html << "<td>#{e['code']}</td>"
	media_html << "<td>#{e['date'].strftime( "%Y-%m-%d" )}</td>"
	media_html << "<td>#{l['text']}</td>"
	unless protect_flag
		media_html << "<td><input class='form-check-input' type='checkbox' id='#{e['code']}'>"
		media_html << "&nbsp;<span onclick=\"deleteFCZlist( '#{e['code']}', '#{page}' )\">#{l['trash']}</span></td>"
	end
	media_html << "</td>"
	media_html << '</tr>'
end


puts "HTML<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-7'><h5>#{base} (#{item_num})</h5></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-2'>

			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1">
				<label class="form-check-label" for="inlineRadio1">#{l['list']}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="option2">
				<label class="form-check-label" for="inlineRadio2">#{l['tile']}</label>
			</div>

		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{l['base']}</label>
				<select class="form-select" id="base">
					#{base_html}
				</select>
			</div>
		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{l['type']}</label>
				<select class="form-select" id="type">
					<option value="jpg">jpeg</option>
				</select>
			</div>
		</div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead class='table-light'>
		<tr>
			<td>#{l['media']}</td>
			<td>#{l['cap']}</td>
			<td>#{l['origin']}</td>
			<td>#{l['code']}</td>
			<td>#{l['date']}</td>
			<td>#{l['pad']}</td>
		</tr>
	</thead>

		#{media_html}
	</table>

	<div class='row'>
		<div class='col-7'></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
</div>
HTML

puts html

#### 検索設定の保存
#media_ = JSON.generate( { "page" => page, "base" => base } )
#db.query( "UPDATE #{$MYSQL_TB_CFG} SET media='#{fcze_}' WHERE user='#{user.name}';", true )
