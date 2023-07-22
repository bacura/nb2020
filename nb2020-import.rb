#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM import 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require './nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'nb2020-import'
@debug = false
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================

#### data loading
import_solid = []
txt_class = ''
line1_flag = true
File.open( ARGV[0], 'r' ) do |f|
	f.each_line do |line|
		if line1_flag
			a = line.chomp.split( "\s" )
			if a[0] == 'NB2020' && a[2] == 'data'
				txt_class = a[1].sub( '[', '' ).sub( ']', '' )
				line1_flag = false
			else
				puts 'Incomplete dic data.'
				exit( 0 )
			end
		else
			import_solid << line.force_encoding( 'utf-8' ).chomp.split( "\t" )
		end
	end
end
puts "[#{txt_class}]"


#### DB upadate
if import_solid.size > 0
    count = 0
	case txt_class
	when 'dic'
		if import_solid[0].size == 5
			db.query( "DELETE FROM #{$MYSQL_TB_DIC};" )
			import_solid.each do |e|
				print "#{count}\r"
				begin
					#FG org_name alias user def_fn
					db.query( "INSERT INTO #{$MYSQL_TB_DIC} SET FG='#{e[0]}', org_name='#{e[1]}', alias='#{e[2]}', user='#{e[3]}', def_fn='#{e[4]}';" )
				rescue
					puts "[ERROR]#{e}"
				end
				count += 1
			end
		else
			puts 'Incomplete dic data.'
		end
	else
		puts 'Importable data list..'
		puts 'dic'
	end
	db.close

else
	puts 'ruby nb2020-import [data.txt]'
end
