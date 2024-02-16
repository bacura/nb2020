#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 media list 0.00b (2024/02/12)


#==============================================================================
#STATIC
#==============================================================================
@debug = true
#script = File.basename( $0, '.cgi' )
page_limit = 50

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
		'alt' 	=> "alt",\
		'origin' 	=> "Origin",\
		'type' 	=> "Type",\
		'date' => "Date",\
		'zidx' => "zidx",\
		'base' => "Base",\
		'yyyy' => "Year",\
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
		html << "<li class='page-item'><span class='page-link' onclick=\"changeMedialist( #{page - 1} )\">#{l['pre']}</span></li>"
	end
	html << "<li class='page-item'><a class='page-link' onclick=\"changeMedialist( 1 )\">1…</a></li>" unless page_start == 1

	page_start.upto( page_end ) do |c|
		active = ''
		active = ' active' if page == c
		html << "<li class='page-item#{active}'><a class='page-link' onclick=\"changeMedialist( #{c} )\">#{c}</a></li>"
	end
	html << "<li class='page-item active'><a class='page-link' onclick=\"changeMedialist( 1 )\">1</a></li>" if page_end == 0

	html << "<li class='page-item'><a class='page-link' onclick=\"changeMedialist( #{page_max} )\">…#{page_max}</a></li>" unless page_end == page_max
	if page == page_max
		html << "<li class='page-item disabled'><span class='page-link'>#{l['next']}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"changeMedialist( #{page + 1} )\">#{l['next']}</span></li>"
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


all_media = Media.new( user )
( item_num, yyyy_min, yyyy_max ) = all_media.count()
bases = all_media.bases()

#### POST
command = @cgi['command']
page = @cgi['page'].to_i
base = @cgi['base'].to_s
type = @cgi['type'].to_s
mode = @cgi['mode'].to_i
mcode = @cgi['mcode'].to_s

media_cfg = Hash.new
r = db.query( "SELECT media FROM cfg WHERE user='#{user.name}';", false )
if r.first
	if r.first['media'] != nil
		media_cfg = JSON.parse( r.first['media'] )
		puts media_cfg if @debug
		page = media_cfg['page'].to_i if page == 0
		base = media_cfg['base'] if base == ''
		type = media_cfg['type'] if type == ''
		mode = media_cfg['mode'] if mode == ''
	end
end
base = 'all' if base == nil || base == ''
puts command, page, base, type, mode, '<hr>' if @debug


case command
when 'delete'
	puts "Deleting FCZ<br>" if @debug
	db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}' AND code='#{fcz_code}';", true )
end


puts "Paging parts + year<br>" if @debug
page_limit = 120 if true

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


puts "year html<br>" if @debug
year_html = ''
year_html << "<option value='all'>All</option>"
yyyy_min.upto( yyyy_max ) do |yyyy|
	year_html << "<option value='#{yyyy}'>#{yyyy}</option>"
end


puts "base html<br>" if @debug
base_html = ''
base_html << "<option value='all'>All</option>"
bases.each do |e| base_html << "<option value='#{e}'>#{e}</option>" end


media_html = ''
if mode == 0
	puts "media list<br>" if @debug
	media_html << '<table class="table table-sm table-hover">'
	media_html << '<thead class="table-light">'
	media_html << '<tr>'
	media_html << "	<td>#{l['media']}</td>"
	media_html << "	<td>#{l['alt']}</td>"
	media_html << "	<td>#{l['origin']}</td>"
	media_html << "	<td>#{l['code']}</td>"
	media_html << "	<td>#{l['date']}</td>"
	media_html << "	<td>#{l['pad']}</td>"
	media_html << '</tr>'
	media_html << '</thead>'

	offset = ( page - 1 ) * page_limit
	offset = 0 if offset < 0
	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' ORDER BY date LIMIT #{offset}, #{page_limit};", false )
	r.each do |e|
		media_html << '<tr style="font-size:medium;">'
		media_html << "<td><img src='#{$PHOTO}/#{e['code']}-tns.jpg'></td>"
		media_html << "<td>#{e['alt']}</td>"
		media_html << "<td>#{e['origin']}</td>"
		media_html << "<td>#{e['code']}</td>"
		media_html << "<td>#{e['date'].strftime( "%Y-%m-%d" )}</td>"
		media_html << "<td>#{l['text']}</td>"
		media_html << "</td>"
		media_html << '</tr>'
	end
	media_html << '</table>'
else
	puts "media tile<br>" if @debug
	offset = ( page - 1 ) * page_limit
	offset = 0 if offset < 0
	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' ORDER BY date LIMIT #{offset}, #{page_limit};", false )
	media_html << '<div class="row">'
	r.each do |e|
		media_html << '<div class="col-1">'
		media_html << "<img src='#{$PHOTO}/#{e['code']}-tns.jpg'><br><br>"
		media_html << "#{e['alt']}"
		media_html << "</div>"
	end
	media_html << '</div>'
end

checkd = [ 'CHECKED', '' ]
checkd = [ '', 'CHECKED' ] if mode == 1



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
				<input class="form-check-input" type="radio" name="mode" id="mode_rb1" onchange="changeMedialist( '#{page}' )" #{checkd[0]}>
				<label class="form-check-label">#{l['list']}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="mode" id="mode_rb2" onchange="changeMedialist( '#{page}' )" #{checkd[1]}>
				<label class="form-check-label">#{l['tile']}</label>
			</div>

		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{l['base']}</label>
				<select class="form-select" id="base" onchange="changeMedialist( '#{page}' )">
					#{base_html}
				</select>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{l['type']}</label>
				<select class="form-select" id="type" onchange="changeMedialist( '#{page}' )">
					<option value="jpg">jpeg</option>
				</select>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{l['yyyy']}</label>
				<select class="form-select" id="media_yyyy" onchange="changeMedialist( '#{page}' )">
					#{year_html}
				</select>
			</div>
		</div>
	</div>
	<br>

	#{media_html}

	<div class='row'>
		<div class='col-7'></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
</div>
HTML

puts html

#### 検索設定の保存
media_ = JSON.generate( { "page" => page, "base" => base, "type" => type, "mode" => mode } )
db.query( "UPDATE #{$MYSQL_TB_CFG} SET media='#{media_}' WHERE user='#{user.name}';", true )
