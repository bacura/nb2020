#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM export 0.01b

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
	puts "SELECT * FROM #{$MYSQL_TB_EXT};"
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['unit']}\n" end
	puts "NB2020 [unit] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'gycv'
	export = ''
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['gycv']}\n" end
	puts "NB2020 [gycv] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'shun'
	export = ''
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['shun1s']}\t#{e['shun1e']}\t#{e['shun2s']}\t#{e['shun2e']}\n" end
	puts "NB2020 [shun] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'allergen'
	export = ''
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, false )
	r.each do |e| export << "#{e['FN']}\t#{e['allergen1']}\t#{e['allergen2']}\n" end
	puts "NB2020 [allergen] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'dic'
	export = ''
	r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC};", false, false )
	r.each do |e| export << "#{e['FG']}\t#{e['org_name']}\t#{e['alias']}\t#{e['user']}\t#{e['def_fn']}\n" end
	puts "NB2020 [dic] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'memory'
	export = ''
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY};", false, false )
	r.each do |e| export << "#{e['user']}\t#{e['category']}\t#{e['pointer']}\t#{e['memory']}\t#{e['rank']}\t#{e['total_rank']}\t#{e['count']}t#{e['know']}\t#{e['date']}\n" end
	puts "NB2020 [memory] data\n"
	puts export.force_encoding( 'UTF-8' )
else
	puts 'Exportable data list..'
	puts 'unit'
	puts 'gycv'
	puts 'shun'
	puts 'allergen'
	puts 'dic'
	puts 'memory'
end
