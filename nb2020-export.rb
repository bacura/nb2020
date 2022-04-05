#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM export 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require './nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-export'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================


case ARGV[0]
when 'unit'
	export = ''
	r = mdb( "SELECT FN, unit FROM #{$MYSQL_TB_EXT};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['unit']}\n" end
	puts "NB2020 [unit] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'shun'
	export = ''
	r = mdb( "SELECT FN, unit FROM #{$MYSQL_TB_EXT};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['unit']}\n" end
	puts "NB2020 [shun] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'dic'
	export = ''
	r = mdb( "SELECT FN, unit FROM #{$MYSQL_TB_DIC};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['unit']}\n" end
	puts "NB2020 [dic] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'memory'
	export = ''
	r = mdb( "SELECT FN, unit FROM #{$MYSQL_TB_MEMORY};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['unit']}\n" end
	puts "NB2020 [memory] data\n"
	puts export.force_encoding( 'UTF-8' )
else
	puts 'Exportable data list..'
	puts 'unit'
	puts 'shun'
	puts 'dic'
	puts 'memory'
end
