#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 import 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require './nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'nb2020-import'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================

file = ARGV[0]

f = open( file, 'r' )
data_solid = f.read
f.close

tables = data_solid.force_encoding( 'UTF-8' ).split( "////\n" )

tables.each do |e|
	a = e.split( "\n" )
	table = a[0]
	dbi = a[1]
	columns = a[2].split( "\t" )

	puts "Table:#{table}"
	puts "dbi:#{dbi}"
	puts "Columns:#{columns}"
	puts "Data#:#{a.size - 3 }"
	exit if table == '' || /\,/ !~ dbi || columns.size < 3 || ( a.size - 3 ) < 1

	mdb( "DROP TABLE #{table};", false, @debug )
	mdb( "CREATE TABLE #{table} (#{dbi});", false, @debug )

	data_size = a.size
	3.upto( data_size - 1 ) do |c|
		values = a[c].split( "\t" )
		sql_set = ''
		columns.size.times do |cc|
			sql_set << "#{columns[cc]}='#{values[cc]}',"
		end
		sql_set.chop!
		r = mdb( "INSERT INTO #{table} SET #{sql_set};", false, @debug )
		print "#{c - 2}/#{data_size - 3}\r"
	end
	puts ''
	puts 'Done'

end
