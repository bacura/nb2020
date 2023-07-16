#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 Astral body projection 0.00b (2023/07/15)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

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
		'yuid' 	=> "幽体ID",\
		'yupw'=> "幽体パスワード",\
		'enable'	=> "幽体アカウントを有効にする"
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


#### Getting POST data
command = @cgi['command']
astral_sw = @cgi['astral_sw'].to_i
if @debug
	puts "command:#{command}<br>\n"
	puts "astral_sw:#{astral_sw}<br>\n"
	puts "<hr>\n"
end

db = Db.new( user, false )

yuid = ''
yupw = ''
if command == 'change'
	if astral_sw == 1
		yuid = "#{user.name}~"
		yupw = SecureRandom.alphanumeric( 16 )
		db.query( "INSERT INTO #{$MYSQL_TB_USER} SET user='#{yuid}', pass='#{yupw}', status=7, language='#{user.language}';", true, false )
		db.query( "UPDATE #{$MYSQL_TB_USER} SET astral=1 WHERE user='#{user.name}';", true, false )
	else
		yuid = ''
		yupw = ''
		db.query( "UPDATE #{$MYSQL_TB_USER} SET astral=0 WHERE user='#{user.name}';", true, false )
		db.query( "DELETE FROM #{$MYSQL_TB_USER} WHERE user='#{user.name}~';", true, false )
	end
else
	if user.astral == 1
		r = db.query( "SELECT pass FROM #{$MYSQL_TB_USER} WHERE user='#{user.name}~';", false, false )
		if r.first
			yuid = "#{user.name}~"
			yupw = r.first['pass']
			astral_sw = 1
		end
	end
end

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'></div>
		<div class='col-3'>
			<div class="form-check form-switch">
  				<input class="form-check-input" type="checkbox" id="astral_sw" onchange="changeAstral();" #{$CHECK[astral_sw]}>
				<label class="form-check-label">#{l['enable']}</label>
			</div>
		</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-2'>#{l['yuid']}</div>
		<div class='col-3'>
  			<input type="text" class="form-control form-control-sm" id="yuid" value="#{yuid}" DISABLED>
		</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-2'>#{l['yupw']}</div>
		<div class='col-3'>
		  	<input type="text" class="form-control form-control-sm" id="yupw" value="#{yupw}" DISABLED>
		</div>
	</div>
</div>
HTML

puts html
