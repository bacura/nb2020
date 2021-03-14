#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 config 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'config'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================
#### 初期画面
def init( lp, user )
	bio = ''
	bio = "<span class='badge rounded-pill bg-info' onclick=\"configForm( 'bio' )\">#{lp[11]}</span>" if user.status >= 2
	koyomiex = ''
	koyomiex = "<span class='badge rounded-pill bg-info' onclick=\"configForm( 'koyomi' )\">#{lp[9]}</span>" if user.status >= 2
	schoolm = ''
	schoolm = "<span class='badge rounded-pill bg-info' onclick=\"configForm( 'school' )\">#{lp[71]}</span>" if user.status >= 5 && user.status != 6

	html = <<-"HTML"
<span class="badge rounded-pill bg-info" onclick="configForm( 'account' )">#{lp[1]}</span>
<span class="badge rounded-pill bg-info" onclick="configForm( 'display' )">#{lp[10]}</span>
<span class="badge rounded-pill bg-info" onclick="configForm( 'palette' )">#{lp[2]}</span>
<span class="badge rounded-pill bg-info" onclick="configForm( 'history' )">#{lp[6]}</span>
<span class="badge rounded-pill bg-info" onclick="configForm( 'sum' )">#{lp[7]}</span>
#{bio}
#{koyomiex}
#{schoolm}
<span class="badge rounded-pill bg-danger" onclick="configForm( 'release' )">#{lp[8]}</span>
HTML

	return html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### Getting POST
mod = @cgi['mod']
if @debug
	puts"mod: #{mod}"
	puts"<hr>"
end


####
html = ''
if mod == ''
	html = init( lp, user )
else
	require "#{$HTDOCS_PATH}/config_/mod_#{mod}.rb"
	html = config_module( @cgi, user, lp )
end


#### 画面表示
puts html
