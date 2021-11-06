#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 nutrition assessment tools 0.01b


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
script = 'ginmi'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### line menu
def line( lp )
	html = <<-"HTML"
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'bmi' )">#{lp[1]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'kaupi' )">#{lp[2]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'laureli' )">#{lp[3]}</span>
	<span class='btn badge rounded-pill bg-light text-light' onclick="ginmiForm( 'obesity' )">#{lp[4]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'energy-ref' )">#{lp[5]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'energy-hn' )">#{lp[6]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'energy-hb' )">#{lp[7]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'energy-ath' )">#{lp[8]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'energy-mets' )">#{lp[9]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'es-height' )">#{lp[10]}</span>
	<span class='btn badge rounded-pill bg-info text-dark' onclick="ginmiForm( 'es-muscle' )">#{lp[11]}</span>
	<span class='btn badge rounded-pill bg-light text-light' onclick="">#{lp[12]}</span>
	<span class='btn badge rounded-pill bg-light text-light' onclick="">#{lp[13]}</span>
	<span class='btn badge rounded-pill bg-light text-light' onclick="">#{lp[14]}</span>
HTML

	return html
end


####
def init( lp )
	puts "<div align='center'>#{lp[15]}</div>"
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
	puts "mod:#{mod}<br>\n"
	puts "<hr>\n"
end


####
html = "<div class='container-fluid'>"
if mod == 'line'
	html = line( lp )
elsif mod == ''
	html = init( lp )
else
	require "#{$HTDOCS_PATH}/ginmi_/mod_#{mod}.rb"
	html = ginmi_module( @cgi, user )
end
html << "</div>"


####
puts html
