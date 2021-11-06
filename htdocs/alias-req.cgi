#! /usr/bin/ruby
# coding: utf-8
#Nutrition browser search alias request 0.12b


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'alias-req'

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


#### Geeting POST
food_no = cgi['food_no']
request_alias = cgi['alias']
if @debug
	puts "food_no: #{food_no}<br>"
	puts "request_alias: #{request_alias}<br>"
	puts "<hr>"
end

#### Update alias
if request_alias != '' && request_alias != nil
	mdb( "INSERT INTO #{$MYSQL_TB_SLOGF} SET code='#{food_no}', user='#{user.name}', words='#{request_alias}', date='#{@datetime}';", false, @debug )
end
