#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 menu 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'menu'


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


#### Getting POST data
command = @cgi['command']
code = @cgi['code']
if @debug
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
	puts "<hr>"
end


menu = Menu.new( user.name )
menu.debug if @debug


case command
when 'view'
	puts 'Displaing menu<br>' if @debug
	menu.load_db( code, true ) unless code == ''

when 'save'
	puts 'Saving menu<br>' if @debug
	menu.load_cgi( @cgi )

	r = mdb( "SELECT * from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, @debug )
	# Inserting new menu
	if r.first['name'] == ''
		menu.code = generate_code( user.name, 'm' )
		menu.meal = r.first['meal']
  		menu.insert_db

	# Updating menu
	else
		pre_menu = Menu.new( user.name )
		pre_menu.code = menu.code
		pre_menu.load_db( code, true )
		menu.meal = r.first['meal']

		if menu.name != pre_menu.name
			# 名前が一致しなければ、新規コードとメニューを登録
			# バグに近い仕様：名前を変えて新規コードになるけど、写真はコピーされない
			menu.code = generate_code( user.name, 'm' )
			menu.insert_db
			mdb( "UPDATE #{$MYSQL_TB_MEAL} SET name='#{menu.name}', code='#{menu.code}', protect='#{recipe.protect}' WHERE user='#{user.name}';", false, @debug )
		end
	end
	# Updating menu
	menu.debug if @debug
	menu.update_db
end


puts 'Label HTML<br>' if @debug
r = mdb( "SELECT label from #{$MYSQL_TB_MENU} WHERE user='#{user.name}' AND name!='';", false, @debug )
label_list = []
r.each do |e| label_list << e['label'] end
label_list.uniq!

html_label = '<select class="form-select form-select-sm" id="label">'
html_label << "<option value='#{lp[2]}'>#{lp[2]}</option>"

label_list.each do |e|
	selected = ''
	selected = 'SELECTED' if e == menu.label
	html_label << "<option value='#{e}' #{selected}>#{e}</option>" unless e == lp[2]
end

if user.status >= 5 && user.status != 6
	r = mdb( "SELECT schooll FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first
		a =  r.first['schooll'].split( ':' )
		a.each do |e|
			selected = ''
			selected = 'SELECTED' if e == menu.label
			html_label << "<option value='#{e}' #{selected}>[#{e}]</option>" if e != '' &&  e != nil
		end
	end
end
html_label << '</select>'


puts 'Photo upload form<br>' if @debug
form_photo = ''
form_photo = "<form method='post' enctype='multipart/form-data' id='photo_form'>"
form_photo << '<div class="input-group input-group-sm">'
form_photo << "<label class='input-group-text'>#{lp[12]}</label>"
if menu.code == nil
	form_photo << "<input type='file' class='form-control' DISABLED>"
else
	form_photo << "<input type='file' class='form-control' name='photo' onchange=\"photoSave( '#{menu.code}', '#photo_form', 'menu' )\">"
end
form_photo << '</form></div>'


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[3]}</h5></div>
		<div class="col-4">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{checked( menu.public )}> #{lp[4]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{checked( menu.protect )}> #{lp[5]}
  				</label>
			</div>
		</div>
		<div class="col-6">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="menu_name">#{lp[6]}</label>
      			<input type="text" class="form-control" id="menu_name" value="#{menu.name}" required>
      			<button class="btn btn-outline-primary" type="button" onclick="menuSave( '#{menu.code}' )">#{lp[7]}</button>
    		</div>
    	</div>
    </div>
    <br>
	<div class='row'>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="menu_name">#{lp[9]}</label>
				#{html_label}
			</div>
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="menu_name">#{lp[10]}</label>
      			<input type="text" class="form-control" id="new_label" value="">
	   		</div>
    	</div>
	</div>
    <br>
	<div class='row'>
		<div class="col">
			<div class="form-group">
    			<label for='memo'>メモ</label>
				<textarea class="form-control" id='memo' rows="3">#{menu.memo}</textarea>
   			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-4'>
			#{form_photo}
		</div>
		<div align='right' class='col-8 code'>#{menu.code}</div>
	</div>
</div>
HTML

puts html
