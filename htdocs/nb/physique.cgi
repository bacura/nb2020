#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 nutrition physical tools 0.04b (2023/07/06)


#==============================================================================
#STATIC
#==============================================================================
@debug = true
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
		'physique' 	=> "体格管理モジュール",\
		'loss' 	=> "減量チャート",\
		'keep' 	=> "維持チャート",\
		'build' => "増量チャート"
	}

	return l[language]
end


#### line menu
def line( l )
	html = <<-"HTML"
	<span class='badge rounded-pill ppill' onclick="PhysiqueForm( 'weight-loss' )">#{l['loss']}</span>
	<span class='badge rounded-pill ppill' onclick="PhysiqueForm( 'weight-keep' )">#{l['keep']}</span>
	<span class='badge rounded-pill ppill' onclick="PhysiqueForm( 'weight-gain' )">#{l['build']}</span>
HTML

	return html
end


####
def init( l )
	html = "<div align='center'>#{l['physique']}</div>"

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
	require "#{$HTDOCS_PATH}/physique_/mod_#{mod}.rb"
	html = physique_module( @cgi, user )
end
html << "</div>"


puts html
