#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 meal 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'meal'
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
meal = Meal.new( user.name )
meal.load_menu( code ) if command == 'load'
meal.debug if @debug


puts "Loading recipe<br>" if @debug
recipe_list = []
if meal.meal
	meal.meal.split( "\t" ).each do |e|
		recipe = Recipe.new( user.name )
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
		meal.name = ''
		meal.code = ''
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
		<div class='col-10'><h5>#{lp[1]}: #{meal.name}</h5></div>
		<div class='col-2' align='right'>
			<input type='checkbox' id='meal_all_check'>&nbsp;
			<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"clear_meal( 'all', '#{meal.code}' )\">#{lp[2]}</button>
		</div>
	</div>
	<hr>

	<div class='row'>
		<div class='col-1 meal_header'>#{lp[3]}</div>
		<div class='col-1 meal_header'>#{lp[4]}</div>
		<div class='col-4 meal_header'>#{lp[5]}</div>
		<div class='col-2 meal_header'>#{lp[6]}</div>
	</div>
	<br>
HTML

c = 0
recipe_list.each do |e|
	html << "	<div class='row'>"
 	html << "		<div class='col-1'>"
 	html << "			<span onclick=\"upper_meal( '#{c}', '#{e.code}' )\">#{lp[10]}</span>"
 	html << "			<span onclick=\"lower_meal( '#{c}', '#{e.code}' )\">#{lp[11]}</span>"
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
  	html << "		<div class='col-1' align='right'><span onclick=\"clear_meal( '#{c}', '#{e.code}' )\">#{lp[12]}</span></div>"
	html << "	</div>"
	c += 1
end


html << "	<br>"
html << "	<div class='row'>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuEdit( 'view', '#{meal.code}' )\">#{lp[7]}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuCalcView( '#{meal.code}' )\">#{lp[8]}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuAnalysis( '#{meal.code}' )\">#{lp[9]}</button></div>"
html << "	</div>"
html << "	<div class='code'>#{meal.code}</div>"
html << "</div>"

puts html


puts "Updating MEAL<br>" if @debug
meal_new = ''
recipe_list.each do |e| meal_new << "#{e.code}\t" end
meal.meal = meal_new.chop!
meal.update_db
