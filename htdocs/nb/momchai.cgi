#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 nutrition mother & child tools 0.10b (2024/07/06)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )
@mod_path = 'momchai_'

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'
require './body'

#==============================================================================
#DEFINITION
#==============================================================================

#### Menu on line
def menu( user )
	mods = Dir.glob( "#{$HTDOCS_PATH}/#{@mod_path}/mod_*" )
	mods.map! do |x|
		x = File.basename( x )
		x = x.sub( 'mod_', '' )
		x = x.sub( '.rb', '' )
	end

	html = ''
	mods.each.with_index( 1 ) do |e, i|
		require "#{$HTDOCS_PATH}/#{@mod_path}/mod_#{e}.rb"
		ml = module_lp( user.language )
		html << "<span class='btn badge rounded-pill ppill' onclick='MomChaiForm( \"#{e}\" )'>#{ml['mod_name']}</span>&nbsp;"
	end

	return html
end

#==============================================================================
# Main
#==============================================================================
user = User.new( @cgi )
db = Db.new( user, @debug, false )


#### Getting POST
mod = @cgi['mod']
html_init( nil ) if @cgi['step'] != 'json'

if @debug
	user.debug
	puts "mod:#{mod}<br>\n"
	puts "<hr>\n"
end


#### Driver
html = ''
if mod == 'menu'
	puts 'MENU<br>' if @debug
	unless user.status == 7
		html = menu( user )
	else
		html = "<span class='ref_error'>[ginmi]Astral user limit!</span><br>"
	end
else
	if mod == ''
		html =  "<div align='center'>Mother and child assessment tools</div>"
	else
		require "#{$HTDOCS_PATH}/#{@mod_path}/mod_#{mod}.rb"
		html = momchai_module( @cgi, db ) unless user.status == 7
	end
end
puts 'HTML<br>' if @debug
puts html

#==============================================================================
#FRONT SCRIPT
#==============================================================================
if mod == ''
	js = <<-"JS"
<script type='text/javascript'>

var MomChaiForm = function( mod ){
	$.post( "#{script}.cgi", { mod:mod, step:'form' }, function( data ){
		$( "#L1" ).html( data );

		$.post( "#{script}.cgi", { mod:mod, step:'results' }, function( data ){
			$( "#L2" ).html( data );
		});

		dl2 = true;
		displayBW();
	});
};

</script>
JS

	puts js 
end