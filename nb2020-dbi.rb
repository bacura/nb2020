#! /usr/bin/ruby
#nb2020-dbi.rb 0.06b

#Bacura KYOTO Lab
#Saga Ukyo-ku Kyoto, JAPAN
#https://bacura.jp
#yossy@bacura.jp

#==============================================================================
#LIBRARY
#==============================================================================
require './nb2020-soul'


#==============================================================================
#DB
#==============================================================================
puts "CREATE DATABASE #{$MYSQL_DB};"
puts "CREATE DATABASE #{$MYSQL_DBR};"
puts ''
puts "CREATE USER '#{$MYSQL_USER}'@'#{$MYSQL_HOST}' IDENTIFIED BY '#{$MYSQL_PW}';"
puts "GRANT ALL ON #{$MYSQL_DB}.* TO '#{$MYSQL_USER}'@'#{$MYSQL_HOST}';"
puts "GRANT ALL ON #{$MYSQL_DBR}.* TO '#{$MYSQL_USER}'@'#{$MYSQL_HOST}';"
puts ''
puts "CREATE USER '#{$MYSQL_USERR}'@'#{$MYSQL_HOST}';"
puts "GRANT ALL ON #{$MYSQL_DBR}.* TO '#{$MYSQL_USERR}'@'#{$MYSQL_HOST}';"
puts "GRANT SELECT ON #{$MYSQL_DB}.#{$MYSQL_TB_RECIPE} TO '#{$MYSQL_USERR}'@'#{$MYSQL_HOST}';"
puts ''
puts "FLUSH PRIVILEGES;\n\n"
puts "Register the database and user as described above with administrator privileges."
puts "If you have already registered, skip to the next step.\n\n"
puts "[Enter]"
gets.chomp
#==============================================================================
#DEFINITION
#==============================================================================


#### Updating fct table.
def fct_update( source_file )
	query = 'DELETE FROM fct;'
	$DB.query( query )

	f = open( source_file, 'r' )
	label = true
	f.each_line do |e|
		items = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )

		query = "INSERT INTO #{$MYSQL_TB_FCT} SET"
		@fct_item.size.times do |c|
			query << " #{@fct_item[c]}='#{items[c]}',"
		end
		query.chop!
		query << ";"

		$DB.query( query ) unless label
		label = false
	end
	f.close
	puts 'fct table has been updated.'
end


#### Making fct table.
def fct_init( source_file )
	query = "SHOW TABLES LIKE 'fct';"
	res = $DB.query( query )
	if res.first
		puts 'fct table already exists.'
		fct_update( source_file )
	else
		query = 'CREATE TABLE fct (FG VARCHAR(2),FN VARCHAR(5) NOT NULL PRIMARY KEY,SID SMALLINT UNSIGNED,Tagnames VARCHAR(255),REFUSE TINYINT UNSIGNED,ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(8),PROTCAA VARCHAR(8),PROT VARCHAR(8),FATNLEA VARCHAR(8),CHOLE VARCHAR(8),FAT VARCHAR(8),CHOAVLM VARCHAR(8),CHOAVL VARCHAR(8),CHOAVLMF VARCHAR(8),FIB VARCHAR(8),POLYL VARCHAR(8),CHOCDF VARCHAR(8),OA VARCHAR(8),ASH VARCHAR(8),NA VARCHAR(8),K VARCHAR(8),CA VARCHAR(8),MG VARCHAR(8),P VARCHAR(8),FE VARCHAR(8),ZN VARCHAR(8),CU VARCHAR(8),MN VARCHAR(8),ID VARCHAR(8),SE VARCHAR(8),CR VARCHAR(8),MO VARCHAR(8),RETOL VARCHAR(8),CARTA VARCHAR(8),CARTB VARCHAR(8),CRYPXB VARCHAR(8),CARTBEQ VARCHAR(8),VITA_RAE VARCHAR(8),VITD VARCHAR(8),TOCPHA VARCHAR(8),TOCPHB VARCHAR(8),TOCPHG VARCHAR(8),TOCPHD VARCHAR(8),VITK VARCHAR(8),THIAHCL VARCHAR(8),RIBF VARCHAR(8),NIA VARCHAR(8),NE VARCHAR(8),VITB6A VARCHAR(8),VITB12 VARCHAR(8),FOL VARCHAR(8),PANTAC VARCHAR(8),BIOT VARCHAR(8),VITC VARCHAR(8),ALC VARCHAR(8),NACL_EQ VARCHAR(8),Notice VARCHAR(255));'
		$DB.query( query )

		f = open( source_file, 'r' )
		label = true
		f.each_line do |e|
			items = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )

			query = "INSERT INTO #{$MYSQL_TB_FCT} SET"
			@fct_item.size.times do |c|
				query << " #{@fct_item[c]}='#{items[c]}',"
			end
			query.chop!
			query << ";"

			$DB.query( query ) unless label
			label = false
		end
		f.close
		puts 'fct table has been created.'
	end
end


#### Updating food tag table.
def tag_update( source_file )
	query = 'DELETE FROM tag WHERE user IS NULL;'
	res = $DB.query( query )

	# タグテーブルから読み込んでタグテーブル更新
	f = open( source_file, 'r' )
	label = true
	f.each_line do |e|
		items = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )
		sql_query_tag = "INSERT INTO #{$MYSQL_TB_TAG} SET"
		t = items[3]

		t.gsub!( '（', "｛" )
		t.gsub!( '＞　｛', "＞　（" )
		t.gsub!( '］　｛', "］　（" )
		t.gsub!( /^｛/, "（" )
		t.gsub!( '｛', '' )
		t.gsub!( 'もの｝', '' )

		t.gsub!( '　', "\t" )
		t.gsub!( '＞', "\t" )
		t.gsub!( '）', "\t" )
		t.gsub!( '］', "\t" )
		t.gsub!( "\s", "\t" )
		t.gsub!( /\t{2,}/, "\t" )
		t.gsub!( /\t+$/, '' )

		tags = t.split( "\t" )
		class1 = ''
		class2 = ''
		class3 = ''
		name_ = ''
		tag1 = ''
		tag2 = ''
		tag3 = ''
		tag4 = ''
		tag5 = ''
		count = 0

		tags.each do |ee|
			if /＜/ =~ ee
				class1 = ee.sub( '＜', '' )
			elsif /［/ =~ ee
				class2 = ee.sub( '［', '' )
			elsif /（/ =~ ee
				class3 = ee.sub( '（', '' )
			else
				case count
				when 0
					name_ = ee
					count += 1
				when 1
					tag1 = ee
					count += 1
				when 2
					tag2 = ee
					count += 1
				when 3
					tag3 = ee
					count += 1
				when 4
					tag4 = ee
					count += 1
				when 5
					tag5 = ee
					count += 1
				end
			end
		end
		sql_query_tag << " FG='#{items[0]}',FN='#{items[1]}',SID='#{items[2]}',name='#{name_}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='9';"
		$DB.query( sql_query_tag ) unless label
		label = false
	end
	f.close
	puts 'tag table has been updated.'
