#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 food ranking 0.11b


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'food-rank'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
#user.debug if @debug
lp = user.load_lp( script )


#### POST
command = @cgi['command']
ex_inf = @cgi['ex_inf'].to_i
ex_zero = @cgi['ex_zero'].to_i
p command, ex_inf, ex_zero, '<hr>' if @debug


main_item = 'ENERC_KCAL'
comp_item = 'weight'
rank_order = 0
rank_display = 50

list_html = ''
if command == 'list'
	puts 'Lsit<br>' if @debug
	main_item = @cgi['main_item'].to_s
	comp_item = @cgi['comp_item'].to_s

	rank_order = @cgi['rank_order'].to_i
	rank_display = @cgi['rank_display'].to_i
	p main_item, comp_item, rank_order, rank_display, '<hr>' if @debug

	comp_sql = nil
	comp_flag = false
	if comp_item != 'weight' && comp_item != ''
		comp_sql = ", #{comp_item}"
		comp_flag = true
	end

	r = mdb( "SELECT FN, #{main_item} #{comp_sql} FROM #{$MYSQL_TB_FCT};", false, @debug )
	main_value = Hash.new
	comp_value = Hash.new
	ratio = Hash.new

	puts 'Zero process<br>' if @debug
	r.each do |r|
		food_no = r['FN']
		main_value[food_no] = BigDecimal( convert_zero( r[main_item] ).to_s )
		if comp_flag
			comp_value[food_no] =  BigDecimal( convert_zero( r[comp_item] ).to_s )
			if comp_value[food_no] != 0
				# normal
				ratio[food_no] = ( main_value[food_no] / comp_value[food_no] ).round( 4 )
			elsif main_value[food_no] == 0 && comp_value[food_no] == 0
				# zero / zero
				ratio[food_no] = 0
			else
				#infinity
				ratio[food_no] = 99999999
			end
		else
			comp_value[food_no] = 1
			ratio[food_no] = main_value[food_no]
		end
	end
	a = ratio.sort_by do |_, v| v end
	a.reverse! if rank_order == 0
	ratio = a.to_h

	puts 'Rank HTML<br>' if @debug
	list_html = '<table class="table table-sm">'
	list_html << '<thead>'
	list_html << '<tr>'
	list_html << "<td>#{lp[7]}</td><td>#{lp[8]}</td><td>#{lp[9]}</td><td>#{@fct_name[main_item]}</td><td>#{@fct_name[comp_item]}</td><td>#{lp[10]}</td><td>&nbsp;</td>"
	list_html << '</tr>'
	list_html << '</thead>'

	food_tag = Hash.new
	rr = mdb( "SELECT * FROM #{$MYSQL_TB_TAG};", false, @debug )
	rr.each do |rr| food_tag[rr['FN']] = rr end

	recipei = Hash.new
	rr = mdb( "SELECT word FROM #{$MYSQL_TB_RECIPEI} WHERE user='#{user.name}' OR public=1;", false, @debug )
	rr.each do |rr| recipei[rr['word']] = true end

	count = 1
	ratio.each do |k, v|
		sub_class = ''
		sub_class << food_tag[k]['class1'].sub( '+', '' ) if /\+$/ =~ food_tag[k]['class1']
		sub_class << food_tag[k]['class2'].sub( '+', '' ) if /\+$/ =~ food_tag[k]['class2']
		sub_class << food_tag[k]['class3'].sub( '+', '' ) if /\+$/ =~ food_tag[k]['class3']
		food_name = food_tag[k]['name']
		tag1 = food_tag[k]['tag1']
		tag2 = food_tag[k]['tag2']
		tag3 = food_tag[k]['tag3']
		tag4 = food_tag[k]['tag4']
		tag5 = food_tag[k]['tag5']
		tags = "<span class='tagc'>#{sub_class}</span> #{food_name} <span class='tag1'>#{tag1}</span> <span class='tag2'>#{tag2}</span> <span class='tag3'>#{tag3}</span> <span class='tag4'>#{tag4}</span> <span class='tag5'>#{tag5}</span>"

		recipe_serch = ''
		recipe_serch = "<span class='badge bg-info text-dark' onclick=\"searchDR( '#{food_name}' )\">#{lp[11]}</span>" if recipei[food_name] == true

		unless ( v == 99999999 && ex_inf == 1 ) || ( v == 0 && ex_zero == 1 )
			list_html << '<tr>'
			list_html << "<td>#{count}</td>"
			list_html << "<td>#{k}</td>"
			list_html << "<td class='link_cursor' onclick=\"detailView_his( '#{k}' )\">#{tags}</td>"
			list_html << "<td>#{main_value[k].to_f}</td>"
			list_html << "<td>#{comp_value[k].to_f}</td>"

			if v == 99999999
				list_html << "<td>∞</td>"
			else
				list_html << "<td>%.4f</td>" % v.to_f
			end

			list_html << "<td>#{recipe_serch}</td>"
			list_html << '</tr>'
		end

		break if count == rank_display
		count += 1
	end
	list_html << '</table>'
