#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 nutrition physical tools 0.03b (2022/09/18)


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'physique'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### line menu
def line( lp )
	html = <<-"HTML"
	<span class='badge rounded-pill ppill' onclick="PhysiqueForm( 'weight-loss' )">#{lp[1]}</span>
	<span class='badge rounded-pill ppill' onclick="PhysiqueForm( 'weight-keep' )">#{lp[3]}</span>
	<span class='badge rounded-pill ppill' onclick="PhysiqueForm( 'weight-gain' )">#{lp[4]}</span>
HTML

	return html
end


####
def init( lp )
	html = "<div align='center'>#{lp[2]}</div>"

	return html
end

#==============================================================================
# Main
#==============================================================================

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


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
	html = line( lp )
elsif mod == ''
	html = init( lp )
else
	require "#{$HTDOCS_PATH}/physique_/mod_#{mod}.rb"
	html = physique_module( @cgi, user )
end
html << "</div>"


puts html
