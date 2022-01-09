#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM export 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-export'


#==============================================================================
#DEFINITION
#==============================================================================
def assemble( tables, pk_set, sk_set )
	export = ''

	tables.size.times do |c|
		r = mdb( "SELECT * FROM #{tables[c]};", false, @debug )
		if r.first
			columns = []

			r.first.each_key do |k| columns << k end

			export << "#{tables[c]}\n#{pk_set[c]}\n#{sk_set[c]}\n"
			columns.each do |e| export << "#{e}\t" end
			export.chop!
			export << "\n"

			r.each do |e|
				columns.each do |ee| export << "#{e[ee]}\t" end
				export.chop!
				export << "\n"
			end
			export << "////\n"
		end
	end

	return export
end

#==============================================================================
# Main
#==============================================================================

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### GMチェック
if user.status < 9
	puts "GM error."
	exit
end

command = @cgi['command']
if command == 'init'
	html_init( nil )
	html = <<-"HTML"
	<table class="table table-hover">
  		<thead>
    		<tr>
				<th scope="col"></th>
				<th scope="col">Table</th>
				<th scope="col"></th>
    		</tr>
		</thead>
 		<tr><td>#{lp[2]}</td><td>user, cfg</td>
			<td><a href='gm-export.cgi?table=user' download='user_set.txt'>
			<button type="button" class="btn btn-info btn-sm">#{lp[1]}</button></a></td>
		</tr>

		<tr><td>#{lp[3]}</td><td>fctp, tag, ext, pricem</td>
			<td><a href='gm-export.cgi?table=food' download='food_set.txt'>
			<button type="button" class="btn btn-info btn-sm">#{lp[1]}</button></a></td>
		</tr>

		<tr><td>#{lp[4]}</td><td>recipe, price</td>
			<td><a href='gm-export.cgi?table=recipe' download='recipe.txt'>
			<button type="button" class="btn btn-info btn-sm">#{lp[1]}</button></a></td>
		</tr>
		<tr><td>#{lp[5]}</td><td>menu</td>
			<td><a href='gm-export.cgi?table=menu' download='menu.txt'>
			<button type="button" class="btn btn-info btn-sm">#{lp[1]}</button></a></td>
		</tr>
		<tr><td>#{lp[6]}</td><td>memory</td>
			<td><a href='gm-export.cgi?table=memory' download='memory.txt'>
			<button type="button" class="btn btn-info btn-sm">#{lp[1]}</button></a></td>
		</tr>
		<tr><td>#{lp[7]}</td><td>media</td>
			<td><a href='gm-export.cgi?table=media' download='media.txt'>
			<button type="button" class="btn btn-info btn-sm">#{lp[1]}</button></a></td>
		</tr>
	</table>
HTML

puts html

else
	puts "Content-type: text/text\n\n"

	get = get_data()
	table = get['table']
	tables = []
	pk_set = []
	sk_set = []

	case table
	when 'user'
		tables = %w( user cfg )
		pk_set = %w( user user )
		sk_set = %w( user user )
	when 'food'
		tables = %w( fctp tag ext pricem )
		pk_set = %w( FN FN FN FN )
		sk_set = %w( user user user user )
	when 'recipe'
		tables = %w( recipe pricem )
		pk_set = %w( code code )
		sk_set = %w( user user )
	when 'menu'
		tables = %w( menu )
		pk_set = %w( code )
		sk_set = %w( user )
	when 'memory'
		tables = %w( memory )
		pk_set = %w( pointer )
		sk_set = %w( category )
	when 'media'
		tables = %w( media )
		pk_set = %w( mcode )
		sk_set = %w( user )
	end

	export = assemble( tables, pk_set, sk_set )

	puts export.force_encoding( 'UTF-8' )
end
