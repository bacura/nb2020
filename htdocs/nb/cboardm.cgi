#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 cutting board monitor 0.03b (2023/05/07)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'

#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug


#### POST
food_no = @cgi['food_no']
food_weight = @cgi['food_weight']
food_check = @cgi['food_check']
base_fn = @cgi['base_fn']
mode = @cgi['mode']

food_weight = BigDecimal( food_weight_check( food_weight ).first )


if user.name
	# Loading CB
	r = mdb( "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	sum = r.first['sum'].split( "\t" )
	cb_num = sum.size
	new_sum = ''

	if mode == 'add'
		# Generating new SUM
		if cb_num == 0
			new_sum = "#{food_no}:#{food_weight}:g:#{food_weight}:#{food_check}::1.0:#{food_weight}"
		else
			new_sum = "#{r.first['sum']}\t#{food_no}:#{food_weight}:g:#{food_weight}:#{food_check}::1.0:#{food_weight}"
		end

		# Updating CB
		mdb( "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{user.name}';", false, @debug )
		cb_num += 1
		puts cb_num

		# Updating history
		add_his( user.name, food_no )

	elsif mode == 'change'
		sum.each do |e|
			t = e.split( ':' )
			if t[0] == base_fn
				new_sum << "#{food_no}:#{t[1]}:#{food_weight}:#{t[3]}:#{t[4]}:#{t[5]}:#{t[6]}:#{t[7]}\t"
			else
				new_sum << "#{e}\t"
			end
		end
		new_sum.chop!

		# Updating CB
		mdb( "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{user.name}';", false, @debug )
		puts cb_num
	elsif mode == 'refresh'

		puts cb_num
	end
else
	puts '-'
end
