#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 config 0.21b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


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
	bio = "<span class='badge rounded-pill bg-info text-dark' onclick=\"configForm( 'bio' )\">#{lp[11]}</span>" if user.status >= 2
	koyomiex = ''
	koyomiex = "<span class='badge rounded-pill bg-info text-dark' onclick=\"configForm( 'koyomi' )\">#{lp[9]}</span>" if user.status >= 2

	html = <<-"HTML"
<span class="btn badge rounded-pill bg-info text-dark" onclick="configForm( 'account' )">#{lp[1]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="configForm( 'display' )">#{lp[10]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="configForm( 'palette' )">#{lp[2]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="configForm( 'history' )">#{lp[6]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="configForm( 'sum' )">#{lp[7]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="configForm( 'convert' )">#{lp[72]}</span>
#{bio}
#{koyomiex}

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


#### Driver
html = ''
if mod == ''
	puts 'INIT<br>' if @debug
	html = init( lp, user )
else
	require "#{$HTDOCS_PATH}/config_/mod_#{mod}.rb"

	puts "MOD (#{mod})<br>" if @debug
	html = config_module( @cgi, user, lp )
end


puts 'HTML<br>' if @debug
puts html
