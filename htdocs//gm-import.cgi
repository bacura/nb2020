#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM import 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'gm-import'
@debug = true


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


# POST
command = @cgi['command']
mode = @cgi['mode']
tf_name = @cgi['tf_name']

if @debug
	puts "command: #{command}<br>"
	puts "mode: #{mode}<br>"
	puts "tf_name: #{tf_name}<br>"
	puts "<hr>"
end


case command
when 'init'
	puts 'init<br>' if @debug
	form_html = ''

	form_html << "<form method='post' enctype='multipart/form-data' id='import_form'>"
	form_html << "<div class='row'>"
	form_html << "<div class='col-4'>"
	form_html << '	<div class="input-group input-group-sm">'
	form_html << "		<label class='input-group-text'>#{lp[1]}</label>"
	form_html << "		<input type='file' class='form-control' name='table'>"
	form_html << '	</div>'
	form_html << '</div>'

	form_html << "<div class='col-2'>"
	form_html << '	<div class="form-check form-switch">'
  	form_html << '		<input class="form-check-input" type="checkbox" id="mode">'
  	form_html << "		<label class='form-check-label'>#{lp[2]}</label>"
	form_html << '	</div>'
	form_html << '</div>'

	form_html << "<div class='col-2'>"
  	form_html << "	<button type='button' class='btn btn-sm btn-outline-primary' onclick=\"confirmImport()\">#{lp[3]}</button>"
	form_html << '</div>'

	form_html << '</div>'
	form_html << '</form>'

	puts form_html

when 'confirm'
	puts 'Confirm<br>' if @debug
	data_body = @cgi['table'].read
	file_name = @cgi['table'].original_filename

	if @debug
		puts "#{file_name}<br>"
		puts "#{data_body.size}<br>"
		puts "<hr>"
	end

	puts "Save temporary file<br>" if @debug
	f = open( "#{$TMP_PATH}/#{file_name}", 'w' )
	f.puts data_body
	f.close

	tables = data_body.split( "////\n" )
	tables.each do |e|
		a = e.split( "\n" )
		puts "<h4>Table:#{a[0]}</h4>"
		puts "<h5>Primary key:#{a[1]}</h5>"
		puts "<h5>Secondry key:#{a[2]}</h5>"

		items = a[3].split( "\t" )
		items.each do |ee| puts "#{ee} / " end
	end
	puts "<br><br>"
  	puts "<button type='button' class='btn btn-sm btn-warning' onclick=\"updateImport( '#{file_name}', '#{mode}' )\">#{lp[4]}</button>"

when 'update'
	puts 'DB update<br>' if @debug
	f = open( "#{$TMP_PATH}/#{tf_name}", 'r' )
	data_solid = f.read
	f.close
	tables = data_solid.force_encoding( 'UTF-8' ).split( "////\n" )

	tables.each do |e|
		a = e.split( "\n" )
		table = a[0]
		pk = a[1]
		sk = a[2]
		items = a[3].split( "\t" )

		set_sql = ''
		items.each do |ee|

		end



	end
end

