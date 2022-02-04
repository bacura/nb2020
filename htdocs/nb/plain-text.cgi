#! /usr/bin/ruby
#encoding: utf-8
#fct browser plain text 0.02b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'plain-text'
@fct_start = 4


#==============================================================================
#DEFINITION
#==============================================================================

#### Language init
def lp_init( script, language_set )
  f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{language_set}", "r" )
  lp = [nil]
  f.each do |line|
    lp << line.chomp.force_encoding( 'UTF-8' )
  end
  f.close

  return lp
end


#==============================================================================
# Main
#==============================================================================
puts "Content-type: text/text\n\n"

puts "Getting GET\n" if @debug
get_data = get_data()
frct_mode = get_data['frct_mode'].to_i
food_weight = BigDecimal( get_data['food_weight'] )
food_no = get_data['food_no']
lg = get_data['lg']
lg = $DEFAULT_LP if lg = '' || lg = nil
lp = lp_init( script, lg )


puts "Food weight\n" if @debug
food_weight = 100 if food_weight == nil || food_weight == ''
food_weight = food_weight.to_i


# 全ての栄養素を取得
r = mdb( "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no}';", false, @debug )
fct_opt = Hash.new
@fct_item.each do |e| fct_opt[e] = num_opt( r.first[e], food_weight, frct_mode, @fct_frct[e] ) end


fraction = ''
if frct_mode == 1
	fraction = lp[1]
elsif frct_mode == 2
	fraction = lp[2]

elsif frct_mode == 3
	fraction = lp[3]
else
	fraction = lp[1]
end
weight = "#{lp[5]} #{food_weight} #{lp[6]} （#{fraction}）\n"


item_name = "#{@fct_name['FN']}\t#{@fct_name['SID']}\t#{@fct_name['Tagnames']}\t"
@fct_start.upto( @fct_end ) do |c| item_name << "#{@fct_name[@fct_item[c]]}\t" end
item_name.chop
item_name << "\n"


item_unit = "#{@fct_unit['FN']}\t#{@fct_unit['SID']}\t#{@fct_unit['Tagnames']}\t"
@fct_start.upto( @fct_end ) do |c| item_unit << "#{@fct_unit[@fct_item[c]]}\t" end
item_unit.chop
item_unit << "\n"


item_opt = "#{fct_opt['FN']}\t#{fct_opt['SID']}\t#{fct_opt['Tagnames']}\t"
@fct_start.upto( @fct_end ) do |c| item_opt << "#{fct_opt[@fct_item[c]]}\t" end
item_opt.chop
item_opt << "\n"


puts weight.encode( 'Shift_JIS' )
puts item_name.encode( 'Shift_JIS' )
puts item_unit.encode( 'Shift_JIS' )
puts item_opt.encode( 'Shift_JIS' )
