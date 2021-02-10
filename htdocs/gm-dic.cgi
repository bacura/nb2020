#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM food alias dictionary editor 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-dic'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.language( script )


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### POST
command = @cgi['command']
sg = @cgi['sg']
sg = '01' if command == 'init'
org_name = @cgi['org_name']
aliases = @cgi['aliases']
if @debug
	puts "command:#{command}<br>\n"
	puts "sg:#{sg}<br>\n"
	puts "org_name:#{org_name}<br>\n"
	puts "aliases:#{aliases}<br>\n"
	puts "<hr>\n"
end

list_html = ''
case command
when 'menu'
	html_sub = <<-"HTML_SUB"
<span class="badge rounded-pill bg-info text-dark" id="category1" onclick="changeDic( '01' )">#{lp[2]}</span>
<span class="badge rounded-pill bg-info text-dark" id="category2" onclick="changeDic( '02' )">#{lp[3]}</span>
<span class="badge rounded-pill bg-info text-dark" id="category3" onclick="changeDic( '03' )">#{lp[4]}</span>
<span class="badge rounded-pill bg-danger" id="category4" onclick="changeDic( '04' )">#{lp[5]}</span>
<span class="badge rounded-pill bg-warning text-dark" id="category5" onclick="changeDic( '05' )">#{lp[6]}</span>
<span class="badge rounded-pill bg-success" id="category6" onclick="changeDic( '06' )">#{lp[7]}</span>
<span class="badge rounded-pill bg-info text-dark" id="category7" onclick="changeDic( '07' )">#{lp[8]}</span>
<span class="badge rounded-pill bg-success" id="category8" onclick="changeDic( '08' )">#{lp[9]}</span>
<span class="badge rounded-pill bg-success" id="category9" onclick="changeDic( '09' )">#{lp[10]}</span>
<span class="badge rounded-pill bg-danger" id="category10" onclick="changeDic( '10' )">#{lp[11]}</span>
<span class="badge rounded-pill bg-danger" id="category11" onclick="changeDic( '11' )">#{lp[12]}</span>
<span class="badge rounded-pill bg-danger" id="category12" onclick="changeDic( '12' )">#{lp[13]}</span>
<span class="badge rounded-pill bg-light text-dark" id="category13" onclick="changeDic( '13' )">#{lp[14]}</span>
<span class="badge rounded-pill bg-warning text-dark" id="category14" onclick="changeDic( '14' )">#{lp[15]}</span>
<span class="badge rounded-pill bg-secondary" id="category15" onclick="changeDic( '15' )">#{lp[16]}</span>
<span class="badge rounded-pill bg-primary" id="category16" onclick="changeDic( '16' )">#{lp[17]}</span>
<span class="badge rounded-pill bg-light text-dark" id="category17" onclick="changeDic( '17' )">#{lp[18]}</span>
<span class="badge rounded-pill bg-secondary" id="category18" onclick="changeDic( '18' )">#{lp[19]}</span>
<span class="badge rounded-pill bg-light text-dark" id="category0" onclick="changeDic( '00' )">#{lp[20]}</span>
HTML_SUB
	puts html_sub
	exit

when 'update'
	aliases.gsub!( "\s", '' )
	aliases.gsub!( '、', ',' )
	aliases.gsub!( '，', ',' )

	mdb( "UPDATE #{$MYSQL_TB_DIC} SET alias='#{aliases}' WHERE org_name='#{org_name}';", false, @debug )

	exit
else
	r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE FG ='#{sg}';", false, @debug )
	r.each do |e|
		list_html << "<div class='row'>"
		list_html << "<div class='col-2'>"
		list_html << "#{e['org_name']}"
		list_html << '</div>'
		list_html << "<div class='col-10'>"
		list_html << "<input type='text' class='form-control' id=\'#{e['org_name']}' value='#{e['alias']}' onchange=\"saveDic( '#{e['org_name']}' )\">"
		list_html << '</div>'
		list_html << '</div>'
	end
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: </h5></div>
	</div><br>
	#{list_html}
HTML

puts html
