#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 export 0.02b (2023/07/17)

#==============================================================================
#LIBRARY
#==============================================================================
require './nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-export'
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )


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
	r = db.query( "SELECT * FROM #{$MYSQL_TB_EXT} ORDER BY FN;" )
	r.each do |e| export << "#{e['FN']}\t#{e['unit']}\n" end
	puts "NB2020 [unit] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'gycv'
	export = ''
	r = db.query( "SELECT * FROM #{$MYSQL_TB_EXT} ORDER BY FN;" )
	r.each do |e| export << "#{e['FN']}\t#{e['gycv']}\n" end
	puts "NB2020 [gycv] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'shun'
	export = ''
	r = db.query( "SELECT * FROM #{$MYSQL_TB_EXT} ORDER BY FN;" )
	r.each do |e| export << "#{e['FN']}\t#{e['shun1s']}\t#{e['shun1e']}\t#{e['shun2s']}\t#{e['shun2e']}\n" end
	puts "NB2020 [shun] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'allergen'
	export = ''
	r = db.query( "SELECT * FROM #{$MYSQL_TB_EXT} ORDER BY FN;" )
	r.each do |e| export << "#{e['FN']}\t#{e['allergen1']}\t#{e['allergen2']}\n" end
	puts "NB2020 [allergen] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'dic'
	export = ''
	r = db.query( "SELECT * FROM #{$MYSQL_TB_DIC} ORDER BY FG;" )
	r.each do |e| export << "#{e['FG']}\t#{e['org_name']}\t#{e['alias'].gsub( '<br>', ',' )}\t#{e['user']}\t#{e['def_fn']}\n" end
	puts "NB2020 [dic] data\n"
	puts export.force_encoding( 'UTF-8' )

when 'memory'
	export = ''
	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY};" )
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
