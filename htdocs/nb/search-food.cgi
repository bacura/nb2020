#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser food search 0.10 (2023/07/22)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'gy' 	=> "緑黄",\
		'gyh' 	=> "りょくおう",\
		'gycv' 	=> "緑黄色野菜",\
		'shun' 	=> "旬",\
		'month' => "月が旬の食材",\
		'result' 	=> "検索結果:",\
		'ken' 	=> "件",\
		'non' 	=> "該当する食品は見つかりませんでした。",\
		'food_no' 	=> "食品番号"
	}

	return l[language]
end


#### getting gycv result
def gycv_result( db )
	h = Hash.new

	r = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN IN ( SELECT FN FROM #{$MYSQL_TB_EXT} WHERE gycv='1' );", false )
	r.each do |e|
		h["#{e['FG']}:#{e['class1']}:#{e['class2']}:#{e['class3']}:#{e['name']}"] = 1
	end

	return h
end


### getting shun result
def shun_result( db, words )
	sm = 0
	words.tr!( "０-９", "0-9" ) if /[０-９]/ =~ words
	a = words.scan( /\d+/ )
	if a.size == 0
		sm = @time_now.month
	else
		sm = a[0].to_i
	end

	h = Hash.new
	r = db.query( "SELECT FN, shun1s, shun1e, shun2s, shun2e FROM #{$MYSQL_TB_EXT} WHERE ( shun1s IS NOT NULL ) AND shun1s!=0;", false )
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
			rr = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false )
			h["#{rr.first['FG']}:#{rr.first['class1']}:#{rr.first['class2']}:#{rr.first['class3']}:#{rr.first['name']}"] = 1
		end
	end

	return h, sm
end

#### food number result
def fn_result( db, code )
	h = Hash.new
	r = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false )
	if r.first
		h["#{r.first['FG']}:#{r.first['class1']}:#{r.first['class2']}:#{r.first['class3']}:#{r.first['name']}"] = 1
	end

	return h
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )


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
if /#{l['gy']}/ =~ words || /#{l['gyh']}/ =~ words
	result_keys_hash = gycv_result( db )
	words = l['gycv']

elsif /#{l['shun']}/ =~ words
	result_keys_hash, sm = shun_result( db, words )
	words = "#{sm}#{l['month']}"

elsif /\d{5}/ =~ words
	result_keys_hash = fn_result( db, words )
	words = "#{l['food_no']}[#{words}]"

else
	puts "Dictionary<br>" if @debug
	words_count = 0
	result_keys = []
	query_word.each do |e|
		# Record into slogf
		db.query( "INSERT INTO #{$MYSQL_TB_SLOGF} SET user='#{user.name}', words='#{e}', date='#{@datetime}';", true )

		# 変換
		r = db.query( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{e}';", true )
		true_query << r.first['org_name'] if r.first
	end

	puts "Search & generate food key #{true_query}<br>" if @debug
	if true_query.size > 0
		true_query.each do |e|
			r = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE name LIKE '%#{e}%' OR class1 LIKE '%#{e}%' OR class2 LIKE '%#{e}%'  OR class3 LIKE '%#{e}%';", false )
			r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

			# 食品キーのカウント
			result_keys.uniq!
			result_keys.each do |ee|
				result_keys_hash[ee] = 0 if result_keys_hash[ee] == nil
				result_keys_hash[ee] += 1
			end

			# 検索結果コードの記録
			db.query( "UPDATE #{$MYSQL_TB_SLOGF} SET code='#{result_keys.size}' WHERE user='#{user.name}' AND words='#{query_word[words_count]}' AND date='#{@datetime}';", true )
			words_count += 1
		end
	else
		# 検索結果無しコードの記録
		query_word.each do |e| db.query( "UPDATE #{$MYSQL_TB_SLOGF} SET code='0' WHERE user='#{user.name}' AND words='#{e}' AND date='#{@datetime}';", true ) end
	end
end


#### 食品キーのソート
result_keys_sort = result_keys_hash.sort_by{|k, v| -v }


html = ''
if result_keys_sort.size > 0
	html << "<h6>#{l['result']} #{words}: #{result_keys_sort.size}#{l['ken']}</h6>"
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

		html << "<button type='button' #{button_class} onclick=\"viewDetailSub( 'init', '#{e[0]}', '1' )\">#{class1_sub}#{class2_sub}#{class3_sub}#{class_space}#{a[4]}</button>\n"
	end
else
	html << "<h6>#{l['result']} #{words}: 0 #{l['ken']}</h6>"
	html << "<h6>#{l['non']}</h6>"

end

puts html
