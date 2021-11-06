#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser statistics tools 0.01b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require 'fileutils'


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
	mod_list = []
	mod_name_list = []
	Dir.glob('toker_/*.rb') do |mod|
		detect_mod = ''
		detect_mod = mod.sub( 'toker_/mod_', '' ).sub( '.rb', '' )
		detect_mod_name = ''
		open( "#{$HTDOCS_PATH}/#{mod}" ) do |file|
			detect_mod_name = file.readlines[0].sub( '#', '' )
		end

		if detect_mod != '' && detect_mod_name != ''
 			mod_list << detect_mod
 			mod_name_list <<detect_mod_name
 		end
	end

	html = ''
	mod_list.size.times do |c|
		html << "<span class='badge rounded-pill bg-info text-dark btn' onclick=\"tokerForm( '#{mod_list[c]}' )\">#{mod_name_list[c]}</span>&nbsp;"
	end

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
	html = "<div align='center'>Statistical analysis with R</div>"
else
	require "#{$HTDOCS_PATH}/toker_/mod_#{mod}.rb"
	table_check( mod )
	html = toker_module( @cgi, user, @debug )
end
html << "</div>"


####
puts html
