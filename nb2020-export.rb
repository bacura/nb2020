#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 export 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require './nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'nb2020-export'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================

table_set = ARGV[0]

dbis = []
case table_set
when 'user'
	tables = %w( user cfg )
	dbis[0] = ""
	dbis[1] = ""
when 'food'
	tables = %w( fctp tag ext pricem )
	dbis[0] = ""
	dbis[1] = ""
	dbis[2] = ""
	dbis[3] = ""
when 'recipe'
	tables = %w( recipe pricem )
	dbis[0] = ""
	dbis[1] = ""
when 'menu'
	tables = %w( menu )
	dbis[0] = ""
when 'memory'
	tables = %w( memory )
	dbis[0] = ""
when 'media'
	tables = %w( media )
	dbis[0] = ""
when 'dic'
	tables = %w( dic )
	dbis[0] = "FG VARCHAR(2), org_name VARCHAR(64), alias VARCHAR(128), user VARCHAR(32)"
else
	puts "user"
	puts "food"
	puts "recipe"
	puts "menu"
	puts "memory"
	puts "media"
	puts "dic"

	exit
end


tables.size.times do |c|
	r = mdb( "SELECT * FROM #{tables[c]};", false, @debug )
	if r.first
		columns = []

		r.first.each_key do |k| columns << k end

		puts "#{tables[c]}\n"
		puts "#{dbis[c]}\n"
		line = ''
		columns.each do |e| line << "#{e}\t" end
		line.chop!
		line << "\n"
		puts line

		r.each do |e|
			line = ''
			columns.each do |ee| line << "#{e[ee]}\t" end
			line.chop!
			line << "\n"
			puts line.force_encoding( 'UTF-8' )
		end

		puts "////\n"
	end
end
