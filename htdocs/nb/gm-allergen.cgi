#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM allergen editor 0.00b (2022/11/19)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-allergen'


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require "./language_/#{script}.lp"


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### POST
command = @cgi['command']
allergen = @cgi['allergen']
code = @cgi['code']
code.gsub!( /\s/, ',' ) unless code == ''
code.gsub!( '　', ',' ) unless code == ''
code.gsub!( '、', ',' ) unless code == ''
if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"
	puts "allergen:#{allergen}<br>\n"
	puts "<hr>\n"
end

case command
when 'on'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mdb( "UPDATE #{$MYSQL_TB_EXT} SET allergen='#{allergen}' WHERE FN='#{e}';", false, @debug )
		end
	end
when 'off'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mdb( "UPDATE #{$MYSQL_TB_EXT} SET allergen='0' WHERE FN='#{e}';", false, @debug )
		end
	end
end

food_name = ''
unless code == ''
	r = mdb( "SELECT name from #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false, @debug )
	food_name = r.first['name'] if r.first
end

list_html = ''
r = mdb( "SELECT t1.*, t2.allergen FROM #{$MYSQL_TB_TAG} AS t1 INNER JOIN #{$MYSQL_TB_EXT} AS t2 ON t1.fn = t2.fn WHERE t2.allergen>='1';", false, @debug )
r.each do |e|
	list_html << "<tr>"
	list_html << "<td>#{e['FN']}</td>"
	list_html << "<td>#{e['name']}・#{e['tag1']} #{e['tag2']} #{e['tag3']} #{e['tag4']} #{e['tag5']}</td>"
	case e['allergen'].to_i
	when 1
		list_html << "<td align='center'>#{l['check']}</td><td></td><td></td>"
	when 2
		list_html << "<td></td><td align='center'>#{l['check']}</td><td></td>"
	when 3
		list_html << "<td></td><td></td><td align='right'></td>"
	end
	list_html << "<td><span onclick=\"offAllergen( '#{e['FN']}' )\">#{l['trash']}</span></td>"
	list_html << '</tr>'
end
list_html << '<tr><td>no item listed.</td></tr>' if list_html == ''

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{l['allergen']}: #{food_name}</h5></div>
	</div>
	<div class='row'>
		<div class='col-9'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="weight">#{l['fn']}</label>
				<input type="text" class="form-control" id="code" value="#{code}">
			</div>
		</div>
		<div class='col-3' align='right'>
			<div class="form-check form-check-inline">
  				<input class="form-check-input" type="radio" name="level" id="ag_class1" CHECKED>
				<label class="form-check-label" for="inlineRadio1">#{l['obligate']}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="level" id="ag_class2">
				<label class="form-check-label" for="inlineRadio2">#{l['recommend']}</label>
			</div>
		</div>
	</div>
	<br>

	<div class='row'>
		<button class="btn btn-sm btn-info" type="button" onclick="onAllergen()">#{l['regist']}</button>
	</div>
	<br>

	<table class='table table-sm table-striped'>
		<thead>
			<td>#{l['fn']}</td>
			<td>#{l['name']}</td>
			<td align='center'>#{l['obligate']}</td>
			<td align='center'>#{l['recommend']}</td>
			<td align='center'>#{l['others']}</td>
		</thead>

		#{list_html}
	</table>
HTML

puts html
