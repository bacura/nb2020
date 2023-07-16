#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 nutrition mother & child tools 0.00b (2023/07/05)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'momchai' 	=> "母子管理モジュール",\
		'growth' 	=> "成長曲線"
	}

	return l[language]
end


#### line menu
def line( l )
	html = <<-"HTML"
	<div align='center' class='badge rounded-pill bg-info text-dark' onclick="MomChaiForm( 'growth-curve' )">#{l['growth']}</div>
HTML

	return html
end


####
def init( l )
	html = "<div align='center'>#{l['momchai']}</div>"

	return html
end

#==============================================================================
# Main
#==============================================================================

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )


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
	html = line( l )
elsif mod == ''
	html = init( l )
else
	require "#{$HTDOCS_PATH}/momchai_/mod_#{mod}.rb"
	html = momchai_module( @cgi, user, @debug )
end
html << "</div>"


puts html
