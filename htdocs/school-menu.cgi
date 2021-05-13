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
@debug = false


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
label_group = @cgi['label_group']
label_no = @cgi['label_no'].to_i
label_new = @cgi['label_new']
group_new = @cgi['group_new']
group_select = @cgi['group_select']
label_select = @cgi['label_select']
month_select = @cgi['month_select'].to_i
week_select = @cgi['week_select'].to_i
if @debug
	puts "command:#{command}<br>\n"
	puts "label_group:#{label_group}<br>\n"
	puts "label_no:#{label_no}<br>\n"
	puts "label_new:#{label_new}<br>\n"
	puts "group_new:#{group_new}<br>\n"
	puts "group_select:#{group_select}<br>\n"
	puts "label_select:#{label_select}<br>\n"
	puts "week_select:#{week_select}<br>\n"
	puts "<hr>\n"
end


school_mode = 3;
r = mdb( "SELECT school FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
school_mode = r.first['school'] if r.first


calendar = Calendar.new( user.name, 0, 0, 0 )
calendar.debug if @debug


case command
when 'label_change'
	puts "label update<br>" if @debug
	r = mdb( "SELECT label FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}' AND label_group='#{label_group}';", false, @debug )
	if r.first
		label = []
		label = r.first['label'].split( "\t" ) unless r.first['label'] == nil
		label[label_no] = label_new
		label_join = label.join( "\t" )
		mdb( "UPDATE #{$MYSQL_TB_SCHOOLM} SET label='#{label_join}' WHERE user='#{user.name}' AND label_group='#{label_group}';", false, @debug )
	end
when 'group_new'
	mdb( "INSERT INTO #{$MYSQL_TB_SCHOOLM} SET user='#{user.name}', label_group='#{group_new}';", false, @debug )
	group_select = group_new
when 'group_del'
	mdb( "DELETE FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}' AND label_group='#{group_new}';", false, @debug )
when 'menu_select'
end


puts "Loading label from DB<br>" if @debug
label_matrix = Hash.new
r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}';", false, @debug )
if r.first
	r.each do |e|
		unless e['label_group'] == nil
			a = e['label']
			if a != nil
				label_matrix[e['label_group']] = a.split( "\t" )
			else
				label_matrix[e['label_group']] = [nil, nil, nil, nil, nil, nil]
			end
		end
	end
end
puts "label_matrix:#{label_matrix}<br>" if @debug


puts 'HTML label<br>' if @debug
html_groups = ''
disabled_flag = []
count = 0
label_matrix.each do |group, label|
	html_groups << "<div class='row'>"
	html_groups << "<div class='col-11'><h6>#{group}</h6></div>"
	html_groups << "<div align='right' class='col-1'>"
    html_groups << "<input type='checkbox' class='form-check-input' id='del_check_#{group}'>"
  	html_groups << "&nbsp;<span onclick=\"delSchoolGroup( '#{group}' )\">#{lp[7]}</span>"
	html_groups << '</div>'
	html_groups << '</div>'

	html_groups << "<div class='row'>"
	0.upto( 5 ) do |c|
		html_groups << "<div class='col-2'>"
		if label != nil
			html_groups << "<input type='text' class='form-control form-control-sm' id='label#{count}_#{c}' value='#{label[c]}' placeholder='#{lp[8]}' onChange=\"changeSchoolLabel( '#{group}', '#{count}', '#{c}' )\" #{disabled_flag[c]}>"
		else
			html_groups << "<input type='text' class='form-control form-control-sm' id='label#{count}_#{c}' value='' onChange=\"changeSchoollabel( '#{group}', '#{count}', '#{c}' )\" #{disabled_flag[c]}>"
		end
		html_groups << "</div>"
	end
	html_groups << '</div><br>'

	count += 1
end


puts 'HTML group option<br>' if @debug
group_html = ''
group_tmp = ''
label_tmp = ''
label_matrix.each do |group, label|
	if group_select == group
		group_html << "<option value='#{group}' SELECTED>#{group}</option>"
	else
		group_html << "<option value='#{group}'>#{group}</option>"
	end
	group_tmp = group if group_tmp == ''
end
group_select = group_tmp if group_select == ''


