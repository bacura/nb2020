#! /usr/bin/ruby
#encoding: utf-8
# Nutrition browser food search 0.1.1.AI (2024/09/09)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
# LIBRARY
#==============================================================================
require './soul'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	language_data = {}

	# Japanese
	language_data['jp'] = {
		gy: "緑黄",
		gyh: "りょくおう",
		gycv: "緑黄色野菜",
		shun: "旬",
		month: "月が旬の食材",
		result: "検索結果:",
		ken: "件",
		non: "該当する食品は見つかりませんでした。",
		food_no: "食品番号"
	}

	return language_data[language]
end

# Getting gycv result
def gycv_result( db )
	results_hash = Hash.new

	r = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN IN ( SELECT FN FROM #{$MYSQL_TB_EXT} WHERE gycv='1' );", false )
	r.each do |entry|
		results_hash["#{entry['FG']}:#{entry['class1']}:#{entry['class2']}:#{entry['class3']}:#{entry['name']}"] = 1
	end

	return results_hash
end

# Getting shun result
def shun_result( db, words )
	search_month = 0
	words.tr!( "０-９", "0-9" ) if /[０-９]/ =~ words
	numbers = words.scan( /\d+/ )
	search_month = numbers.empty? ? @time_now.month : numbers[0].to_i

	results_hash = Hash.new
	r = db.query( "SELECT FN, shun1s, shun1e, shun2s, shun2e FROM #{$MYSQL_TB_EXT} WHERE ( shun1s IS NOT NULL ) AND shun1s!=0;", false )
	r.each do |entry|
		is_in_season = false
		sm_adjusted = search_month
		shun1_start = entry['shun1s']
		shun1_end = entry['shun1e']
		if shun1_start > shun1_end
			shun1_end += 12
			sm_adjusted += 12 if sm_adjusted < shun1_start
		end
		is_in_season = true if shun1_start <= sm_adjusted && sm_adjusted <= shun1_end

		if entry['shun2s'] != 0
			sm_adjusted = search_month
			shun2_start = entry['shun2s']
			shun2_end = entry['shun2e']
			if shun2_start > shun2_end
				shun2_end += 12
				sm_adjusted += 12 if sm_adjusted < shun2_start
			end
			is_in_season = true if shun2_start <= sm_adjusted && sm_adjusted <= shun2_end
		end

		if is_in_season
			related_result = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{entry['FN']}';", false )
			results_hash["#{related_result.first['FG']}:#{related_result.first['class1']}:#{related_result.first['class2']}:#{related_result.first['class3']}:#{related_result.first['name']}"] = 1
		end
	end

	return results_hash, search_month
end

# Food number result
def fn_result( db, code )
	results_hash = {}
	r = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false )
	if r.first
		results_hash["#{r.first['FG']}:#{r.first['class1']}:#{r.first['class2']}:#{r.first['class3']}:#{r.first['name']}"] = 1
	end

	return results_hash
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )

# POSTデータの取得
words = @cgi['words']
words.gsub!( /\s+/, "\t")
words.gsub!( /　+/, "\t")
words.gsub!( /,+/, "\t")
words.gsub!( /、+/, "\t")
words.gsub!( /\t{2,}/, "\t")
query_words = words.split( "\t" ).uniq!


if @debug
	puts "query_words: #{query_words}<br>"
	puts "<hr>"
end

results_hash = {}
true_queries = []
if /#{l[:gy]}/ =~ words || /#{l[:gyh]}/ =~ words
	results_hash = gycv_result( db )
	words = l[:gycv]

elsif /#{l[:shun]}/ =~ words
	results_hash, search_month = shun_result( db, words )
	words = "#{search_month}#{l[:month]}"

elsif /\d{5}/ =~ words
	results_hash = fn_result( db, words )
	words = "#{l[:food_no]}[#{words}]"

else
	puts "Dictionary<br>" if @debug
	word_count = 0
	result_keys = []

	query_words.each do |word|
		db.query( "INSERT INTO #{$MYSQL_TB_SLOGF} SET user='#{user.name}', words='#{word}', date='#{@datetime}';", true )

		dictionary_result = db.query( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{word}';", true )
		true_queries << dictionary_result.first['org_name'] if dictionary_result.first
	end

	puts "Search & generate food key #{true_queries}<br>" if @debug

	if true_queries.size > 0
		true_queries.each do |query|
			r = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE name LIKE '%#{query}%' OR class1 LIKE '%#{query}%' OR class2 LIKE '%#{query}%'  OR class3 LIKE '%#{query}%';", false )
			r.each do |entry|
				result_keys << "#{entry['FG']}:#{entry['class1']}:#{entry['class2']}:#{entry['class3']}:#{entry['name']}"
			end

			result_keys.uniq!
			result_keys.each { |key| results_hash[key] = ( results_hash[key] || 0 ) + 1 }

			db.query( "UPDATE #{$MYSQL_TB_SLOGF} SET code='#{result_keys.size}' WHERE user='#{user.name}' AND words='#{query_words[word_count]}' AND date='#{@datetime}';", true )
			word_count += 1
		end
	else
		query_words.each do |word|
			db.query( "UPDATE #{$MYSQL_TB_SLOGF} SET code='0' WHERE user='#{user.name}' AND words='#{word}' AND date='#{@datetime}';", true )
		end
	end
end

# 食品キーのソート
sorted_result_keys = results_hash.sort_by { |_, count| -count }

html_content = ''
if sorted_result_keys.size > 0
	html_content << "<h6>#{l[:result]} #{words}: #{sorted_result_keys.size}#{l[:ken]}</h6>"
	sorted_result_keys.each do |entry|
		class1_sub, class2_sub, class3_sub, class_space = '', '', '', ''
		entry_data = entry[0].split( ':' )
		class1_sub = "<span class='tagc'>#{entry_data[1].sub( '+', '' )}</span>" if /\+/ =~ entry_data[1]
		class2_sub = "<span class='tagc'>#{entry_data[2].sub( '+', '' )}</span>" if /\+/ =~ entry_data[2]
		class3_sub = "<span class='tagc'>#{entry_data[3].sub( '+', '' )}</span>" if /\+/ =~ entry_data[3]
		class_space = ' ' unless class1_sub.empty? && class2_sub.empty? && class3_sub.empty?

		button_class = "class='btn btn-outline-secondary btn-sm nav_button'"
		button_class = "class='btn btn-outline-primary btn-sm nav_button visited'" if entry[1] == true_queries.size

		html_content << "<button type='button' #{button_class} onclick=\"viewDetailSub( 'init', '#{entry[0]}', '1' )\">#{class1_sub}#{class2_sub}#{class3_sub}#{class_space}#{entry_data[4]}</button>\n"
	end
else
	html_content << "<h6>#{l[:result]} #{words}: 0 #{l[:ken]}</h6>"
	html_content << "<h6>#{l[:non]}</h6>"
end

puts html_content
