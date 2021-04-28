#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser school menu 0.00b


#==============================================================================
#MEMO
#==============================================================================


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'school-menu'
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

#### Guild member check
if user.status < 5 && !@debug
	puts "Guild member shun error."
	exit
end


#### Getting POST
command = @cgi['command']
tag_group = @cgi['tag_group']
tag_no = @cgi['tag_no'].to_i
tag_new = @cgi['tag_new']
tag_name_new = @cgi['tag_name_new']
group_new = @cgi['group_new']
if @debug
	puts "command:#{command}<br>\n"
	puts "tag_group:#{tag_group}<br>\n"
	puts "tag_no:#{tag_no}<br>\n"
	puts "tag_new:#{tag_new}<br>\n"
	puts "tag_name_new:#{tag_name_new}<br>\n"
	puts "group_new:#{group_new}<br>\n"
	puts "<hr>\n"
end


calendar = Calendar.new( user.name, 0, 0, 0 )
calendar.debug if @debug


case command
when 'tag_name_change'
	puts "Tag name update<br>" if @debug
	r = mdb( "SELECT tags_name FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}' AND tag_group='#{tag_group}';", false, @debug )
	if r.first
		tags_name = []
		tags_name = r.first['tags_name'].split( "\t" ) unless r.first['tags_name'] == nil
		tags_name[tag_no] = tag_name_new
		tags_name_join = tags_name.join( "\t" )
		mdb( "UPDATE #{$MYSQL_TB_SCHOOLM} SET tags_name='#{tags_name_join}' WHERE user='#{user.name}' AND tag_group='#{tag_group}';", false, @debug )
	end
when 'tag_change'
	puts "Tag update<br>" if @debug
	r = mdb( "SELECT tags FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}' AND tag_group='#{tag_group}';", false, @debug )
	if r.first
		tags = []
		tags = r.first['tags'].split( "\t" ) unless r.first['tags'] == nil
		tags[tag_no] = tag_new
		tags_join = tags.join( "\t" )
		mdb( "UPDATE #{$MYSQL_TB_SCHOOLM} SET tags='#{tags_join}' WHERE user='#{user.name}' AND tag_group='#{tag_group}';", false, @debug )
	end
when 'group_new'
	mdb( "INSERT INTO #{$MYSQL_TB_SCHOOLM} SET user='#{user.name}', tag_group='#{group_new}';", false, @debug )
end


puts "Loading tag from DB<br>" if @debug
tags = []
tags_name = []
tag_group = []
r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}';", false, @debug )
if r.first
	r.each do |e|
		unless e['tag_group'] == nil
			tag_group << e['tag_group']
			a = r.first['tags_name']
			tags_name << a.split( "\t" ) if a != nil
			a = r.first['tags']
			tags << a.split( "\t" ) if a != nil

		end
	end
end
tags_name << Array.new if tags_name[0] == nil
tags << Array.new if tags[0] == nil
if @debug
	puts "tag_group:#{tag_group}<br>"
	puts "tags_name:#{tags_name}<br>"
	puts "tags:#{tags}<br>"
end


puts 'HTML tag<br>' if @debug
html_groups = ''
disabled_flag = []
tag_group.size.times do |c|
	html_groups << "<h6>#{tag_group[c]}</h6>"
	html_groups << "<div class='row'>"
	0.upto( 5 ) do |cc|
		html_groups << "<div class='col-2'>"
		html_groups << "<input type='text' class='form-control form-control-sm' id='tag_name#{c}_#{cc}' placeholder='#{lp[5]}' value='#{tags_name[c][cc]}' onChange=\"changeSchoolTagName( '#{tag_group[c]}', '#{c}', '#{cc}' )\">"
		html_groups << "</div>"
		disabled_flag[cc] = 'DISABLED' if tags_name[c][cc] == '' || tags_name[c][cc] == nil
	end

	html_groups << '</div>'
	html_groups << "<div class='row'>"
	0.upto( 5 ) do |cc|
		html_groups << "<div class='col-2'>"
		html_groups << "<input type='text' class='form-control form-control-sm' id='tag#{c}_#{cc}' value='#{tags[c][cc]}' onChange=\"changeSchoolTag( '#{tag_group[c]}', '#{c}', '#{cc}' )\" #{disabled_flag[cc]}>"
		html_groups << "</div>"
	end
	html_groups << '</div><br>'
end


puts 'HTML month option<br>' if @debug
month_html = ''
1.upto( 12 ) do |c|
	if calendar.mm == c
		month_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		month_html << "<option value='#{c}'>#{c}</option>"
	end
end
month_html << "<option value='0'>#{lp[6]}</option>"
month_html << '</div>'






puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{lp[1]}</h5></div>
		<div class='col-5'></div>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text'>#{lp[3]}</label>
				<input type='text' class='form-control' id='group_new'>
				<button type='button' class='btn btn-outline-secondary' onclick="mekeSchoolGroup()">#{lp[4]}</button>
			</div>
		</div>
	</div>

	<h6>#{html_groups}</h6>
	#{lp[2]}
	<hr>

	<div class='row'>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text'>グループ</label>
				<select class='form-select' id='group_select'>
					<option value="0">基本の料理</option>
					<option value="1">季節の料理</option>
				</select>
			</div>
		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text'>タグ</label>
				<select class='form-select' id='tag_select'>
					<option value=""></option>
				</select>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<select class='form-select' id='month_select'>
					#{month_html}
				</select>
				<label class='input-group-text'>月</label>
			</div>
		</div>
	</div>
</div>


HTML

puts html
