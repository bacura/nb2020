#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 media list 0.0.0b (2024/05/05)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )
page_limit = 50

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './body'

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
		'secure' => "Secure",\
		'base' => "Base",\
		'yyyy' => "Year",\
		'list' => "<img src='bootstrap-dist/icons/list-task.svg' style='height:1.8em; width:1.8em;'>",\
		'tile' => "<img src='bootstrap-dist/icons/grid-3x3-gap.svg' style='height:1.8em; width:1.8em;'",\
		'datedele' 	=> "起源",\
		'command' => "<img src='bootstrap-dist/icons/command.svg' style='height:1.2em; width:1.2em;'>",\
		'com' => "Command",\
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
item_num = all_media.get_count()
( yyyy_min, yyyy_max ) = all_media.get_yyyy()
bases = all_media.get_bases()


puts 'POST<br>' if @debug
command = @cgi['command']
page = @cgi['page'].to_i
base = @cgi['base'].to_s
type = @cgi['type'].to_s
mode = @cgi['mode'].to_i
mcode = @cgi['mcode'].to_s
yyyy = @cgi['yyyy'].to_i


media_cfg = Hash.new
if command == 'init'
	r = db.query( "SELECT media FROM cfg WHERE user='#{user.name}';", false )
	if r.first
		if r.first['media'] != nil
			media_cfg = JSON.parse( r.first['media'] )
			puts media_cfg if @debug
			page = media_cfg['page'].to_i if page == 0
			base = media_cfg['base'] if base == ''
			type = media_cfg['type'] if type == ''
			mode = media_cfg['mode'].to_i if mode == 0
			yyyy = media_cfg['yyyy'].to_i if yyyy == 0
		end
	end
	puts command, page, base, type, mode, '<hr>' if @debug
end
base = 'all' if base == nil || base == ''


case command
when 'delete'
	puts "Deleting media<br>" if @debug
#	db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}' AND code='#{fcz_code}';", true )

when 'modal_body'
	modal_body = <<-"MB"
	<div class='input-group'>
	<span class="input-group-text" id="alt">#{l['alt']}</span>
	<input type="text" class="form-control" id='alt'>
	</div>
MB

	puts modal_body

	exit
when 'modal_label'
	puts mcode

	exit
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
yyyy_min.upto( yyyy_max ) do |yyyy_|
	year_html << "<option value='#{yyyy_}' #{$SELECT[yyyy == yyyy_]}>#{yyyy_}</option>"
end


puts "base html<br>" if @debug
base_html = ''
base_html << "<option value='all'>All</option>"
bases.each do |e| base_html << "<option value='#{e}' #{$SELECT[e == base]}>#{e}</option>" end


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
	media_html << "	<td>#{l['secure']}</td>"
	media_html << "	<td>#{l['com']}</td>"
	media_html << '</tr>'
	media_html << '</thead>'

	offset = ( page - 1 ) * page_limit
	offset = 0 if offset < 0
	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' ORDER BY date LIMIT #{offset}, #{page_limit};", false )
	r.each do |e|
		media_html << "<tr style='font-size:medium;' oncontextmenu=\"modalTip( '#{e['code']}' )\">"
		if e['secure'] == 1
			media_html << "<td><img src='photo.cgi?iso=Q&code=#{e['code']}&tn=-tns' class='img-thumbnail' onclick=\"modalPhoto( '#{e['code']}' )\"></td>"
		else
			media_html << "<td><img src='#{$PHOTO}/#{e['code']}-tns.jpg'></td>"
		end
		media_html << "<td>#{e['alt']}</td>"
		media_html << "<td>#{e['origin']}</td>"
		media_html << "<td>#{e['code']}</td>"
		media_html << "<td>#{e['date'].strftime( "%Y-%m-%d" )}</td>"
		media_html << "<td>#{e['secure']}</td>"
		media_html << "<td onclick=\"modalTip( '#{e['code']}' )\">#{l['command']}</td>"
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
		media_html << "<div class='col-1' oncontextmenu=\"modalTip( '#{e['code']}' )\">"
		if e['secure'] == 1
			media_html << "<img src='photo.cgi?iso=Q&code=#{e['code']}&tn=-tn' class='img-thumbnail' onclick=\"modalPhoto( '#{e['code']}' )\">"
		else
			media_html << "<img src='#{$PHOTO}/#{e['code']}-tn.jpg'><br><br>"
		end
		media_html << "#{e['alt']}<br>"
		media_html << "<span onclick=\"modalTip( '#{e['code']}' )\">#{l['command']}</span>"
		media_html << "</div>"
	end
	media_html << '</div>'
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
				<input class="form-check-input" type="radio" name="mode" id="mdida_mode1" onchange="changeMedialist( '#{page}' )" #{$CHECK[mode == 0]}>
				<label class="form-check-label">#{l['list']}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="mode" id="media_mode2" onchange="changeMedialist( '#{page}' )" #{$CHECK[mode == 1]}>
				<label class="form-check-label">#{l['tile']}</label>
			</div>

		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{l['base']}</label>
				<select class="form-select" id="media_base" onchange="changeMedialist( '#{page}' )">
					#{base_html}
				</select>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{l['type']}</label>
				<select class="form-select" id="media_type" onchange="changeMedialist( '#{page}' )">
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

#==============================================================================
# POST PROCESS
#==============================================================================

#### 検索設定の保存
media_ = JSON.generate( { "page" => page, "base" => base, "type" => type, "mode" => mode, "yyyy" => yyyy } )
db.query( "UPDATE #{$MYSQL_TB_CFG} SET media='#{media_}' WHERE user='#{user.name}';", true )

#==============================================================================
# FRONT SCRIPT START
#==============================================================================
if command == 'init'
	js = <<-"JS"
<script type='text/javascript'>

// Media list change
 changeMedialist = function( page ){
	const base = document.getElementById( "media_base" ).value;
	const type = document.getElementById( "media_type" ).value;
	const yyyy = document.getElementById( "media_yyyy" ).value;

 	let mode = 0;
 	if( document.getElementById( "media_mode2" ).checked ){ mode = 1; }

	$.post( "media-list.cgi", { command:'change', page:page, base:base, type:type, mode:mode, yyyy:yyyy }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// Modal Tip for media list
var modalTip = function( code ){
	$.post( "#{script}.cgi", { command:'modal_body', mcode:code }, function( data ){
		$( "#modal_tip_body" ).html( data );
		$.post( "#{script}.cgi", { command:'modal_label', mcode:code }, function( data ){
			$( "#modal_tip_label" ).html( data );
			$( '#modal_tip' ).modal( 'show' );
		});
	});
}

</script>

JS

	puts js
end
