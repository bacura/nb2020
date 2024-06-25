#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 memory editor 0.0.1 (2024/06/16)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )

#==============================================================================
# LIBRARY
#==============================================================================
require './soul'
require './brain'
require './body'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'delete' 	=> "削除",\
		'category' 	=> "カテゴリー",\
		'key'	=> "ポインタ",\
		'memory'	=> "記憶",\
		'save' 	=> "保存",\
		'camera'	=> "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>",\
		'return'	=> "<img src='bootstrap-dist/icons/signpost-r.svg' style='height:2em; width:2em;'>",\
		'special' 	=> "【行頭特殊記号】　<b>!</b>[文字]:強調、<b>@</b>[文字]:ただし書き（薄カッコ表示）、<b>#</b>[文字]:コメント（非表示）、<b>~</b>[URL]:外部リンク、<b>[]と|</b>[構造]:簡易表",\
		'special2' 	=> "【行内特殊記号】　<b>{{[文字]}}</b>:自動内部リンク",\
		'memory_edit' => "記憶編集:"
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
memory = Memory.new( user )


#### Getting POST data
command = @cgi['command']
mode = @cgi['mode']
code = @cgi['code']
category = @cgi['category']
pointer = @cgi['pointer']
content = @cgi['content']
if @debug
	puts "command:#{command}<br>\n"
	puts "mode:#{mode}<br>\n"
	puts "code:#{code}<br>\n"
	puts "category:#{category}<br>\n"
	puts "pointer:#{pointer}<br>\n"
	puts "content:#{content.size}<br>\n"
	puts "<hr>\n"
end


case command
when 'new'
	puts 'Edit pointer<br>' if @debug
	memory.load_cgi( @cgi )

when 'edit'
	puts 'Edit pointer<br>' if @debug
	memory.load_cgi( @cgi )
	memory.load_db()

when 'save'
	memory.load_cgi( @cgi )
	if memory.code == ''
		code = generate_code( user.name, 'k' ) 
		memory.code = code
	end
	memory.date = @datetime
	memory.save_db()

	exit( 0 )
when 'delete'
	memory.load_cgi( @cgi )
	memory.delete_db()

	exit( 0 )
when 'photo_upload'
	new_photo = Media.new( user )
	new_photo.load_cgi( @cgi )
	new_photo.save_photo( @cgi )
    new_photo.get_series()
    new_photo.save_db()

	memory.load_cgi( @cgi )
	memory.code = @cgi['origin']
	memory.load_db()

when 'photo_mv'
	target_photo = Media.new( user )
	target_photo.load_cgi( @cgi )
    target_photo.get_series()
    target_photo.move_series()

	memory.load_cgi( @cgi )
	memory.code = @cgi['origin']
	memory.load_db()

when 'photo_del'
	target_photo = Media.new( user )
	target_photo.load_cgi( @cgi )
	target_photo.delete_photo( true )
	target_photo.delete_db( true )

	memory.load_cgi( @cgi )
	memory.code = @cgi['origin']
	memory.load_db()
end


puts "select category<br>" if @debug
category_select_html = "<select class='form-select form-select-sm' id='edit_category'>"
category_set = memory.get_categories()
category_set.each do |e|
	category_select_html << "<option value='#{e}' #{$SELECT[e == memory.category]}>#{e}</option>"
end
category_select_html << "</select>"


puts "Photo upload form<br>" if @debug
form_photo = "<form method='post' enctype='multipart/form-data' id='memory_puf'>"
form_photo << '<div class="input-group input-group-sm">'
form_photo << "<label class='input-group-text'>#{l['camera']}</label>"

if code == nil || code == ''
	form_photo << "<input type='file' class='form-control' DISABLED>"
else
	form_photo << "<input type='file' class='form-control' name='photo' onchange=\"photoUpload( '#{memory.code}' )\">"
end
form_photo << '</form></div>'


