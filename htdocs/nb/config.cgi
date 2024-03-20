#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 config 0.31b (2024/03/20)


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
require './body'

#==============================================================================
#DEFINITION
#==============================================================================

#### Menu no line
def menu( user )
	mods = Dir.glob( "#{$HTDOCS_PATH}/config_/mod_*" )
	mods.map! do |x|
		x = File.basename( x )
		x = x.sub( 'mod_', '' )
		x = x.sub( '.rb', '' )
	end
	mods.delete( 'release' )
	mods.push( 'release' )

	html = ''
	mods.each.with_index( 1 ) do |e, i|
		require "#{$HTDOCS_PATH}/config_/mod_#{e}.rb"
		ml = module_lp( user.language )
		bclass = 'ppill'
		bclass = 'bg-danger' if i == mods.size
		html << "<span class='btn badge rounded-pill #{bclass}' onclick='configForm( \"#{e}\" )'>#{ml['mod_name']}</span>"
	end

	return html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
db = Db.new( user, @debug, false )

#### Getting POST
mod = @cgi['mod']


#### Driver
html = ''
if mod == 'menu'
	puts 'MENU<br>' if @debug
	unless user.status == 7
		html = menu( user )
	else
		html = "<span class='ref_error'>[config]Astral user limit!</span><br>"
	end
else
	if mod == ''
		html =  "<div align='center'>Config</div>"
	else
		require "#{$HTDOCS_PATH}/config_/mod_#{mod}.rb"

		puts "MOD (#{mod})<br>" if @debug
		html = config_module( @cgi, db ) unless user.status == 7
	end
end


puts 'HTML<br>' if @debug
puts html