end


#### Making food tag table.
def tag_init( source_file )
	query = "SHOW TABLES LIKE 'tag';"
	res = $DB.query( query )
	if res.first
		puts 'tag table already exists.'
		tag_update( source_file )
	else
		query = 'CREATE TABLE tag (FG VARCHAR(2), FN VARCHAR(6), SID VARCHAR(5), user VARCHAR(32), name VARCHAR(64),class1 VARCHAR(64),class2 VARCHAR(64),class3 VARCHAR(64),tag1 VARCHAR(64),tag2 VARCHAR(64),tag3 VARCHAR(64),tag4 VARCHAR(64),tag5 VARCHAR(64), public TINYINT(1));'
		$DB.query( query )

		# タグテーブルから読み込んでタグテーブル更新
		f = open( source_file, 'r' )
		label = true
		f.each_line do |e|
			items = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )
			sql_query_tag = "INSERT INTO #{$MYSQL_TB_TAG} SET"
			t = items[3]

			t.gsub!( '（', "｛" )
			t.gsub!( '＞　｛', "＞　（" )
			t.gsub!( '］　｛', "］　（" )
			t.gsub!( /^｛/, "（" )
			t.gsub!( '｛', '' )
			t.gsub!( 'もの｝', '' )

			t.gsub!( '　', "\t" )
			t.gsub!( '＞', "\t" )
			t.gsub!( '）', "\t" )
			t.gsub!( '］', "\t" )
			t.gsub!( "\s", "\t" )
			t.gsub!( /\t{2,}/, "\t" )
			t.gsub!( /\t+$/, '' )

			tags = t.split( "\t" )
			class1 = ''
			class2 = ''
			class3 = ''
			name_ = ''
			tag1 = ''
			tag2 = ''
			tag3 = ''
			tag4 = ''
			tag5 = ''
			count = 0

			tags.each do |ee|
				if /＜/ =~ ee
					class1 = ee.sub( '＜', '' )
				elsif /［/ =~ ee
					class2 = ee.sub( '［', '' )
				elsif /（/ =~ ee
					class3 = ee.sub( '（', '' )
				else
					case count
					when 0
						name_ = ee
						count += 1
					when 1
						tag1 = ee
						count += 1
					when 2
						tag2 = ee
						count += 1
					when 3
						tag3 = ee
						count += 1
					when 4
						tag4 = ee
						count += 1
					when 5
						tag5 = ee
						count += 1
					end
				end
			end
			sql_query_tag << " FG='#{items[0]}',FN='#{items[1]}',SID='#{items[2]}',name='#{name_}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='9';"
			$DB.query( sql_query_tag ) unless label
			label = false
		end
		f.close
		puts 'tag table has been created.'
	end
end


#### Updating food extra tag table.
def ext_update( gycv_file, shun_file, unit_file )
	query = "SELECT FN FROM #{$MYSQL_TB_TAG};"
	res = $DB.query( query )
	res.each do |e|
		query = "UPDATE #{$MYSQL_TB_EXT} SET color1='0', color2='0', color1h='0', color2h='0' WHERE FN='#{e['FN']}';"
		$DB.query( query )
	end

	# Green/Yellow color vegitable
	f = open( gycv_file, 'r' )
	f.each_line do |e|
		food_no = e.chomp
		query = "UPDATE #{$MYSQL_TB_EXT} SET gycv='1' WHERE FN=#{food_no};"
		$DB.query( query )
	end
	f.close
	puts 'Green/Yellow color vegitable in ext has been updated.'

	# Shun
	f = open( shun_file, 'r' )
	f.each_line do |e|
		a = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )
		food_no = a[0]
		shun1s = a[2]
		shun1e = a[3]
		shun2s = a[4]
		shun2e = a[5]
		shun1s = 0 if shun1s == nil || shun1s == ''
		shun1e = 0 if shun1e == nil || shun1e == ''
		shun2s = 0 if shun2s == nil || shun2s == ''
		shun2e = 0 if shun2e == nil || shun2e == ''
		query = "UPDATE #{$MYSQL_TB_EXT} SET shun1s=#{shun1s}, shun1e=#{shun1e}, shun2s=#{shun2s}, shun2e=#{shun2e} WHERE FN='#{food_no}';"
		$DB.query( query )
	end
	f.close
	puts 'Shun in ext has been updated.'

	# Unit
	f = open( unit_file, 'r' )
	f.each_line do |e|
		a = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )
		food_no = a[0]
		unitc = a[2]
		unitn = a[3]
		query = "UPDATE #{$MYSQL_TB_EXT} SET unitc='#{unitc}', unitn='#{unitn}' WHERE FN='#{food_no}';"
		$DB.query( query )
	end
	f.close
	puts 'Unit in ext has been updated.'
end


