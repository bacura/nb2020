#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 fcz edit list 0.1.0 (2024/05/20)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )
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
		'fczcode' 	=> "FCZ code",\
		'name' 		=> "名前",\
		'origin' 	=> "起源",\
		'pre' 		=> "前項",\
		'next' 		=> "次項",\
		'new' 		=> "新規作成",\
		'com' 		=> "コマンド",\
		'save'		=> "テキスト保存",\
		'pick'		=> "コードピック",\
		'command' 	=> "<img src='bootstrap-dist/icons/command.svg' style='height:1.2em; width:1.2em;'>",\
		'text'		=> "<img src='bootstrap-dist/icons/filetype-txt.svg' style='height:2.4em; width:2.4em;'>",\
		'delete'	=> "削除（要チェック）",\
		'trash'		=> "<img src='bootstrap-dist/icons/trash-red.svg' style='height:2.4em; width:2.4em;'>",\
		'cp2words'	=> "<img src='bootstrap-dist/icons/eyedropper.svg' style='height:2.4em; width:2.4em;'>"
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
fcz_code = @cgi['fcz_code'].to_s


fcze_cfg = Hash.new
r = db.query( "SELECT fcze FROM cfg WHERE user='#{user.name}';", false )
if r.first
	if r.first['fcze'] != nil
		fcze_cfg = JSON.parse( r.first['fcze'] )
		puts fcze_cfg if @debug
		page = fcze_cfg['page'].to_i if page == 0
		base = fcze_cfg['base'] if base == ''
	end
end
base = 'general' if base == nil || base == ''
puts command, base, page, '<hr>' if @debug


case command
when 'delete'
	puts "Deleting FCZ<br>" if @debug
	db.query( "DELETE FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}' AND code='#{fcz_code}';", true )

when 'modal_body'
	modal_body = <<-"MB"
	<table class='table table-borderless'><tr>
	<td align='center' onclick=\"cp2words( '#{fcz_code}', '' )\">#{l['cp2words']}<br><br>#{l['pick']}</td>
	<td align='center'  onclick=\"cp2words( '#{fcz_code}', '' )\">#{l['text']}<br><br>#{l['save']}</td>
	<td align='center' ><input class='form-check-input' type='checkbox' id='#{fcz_code}'>
	<span onclick=\"deleteFCZlist( '#{fcz_code}', '#{page}' )\">#{l['trash']}</span><br><br>#{l['delete']}</td>
	</tr></table>
MB

	puts modal_body
	exit
when 'modal_label'
	r = db.query( "SELECT name FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND code='#{fcz_code}';", false )
	puts r.first['name'] if r.first

	exit
end


puts "Paging parts<br>" if @debug
r = db.query( "SELECT COUNT(code) FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}';", false )
item_num = r.first['COUNT(code)']

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


puts "Base select parts<br>" if @debug
base_select = "<SELECT class='form-select form-select-sm' id='base_select' onchange=\"baseFCZlist( #{page} )\">"
r = db.query( "SELECT DISTINCT base FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}';", false )
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
offset = 0 if offset < 0
r = db.query( "SELECT code, origin, base, name FROM #{$MYSQL_TB_FCZ} WHERE base='#{base}' ORDER BY name LIMIT #{offset}, #{page_limit};", false )
r.each do |e|
	fcz_html << "<tr style='font-size:medium;' oncontextmenu=\"modalTip( '#{e['code']}' )\">"
	fcz_html << "<td onclick=\"initFCZedit( '#{e['code']}' )\">#{e['name']}</td>"
	fcz_html << "<td onclick=\"initFCZedit( '#{e['code']}' )\">#{e['code']}</td>"
	fcz_html << "<td>#{e['origin']}</td>"
	fcz_html << "<td onclick=\"modalTip( '#{e['code']}' )\">#{l['command']}</td>"
	fcz_html << '</tr>'
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
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">Base</label>
				#{base_select}
			</div>
			</div>
		<div class='col-3'><button class="btn btn-outline-primary btn-sm" type="button" onclick="initFCZedit( 'new' )">#{l['new']}</button></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead class='table-light'>
		<tr>
			<td>#{l['name']}</td>
			<td>#{l['fczcode']}</td>
			<td>#{l['origin']}</td>
			<td>#{l['com']}</td>
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

#==============================================================================
# POST PROCESS
#==============================================================================

#### save config
fcze_ = JSON.generate( { "page" => page, "base" => base } )
db.query( "UPDATE #{$MYSQL_TB_CFG} SET fcze='#{fcze_}' WHERE user='#{user.name}';", true )

#==============================================================================
# FRONT SCRIPT START
#==============================================================================
if command == 'init'
js = <<-"JS"
<script type='text/javascript'>

// FCZ list change
var baseFCZlist = function( page ){
	const base = document.getElementById( "base_select" ).value;
	$.post( "#{script}.cgi", { command:'init', base:base, page:page }, function( data ){ $( "#L1" ).html( data ); });
};

// FCZ list delete
var deleteFCZlist = function( fcz_code, page ){
	const base = document.getElementById( "base_select" ).value;
	if( document.getElementById( fcz_code ).checked ){
		$.post( "#{script}.cgi", { command:'delete', base:base, page:page, fcz_code:fcz_code }, function( data ){ $( "#L1" ).html( data ); });
		$( '#modal_tip' ).modal( 'hide' );
	}else{
		displayVIDEO( 'Check!(>_<)' );
	}
};

// Modal Tip for fcz list
var modalTip = function( fcz_code ){
	$.post( "#{script}.cgi", { command:'modal_body', fcz_code:fcz_code }, function( data ){
		$( "#modal_tip_body" ).html( data );
		$.post( "#{script}.cgi", { command:'modal_label', fcz_code:fcz_code }, function( data ){
			$( "#modal_tip_label" ).html( data );
			$( '#modal_tip' ).modal( 'show' );
		});
	});
}

</script>
JS

	puts js
end

puts '(^q^)' if @debug
