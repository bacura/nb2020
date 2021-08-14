#! /usr/bin/ruby
#encoding: utf-8
#fct browser pass as plain text 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'psss-text'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
puts "Content-type: text/text\n\n"

#### GETデータの取得
get_data = get_data()
toker = get_data['toker'].to_s

if toker != '' && toker != nil
  f = open( "#{$HTDOCS_PATH}/toker_/mod_#{toker}.R", mode = 'r:utf-8:utf-8' )
  f.each_line do |el|
    puts el.encode( 'Shift_JIS' )
  end
else
  puts "No code"
end



#puts weight.encode( 'Shift_JIS' )
#puts item_name.encode( 'Shift_JIS' )
#puts item_unit.encode( 'Shift_JIS' )
#puts item_opt.encode( 'Shift_JIS' )