#### Making food extra tag table.
def ext_init( gycv_file, shun_file, unit_file )
	query = "SHOW TABLES LIKE 'ext';"
	res = $DB.query( query )
	if res.first
		puts 'ext table already exists.'
		ext_update( gycv_file, shun_file, unit_file )
	else
		query = 'CREATE TABLE ext (FN VARCHAR(6), user VARCHAR(32), gycv TINYINT(1), allergen TINYINT(1), unitc VARCHAR(255), unitn VARCHAR(255), color1 TINYINT, color2 TINYINT, color1h TINYINT, color2h TINYINT, shun1s TINYINT(2), shun1e TINYINT(2), shun2s TINYINT(2), shun2e TINYINT(2));'
		$DB.query( query )

		query = "SELECT FN FROM #{$MYSQL_TB_TAG};"
		res = $DB.query( query )
		res.each do |e|
			query = "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{e['FN']}', color1='0', color2='0', color1h='0', color2h='0';"
			$DB.query( query )
		end
		puts 'ext table has been created.'

		# Green/Yellow color vegitable
		f = open( gycv_file, 'r' )
		f.each_line do |e|
			food_no = e.chomp
			query = "UPDATE #{$MYSQL_TB_EXT} SET gycv='1' WHERE FN=#{food_no};"
			$DB.query( query )
		end
		f.close
		puts 'Green/Yellow color vegitable in ext has been updated.'

		# Shun
		f = open( shun_file, 'r' )
		f.each_line do |e|
			a = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )
			food_no = a[0]
			shun1s = a[2]
			shun1e = a[3]
			shun2s = a[4]
			shun2e = a[5]
			shun1s = 0 if shun1s == nil || shun1s == ''
			shun1e = 0 if shun1e == nil || shun1e == ''
			shun2s = 0 if shun2s == nil || shun2s == ''
			shun2e = 0 if shun2e == nil || shun2e == ''
			query = "UPDATE #{$MYSQL_TB_EXT} SET shun1s=#{shun1s}, shun1e=#{shun1e}, shun2s=#{shun2s}, shun2e=#{shun2e} WHERE FN='#{food_no}';"
			$DB.query( query )
		end
		f.close
		puts 'Shun in ext has been updated.'

		# Unit
		f = open( unit_file, 'r' )
		f.each_line do |e|
			a = e.force_encoding( 'UTF-8' ).chomp.split( "\t" )
			food_no = a[0]
			unitc = a[2]
			unitn = a[3]
			query = "UPDATE #{$MYSQL_TB_EXT} SET unitc='#{unitc}', unitn='#{unitn}' WHERE FN='#{food_no}';"
			$DB.query( query )
		end
		f.close
		puts 'Unit in ext has been updated.'
	end
end


