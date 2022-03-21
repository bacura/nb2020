#! /usr/bin/ruby
#encoding: utf-8
#fct browser plain text 0.03b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'plain-text'


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
food_weight = food_weight.to_f


# 全ての栄養素を取得
r = mdb( "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no}';", false, @debug )
txt = ''
@fct_item.each do |e|
  if e == 'FG' ||  e == 'FN' || e == 'SID' || e == 'Tagnames'
    txt << "#{@fct_name[e]}\t\t#{r.first[e]}\n"
  else
    t = num_opt( r.first[e], food_weight, frct_mode, @fct_frct[e] )
    txt << "#{@fct_name[e]}\t#{@fct_unit[e]}\t#{t}\n"
  end
end

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


puts weight
puts txt