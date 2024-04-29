#! /usr/bin/ruby
#encoding: utf-8
#Nutritoin browser note bridge 0.00b (2024/04/28)


#==============================================================================
# STATIC
#==============================================================================
@debug = true
script = File.basename( $0, '.cgi' )


#==============================================================================
# LIBRARY
#==============================================================================
require './soul'
require './body'

#==============================================================================
# DEFINITION
#==============================================================================

def koyomi( db, code, origin )
	note = ''

	return note
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
db = Db.new( user, @debug, false )


#### Getting POST
command = @cgi['command']
base = @cgi['base']
code = @cgi['code']
origin = @cgi['origin']

case base
when 'koyomi'
	note = koyomi( db, code, origin )
else
	exit
end

p note

aliasm = ''
if user.mid != nil
	r = db.query( "SELECT aliasu from #{$MYSQL_TB_USER} WHERE user='#{user.mom}';", false )
	if r.first
		aliasm = r.first['aliasu']
		aliasm = user.mom if aliasm == '' || aliasm == nil
	end
end

case command
when 'write'
	note_code = generate_code( user.name, 'n' )
	p @datetime, note_code, aliasm,note if @debug
	db.query( "INSERT INTO #{$MYSQL_TB_NOTE} SET code='#{note_code}', user='#{user.name}', aliasm='#{aliasm}', note='#{note}', datetime='#{@datetime}';", true )

when 'photo_upload'
	puts 'photo_upload' if @debug
	note_code = generate_code( user.name, 'n' )
	new_photo = Media.new( user )
	new_photo.load_cgi( @cgi )
	new_photo.origin = note_code
	new_photo.save_photo( @cgi )
	new_photo.save_db()

	db.query( "INSERT INTO #{$MYSQL_TB_NOTE} SET code='#{note_code}', media='#{new_photo.code}', user='#{user.name}', aliasm='#{aliasm}', note='', datetime='#{@datetime}';", true )
end

#==============================================================================
#FRONT SCRIPT
#==============================================================================

js = <<-"JS"
<script type='text/javascript'>

var PhotoUpload = function(){
	var now = new Date();
    var yyyy = now.getFullYear();
    var mm = now.getMonth() + 1;
    var dd = now.getDate();
    var hh = now.getHours();
    var m60 = now.getMinutes();
    var s60 = now.getSeconds();
    var origin = yyyy + "-" +  mm + "-" + dd + "-" + hh + "-" + m60 + "-" + s60

	form_data = new FormData( $( '#note_puf' )[0] );
	form_data.append( 'command', 'photo_upload' );
	form_data.append( 'origin', '' );
	form_data.append( 'base', 'note' );
	form_data.append( 'alt', 'Photo' );
	form_data.append( 'secure', '1' );

	$.ajax( "#{script}.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){ $( '#L1' ).html( data ); }
		}
	);
};

</script>
JS
