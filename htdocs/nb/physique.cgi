#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 nutrition physical tools 0.05b (2024/02/26)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )
$mod_path = 'physique_'

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'
require './body'

#==============================================================================
#DEFINITION
#==============================================================================

#### Menu no line
def menu( user )
	mods = Dir.glob( "#{$HTDOCS_PATH}/#{$mod_path}/mod_*" )
	mods.map! do |x|
		x = File.basename( x )
		x = x.sub( 'mod_', '' )
		x = x.sub( '.rb', '' )
	end

	html = ''
	mods.each.with_index( 1 ) do |e, i|
		require "#{$HTDOCS_PATH}/#{$mod_path}/mod_#{e}.rb"
		ml = module_lp( user.language )
		html << "<span class='btn badge rounded-pill ppill' onclick='PhysiqueForm( \"#{e}\" )'>#{ml['mod_name']}</span>"
	end

	return html
end


#==============================================================================
# Main
#==============================================================================

user = User.new( @cgi )
user.debug if @debug
db = Db.new( user, @debug, false )


#### Getting POST
mod = @cgi['mod']
html_init( nil ) if @cgi['step'] != 'json'


if @debug
	puts "mod:#{mod}<br>\n"
	puts "<hr>\n"
end


####
html = "<div class='container-fluid'>"
if mod == 'line'
	exlib_plot()
	html = menu( user )
elsif mod == ''
	html =  "<div align='center'>Physique</div>"
else
	require "#{$HTDOCS_PATH}/physique_/mod_#{mod}.rb"
	html = physique_module( @cgi, db )
end
html << "</div>"


puts html