#### Making food dictionary table.
def dic_init()
	query = "SHOW TABLES LIKE 'dic';"
	res = $DB.query( query )
	if res.first
		puts 'dic table already exists.'
	else
		query = 'CREATE TABLE dic ( FG VARCHAR(2), org_name VARCHAR(64), alias VARCHAR(128) NOT NULL PRIMARY KEY, user VARCHAR(32));'
		$DB.query( query )
		puts 'dic table has been created.'

		res = $DB.query( "SELECT * FROM #{$MYSQL_TB_TAG};" )
		names = []
		sgh = Hash.new
		res.each do |e|
			names << e['name']
			sgh[e['name']] = e['FG']
			unless e['class1'] == ''
				names << e['class1']
				sgh[e['class1']] = e['FG']
			end
			unless e['class2'] == ''
				names << e['class2']
				sgh[e['class2']] = e['FG']
			end
			unless e['class3'] == ''
				names << e['class3']
				sgh[e['class3']] = e['FG']
			end
		end
		names.uniq!

		names.each do |e|
			sql_query_dic = "INSERT INTO #{$MYSQL_TB_DIC} SET FG='#{sgh[e]}', org_name='#{e}',alias='#{e}', user='#{$GM}';"
			$DB.query( sql_query_dic )
		end


		query = 'SELECT * FROM fct;'
		res = $DB.query( query )
		res.each do |e|
			food_no = e['FN']
			food_group = e['FG']
			notice = e['Notice']

			query = "SELECT name FROM tag WHERE FN='#{food_no}';"
			res2 = $DB.query( query )
			food_name = res2.first['name']

			if /別名/ =~ notice

				notice.gsub!( /食物.+/, '' )
				notice.gsub!( /歩留り.+/, '' )
				notice.gsub!( /試料.+/, '' )
				notice.gsub!( /原料.+/, '' )
				notice.gsub!( /原材.+/, '' )
				notice.gsub!( /廃棄.+/, '' )
				notice.gsub!( /損傷.+/, '' )
				notice.gsub!( /表層.+/, '' )
				notice.gsub!( /すじ.+/, '' )
				notice.gsub!( /さや.+/, '' )
				notice.gsub!( /しんを.+/, '' )
				notice.gsub!( /へた.+/, '' )
				notice.gsub!( /ゆでた.+/, '' )
				notice.gsub!( /硝酸.+/, '' )
				notice.gsub!( /植物.+/, '' )
				notice.gsub!( /茎部.+/, '' )
				notice.gsub!( /茎基.+/, '' )
				notice.gsub!( /根端.+/, '' )
				notice.gsub!( /根を.+/, '' )
				notice.gsub!( /根元.+/, '' )
				notice.gsub!( /水洗.+/, '' )
				notice.gsub!( /種子.+/, '' )
				notice.gsub!( /株元.+/, '' )
				notice.gsub!( /花床.+/, '' )
				notice.gsub!( /酸化.+/, '' )
				notice.gsub!( /果粒.+/, '' )
				notice.gsub!( /同一.+/, '' )
				notice.gsub!( /内臓.+/, '' )
				notice.gsub!( /三枚.+/, '' )
				notice.gsub!( /切り.+/, '' )
				notice.gsub!( /小型.+/, '' )
				notice.gsub!( /魚体.+/, '' )
				notice.gsub!( /幼魚.+/, '' )
				notice.gsub!( /卵巣.+/, '' )
				notice.gsub!( /腎臓.+/, '' )
				notice.gsub!( /※.+/, '' )
				notice.gsub!( /添付.+/, '' )
				notice.gsub!( /調理.+/, '' )
				notice.gsub!( /増加.+/, '' )
				notice.gsub!( /薄皮.+/, '' )
				notice.gsub!( /はく皮.+/, '' )
				notice.gsub!( /全.+/, '' )
				notice.gsub!( /果肉.+/, '' )
				notice.gsub!( /ビタミ.+/, '' )
				notice.gsub!( /液汁.+/, '' )
				notice.gsub!( /基.+/, '' )
				notice.gsub!( /茎葉.+/, '' )
				notice.gsub!( /穂軸.+/, '' )
				notice.gsub!( /両端.+/, '' )
				notice.gsub!( /表皮.+/, '' )
				notice.gsub!( /熟果.+/, '' )
				notice.gsub!( /果.+/, '' )
				notice.gsub!( /内容.+/, '' )
				notice.gsub!( /頭部.+/, '' )
				notice.gsub!( /材料.+/, '' )
				notice.gsub!( /皮.+/, '' )
				notice.gsub!( /皮及.+/, '' )
				notice.gsub!( /脂質.+/, '' )
				notice.gsub!( /部分.+/, '' )
				notice.gsub!( /使用.+/, '' )
				notice.gsub!( /無頭.+/, '' )
				notice.gsub!( /殻つき.+/, '' )
				notice.gsub!( /具材.+/, '' )
				notice.gsub!( /粉末.+/, '' )
				notice.gsub!( /調味.+/, '' )
				notice.gsub!( /液状だし.+/, '' )
				notice.gsub!( /食塩無添.+/, '' )
				notice.gsub!( /顆粒状の.+/, '' )
				notice.gsub!( /顆粒状の.+/, '' )
				notice.gsub!( /顆粒状の.+/, '' )
				notice.gsub!( /顆粒状の.+/, '' )
				notice.gsub!( /顆粒状の.+/, '' )
				notice.gsub!( /\(\d.+/, '' )
				notice.gsub!( /\d.+/, '' )
				notice.gsub!( /\*.+/, '' )

				notice.gsub!( 'あるいは', '、' )
				notice.gsub!( '別名：', '' )
				notice.gsub!( '別名:', '' )
				notice.gsub!( 'を含む', '' )
				notice.gsub!( '皮を除いたもの', '' )
				notice.gsub!( 'まくさ角寒天をゼリー状にしたもの', '' )
				notice.gsub!( 'まくさ角寒天をゼリー状にしたもの,', '' )
				notice.gsub!( '小豆こしあん入り', '' )
				notice.gsub!( '小豆つぶしあん入り', '' )
				notice.gsub!( '乳児用としてカルシウム', '' )
				notice.gsub!( 'ビスケット等をチョコレートで被覆したもの', '' )
				notice.gsub!( '塩事業センター及び日本塩工業会の品質規格では', '' )
				notice.gsub!( 'テオブロミン：', '' )
				notice.gsub!( '湯,たん,液状だし,鶏肉,豚もも肉,ねぎ,しょうがなどでとっただし', '' )
				notice.gsub!( '牛もも肉,にんじん,たまねぎ,セロリーなどでとっただし', '' )
				notice.gsub!( 'さるぼう味付け缶詰', '' )
				notice.gsub!( 'まくさ角寒天をゼリー状にしたもの', '' )
				notice.gsub!( 'まくさ角寒天をゼリー状にしたもの', '' )
				notice.gsub!( '同一', '' )
				notice.gsub!( '（', '、' )
				notice.gsub!( '）', '' )
				notice.gsub!( '和名' , '' )
				notice.gsub!( '標準' , '' )
				notice.gsub!( '関西' , '' )

				notice.gsub!( '　' , '' )
				notice.gsub!( "\s" , '' )
				notice.gsub!( /、+$/ , '' )
				notice.gsub!( /、、/ , '' )
				notice.gsub!( /、/ , ',' )

				query = "SELECT * FROM dic WHERE alias='#{notice}';"
				res3 = $DB.query( query )
				unless res3.first
					query = "INSERT dic SET alias='#{notice}', org_name='#{food_name}', FG='#{food_group}', user='#{$GM}';"
					$DB.query( query )
				end
			end
		end
		puts 'dic in ext has been updated.'
	end
end


#### Making fctp table.
def fct_pseudo_init()
	query = "SHOW TABLES LIKE 'fctp';"
	res = $DB.query( query )
	if res.first
		puts 'fctp table already exists.'
	else
		query = 'CREATE TABLE fctp (FG VARCHAR(2),FN VARCHAR(6),user VARCHAR(32) NOT NULL,Tagnames VARCHAR(255),REFUSE TINYINT UNSIGNED,ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(16),PROTCAA VARCHAR(16),PROT VARCHAR(16),FATNLEA VARCHAR(16),CHOLE VARCHAR(16),FAT VARCHAR(16),CHOAVLM VARCHAR(16),CHOAVL VARCHAR(16),CHOAVLMF VARCHAR(16),FIB VARCHAR(16),POLYL VARCHAR(16),CHOCDF VARCHAR(16),OA VARCHAR(16),ASH VARCHAR(16),NA VARCHAR(16),K VARCHAR(16),CA VARCHAR(16),MG VARCHAR(16),P VARCHAR(16),FE VARCHAR(16),ZN VARCHAR(16),CU VARCHAR(16),MN VARCHAR(16),ID VARCHAR(16),SE VARCHAR(16),CR VARCHAR(16),MO VARCHAR(16),RETOL VARCHAR(16),CARTA VARCHAR(16),CARTB VARCHAR(16),CRYPXB VARCHAR(16),CARTBEQ VARCHAR(16),VITA_RAE VARCHAR(16),VITD VARCHAR(16),TOCPHA VARCHAR(16),TOCPHB VARCHAR(16),TOCPHG VARCHAR(16),TOCPHD VARCHAR(16),VITK VARCHAR(16),THIAHCL VARCHAR(16),RIBF VARCHAR(16),NIA VARCHAR(16),NE VARCHAR(16),VITB6A VARCHAR(16),VITB12 VARCHAR(16),FOL VARCHAR(16),PANTAC VARCHAR(16),BIOT VARCHAR(16),VITC VARCHAR(16),ALC VARCHAR(16),NACL_EQ VARCHAR(16),Notice VARCHAR(255));'
		$DB.query( query )
		puts 'fctp table has been created.'
	end
end


#### Making user table.
def user_init()
	query = "SHOW TABLES LIKE 'user';"
	res = $DB.query( query )
	if res.first
		puts 'user table already exists.'
	else
		query = 'CREATE TABLE user (user VARCHAR(32) NOT NULL PRIMARY KEY, pass VARCHAR(32), cookie VARCHAR(32), cookie_m VARCHAR(32), mail VARCHAR(64), aliasu VARCHAR(64), status TINYINT, reg_date DATETIME, language VARCHAR(2), mom VARCHAR(32), switch TINYINT(1));'
		$DB.query( query )
		puts 'user in ext has been created.'

		$DB.query( "INSERT INTO user SET user='#{$GM}', pass='', status='9', language='#{$DEFAULT_LP}';" )

		['guest', 'guest2', 'guest3'].each do |e|
			$DB.query( "INSERT INTO user SET user='#{e}', pass='', status='3', language='#{$DEFAULT_LP}';" )
		end

		puts 'GM & guests have been registed.'
	end
end


#### Making config table.
def cfg_init()
	query = "SHOW TABLES LIKE 'cfg';"
	res = $DB.query( query )
	if res.first
		puts 'cfg table already exists.'
	else
		query = 'CREATE TABLE cfg (user VARCHAR(32) NOT NULL PRIMARY KEY, recipel VARCHAR(32), recipel_max TINYINT, reciperr VARCHAR(128), menul VARCHAR(32), his_sg VARCHAR(2), his_max SMALLINT(6), calcc VARCHAR(8), icalc TINYINT, koyomiy VARCHAR(16), koyomiex VARCHAR(255), koyomiexn VARCHAR(256), icache TINYINT(1), ifix TINYINT(1), sex TINYINT(1), age TINYINT UNSIGNED, height FLOAT UNSIGNED, weight FLOAT UNSIGNED);'
		$DB.query( query )

		[$GM, 'guest', 'guest2', 'guest3'].each do |e|
			$DB.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{e}', his_max=200, recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';" )
		end

		puts 'cfg table has been created.'
	end
end


#### Making history table.
def his_init()
	query = "SHOW TABLES LIKE 'his';"
	res = $DB.query( query )
	if res.first
		puts 'his table already exists.'
	else
		query = 'CREATE TABLE his (user VARCHAR(32) NOT NULL PRIMARY KEY,his VARCHAR(2048));'
		$DB.query( query )
		puts 'his table has been created.'
	end
end


#### Making sum table.
def sum_init()
	query = "SHOW TABLES LIKE 'sum';"
	res = $DB.query( query )
	if res.first
		puts 'sum table already exists.'
	else
		query = 'CREATE TABLE sum (user VARCHAR(32) NOT NULL PRIMARY KEY, code VARCHAR(32), name VARCHAR(255), sum varchar(1024), protect TINYINT(1), dish TINYINT);'
		$DB.query( query )

		[$GM, 'guest', 'guest2', 'guest3'].each do |e|
			$DB.query( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{e}', sum='';" )
		end

		puts 'sum table has been created.'
	end
end


#### Making recipe table.
def recipe_init()
	query = "SHOW TABLES LIKE 'recipe';"
	res = $DB.query( query )
	if res.first
		puts 'recipe table already exists.'
	else
		query = 'CREATE TABLE recipe (code VARCHAR(32) PRIMARY KEY, user VARCHAR(32) NOT NULL, root VARCHAR(32), branch TINYINT, public TINYINT(1), protect TINYINT(1), draft TINYINT(1), name VARCHAR(255) NOT NULL, dish TINYINT, type TINYINT, role TINYINT, tech TINYINT, time TINYINT, cost TINYINT, sum VARCHAR(1024), protocol VARCHAR(2048), fig1 TINYINT(1), fig2 TINYINT(1), fig3 TINYINT(1), date DATETIME);'
		$DB.query( query )
		puts 'recipe table has been created.'
	end
end


#### Making recipe index table.
def recipei_init()
	query = "SHOW TABLES LIKE 'recipei';"
	res = $DB.query( query )
	if res.first
		puts 'recipei table already exists.'
	else
		query = 'CREATE TABLE recipei (user VARCHAR(32), word VARCHAR(64), code VARCHAR(32), public TINYINT(1), count SMALLINT UNSIGNED, f TINYINT(1));'
		$DB.query( query )
		puts 'recipei table has been created.'
	end
end


#### Making meal table.
def meal_init()
	query = "SHOW TABLES LIKE 'meal';"
	res = $DB.query( query )
	if res.first
		puts 'meal table already exists.'
	else
		query = 'CREATE TABLE meal (user VARCHAR(32) NOT NULL PRIMARY KEY, code varchar(32), name VARCHAR(255), meal VARCHAR(255), protect TINYINT(1));'
		$DB.query( query )

		[$GM, 'guest', 'guest2', 'guest3'].each do |e|
			$DB.query( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{e}', meal='';" )
		end

		puts 'meal table has been created.'
	end
end


#### Making menu table.
def menu_init()
	query = "SHOW TABLES LIKE 'menu';"
	res = $DB.query( query )
	if res.first
		puts 'menu table already exists.'
	else
		query = 'CREATE TABLE menu ( code VARCHAR(32) PRIMARY KEY, user VARCHAR(32) NOT NULL, public TINYINT(1), protect TINYINT(1), name VARCHAR(64) NOT NULL, meal VARCHAR(255), fig TINYINT(1), date DATETIME, label VARCHAR(64), memo VARCHAR(255), root VARCHAR(16), branch VARCHAR(256));'
		$DB.query( query )
		puts 'menu table has been created.'
	end
end


#### Making palette table.
def palette_init()
	query = "SHOW TABLES LIKE 'palette';"
	res = $DB.query( query )
	if res.first
		puts 'palette table already exists.'
	else
		query = 'CREATE TABLE palette (user VARCHAR(32) NOT NULL, name VARCHAR(64), palette VARCHAR(128));'
		$DB.query( query )
		puts 'palette table has been created.'
	end
end


#### Making media table.
def media_init()
	query = "SHOW TABLES LIKE 'media';"
	res = $DB.query( query )
	if res.first
		puts 'media table already exists.'
	else
		query = 'CREATE TABLE media (user VARCHAR(32) NOT NULL, code VARCHAR(32), mcode VARCHAR(32) NOT NULL PRIMARY KEY, origin VARCHAR(64), date DATETIME );'
		$DB.query( query )
		puts 'media table has been created.'
	end
end


#### Making search food log table
def slogf_init()
	query = "SHOW TABLES LIKE 'slogf';"
	res = $DB.query( query )
	if res.first
		puts 'slogf already exists.'
	else
		query = 'CREATE TABLE slogf (user VARCHAR(32), words VARCHAR(128), code VARCHAR(32), date DATETIME );'
		$DB.query( query )
		puts 'slogf table has been created.'
	end
end


#### Making search recipe log table
def slogr_init()
	query = "SHOW TABLES LIKE 'slogr';"
	res = $DB.query( query )
	if res.first
		puts 'slogr already exists.'
	else
		query = 'CREATE TABLE slogr (user VARCHAR(32), words VARCHAR(128), code VARCHAR(32), date DATETIME );'
		$DB.query( query )
		puts 'slogr table has been created.'
	end
end


#### Making search memory log table
def slogm_init()
	query = "SHOW TABLES LIKE 'slogm';"
	res = $DB.query( query )
	if res.first
		puts 'slogm already exists.'
	else
		query = 'CREATE TABLE slogm (user VARCHAR(32), words VARCHAR(128), score VARCHAR(4), date DATETIME );'
		$DB.query( query )
		puts 'slogm table has been created.'
	end
end


#### Making price table
def price_init()
	query = "SHOW TABLES LIKE 'price';"
	res = $DB.query( query )
	if res.first
		puts 'price already exists.'
	else
		query = 'CREATE TABLE price (code VARCHAR(32) PRIMARY KEY, user VARCHAR(32), price varchar(1024));'
		$DB.query( query )
		puts 'price table has been created.'
	end
end


#### Making master price table
def pricem_init()
	query = "SHOW TABLES LIKE 'pricem';"
	res = $DB.query( query )
	if res.first
		puts 'pricem already exists.'
	else
		query = 'CREATE TABLE pricem (FN VARCHAR(6), user VARCHAR(32), price INT, volume SMALLINT);'
		$DB.query( query )
		puts 'pricem table has been created.'
	end
end


#### Making search memory log table
def memory_init()
	query = "SHOW TABLES LIKE 'memory';"
	res = $DB.query( query )
	if res.first
		puts 'memory already exists.'
	else
		query = 'CREATE TABLE memory (user VARCHAR(32), category VARCHAR(32), pointer VARCHAR(64), memory VARCHAR(1024), rank TINYINT, total_rank TINYINT, count BIGINT UNSIGNED, know BIGINT UNSIGNED, date DATETIME );'
		$DB.query( query )
		puts 'memory table has been created.'
	end
end


#### Koyomi table
def koyomi_init()
	query = "SHOW TABLES LIKE 'koyomi';"
	res = $DB.query( query )
	if res.first
		puts 'koyomi already exists.'
	else
		query = 'CREATE TABLE koyomi (user VARCHAR(32), freeze TINYINT(1), fzcode VARCHAR(32), tdiv TINYINT(1), koyomi VARCHAR(256), date DATE );'
		$DB.query( query )
		puts 'koyomi table has been created.'
	end
end


#### Koyomi EX table
def koyomiex_init()
	query = "SHOW TABLES LIKE 'koyomiex';"
	res = $DB.query( query )
	if res.first
		puts 'koyomiex already exists.'
	else
		query = 'CREATE TABLE koyomiex (user VARCHAR(32), item0 VARCHAR(16), item1 VARCHAR(16), item2 VARCHAR(16), item3 VARCHAR(16), item4 VARCHAR(16), item5 VARCHAR(16), item6 VARCHAR(16), item7 VARCHAR(16), item8 VARCHAR(16), item9 VARCHAR(16), date DATE );'
		$DB.query( query )
		puts 'koyomiex table has been created.'
	end
end


#### Making fct static table.
def fcs_init()
	query = "SHOW TABLES LIKE 'fcs';"
	res = $DB.query( query )
	if res.first
		puts 'fcs already exists.'
	else
		query = 'CREATE TABLE fcs ( code VARCHAR(32) NOT NULL PRIMARY KEY, name VARCHAR(64), user VARCHAR(32), ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(16),PROTCAA VARCHAR(16),PROT VARCHAR(16),FATNLEA VARCHAR(16),CHOLE VARCHAR(16),FAT VARCHAR(16),CHOAVLM VARCHAR(16),CHOAVL VARCHAR(16),CHOAVLMF VARCHAR(16),FIB VARCHAR(16),POLYL VARCHAR(16),CHOCDF VARCHAR(16),OA VARCHAR(16),ASH VARCHAR(16),NA VARCHAR(16),K VARCHAR(16),CA VARCHAR(16),MG VARCHAR(16),P VARCHAR(16),FE VARCHAR(16),ZN VARCHAR(16),CU VARCHAR(16),MN VARCHAR(16),ID VARCHAR(16),SE VARCHAR(16),CR VARCHAR(16),MO VARCHAR(16),RETOL VARCHAR(16),CARTA VARCHAR(16),CARTB VARCHAR(16),CRYPXB VARCHAR(16),CARTBEQ VARCHAR(16),VITA_RAE VARCHAR(16),VITD VARCHAR(16),TOCPHA VARCHAR(16),TOCPHB VARCHAR(16),TOCPHG VARCHAR(16),TOCPHD VARCHAR(16),VITK VARCHAR(16),THIAHCL VARCHAR(16),RIBF VARCHAR(16),NIA VARCHAR(16),NE VARCHAR(16),VITB6A VARCHAR(16),VITB12 VARCHAR(16),FOL VARCHAR(16),PANTAC VARCHAR(16),BIOT VARCHAR(16),VITC VARCHAR(16),ALC VARCHAR(16),NACL_EQ VARCHAR(16));'
		$DB.query( query )
		puts 'fcs table has been created.'
	end
end


#### Making fct freeze table for koyomi.
def fcz_init()
	query = "SHOW TABLES LIKE 'fcz';"
	res = $DB.query( query )
	if res.first
		puts 'fcz already exists.'
	else
		query = 'CREATE TABLE fcz ( code VARCHAR(32) NOT NULL PRIMARY KEY, user VARCHAR(32),ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(16),PROTCAA VARCHAR(16),PROT VARCHAR(16),FATNLEA VARCHAR(16),CHOLE VARCHAR(16),FAT VARCHAR(16),CHOAVLM VARCHAR(16),CHOAVL VARCHAR(16),CHOAVLMF VARCHAR(16),FIB VARCHAR(16),POLYL VARCHAR(16),CHOCDF VARCHAR(16),OA VARCHAR(16),ASH VARCHAR(16),NA VARCHAR(16),K VARCHAR(16),CA VARCHAR(16),MG VARCHAR(16),P VARCHAR(16),FE VARCHAR(16),ZN VARCHAR(16),CU VARCHAR(16),MN VARCHAR(16),ID VARCHAR(16),SE VARCHAR(16),CR VARCHAR(16),MO VARCHAR(16),RETOL VARCHAR(16),CARTA VARCHAR(16),CARTB VARCHAR(16),CRYPXB VARCHAR(16),CARTBEQ VARCHAR(16),VITA_RAE VARCHAR(16),VITD VARCHAR(16),TOCPHA VARCHAR(16),TOCPHB VARCHAR(16),TOCPHG VARCHAR(16),TOCPHD VARCHAR(16),VITK VARCHAR(16),THIAHCL VARCHAR(16),RIBF VARCHAR(16),NIA VARCHAR(16),NE VARCHAR(16),VITB6A VARCHAR(16),VITB12 VARCHAR(16),FOL VARCHAR(16),PANTAC VARCHAR(16),BIOT VARCHAR(16),VITC VARCHAR(16),ALC VARCHAR(16),NACL_EQ VARCHAR(16), someb VARCHAR(3), somel VARCHAR(3), somed VARCHAR(3), somes VARCHAR(3));'
		$DB.query( query )
		puts 'fcz table has been created.'
	end
end


#### Making fct result table.
def fcr_init()
	query = "SHOW TABLES LIKE 'fcr';"
	res = $DB.query( query )
	if res.first
		puts 'fcr already exists.'
	else
		query = 'CREATE TABLE fcr ( code VARCHAR(32) NOT NULL PRIMARY KEY, user VARCHAR(32), ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(16),PROTCAA VARCHAR(16),PROT VARCHAR(16),FATNLEA VARCHAR(16),CHOLE VARCHAR(16),FAT VARCHAR(16),CHOAVLM VARCHAR(16),CHOAVL VARCHAR(16),CHOAVLMF VARCHAR(16),FIB VARCHAR(16),POLYL VARCHAR(16),CHOCDF VARCHAR(16),OA VARCHAR(16),ASH VARCHAR(16),NA VARCHAR(16),K VARCHAR(16),CA VARCHAR(16),MG VARCHAR(16),P VARCHAR(16),FE VARCHAR(16),ZN VARCHAR(16),CU VARCHAR(16),MN VARCHAR(16),ID VARCHAR(16),SE VARCHAR(16),CR VARCHAR(16),MO VARCHAR(16),RETOL VARCHAR(16),CARTA VARCHAR(16),CARTB VARCHAR(16),CRYPXB VARCHAR(16),CARTBEQ VARCHAR(16),VITA_RAE VARCHAR(16),VITD VARCHAR(16),TOCPHA VARCHAR(16),TOCPHB VARCHAR(16),TOCPHG VARCHAR(16),TOCPHD VARCHAR(16),VITK VARCHAR(16),THIAHCL VARCHAR(16),RIBF VARCHAR(16),NIA VARCHAR(16),NE VARCHAR(16),VITB6A VARCHAR(16),VITB12 VARCHAR(16),FOL VARCHAR(16),PANTAC VARCHAR(16),BIOT VARCHAR(16),VITC VARCHAR(16),ALC VARCHAR(16),NACL_EQ VARCHAR(16));'
		$DB.query( query )
		puts 'fcr table has been created.'
	end
end


#### Making METs standard table for koyomi.
def metst_init( mets_file )
	query = "SHOW TABLES LIKE 'metst';"
	res = $DB.query( query )
	if res.first
		puts 'metst already exists.'
	else
		query = 'CREATE TABLE metst (code VARCHAR(5), mets VARCHAR(4), heading VARCHAR(32), sub_heading VARCHAR(32), active VARCHAR(100));'
		$DB.query( query )

		f = open( mets_file, 'r' )
		f.each_line do |l|
			t = l.chomp
			a = t.force_encoding( 'utf-8' ).split( "\t" )
			query = "INSERT INTO metst set code='#{a[0]}', mets='#{a[1]}', heading='#{a[2]}', sub_heading='#{a[3]}', active='#{a[4]}';"
			$DB.query( query )
		end
		f.close
		puts 'metst table has been created.'
	end
end


#### Making METs record table for koyomi.
def mets_init()
	query = "SHOW TABLES LIKE 'mets';"
	res = $DB.query( query )
	if res.first
		puts 'mets already exists.'
	else
		query = 'CREATE TABLE mets (user VARCHAR(32), name VARCHAR(64), mets VARCHAR(1000), metsv VARCHAR(6));'
		$DB.query( query )
		puts 'mets table has been created.'
	end
end


#### Making reference BMI table for koyomi.
def ref_bmi_init( ref_bmi )
	query = "SHOW TABLES LIKE 'ref_bmi';"
	res = $DB.query( query )
	if res.first
		puts 'ref_bmi already exists.'
	else
		query = 'CREATE TABLE ref_bmi ( period_class VARCHAR(1), periods VARCHAR(2), periode VARCHAR(2), BMI_targetl VARCHAR(4), BMI_targetu VARCHAR(4));'
		$DB.query( query )

		ref_solid = []
		f = open( ref_bmi, 'r')
		f.each_line do |e| ref_solid << e.chomp end
		ref_solid.shift
		ref_solid.each do |e|
			a = e.force_encoding( 'utf-8' ).split( "\t" )
			query = "INSERT INTO ref_bmi set period_class='#{a[0]}', periods='#{a[1]}', periode='#{a[2]}', BMI_targetl='#{a[3]}', BMI_targetu='#{a[4]}';"
			$DB.query( query )
		end
		puts 'ref_bmi table has been created.'
	end
end


#### Making reference Physics table for koyomi.
def ref_phys_init( ref_phys )
	query = "SHOW TABLES LIKE 'ref_phys';"
	res = $DB.query( query )
	if res.first
		puts 'ref_phys already exists.'
	else
		query = 'CREATE TABLE ref_phys ( sex VARCHAR(1), period_class VARCHAR(1), periods VARCHAR(2), periode VARCHAR(2), height VARCHAR(5), weight VARCHAR(5), height_unit VARCHAR(2), weight_unit VARCHAR(2));'
		$DB.query( query )

		ref_solid = []
		f = open( ref_phys, 'r')
		f.each_line do |e| ref_solid << e.chomp end
		ref_solid.shift
		ref_solid.each do |e|
			a = e.force_encoding( 'utf-8' ).split( "\t" )
			query = "INSERT INTO ref_phys set sex='#{a[0]}', period_class='#{a[1]}', periods='#{a[2]}', periode='#{a[3]}', height='#{a[4]}', weight='#{a[5]}', height_unit='#{a[6]}', weight_unit='#{a[7]}';"
			$DB.query( query )
		end
		puts 'ref_phys table has been created.'
	end
end


#### Making reference EER table for koyomi.
def ref_eer_init( ref_eer )
	query = "SHOW TABLES LIKE 'ref_eer';"
	res = $DB.query( query )
	if res.first
		puts 'ref_eer already exists.'
	else
		query = 'CREATE TABLE ref_eer ( sex VARCHAR(1), period_class VARCHAR(1), periods VARCHAR(2), periode VARCHAR(2), pal1 VARCHAR(4), pal2 VARCHAR(4), pal3 VARCHAR(4), unit VARCHAR(8));'
		$DB.query( query )

		ref_solid = []
		f = open( ref_eer, 'r')
		f.each_line do |e| ref_solid << e.chomp end
		ref_solid.shift
		ref_solid.each do |e|
			a = e.force_encoding( 'utf-8' ).split( "\t" )
			query = "INSERT INTO ref_eer set sex='#{a[0]}', period_class='#{a[1]}', periods='#{a[2]}', periode='#{a[3]}', pal1='#{a[4]}', pal2='#{a[5]}', pal3='#{a[6]}', unit='#{a[7]}';"
			$DB.query( query )
		end
		puts 'ref_eer table has been created.'
	end
end


#### Making reference intake table for koyomi.
def ref_intake_init( ref_intake )
	query = "SHOW TABLES LIKE 'ref_intake';"
	res = $DB.query( query )
	if res.first
		puts 'ref_intake already exists.'
	else
		query = 'CREATE TABLE ref_intake ( name VARCHAR(10), sex VARCHAR(1), period_class VARCHAR(1), periods VARCHAR(2), periode VARCHAR(2), EAR VARCHAR(4), RDA VARCHAR(4), AI VARCHAR(4), UL VARCHAR(4), unit VARCHAR(10), DG_min VARCHAR(4), DG_max VARCHAR(4), DG_unit VARCHAR(10));'
		$DB.query( query )

		ref_solid = []
		f = open( ref_intake, 'r')
		f.each_line do |e| ref_solid << e.chomp end
		ref_solid.shift
		ref_solid.each do |e|
			a = e.force_encoding( 'utf-8' ).split( "\t" )
			query = "INSERT INTO ref_intake set name='#{a[0]}', sex='#{a[1]}', period_class='#{a[2]}', periods='#{a[3]}', periode='#{a[4]}', EAR='#{a[5]}', RDA='#{a[6]}', AI='#{a[7]}', UL='#{a[8]}', unit='#{a[9]}', DG_min='#{a[10]}', DG_max='#{a[11]}', DG_unit='#{a[12]}';"
			$DB.query( query )
		end
		puts 'ref_intake table has been created.'
	end
end


#### Making cooking school koyomi table
def schoolk_init()
	query = "SHOW TABLES LIKE 'schoolk';"
	res = $DB.query( query )
	if res.first
		puts 'schoolk already exists.'
	else
		query = 'CREATE TABLE schoolk ( user VARCHAR(32), student VARCHAR(32), num TINYINT, pass VARCHAR(64), status TINYINT, menu VARCHAR(32), ampm TINYINT(1), date DATE );'
		$DB.query( query )
		puts 'schoolk table has been created.'
	end
end


#### Making cooking school menu tag table
def schoolm_init()
	query = "SHOW TABLES LIKE 'schoolm';"
	res = $DB.query( query )
	if res.first
		puts 'schoolm already exists.'
	else
		query = 'CREATE TABLE schoolm ( user VARCHAR(32) NOT NULL, label_group VARCHAR(64), label VARCHAR(256));'
		$DB.query( query )
		puts 'schoolm table has been created.'
	end
end


#### 生体情報
def bio_init()
	puts '栄養成分安定テーブルの作成'
	# テーブル作成
	query = 'CREATE TABLE bio (user VARCHAR(32), auto TINYINT(1), sex TINYINT(1), age TINYINT UNSIGNED, height TINYINT UNSIGNED, weight TINYINT UNSIGNED);'
	$DB.query( query )
end

#==============================================================================
$DB = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

gycv_file = 'nb2020-gycv.txt'
shun_file = 'nb2020-shun.txt'
unit_file = 'nb2020-unit.txt'
mets_file = 'nb2020-mets.txt'
ref_bmi = 'ref2020-bmi.txt'
ref_phys = 'ref2020-phys.txt'
ref_eer = 'ref2020-eer.txt'
ref_intake = 'ref2020-intake.txt'

#==============================================================================

fct_init( source_file )
tag_init( source_file )
ext_init( gycv_file, shun_file, unit_file )
dic_init()
fct_pseudo_init()

user_init()
cfg_init()
his_init()
sum_init()
recipe_init()
recipei_init()
meal_init()
menu_init()
palette_init()
media_init()

slogf_init()
slogr_init()
slogm_init()

price_init()
pricem_init()

memory_init()

koyomi_init
koyomiex_init

fcs_init()
fcz_init()
fcr_init()

metst_init( mets_file )
mets_init()

ref_bmi_init( ref_bmi )
ref_phys_init( ref_phys )
ref_eer_init( ref_eer )
ref_intake_init( ref_intake )

schoolk_init()
schoolm_init()


#bio_init()

$DB.close