puts "delete html <br>" if @debug
delete_html = ''
unless memory.code == nil
	delete_html << "<div class='col-8' align='right'><input type='checkbox' id='edit_delete_check'>&nbsp;"
	delete_html << "<button type='button' class='btn btn-danger btn-sm' onclick=\"deleteMemory( '#{memory.code}', '#{mode}', '#{memory.category}' )\">#{l['delete']}</button></div>"
end

puts 'photo frame<br>' if @debug
photo = Media.new( user )
photo.base = "memory"
photo.origin = @cgi['origin']
photo.origin = memory.code if @cgi['origin'] == '' || @cgi['origin'] == nil
photo.get_series()
photo_frame = photo.html_series( '-tn', 100, false )


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{l['memory_edit']}</h5></div>
		<div align='center' class='col joystic_koyomi' onclick='memory_return()'>#{l['return']}</div>	</div>
	<br>

	<div class='row'>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='edit_pointer'>#{l['key']}</label>
				<input type='text' class='form-control' id='edit_pointer' value='#{memory.pointer}'>
			</div>
		</div>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='edit_category'>#{l['category']}</label>
				#{category_select_html}
			</div>
		</div>
		<div class='col-4' align='right'>
			<button type='button' class='btn btn-success btn-sm' onclick="saveMemory( '#{memory.code}', '#{mode}' )">#{l['save']}</button>
		</div>
	</div><br>

	<div class='row'>
		<div class="col" align='right'>#{l['special']}&nbsp;#{l['special2']}</div>
	</div>

	<div class='row'>
		<textarea class='form-control' rows='5' aria-label='content' id='edit_content'>#{memory.content}</textarea>
	</div><br>
	<div class='row'>
		<div class='col-4'>
			#{form_photo}
		</div>
		#{delete_html}
	</div>
	<br>

	<div class='row'>
		#{photo_frame}
	</div> 
</div>
HTML

puts html


#==============================================================================
#FRONT SCRIPT
#==============================================================================
if command == 'new' || command == 'edit'
	js = <<-"JS"
<script type='text/javascript'>
// Save memory
var saveMemory = function( code, mode ){
	const category = document.getElementById( 'edit_category' ).value;
	const pointer = document.getElementById( 'edit_pointer' ).value;
	const content = document.getElementById( 'edit_content' ).value;

	if( pointer != '' ){
		$.post( "memory-edit.cgi", { command:'save', code:code, category:category, pointer:pointer, content:content, mode:mode, depth:2 }, function( data ){
			displayREC();
		});
	}else{
		displayVIDEO( 'Pointer! (>_<)' );
	}
};

// Delete memory
var deleteMemory = function( code, mode, category ){
	if( document.getElementById( 'edit_delete_check' ).checked ){
		$.post( "memory-edit.cgi", { command:'delete', code:code, mode:mode, depth:2 }, function( data ){
			listPointers( category );

			displayREC();
			pullBW();
			dlf = false;
			displayBW();
		});
	}else{
		displayVIDEO( 'Check! (>_<)' );
	}
};

//
var memory_return = function(){
	pullBW();
	dlf = false;
	displayBW();
};

///////////////////////////////////////////////////////////////////////////

var PhotoUpload = function(){
	form_data = new FormData( $( '#memory_puf' )[0] );
	form_data.append( 'command', 'photo_upload' );
	form_data.append( 'origin', '#{memory.code}' );
	form_data.append( 'base', 'memory' );
	form_data.append( 'alt', '#{memory.pointer}' );
	form_data.append( 'secure', '0' );

	$.ajax( "#{script}.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){ $( '#LF' ).html( data ); }
		}
	);
};
var photoMove = function( code, zidx ){
	displayVIDEO( code );

	$.post( "#{script}.cgi", { command:'photo_mv', origin:'#{memory.code}', code:code, zidx:zidx, base:'memory' }, function( data ){ $( '#LF' ).html( data );});
};

var photoDel = function( code ){
	$.post( "#{script}.cgi", { command:'photo_del', origin:'#{memory.code}', code:code, base:'memory' }, function( data ){ $( '#LF' ).html( data );});
};


</script>
JS

	puts js
end