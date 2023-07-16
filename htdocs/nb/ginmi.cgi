#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 nutrition assessment tools 0.02b (2023/07/08)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )

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
		'gimmi'	=> "アセスメント",\
		'bmi'	=> "BMI",\
		'kaupi'	=> "カウプ指数",\
		'laureli'	=> "ローレル指数",\
		'obesity'	=> "肥満度",\
		'energy-ref'	=> "E・参照",\
		'energy-hn'	=> "E・国立健栄",\
		'energy-hb'	=> "E・ハリベネ",\
		'energy-ath'	=> "E・アスリート",\
		'energy-mets'	=> "E・METs",\
		'es-height'	=> "推定身長",\
		'es-muscle'	=> "上腕筋面積",\
		'koyomi'	=> "MNA",\
		'koyomi'	=> "MNA-SF",\
		'koyomi'	=> "SGA"
	}

	return l[language]
end


#### line menu
def line( l )
	html = <<-"HTML"
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'bmi' )">#{l['bmi']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'kaupi' )">#{l['kaupi']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'laureli' )">#{l['laureli']}</span>
	<span class='btn badge rounded-pill bg-light text-light' onclick="ginmiForm( 'obesity' )">#{l['obesity']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'energy-ref' )">#{l['energy-ref']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'energy-hn' )">#{l['energy-hn']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'energy-hb' )">#{l['energy-hb']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'energy-ath' )">#{l['energy-ath']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'energy-mets' )">#{l['energy-mets']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'es-height' )">#{l['es-height']}</span>
	<span class='btn badge rounded-pill ppill' onclick="ginmiForm( 'es-muscle' )">#{l['es-muscle']}</span>
HTML

	return html
end

####
def init( l )
	puts "<div align='center'>#{l['gimmi']}</div>"
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )


#### Getting POST
mod = @cgi['mod']
if @debug
	puts "mod:#{mod}<br>\n"
	puts "<hr>\n"
end


####
html = "<div class='container-fluid'>"
if mod == 'line'
	html = line( l )
elsif mod == ''
	html = init( l )
else
	require "#{$HTDOCS_PATH}/ginmi_/mod_#{mod}.rb"
	html = ginmi_module( @cgi, user )
end
html << "</div>"


####
puts html
