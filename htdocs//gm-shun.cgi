#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM Shun editor 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-shun'


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


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### POSTデータの取得
command = @cgi['command']
shun1s = @cgi['shun1s'].to_i
shun1e = @cgi['shun1e'].to_i
shun2s = @cgi['shun2s'].to_i
shun2e = @cgi['shun2e'].to_i
code = @cgi['code']
code.gsub!( /\s/, ',' ) unless code == ''
code.gsub!( '　', ',' ) unless code == ''
if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"
	puts "shun1s:#{shun1s}<br>\n"
	puts "shun1e:#{shun1e}<br>\n"
	puts "shun2s:#{shun2s}<br>\n"
	puts "shun2e:#{shun2e}<br>\n"
	puts "<hr>\n"
end

case command
when 'on'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mdb( "UPDATE #{$MYSQL_TB_EXT} SET shun1s='#{shun1s}', shun1e='#{shun1e}', shun2s='#{shun2s}', shun2e='#{shun2e}' WHERE FN='#{code}';", false, @debug )
		end
	end
when 'off'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mdb( "UPDATE #{$MYSQL_TB_EXT} SET shun1s='0', shun1e='0', shun2s='0', shun2e='0' WHERE FN='#{code}';", false, @debug )
		end
	end
end

food_name = ''
unless code == ''
	r = mdb( "SELECT name from #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false, @debug )
	food_name = r.first['name']
end

list_html = ''
r = mdb( "SELECT FN FROM #{$MYSQL_TB_EXT} WHERE shun1s>='1' and shun1s<='12';", false, @debug )
if r.size != 0
	code_list = []
	name_tag_list = []
	r.each do |e|
		rr = mdb( "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false, @debug )
		code_list << rr.first['FN']
		name_tag_list << "#{rr.first['name']}・#{rr.first['tag1']} #{rr.first['tag2']} #{rr.first['tag3']} #{rr.first['tag4']} #{rr.first['tag5']}"
	end
	code_list.reverse!
	name_tag_list.reverse!

	c = 0
	code_list.each do |e|
		rr = mdb( "SELECT * from #{$MYSQL_TB_EXT} WHERE FN='#{e}';", false, @debug )
		list_html << "<div class='row'>"
		list_html << "<div class='col-1'><button class='btn btn-sm btn-outline-danger' type='button' onclick=\"offShun( '#{e}' )\">x</button></div>"
		list_html << "<div class='col-2'>#{e}</div>"
		list_html << "<div class='col-4'>#{name_tag_list[c]}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun1s']}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun1e']}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun2s']}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun2e']}</div>"
		list_html << '</div>'
		c += 1
	end
else
	list_html << 'no item listed.'
end


select_opt = ''
1.upto( 12) do |c| select_opt << "<option value='#{c}'>1</option>" end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{food_name}</h5></div>
	</div>
	<div class='row'>
		<div class='col-10'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="weight">#{lp[2]}</label>
				<input type="text" maxlength="5" class="form-control" id="code" value="#{code}">
			</div>
		</div>
		<div class='col-1'></div>
		<div class='col-1'>
			<button class="btn btn-sm btn-outline-primary" type="button" onclick="onShun()">#{lp[3]}</button>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-5'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="shun1s">#{lp[4]}</label>
				<select class="form-select form-select-sm" id="shun1s">
					#{select_opt}
				</select>
				　～　
				<label class="input-group-text" for="shun1e">#{lp[5]}</label>
				<select class="form-select form-select-sm" id="shun1e">
					#{select_opt}
				</select>
			</div>
		</div>
		<div class='col-1'></div>
		<div class='col-5'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="shun1s">#{lp[6]}</label>
				<select class="form-select form-select-sm" id="shun2s">
					#{select_opt}
				</select>
				　～　
				<label class="input-group-text" for="shun1e">#{lp[7]}</label>
				<select class="form-select form-select-sm" id="shun2e">
					#{select_opt}
				</select>
			</div>
		</div>
	</div>
	<br>
	<hr>
	#{list_html}
HTML

puts html
