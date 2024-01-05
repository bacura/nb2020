#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 parallel foods 0.10b (2024/01/02)


#==============================================================================
#LIBRARY
#==============================================================================
require './nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
fn_num = 25


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================

fn = []
food_name = Hash.new
energy = []
para_fcts = [] 
@fct_para.size.times do
	para_fcts << Array.new
end
fctsn = [] 

#データ読み込み
res = $DB.query( "SELECT FCT.FN, ENERC_KCAL, NAME, #{@fct_para.join( ',' )} FROM #{$MYSQL_TB_FCT} AS FCT LEFT JOIN #{$MYSQL_TB_TAG} AS TAG ON FCT.FN=TAG.FN;" )
res.each do |e|
	fn << e['FN']
	energy = BigDecimal( convert_zero( e['ENERC_KCAL'] ))
	energy = 1 if energy == 0

	@fct_para.each.with_index( 0 ) do |ee, i|
		para_fcts[i] << BigDecimal( convert_zero( e[ee] )) / energy
	end

	food_name[e['FN']] = e['NAME']
end
size_ = fn.size

#正規化
para_fcts.each do |ea|
	sum_ = ea.sum
	mean_ = BigDecimal( sum_ / size_ )

	diff_sq_ = ea.map do |x| ( x - mean_ ) ** 2 end
	sd_ = Math.sqrt( diff_sq_.sum / size_ )
	fctsn << ea.map do |x| (( x - mean_ ) / sd_) end
end

#ユークリッド距離の算出(FLAT)
dista = Hash.new
fn.each.with_index do |e, i|
	base_name = food_name[e]
	dista = {}

	size_.times do |j|
		fn_vs = fn[j]
		target_name = food_name[fn_vs]

		unless base_name == target_name
			d = BigDecimal( 0 )
			@fct_para.size.times do |k|
				d += ( fctsn[k][i] - fctsn[k][j] ) ** 2
			end
			dista[fn[j]] = Math.sqrt( d )
		end
	end

	sorted_dista = dista.sort_by do |_, v| v end
	dista_near = sorted_dista.first( fn_num )

	near_mem = "flat\t#{e}\t"
	dista_near.to_h.each_key do |k|
  		near_mem << "'#{k}',"
  	end
	near_mem.chop!
	puts near_mem
end

#ユークリッド距離の算出(JUTEN)
@fct_para.each do |juten|
	fn.each.with_index do |e, i|
		base_name = food_name[e]
		dista = {}

		size_.times do |j|
			fn_vs = fn[j]
			target_name = food_name[fn_vs]

			unless base_name == target_name
				d = BigDecimal( 0 )
				@fct_para.each.with_index do |ee, k|
					if juten != ee
						d += ( fctsn[k][i] - fctsn[k][j] ) ** 2
					else
						d += (( fctsn[k][i] - fctsn[k][j] ) / 3 ) ** 2
					end
				end
				dista[fn[j]] = Math.sqrt( d )
			end
		end

		sorted_dista = dista.sort_by do |_, v| v end
		dista_near = sorted_dista.first( fn_num )

		near_mem = "#{juten}\t#{e}\t"
		dista_near.to_h.each_key do |k|
	  		near_mem << "'#{k}',"
	  	end
		near_mem.chop!
		puts near_mem
	end
end

