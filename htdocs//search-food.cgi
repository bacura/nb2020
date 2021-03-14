#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser food search 0.00

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'search-food'


#==============================================================================
#DEFINITION
#==============================================================================

#### getting gycv result
def gycv_result()
	h = Hash.new
	r = mdb( "SELECT FN FROM #{$MYSQL_TB_EXT} WHERE gycv='1';", false, @debug )
	r.each do |e|
		rr = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false, @debug )
		h["#{rr.first['FG']}:#{rr.first['class1']}:#{rr.first['class2']}:#{rr.first['class3']}:#{rr.first['name']}"] = 1
	end

	return h
end


### getting shun result
def shun_result( words )
	sm = 0
	words.tr!( "０-９", "0-9" ) if /[０-９]/ =~ words
	a = words.scan( /\d+/ )
	if a.size == 0
		sm = @time_now.month
	else
		sm = a[0].to_i
	end

	h = Hash.new
	r = mdb( "SELECT FN, shun1s, shun1e, shun2s, shun2e FROM #{$MYSQL_TB_EXT} WHERE ( shun1s IS NOT NULL ) AND shun1s!=0;", false, @debug )
	r.each do |e|
		flag = false
		sm_ = sm
		s1s = e['shun1s']
		s1e = e['shun1e']
		if s1s > s1e
			s1e += 12
			sm_ += 12 if sm_ < s1s
		end
		flag = true if s1s <= sm_ && sm_ <= s1e

		if e['shun2s'] != 0
			sm_ = sm
			s2s = e['shun2s']
			s2e = e['shun2e']
			if s2s > s2e
				s2e += 12
				sm_ += 12 if sm_ < s2s
			end
			flag = true if s2s <= sm_ && sm_ <= s2e
		end

		if flag
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false, @debug )
			h["#{rr.first['FG']}:#{rr.first['class1']}:#{rr.first['class2']}:#{rr.first['class3']}:#{rr.first['name']}"] = 1
		end
	end

	return h, sm
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### POSTデータの取得
words = @cgi['words']
words.gsub!( /\s+/, "\t")
words.gsub!( /　+/, "\t")
words.gsub!( /,+/, "\t")
words.gsub!( /、+/, "\t")
words.gsub!( /\t{2,}/, "\t")
query_word = words.split( "\t" )
query_word.uniq!
if @debug
	puts "query_word: #{query_word}<br>"
	puts "<hr>"
end


result_keys_hash = Hash.new
true_query = []
if /#{lp[1]}/ =~ words || /#{lp[2]}/ =~ words
	result_keys_hash = gycv_result()
	words = lp[3]

elsif /#{lp[4]}/ =~ words
	result_keys_hash, sm = shun_result( words )
	words = "#{sm}#{lp[5]}"

else
	puts "Dictionary<br>" if @debug
	words_count = 0
	result_keys = []
	query_word.each do |e|
		# 記録
		mdb( "INSERT INTO #{$MYSQL_TB_SLOGF} SET user='#{user.name}', words='#{e}', date='#{@datetime}';", false, @debug )

		# 変換
		r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{e}';", false, @debug )
		true_query << r.first['org_name'] if r.first
	end

	puts "Search & generate food key #{true_query}<br>" if @debug
	if true_query.size > 0
		true_query.each do |e|
			# 名前で検索
			r = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE name='#{e}';", false, @debug )
			r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

			# クラス3で検索
			r = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class3='#{e}';", false, @debug )
			r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

			# クラス2で検索
			r = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class2='#{e}';", false, @debug )
			r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

			# クラス1で検索
			r = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class1='#{e}';", false, @debug )
			r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

			# 食品キーのカウント
			result_keys.uniq!
			result_keys.each do |ee|
				result_keys_hash[ee] = 0 if result_keys_hash[ee] == nil
				result_keys_hash[ee] += 1
			end

			# 検索結果コードの記録
			mdb( "UPDATE #{$MYSQL_TB_SLOGF} SET code='#{result_keys.size}' WHERE user='#{user.name}' AND words='#{query_word[words_count]}' AND date='#{@datetime}';", false, @debug )
			words_count += 1
		end
	else
		# 検索結果無しコードの記録
		query_word.each do |e| mdb( "UPDATE #{$MYSQL_TB_SLOGF} SET code='0' WHERE user='#{user.name}' AND words='#{e}' AND date='#{@datetime}';", false, @debug ) end
	end
end


#### 食品キーのソート
result_keys_sort = result_keys_hash.sort_by{|k, v| -v }


html = ''
if result_keys_sort.size > 0
	html << "<h6>#{lp[6]} #{words}: #{result_keys_sort.size}#{lp[7]}</h6>"
	result_keys_sort.each do |e|
		# サブクラス処理
		class1_sub = ''
		class2_sub = ''
		class3_sub = ''
		class_space = ''
		a = e[0].split( ':' )
		class1_sub = "<span class='tagc'>#{a[1].sub( '+', '' )}</span>" if /\+/ =~ a[1]
		class2_sub = "<span class='tagc'>#{a[2].sub( '+', '' )}</span>" if /\+/ =~ a[2]
		class3_sub = "<span class='tagc'>#{a[3].sub( '+', '' )}</span>" if /\+/ =~ a[3]
		class_space = ' ' unless class1_sub == '' and class2_sub == '' and class3_sub == ''

		button_class = "class='btn btn-outline-secondary btn-sm nav_button'"
		button_class = "class='btn btn-outline-primary btn-sm nav_button visited'" if e[1] == true_query.size

		html << "<button type='button' #{button_class} onclick=\"summonL5( '#{e[0]}', '1' )\">#{class1_sub}#{class2_sub}#{class3_sub}#{class_space}#{a[4]}</button>\n"
	end
else
	html << "<h6>#{lp[6]} #{words}: 0 #{lp[7]}</h6>"
	html << "<h6>#{lp[8]}</h6>"

end

puts html