end


####
puts 'Main item select-HTML<br>' if @debug
main_item_select = '<select class="form-select" id="main_item">'
@fct_item.each do |e|
	unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
		s = ''
		s = 'SELECTED' if e == main_item
		main_item_select << "<option value='#{e}' #{s}>#{@fct_name[e]}</option>"
	end
end
main_item_select << '</select>'


####
puts 'Comp item select-HTML<br>' if @debug
comp_item_select = '<select class="form-select" id="comp_item">'
comp_item_select << "<option value='weight'>#{lp[3]}</option>"
@fct_item.each do |e|
	unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
		s = ''
		s = 'SELECTED' if e == comp_item
		comp_item_select << "<option value='#{e}' #{s}>#{@fct_name[e]}</option>"
	end
end
comp_item_select << '</select>'


####
rank_order_select = '<select class="form-select form-select-sm" id="rank_order">'
if rank_order == 0
	rank_order_select << "<option value='0' SELECTED>#{lp[4]}</option>"
	rank_order_select << "<option value='1'>#{lp[5]}</option>"
else
	rank_order_select << "<option value='0'>#{lp[4]}</option>"
	rank_order_select << "<option value='1' SELECTED>#{lp[5]}</option>"
end
rank_order_select << '</select>'


####
rank_nums = [ 50,  100,  500, 1000, 2000, 3000 ]
rank_nums_ = [ '50', '100',  '500', '1000', '2000', 'all' ]
rank_display_select = '<select class="form-select" id="rank_display">'
rank_nums.size.times do |c|
	s = ''
	s = 'SELECTED' if rank_display == rank_nums[c]
	rank_display_select << "<option value='#{rank_nums[c]}' #{s}>#{rank_nums_[c]}</option>"
end


ex_inf_check = ''
ex_inf_check = 'CHECKED' if ex_inf == 1


ex_zero_check = ''
ex_zero_check = 'CHECKED' if ex_zero == 1


puts "Control HTML<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-4'>
			<div class="input-group input-group-sm mb-3">
				<label class="input-group-text">#{lp[1]}</label>
				#{main_item_select}
			</div>
		</div>
		<div class='col-4'>
			<div class="input-group input-group-sm mb-3">
				<label class="input-group-text">#{lp[2]}</label>
				#{comp_item_select}
			</div>
		</div>
		<div class='col-4'>
			#{rank_order_select}
		</div>
	</div>
	<div class='row'>
		<div class='col-3'>
			<div class="input-group input-group-sm">
			<label class="input-group-text">表示数</label>
			<select class="form-select" id="rank_display">
				<option value="50">50</option>
				<option value="100">100</option>
				<option value="500">500</option>
				<option value="1000">1000</option>
				<option value="2000">2000</option>
				<option value="3000">all</option>
			</select>
			</div>
		</div>
		<div class='col-1'>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" id="ex_inf" #{ex_inf_check}>
				<label class="form-check-label">∞を除外</label>
			</div>
		</div>
		<div class='col-2'>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" id="ex_zero" #{ex_zero_check}>
				<label class="form-check-label">0を除外 (0/0含む)</label>
			</div>
		</div>
		<div class='col' align="right">
			<button class="btn btn-outline-primary btn-sm" type="button" onclick="foodRankList()">#{lp[6]}</button>
		</div>
	</div>
	<br>
	<div class='row'>
	#{list_html}
	</div>
</div>
HTML

puts html