puts 'HTML label option<br>' if @debug
label_html = ''
label_tmp = ''
if label_matrix[group_select] != nil
	label_matrix[group_select].each do |e|
		if label_select == e &&  e != nil && e != ''
			label_html << "<option value='#{e}' SELECTED>#{e}</option>"
			label_tmp = e if label_tmp == ''
		elsif e != nil && e != ''
			label_html << "<option value='#{e}'>#{e}</option>"
			label_tmp = e if label_tmp == ''
		end
	end
end

if label_select == ''
	label_select = label_tmp
elsif label_matrix[group_select].include?( label_select )
else
	label_select = label_tmp
end


puts 'HTML month option<br>' if @debug
month_html = ''
month_html << "<option value='0'>#{lp[6]}</option>"
1.upto( 12 ) do |c|
	if month_select.to_i == c
		month_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		month_html << "<option value='#{c}'>#{c}</option>"
	end
end


puts 'HTML month option<br>' if @debug
week_html = ''
week_html << "<option value='0'>#{lp[6]}</option>"
1.upto( 5 ) do |c|
	if week_select.to_i == c
		week_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		week_html << "<option value='#{c}'>#{c}</option>"
	end
end


puts 'HTML menu<br>' if @debug
menu_html = ''
if month_select == 0
	label_select.sub!( '#', '' )
else
	label_select.sub!( '#', month_select.to_s )
end
r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE user='#{user.name}' AND label='#{label_select}';", false, @debug )
r.each do |e|
	menu_html << "<div class='row'>"
	menu_html << "<div class='col'><h5>#{e['name']}</h5></div>"
	menu_html << "</div>"



#ここに教室モードごとの登録メニューを作る



	menu_html << "<div class='row'>"
	menu_html << "<div class='col'>#{e['memo']}</div>"
	menu_html << "</div>"

	menu_html << "<div class='row'>"
	recipe_code = e['meal'].split( "\t" )
	recipe_code.each do |ee|
		rr = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' AND code='#{ee}';", false, @debug )
		if rr.first
			photo = 'no_image.png'
			rrr = mdb( "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND code='#{ee}';", false, @debug )
			photo = "#{rrr.first['mcode']}-tn.jpg" if rrr.first

			menu_html << "<div class='col-2'>"
			menu_html << "	<div class='card'>"
			menu_html << "		<img src='#{$PHOTO}/#{photo}' class='card-img-top'>"
			menu_html << "		<div class='card-body'>"
    		menu_html << "			<h6 class='card-title'>#{rr.first['name']}</h6>"
			menu_html << "			<p class='card-text'>"
			menu_html << "			<ul>"

			menu_html << "			<li>#{@recipe_type[rr.first['type'].to_i]}</li>"
			menu_html << "			<li>#{@recipe_role[rr.first['role'].to_i]}</li>"
			menu_html << "			<li>#{@recipe_tech[rr.first['tech'].to_i]}</li>"
			menu_html << "			<li>#{@recipe_time[rr.first['time'].to_i]}</li>"
			menu_html << "			<li>#{@recipe_cost[rr.first['cost'].to_i]}</li>"

			menu_html << "			</ul>"
			menu_html << "			</p>"
			menu_html << "		</div>"
			menu_html << "	</div>"
			menu_html << "</div>"
		end
	end
	menu_html << "</div>"
	menu_html << "<div class='code'>#{e['code']}</div>"
end

menu_html << "#{lp[10]}" if r.size == 0




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
				<button type='button' class='btn btn-outline-primary' onclick="mekeSchoolGroup()">#{lp[4]}</button>
			</div>
		</div>
	</div>
	<br>
	<h6>#{html_groups}</h6>
	#{lp[2]}
	<hr>

	<div class='row'>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text'>#{lp[3]}</label>
				<select class='form-select' id='group_select' onchange="selectSchoolMenu()">
					#{group_html}
				</select>
			</div>
		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text'>#{lp[8]}</label>
				<select class='form-select' id='label_select' onchange="selectSchoolMenu()">
					#{label_html}
				</select>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<select class='form-select' id='month_select' onchange="selectSchoolMenu()">
					#{month_html}
				</select>
				<label class='input-group-text'>#{lp[9]}</label>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<select class='form-select' id='week_select' onchange="selectSchoolMenu()">
					#{week_html}
				</select>
				<label class='input-group-text'>#{lp[12]}</label>
			</div>
		</div>
	</div>
	<br>
	<div class='row'>
		#{menu_html}
	</div>
</div>
HTML

puts html
