#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser statistics tools 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'toker'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


#### Initial screen menu
def init( lp )
	html = <<-"HTML"
	<button class='btn btn-sm btn-outline-info nav_button' onclick="tokerForm( 'test' )">#{lp[1]}</button>
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
	puts "mod:#{mod}<br>\n"
	puts "<hr>\n"
end


####
html = "<div class='container-fluid'>"
if mod == 'line'
	html = init( lp )
elsif mod == ''
	html = 'Statistical analysis with R'
else
	require "#{$HTDOCS_PATH}/toker_/mod_#{mod}.rb"
	table_check( mod )
	html = toker_module( @cgi, user, @debug )
end
html << "</div>"


####
puts html
