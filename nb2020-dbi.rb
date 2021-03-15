#! /usr/bin/ruby
#nb2020-dbi.rb 0.00b

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
puts "CREATE USER '#{$MYSQL_USER}'@'#{$MYSQL_HOST}' IDENTIFIED BY '#{$MYSQL_PW}';"
puts "GRANT ALL PRIVILEGES ON #{$MYSQL_DB}.* TO '#{$MYSQL_USER}'@'#{$MYSQL_HOST}';"
puts "GRANT ALL PRIVILEGES ON #{$MYSQL_DBR}.* TO '#{$MYSQL_USER}'@'#{$MYSQL_HOST}';"
puts "FLUSH PRIVILEGES;"

puts "[Enter]"
gets.chomp
#==============================================================================
#DEFINITION
#==============================================================================


#### Making fct table.
def fct_init( source_file )
	query = "SHOW TABLES LIKE 'fct';"
	res = $DB.query( query )
	if res.first
		puts 'fct table already exists.'
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


#### Making food tag table.
def tag_init( source_file )
	query = "SHOW TABLES LIKE 'tag';"
	res = $DB.query( query )
	if res.first
		puts 'tag table already exists.'
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


#### Making food extra tag table.
def ext_init( gycv_file, shun_file, unit_file )
	query = "SHOW TABLES LIKE 'ext';"
	res = $DB.query( query )
	if res.first
		puts 'ext table already exists.'
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

		alias_hash = Hash::new
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
		query = 'CREATE TABLE fctp (FG VARCHAR(2),FN VARCHAR(6),user VARCHAR(32) NOT NULL,Tagnames VARCHAR(255),REFUSE TINYINT UNSIGNED,ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(8),PROTCAA VARCHAR(8),PROT VARCHAR(8),FATNLEA VARCHAR(8),CHOLE VARCHAR(8),FAT VARCHAR(8),CHOAVLM VARCHAR(8),CHOAVL VARCHAR(8),CHOAVLMF VARCHAR(8),FIB VARCHAR(8),POLYL VARCHAR(8),CHOCDF VARCHAR(8),OA VARCHAR(8),ASH VARCHAR(8),NA VARCHAR(8),K VARCHAR(8),CA VARCHAR(8),MG VARCHAR(8),P VARCHAR(8),FE VARCHAR(8),ZN VARCHAR(8),CU VARCHAR(8),MN VARCHAR(8),ID VARCHAR(8),SE VARCHAR(8),CR VARCHAR(8),MO VARCHAR(8),RETOL VARCHAR(8),CARTA VARCHAR(8),CARTB VARCHAR(8),CRYPXB VARCHAR(8),CARTBEQ VARCHAR(8),VITA_RAE VARCHAR(8),VITD VARCHAR(8),TOCPHA VARCHAR(8),TOCPHB VARCHAR(8),TOCPHG VARCHAR(8),TOCPHD VARCHAR(8),VITK VARCHAR(8),THIAHCL VARCHAR(8),RIBF VARCHAR(8),NIA VARCHAR(8),NE VARCHAR(8),VITB6A VARCHAR(8),VITB12 VARCHAR(8),FOL VARCHAR(8),PANTAC VARCHAR(8),BIOT VARCHAR(8),VITC VARCHAR(8),ALC VARCHAR(8),NACL_EQ VARCHAR(8),Notice VARCHAR(255));'
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

		query = "INSERT INTO user SET user='guest', pass='', status='3', language='#{$DEFAULT_LP}';"
		$DB.query( query )
		query = "INSERT INTO user SET user='guest1', pass='', status='3', language='#{$DEFAULT_LP}';"
		$DB.query( query )
		query = "INSERT INTO user SET user='guest3', pass='', status='3', language='#{$DEFAULT_LP}';"
		$DB.query( query )
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
		query = 'CREATE TABLE cfg (user VARCHAR(32) NOT NULL PRIMARY KEY, recipel VARCHAR(32), recipel_max TINYINT, reciperr VARCHAR(128), menul VARCHAR(32), his_sg VARCHAR(2), his_max SMALLINT(6), calcc VARCHAR(8), icalc TINYINT, koyomiy VARCHAR(16), koyomiex VARCHAR(255), koyomiexn VARCHAR(256), icache TINYINT(1), ifix TINYINT(1), sex TINYINT(1), age TINYINT UNSIGNED, height FLOAT UNSIGNED, weight FLOAT UNSIGNED, schooll VARCHAR(512));'
		$DB.query( query )

		$DB.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{$GM}', recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='guest', recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='guest2', recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='guest3', recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';" )

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

		$DB.query( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{$GM}', sum='';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_SUM} SET user='guest', sum='';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_SUM} SET user='guest2', sum='';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_SUM} SET user='guest3', sum='';" )

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

		$DB.query( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{$GM}', meal='';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='guest', meal='';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='guest2', meal='';" )
		$DB.query( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='guest3', meal='';" )

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
		query = 'CREATE TABLE palette (user VARCHAR(32) NOT NULL, name VARCHAR(64), palette VARCHAR(128), count TINYINT );'
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
		query = 'CREATE TABLE media (user VARCHAR(32) NOT NULL, code VARCHAR(32), mcode VARCHAR(32), origin VARCHAR(64), date DATETIME );'
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
#		query = 'CREATE TABLE fcs ( code VARCHAR(32),name VARCHAR(64),user VARCHAR(32),ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(8),PROTCAA VARCHAR(8),PROT VARCHAR(8),FATNLEA VARCHAR(8),CHOLE VARCHAR(8),FAT VARCHAR(8),CHOAVLM VARCHAR(8),CHOAVL VARCHAR(8),CHOAVLMF VARCHAR(8),FIB VARCHAR(8),POLYL VARCHAR(8),CHOCDF VARCHAR(8),OA VARCHAR(8),ASH VARCHAR(8),NA VARCHAR(8),K VARCHAR(8),CA VARCHAR(8),MG VARCHAR(8),P VARCHAR(8),FE VARCHAR(8),ZN VARCHAR(8),CU VARCHAR(8),MN VARCHAR(8),ID VARCHAR(8),SE VARCHAR(8),CR VARCHAR(8),MO VARCHAR(8),RETOL VARCHAR(8),CARTA VARCHAR(8),CARTB VARCHAR(8),CRYPXB VARCHAR(8),CARTBEQ VARCHAR(8),VITA_RAE VARCHAR(8),VITD VARCHAR(8),TOCPHA VARCHAR(8),TOCPHB VARCHAR(8),TOCPHG VARCHAR(8),TOCPHD VARCHAR(8),VITK VARCHAR(8),THIAHCL VARCHAR(8),RIBF VARCHAR(8),NIA VARCHAR(8),NE VARCHAR(8),VITB6A VARCHAR(8),VITB12 VARCHAR(8),FOL VARCHAR(8),PANTAC VARCHAR(8),BIOT VARCHAR(8),VITC VARCHAR(8),ALC VARCHAR(8),NACL_EQ VARCHAR(8), period SAMLLINT UNSIGNED);'
		query = 'CREATE TABLE fcs ( code VARCHAR(32),name VARCHAR(64),user VARCHAR(32),ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(8),PROTCAA VARCHAR(8),PROT VARCHAR(8),FATNLEA VARCHAR(8),CHOLE VARCHAR(8),FAT VARCHAR(8),CHOAVLM VARCHAR(8),CHOAVL VARCHAR(8),CHOAVLMF VARCHAR(8),FIB VARCHAR(8),POLYL VARCHAR(8),CHOCDF VARCHAR(8),OA VARCHAR(8),ASH VARCHAR(8),NA VARCHAR(8),K VARCHAR(8),CA VARCHAR(8),MG VARCHAR(8),P VARCHAR(8),FE VARCHAR(8),ZN VARCHAR(8),CU VARCHAR(8),MN VARCHAR(8),ID VARCHAR(8),SE VARCHAR(8),CR VARCHAR(8),MO VARCHAR(8),RETOL VARCHAR(8),CARTA VARCHAR(8),CARTB VARCHAR(8),CRYPXB VARCHAR(8),CARTBEQ VARCHAR(8),VITA_RAE VARCHAR(8),VITD VARCHAR(8),TOCPHA VARCHAR(8),TOCPHB VARCHAR(8),TOCPHG VARCHAR(8),TOCPHD VARCHAR(8),VITK VARCHAR(8),THIAHCL VARCHAR(8),RIBF VARCHAR(8),NIA VARCHAR(8),NE VARCHAR(8),VITB6A VARCHAR(8),VITB12 VARCHAR(8),FOL VARCHAR(8),PANTAC VARCHAR(8),BIOT VARCHAR(8),VITC VARCHAR(8),ALC VARCHAR(8),NACL_EQ VARCHAR(8));'
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
	# テーブル作成
		query = 'CREATE TABLE fcz ( code VARCHAR(32), user VARCHAR(32),ENERC SMALLINT UNSIGNED,ENERC_KCAL SMALLINT UNSIGNED,WATER VARCHAR(8),PROTCAA VARCHAR(8),PROT VARCHAR(8),FATNLEA VARCHAR(8),CHOLE VARCHAR(8),FAT VARCHAR(8),CHOAVLM VARCHAR(8),CHOAVL VARCHAR(8),CHOAVLMF VARCHAR(8),FIB VARCHAR(8),POLYL VARCHAR(8),CHOCDF VARCHAR(8),OA VARCHAR(8),ASH VARCHAR(8),NA VARCHAR(8),K VARCHAR(8),CA VARCHAR(8),MG VARCHAR(8),P VARCHAR(8),FE VARCHAR(8),ZN VARCHAR(8),CU VARCHAR(8),MN VARCHAR(8),ID VARCHAR(8),SE VARCHAR(8),CR VARCHAR(8),MO VARCHAR(8),RETOL VARCHAR(8),CARTA VARCHAR(8),CARTB VARCHAR(8),CRYPXB VARCHAR(8),CARTBEQ VARCHAR(8),VITA_RAE VARCHAR(8),VITD VARCHAR(8),TOCPHA VARCHAR(8),TOCPHB VARCHAR(8),TOCPHG VARCHAR(8),TOCPHD VARCHAR(8),VITK VARCHAR(8),THIAHCL VARCHAR(8),RIBF VARCHAR(8),NIA VARCHAR(8),NE VARCHAR(8),VITB6A VARCHAR(8),VITB12 VARCHAR(8),FOL VARCHAR(8),PANTAC VARCHAR(8),BIOT VARCHAR(8),VITC VARCHAR(8),ALC VARCHAR(8),NACL_EQ VARCHAR(8), someb VARCHAR(3), somel VARCHAR(3), somed VARCHAR(3), somes VARCHAR(3));'
		$DB.query( query )
		puts 'fcz table has been created.'
	end
end


#### 生体情報
def bio_init()
	puts '栄養成分安定テーブルの作成'
	# テーブル作成
	query = 'CREATE TABLE bio (user VARCHAR(32), auto TINYINT(1), sex TINYINT(1), age TINYINT UNSIGNED, height TINYINT UNSIGNED, weight TINYINT UNSIGNED);'
	$DB.query( query )
end


#### METs標準テーブルの作成
def metst_init()
	puts 'METs基準テーブルの作成'
	# テーブル作成
	query = 'CREATE TABLE metst (code VARCHAR(5), mets VARCHAR(4), heading VARCHAR(32), sub_heading VARCHAR(32), active VARCHAR(100));'
	$DB.query( query )

	f = open( "mets_utf8.txt", 'r' )
	f.each_line do |l|
		t = l.chomp
		a = t.split( "\t" )
		query = "INSERT INTO metst set code='#{a[0]}', mets='#{a[1]}', heading='#{a[2]}', sub_heading='#{a[3]}', active='#{a[4]}';"
		$DB.query( query )
	end
	f.close
end

#### METsテーブルの作成
def mets_init()
	puts 'METsテーブルの作成'
	# テーブル作成
	query = 'CREATE TABLE mets (user VARCHAR(32), name VARCHAR(64), mets VARCHAR(1000), metsv VARCHAR(6));'
	$DB.query( query )
end

#### 料理教室予約テーブルの作成
def schoolk_init()
	puts 'school koyomiテーブルの作成'
	# テーブル作成
	query = 'CREATE TABLE schoolk ( user VARCHAR(32), student VARCHAR(32), num TINYINT, pass VARCHAR(64), status TINYINT, menu VARCHAR(32), ampm TINYINT(1), date DATE );'
	$DB.query( query )
end


#### 基準BMIテーブルの作成
#def standard_init()
#	puts '基準BMIテーブルの作成'

#	standard_solid = []
#	f = open( 'standard.txt', 'r')
#	f.each_line do |e| standard_solid << e.chomp end

	# カラム追加
#	column_names = standard_solid.shift.split( "\t" )
#	column_type = standard_solid.shift.split( "\t" )
#	column_names.size.times do |c|
#		query = "ALTER TABLE standard add #{column_names[c]} #{column_type[c]};"
#		$DB.query( query )
#	end

	# データのセット
#	standard_solid.each do |e|
#		query = 'INSERT INTO standard SET '
#		a = e.split( "\t" )
#		c = 0
#		e.each do |ee|
#			query << "#{column_names[c]}='#{ee}',"
#			c += 1
#		end
#		query.chop
#		query << ';'
#		$DB.query( query )
#	end
#end

#==============================================================================
$DB = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

source_file = '20201225-mxt_kagsei-mext_01110_012_clean.txt'
gycv_file = 'nb2020-gycv.txt'
shun_file = 'nb2020-shun.txt'
unit_file = 'nb2020-unit.txt'

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

#standard_init()
#bio_init()
#metst_init()
#mets_init()

#schoolk_init()


$DB.close
