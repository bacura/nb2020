#! /usr/bin/ruby
#encoding: utf-8
#fct
#Nutrition browser GM slogf viewer 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190224, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-slogf'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### POSTデータの取得
command = cgi['command']
if @debug
	puts "command:#{command}<br>\n"
	puts "<hr>\n"
end


if command == 'edit'
#	mdb( "UPDATE #{$MYSQL_TB_USER} SET;", false, @debug )
end


slogf_html = "<div class='row'>"
r = mdb( "SELECT * FROM #{$MYSQL_TB_SLOGF};", false, @debug )
if r.first
	slogf_html << "<table class='table-striped table-bordered'>"
	slogf_html << "<thead>"
	slogf_html << "<th>#{lp[2]}</th>"
	slogf_html << "<th>#{lp[3]}</th>"
	slogf_html << "<th>#{lp[4]}</th>"
	slogf_html << "<th>#{lp[5]}</th>"
	slogf_html << "</thead>"

	r.each do |e|
		if e['code'].to_i == 0 || e['code'].size >= 5
		slogf_html << "<tr>"
		slogf_html << "<td>#{e['user']}</td>"
		slogf_html << "<td>#{e['words']}</td>"
		slogf_html << "<td>#{e['code']}</td>"
		slogf_html << "<td>#{e['date']}</td>"
		slogf_html << "</tr>"
			end
	end
	slogf_html << "</table>"
else
	slogf_html << 'no slogf.'
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: </h5></div>
	</div>
	#{slogf_html}
</div>


HTML

puts html
