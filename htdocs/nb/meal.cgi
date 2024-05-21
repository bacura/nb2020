#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 meal 0.1.2 (2024/05/21)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'meal' 		=> "お膳",\
		'reset' 	=> "お片付け",\
		'command' 	=> "操作",\
		'photo' 	=> "写真",\
		'name' 		=> "献立名",\
		'tag' 		=> "属性",\
		'edit' 		=> "献立編集",\
		'calc' 		=> "栄養計算",\
		'analysis' 	=> "基本解析",\
		'up' 		=> "<img src='bootstrap-dist/icons/chevron-up.svg' style='height:1.5em; width:1.5em;'>",\
		'down' 		=> "<img src='bootstrap-dist/icons/chevron-down.svg' style='height:1.5em; width:1.5em;'>",\
		'eraser' 	=> "<img src='bootstrap-dist/icons/eraser.svg' style='height:1.8em; width:1.8em;'>",\
	}

	return l[language]
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )


#### Getting POST data
command = @cgi['command']
code = @cgi['code']
order = @cgi['order']
if @debug
	puts "command:#{command}<br>"
	puts "code:#{code}<br>"
	puts "order:#{order}<br>"
	puts "<hr>"
end


puts "Loading MEAL<br>" if @debug
meal_o = Meal.new( user.name )
meal_o.load_menu( code ) if command == 'load'
meal_o.debug if @debug


puts "Loading recipe<br>" if @debug
recipe_list = []
if meal_o.meal
	meal_o.meal.split( "\t" ).each do |e|
		recipe = Recipe.new( user )
		recipe.load_db( e, true )
		recipe.load_media
		recipe_list << recipe
	end
end

case command
# Deleting recipe from meal
when 'clear'
	# All
	if order == 'all'
		recipe_list = []
		meal_o.name = ''
		meal_o.code = ''
	# One by one
	else
		recipe_list.delete_at( order.to_i )
		update = '*'
	end

# 食品の順番を１つ上げる
when 'upper'
	if order.to_i == 0
		t = recipe_list.shift
		recipe_list << t
	else
		t = recipe_list.delete_at( order.to_i )
		recipe_list.insert( order.to_i - 1, t )
	end
	update = '*'

# 食品の順番を１つ下げる
when 'lower'
	if order.to_i == recipe_list.size - 1
		t = recipe_list.pop
		recipe_list.unshift( t )
	else
		t = recipe_list.delete_at( order.to_i )
		recipe_list.insert( order.to_i + 1, t )
	end
	update = '*'
end

puts "HTML part<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-10'><h5>#{l['meal']}: #{meal_o.name}</h5></div>
		<div class='col-2' align='right'>
			<input type='checkbox' id='meal_all_check'>&nbsp;
			<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"clear_meal( 'all', '#{meal_o.code}' )\">#{l['reset']}</button>
		</div>
	</div>
	<hr>

	<div class='row'>
		<div class='col-1 meal_header'>#{l['name']}</div>
		<div class='col-1 meal_header'>#{l['photo']}</div>
		<div class='col-4 meal_header'>#{l['name']}</div>
		<div class='col-2 meal_header'>#{l['tag']}</div>
	</div>
	<br>
HTML

c = 0
recipe_list.each do |e|
	html << "	<div class='row'>"
 	html << "		<div class='col-1'>"
 	html << "			<span onclick=\"upper_meal( '#{c}', '#{e.code}' )\">#{l['up']}</span>"
 	html << "			<span onclick=\"lower_meal( '#{c}', '#{e.code}' )\">#{l['down']}</span>"
 	html << "		</div>"
	if e.media[0] != nil
  		html << "		<div class='col-1' align='center'><img src='#{$PHOTO}/#{e.media[0]}-tns.jpg'></div>"
  	else
  		html << "		<div class='col-1' align='center'>-</div>"
  	end
  	html << "		<div class='col-4' onclick=\"initCB( 'load', '#{e.code}' )\">#{e.name}</div>"
  	html << "		<div class='col-1'>"
  	html << "			#{@recipe_type[e.type]}&nbsp;" unless e.type == 0
  	html << "		</div>"
  	html << "		<div class='col-1'>"
  	html << "			#{@recipe_role[e.role]}&nbsp;" unless e.role == 0
  	html << "		</div>"
  	html << "		<div class='col-3'>"
  	html << "			#{@recipe_tech[e.tech]}&nbsp;" unless e.tech == 0
  	html << "		</div>"
  	html << "		<div class='col-1' align='right'><span onclick=\"clear_meal( '#{c}', '#{e.code}' )\">#{l['eraser']}</span></div>"
	html << "	</div>"
	c += 1
end

html << "	<br>"
html << "	<div class='row'>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuEdit( 'view', '#{meal_o.code}' )\">#{l['edit']}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuCalcView( '#{meal_o.code}' )\">#{l['calc']}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuAnalysis( '#{meal_o.code}' )\">#{l['analysis']}</button></div>"
html << "	</div>"
html << "	<div class='code'>#{meal_o.code}</div>"
html << "</div>"

puts html


puts "Updating MEAL<br>" if @debug
meal_new = ''
recipe_list.each do |e| meal_new << "#{e.code}\t" end
meal_o.meal = meal_new.chop!
meal_o.update_db
