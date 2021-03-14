#Nutrition browser 2020 soul 0.00b

#==============================================================================
# LIBRARY
#==============================================================================
require 'cgi'
require 'mysql2'
require 'bigdecimal'
require 'securerandom'

#==============================================================================
#STATIC
#==============================================================================
$GM = ''

$SERVER_PATH = '/var/www'
$HTDOCS_PATH = "#{$SERVER_PATH}/htdocs_nbt"
$TMP_PATH = '/tmp'

$COOKIE_UID = 'UID2020'
$COOKIE_MID = 'MID2020'

$MYSQL_HOST = 'localhost'
$MYSQL_USER = ''
$MYSQL_USERR = ''
$MYSQL_PW = ''
$MYSQL_DB = 'nb2020'
$MYSQL_DBR = 'rr'
$MYSQL_TB_FCT = 'fct'
$MYSQL_TB_FCTP = 'fctp'
$MYSQL_TB_CFG = 'cfg'
$MYSQL_TB_TAG = 'tag'
$MYSQL_TB_EXT = 'ext'
$MYSQL_TB_DIC = 'dic'
$MYSQL_TB_MEDIA = 'media'
$MYSQL_TB_SLOGF = 'slogf'
$MYSQL_TB_SLOGR = 'slogr'
$MYSQL_TB_SLOGM = 'slogm'
$MYSQL_TB_USER = 'user'
$MYSQL_TB_RECIPE = 'recipe'
$MYSQL_TB_RECIPEI = 'recipei'
$MYSQL_TB_PRICE = 'price'
$MYSQL_TB_PRICEM = 'pricem'
$MYSQL_TB_SUM = 'sum'
$MYSQL_TB_HIS = 'his'
$MYSQL_TB_PALETTE = 'palette'
$MYSQL_TB_MEAL = 'meal'
$MYSQL_TB_MENU = 'menu'
$MYSQL_TB_MEMORY = 'memory'
$MYSQL_TB_KOYOMI = 'koyomi'
$MYSQL_TB_KOYOMIEX = 'koyomiex'
$MYSQL_TB_FCS = 'fcs'
$MYSQL_TB_FCZ = 'fcz'
$MYSQL_TB_METS = 'mets'
$MYSQL_TB_METST = 'metst'
$MYSQL_TB_SCHOOLK = 'schoolk'
$MYSQL_TB_SCHOOLM = 'schoolm'
$MYSQL_TB_SCHOOLS = 'schools'

$PHOTO = 'photo_'
$PHOTO_PATH = "#{$HTDOCS_PATH}/#{$PHOTO}"
$SIZE_MAX = 20000000
$TN_SIZE = 400
$TNS_SIZE = 40
$PHOTO_SIZE_MAX = 2000

$JS_PATH = 'js'
$CSS_PATH = 'css'
$BOOK_PATH = 'books'

$LP = ['jp']
$DEFAULT_LP = $LP[0]

$DEBUG = false

#==============================================================================
# CORE LANGAGE & CGI
#==============================================================================
@cgi = CGI.new

soul_language = $DEFAULT_LP
uname = @cgi.cookies['NAME'].first unless @cgi.cookies['NAME'] == nil
uid = @cgi.cookies[$COOKIE_UID].first unless @cgi.cookies[$COOKIE_UID] == nil


if uname != nil && uid != nil

  db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
  res = db.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{uname}' and cookie='#{uid}' and status>0;" )
  db.close

  soul_language = res.first['language'] if res.first

end

require "#{$SERVER_PATH}/nb2020-soul-#{soul_language}"


#==============================================================================
#DEFINITION
#==============================================================================
#### HTML init
def html_init( cookie )
  puts "Content-type: text/html\n"
  puts "Cache-Control: no-store, no-cache, must-revalidate, max-age=0\n"
  puts "Cache-Control: post-check=0, pre-check=0, false\n"
  puts "Pragma: no-cache\n"
  puts cookie unless cookie == nil
  puts "\n"
end


#### HTML init with cache
def html_init_cache( cookie )
  puts "Content-type: text/html\n"
  puts cookie unless cookie == nil
  puts "\n"
end


#### Tracking code
def tracking()
    html = <<-"HTML"
HTML

  puts html
end


#### GETデータの抽出
def get_data()
  data = Hash.new
  if ENV['QUERY_STRING']
    querys = ENV['QUERY_STRING'].split( '&' )
    querys.each { |e|
      ( k, v ) = e.split( '=' )
      data[ k ] = v
    }
  end

  return data
end


#### データベース処理
def mdb( query, html_opt, debug )
  begin
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    t = query.chop
    query_ = ''
    query_ = query if debug
    if /\;/ =~ t
        puts "<span class='error'>[mdb]ERROR!! #{query_}</span><br>"
        exit( 9 )
    end

    res = db.query( query )
    db.close
  rescue
    if html_opt
      html_init( nil )
      html_head( nil )
    end
      puts "<span class='error'>[mdb]ERROR!!<br>"
      puts "#{query_}</span><br>"
  end
  return res
end


#### R用データベース処理
def mdbr( query, html_opt, debug )
  begin
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USERR}", :password => "", :database => "#{$MYSQL_DBR}", :encoding => "utf8" )
    t = query.chop
    query_ = ''
    query_ = query if debug
    if /\;/ =~ t
        puts "<span class='error'>[mdbr]ERROR!! #{query_}</span><br>"
        exit( 9 )
    end
    res = db.query( query )
    db.close
  rescue
    if html_opt
      html_init( nil )
      html_head( nil )
    end
      puts "<span class='error'>[mdbr]ERROR!!<br>"
      puts "#{query_}</span><br>"
  end
  return res
end


#### 食品成分値の処理
def num_opt( num, weight, mode, limit )
  # リミットがない→数値ではない場合はそのまま返す
  return num if limit == nil

    kakko = false
    if /^\(/ =~ num.to_s
      num.sub!( '(', '' )
      num.sub!( ')', '' )
      kakko = true
    end
    ans = BigDecimal( 0 )

  begin
    if num == '-'
      return '-'
    elsif num == 'Tr'
      return 'Tr'
    else
      weight = weight / 100
      #weight_f = 1 if weight_f < 0

      case mode
      # 四捨五入
      when '1'
        ans = ( BigDecimal( num ) * weight ).round( limit )
      # 切り上げ
      when '2'
        ans = ( BigDecimal( num ) * weight ).ceil( limit )
      # 切り捨て
      when '3'
        ans = ( BigDecimal( num ) * weight ).floor( limit )
      else
        ans = ( BigDecimal( num ) * weight ).round( limit )
      end
    end

    if limit == 0
      ans = ans.to_i
    else
      t = ans.to_f.to_s.split( '.' )
      l = t[1].size
      if l != limit
        d = limit - l
        d.times do t[1] << '0' end
      end
      ans = t[0] + '.' + t[1]
    end

    ans = "(#{ans})" if kakko
  rescue
    puts "<span class='error'>[num_opt]ERROR!!<br>"
    puts "num:#{num}<br>"
    puts "weight:#{weight}<br>"
    puts "mode:#{mode}<br>"
    puts "limit:#{limit}</span><br>"
    exit( 9 )
  end

  return ans
end


#### 履歴追加
def add_his( user, fn )
  r = mdb( "SELECT his FROM #{$MYSQL_TB_HIS} WHERE user='#{user}';", true, $DEBUG )
  if r.first
    current_his = r.first['his'].split( "\t" )
  else
    # 新規追加
    mdb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{user}', his='';", true, $DEBUG )
    current_his = []
  end

  #
  r = mdb( "SELECT his_max FROM #{$MYSQL_TB_CFG} WHERE user='#{user}';", false, $DEBUG )
  his_max = r.first['his_max'].to_i  if r.first
  his_max = 200 if his_max < 200 || his_max > 500

  new_his = "#{fn}\t"
  0.upto( his_max - 1 ) do |c|
    new_his << "#{current_his[c]}\t" unless fn == current_his[c]
  end
  new_his.chop!

  # 履歴の更新
  mdb( "UPDATE #{$MYSQL_TB_HIS} SET his='#{new_his}' WHERE user='#{user}';", true, $DEBUG )
end


#### コードの生成
def generate_code( uname, c )
  require 'securerandom'

  code = uname[0, 2]
  code = "x" + uname[0, 1] if code == nil
  10.times do
    code = "#{code}-#{c}-#{SecureRandom.hex( 2 )}-#{SecureRandom.hex( 2 )}-#{SecureRandom.hex( 2 )}-#{SecureRandom.hex( 2 )}"
    query = ''
    case c
    when 'r'
      query = "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';"
    when 'm'
      query = "SELECT * FROM #{$MYSQL_TB_MENU} WHERE code='#{code}';"
    when 'f'
      query = "SELECT * FROM #{$MYSQL_TB_FCS} WHERE code='#{code}';"
    when 'z'
      query = "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE code='#{code}';"
    when 'p'
      query = "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE code='#{code}';"
    end
    r = mdb( query, false, false )
    break unless r.first
  end

  return code
end


#### 食品重量の決定
def food_weight_check( food_weight )
  fw = food_weight
  fw = '100' if fw == nil || fw == '' || fw == '0'
  fw.tr!( "０-９", "0-9" ) if /[０-９]/ =~ fw
  fw.sub!( '．', '.' )
  fw.sub!( '、', '.' )
  fw.sub!( ',', '.' )
  fw.sub!( '，', '.' )
  fw.sub!( '。', '.' )
  fw.sub!( '／', '/')
  fw.sub!( '＋', '+')
  uv = BigDecimal( '0' )

  begin
    # 分数処理
    if /\d+\+\d+\/\d+/ =~ fw
      # 帯分数
      a = fw.scan( /(\d+)\+\d+\/\d+/ )[0][0].to_i
      b = fw.scan( /\d+\+(\d+)\/\d+/ )[0][0].to_i
      c = fw.scan( /\d+\+\d+\/(\d+)/ )[0][0].to_i
      if c == 0
        fw = 100
        uv = 100
      else
        uv = BigDecimal( b ) / c + a
      end
    elsif /\d+\/\d+/ =~ fw
      # 仮分数
      b = fw.scan( /(\d+)\/\d+/ )[0][0].to_i
      c = fw.scan( /\d+\/(\d+)/ )[0][0].to_i
      if c == 0
        fw = 100
        uv = 100
      else
        uv = BigDecimal( b ) / c
      end
    else
      uv = BigDecimal( fw )
    end
  rescue
    puts "<span class='error'>[food_weight_check]ERROR!!"
    puts "food_weight:#{food_weight}</span><br>"
    fw = 100
    uv = 100
  end

  return fw, uv
end


#### TAG要素の結合
def bind_tags( res_tag )
    tags = res_tag.first
    sub_class = ''
    sub_class << tags['class1'].sub( '+', '' ) if /\+$/ =~ tags['class1']
    sub_class << tags['class2'].sub( '+', '' ) if /\+$/ =~ tags['class2']
    sub_class << tags['class3'].sub( '+', '' ) if /\+$/ =~ tags['class3']
    tags = "<span class='tagc'>#{sub_class}</span> #{tags['name']} <span class='tag1'>#{tags['tag1']}</span> <span class='tag2'>#{tags['tag2']}</span> <span class='tag3'>#{tags['tag3']}</span> <span class='tag4'>#{tags['tag4']}</span> <span class='tag5'>#{tags['tag5']}</span>"

    return tags
end


#### 食品番号と重さを抽出
def extract_sum( sum, dish_num, ew_mode )
  foods = sum.split( "\t" )
  food_no = []
  food_weight = []
  total_weight = 0
  foods.each do |e|
    t = e.split( ':' )
    food_no << t[0]
    if t[0] == '-'
      food_weight << '-'
    elsif t[0] == '+'
      food_weight << '+'
    elsif ew_mode == 1 && t[7] != nil && t[7] != ''
      food_weight << ( BigDecimal( t[7] ) / dish_num ).floor( 2 )
      total_weight += ( BigDecimal( t[7] ) / dish_num ).floor( 2 )
    else
      food_weight << ( BigDecimal( t[1] ) / dish_num ).floor( 2 )
      total_weight += ( BigDecimal( t[1] ) / dish_num ).floor( 2 )
    end
  end

  return food_no, food_weight, total_weight
end


#### 合計値の桁合わせ
def adjust_digit( fct_item, fct_sum, frct_mode )
  fct_item.size.times do |fi|
    limit = @fct_frct[fct_item[fi]]
    if limit != nil
        case frct_mode
        # 四捨五入
        when 1
          fct_sum[fi] = fct_sum[fi].round( limit )
        # 切り上げ
        when 2
          fct_sum[fi] = fct_sum[fi].ceil( limit )
        # 切り捨て
        when 3
          fct_sum[fi] = fct_sum[fi].floor( limit )
        else
          fct_sum[fi] = fct_sum[fi].round( limit )
        end
        if limit == 0
            fct_sum[fi] = fct_sum[fi].to_i
        else
            fct_sum[fi] = fct_sum[fi].to_f
        end
    end
  end

  return fct_sum
end


#### 特殊数値変換
def convert_zero( t )
      t = 0 if t == nil
      t.to_s.sub!( '(', '' )
      t.to_s.sub!( ')', '' )
      t = 0 if t == '-'
      t = 0 if t == 'Tr'

  return t
end


#### 端数処理の設定
def frct_check( frct_mode )
  frct_mode = 1 if frct_mode == nil
  fs = []
  0.upto( 3 ) do |c|
    if frct_mode.to_i == c
      fs << 'selected'
    else
      fs << ''
    end
  end

  return frct_mode, fs
end


#### from unit volume to weight
def unit_weight( vol, uc, fn )
  w = 0.0
  r = mdb( "SELECT unitc FROM #{$MYSQL_TB_EXT} WHERE FN='#{fn}'", false, $DEBUG )
  if r.first
    if r.first['unitc']
      begin
        a = r.first['unitc'].split( ':' )
        w = ( BigDecimal( a[uc.to_i] ) * vol.to_f ).round( 1 )  unless  a[uc.to_i] == ''
      rescue
        puts "<span class='error'>[unit_weight]ERROR!!<br>"
        puts "vol:#{vol}<br>"
        puts "uc:#{uc}<br>"
        puts "fn:#{fn}</span><br>"
      end
    end
  end

  return w
end


#### for checkbox
def checked( bit )
  s = ''
  s = 'CHECKED' if bit == 1

  return s
end


#### for select
def selected( s, e, n )
  a = []
  s.upto( e ) do |c|
    if c == n.to_i
      a << 'SELECTED'
    else
      a << ''
    end
  end

  return a
end

#### for select 廃止予定
def selected_( a, b )
  s = ''
  s = 'SELECTED' if a == b

  return s
end


#==============================================================================
# CLASS
#==============================================================================

class User
  attr_accessor :name, :uid, :mom, :mid, :status, :aliasu, :language, :switch

  def initialize( cgi )
    @name = cgi.cookies['NAME'].first
    @uid = cgi.cookies[$COOKIE_UID].first
    @mid = cgi.cookies[$COOKIE_MID].first

    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{@name}' and cookie='#{@uid}' and status>0;" )
    db.close
    if res.first
      @status = res.first['status'].to_i
      @aliasu = res.first['aliasu']
      @mom = res.first['mom']
      @mom = @name if @mom == nil
      @language = res.first['language']
      @switch = res.first['switch'].to_i
    else
      @name = nil
      @uid = nil
      @mom = nil
      @mid = nil
      @status = 0
      @aliasu = nil
      @language = $DEFAULT_LP
      @switch = 0
    end
  end

  def load_lp( script )
    lp = [nil]
    f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{@language}", "r" )
    f.each do |line| lp << line.chomp.force_encoding( 'UTF-8' ) end
    f.close

    return lp
  end

  def debug()
    puts "name:#{@name}<br>"
    puts "uid:#{@uid}<br>"
    puts "status:#{@status}<br>"
    puts "alias:#{@alias}<br>"
    puts "lg:#{@lg}<br>"
    puts "<hr>"
  end
end


class FCT
  attr_accessor :n

  def initialize()
    @n = Hash.new
    @fct_item.each do |e| @n[e] = '' end
  end

  def load( code, user )
  end

  def debug()
  end

end


####
class Calendar
  attr_accessor :yyyy, :yyyyf, :mm, :mms, :dd, :dds, :ddl, :wd, :wf, :wl

  def initialize( uname, yyyy, mm, dd )
    @yyyy = yyyy
    @mm = mm
    @dd = dd

    if @yyyy == 0
      d = Date.today
    else
      d = Date.new( @yyyy, @mm, @dd )
    end
    @wd = Date.new( d.year, d.month, d.day ).wday
    @wf = Date.new( d.year, d.month, 1 ).wday
    @ddl = Date.new( d.year, d.month, -1 ).day
    @wl = Date.new( d.year, d.month, @ddl ).wday

    if @yyyy == 0
      @yyyy = d.year
      @mm = d.month
      @dd = d.day
    end

    @yyyyf = Time.now.year
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';" )
    db.close

    if res.first['koyomiy']
      a = res.first['koyomiy'].split( ':' )
      @yyyyf = a[0].to_i if a[0].to_i != 0
    end

    @mms = @mm
    @mms = "0#{mms}" if @mm < 10
    @dds = @dd
    @dds = "0#{dds}" if @dd < 10
  end

  def move_mm( mm )
    @mm += mm
    if @mm > 12
      @yyyy += 1
      @mm = 1
    end

    if @mm < 1
      @yyyy -= 1
      @mm = 12
    end

    d = Date.new( @yyyy, @mm, @dd )
    @wf = Date.new( d.year, d.month, 1 ).wday
    @ddl = Date.new( d.year, d.month, -1 ).day
    @wl = Date.new( d.year, d.month, @ddl ).wday
  end

  def debug()
    puts "calender.yyyy:#{@yyyy}<br>"
    puts "calender.yyyyf:#{@yyyyf}<br>"
    puts "calender.mm:#{@mm}<br>"
    puts "calender.dd:#{@dd}<br>"
    puts "calender.ddl:#{@ddl}<br>"
    puts "calender.wf:#{@wf}<br>"
    puts "calender.wl:#{@wl}<br>"
  end
end


class Config
  attr_accessor :x

  def initialize()
  end
end


class Sum
  attr_accessor :code, :name, :dish, :protect, :fn, :weight, :unit, :unitv, :check, :init, :rr, :ew

  def initialize()
    @code = nil
    @name = nil
    @dish = 1
    @protect = 0
    @fn = nil
    @weight = 0
    @unit = 0
    @unitv = 0
    @check = 0
    @init = ''
    @rr = 1.0
    @ew = 0
  end

  def load_sum( sum )
    t = sum.split( ':' )
    @fn = t[0]
    @weight = t[1]
    @unit = t[2]
    @unitv = t[3]
    @check = t[4]
    @init = t[5]
    if t[6] == nil || t[6] == ''
      @rr = 1.0
    elsif t[6].to_f > 1
      @rr = 1.0
    elsif t[6].to_f < 0
      @rr = 0.0
    else
      @rr = t[6]
    end
    @ew = t[7]
  end

  def load_recipe( code )
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT code, name, sum, dish, protect from #{$MYSQL_TB_RECIPE} WHERE code='#{code}';" )
    db.close

    @code = res.first['code']
    @name = res.first['name']
    @dish = res.first['dish'].to_i if dish == nil
    @protect = res.first['protect'].to_i
    sum = res.first['sum']
    sum.split( "\t" ).each do |e|
      t = e.split( ':' )
      @fn = t[0]
      @weight = t[1]
      @unit = t[2]
      @unitv = t[3]
      @check = t[4]
      @init = t[5]
      if t[6] == nil || t[6] == ''
        @rr = 1.0
      elsif t[6].to_f > 1
        @rr = 1.0
      elsif t[6].to_f < 0
        @rr = 0.0
      else
        @rr = t[6]
      end
      @ew = t[7]
    end
  end

  def update_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "UPDATE #{$MYSQL_TB_SUM} set code='#{@code}', name='#{@name}', dish='#{@dish}', meal='#{@meal}', protect='#{@protect}', fn='#{@fn}', weight='#{@weight}', unit='#{@unit}', unitv='#{@unitv}', check='#{@check}', init='#{@init}', rr='#{@rr}', ew='#{@ew}' WHERE user='#{@user}';" )
    db.close
  end

  def debug()
    puts "code:#{code}<br>"
    puts "recipe_name:#{recipe_name}<br>"
    puts "dish_num:#{dish_num}<br>"
    puts "protect:#{protect}<br>"
    puts "sum:#{sum}<br>"
    puts "<hr>"
  end
end


class Recipe
  attr_accessor :code, :user, :branch, :root, :public, :protect, :draft, :name, :dish, :type, :role, :tech, :time, :cost, :sum, :protocol, :media, :date

  def initialize( user )
    @code = nil
    @user = user
    @branch = 0
    @root = ''
    @public = 0
    @protect = 0
    @draft = 0
    @name = nil
    @dish = 1
    @type = 0
    @role = 0
    @tech = 0
    @time = 0
    @cost = 0
    @sum = ''
    @protocol = ''
    @date = Time.now.strftime("%Y-%m-%d %H:%M:%S")
    @media = []
  end

  def load_cgi( cgi )
    @code = cgi['code']
    @public = cgi['public'].to_i
    @protect = cgi['protect'].to_i
    @draft = cgi['draft'].to_i
    @name = cgi['recipe_name']
    @type = cgi['type'].to_i
    @role = cgi['role'].to_i
    @tech = cgi['tech'].to_i
    @time = cgi['time'].to_i
    @cost = cgi['cost'].to_i
    @protocol = cgi['protocol']
  end

  def load_db( code, mode )
    res = nil
    if mode
      @code = code
      db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
      res = db.query( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';" )
      db.close
      if res.first
        res = res.first
      else
        puts "<span class='error'>[Recipe load]ERROR!!<br>"
        puts "code:#{@code}</span><br>"
      end
    else
      res = code
      @code = res['code']
    end

    @user = res['user'].to_s
    @branch = res['branch'].to_i
    @root = res['root'].to_s
    @public = res['public'].to_i
    @protect = res['protect'].to_i
    @draft = res['draft'].to_i
    @name = res['name'].to_s
    @dish = res['dish'].to_i
    @type = res['type'].to_i
    @role = res['role'].to_i
    @tech = res['tech'].to_i
    @time = res['time'].to_i
    @cost = res['cost'].to_i
    @sum = res['sum'].to_s
    @protocol = res['protocol'].to_s
    @date = res['date']
  end

  def insert_db()
      db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
      db.query( "INSERT INTO #{$MYSQL_TB_RECIPE} SET code='#{@code}', user='#{@user}', dish=#{@dish}, branch='#{@branch}', root='#{@root}', draft=#{@draft}, protect=#{@protect}, public=#{@public}, name='#{@name}', type=#{@type}, role=#{@role}, tech=#{tech}, time=#{@time}, cost=#{@cost}, sum='#{@sum}', protocol='#{@protocol}', date='#{@date}';" )
      db.close
  end

  def update_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "UPDATE #{$MYSQL_TB_RECIPE} SET name='#{@name}', dish=#{@dish}, branch='#{@branch}', root='#{@root}', type=#{@type}, role=#{@role}, tech=#{@tech}, time=#{@time}, cost=#{@cost}, sum='#{@sum}', protocol='#{@protocol}', public=#{@public}, protect=#{@protect}, draft=#{@draft}, date='#{@date}' WHERE user='#{@user}' and code='#{@code}';" )
    db.close
  end

  def load_media()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and code='#{@code}';" )
    db.close
    @media = []
    res.each do |e| @media << e['mcode'] end
  end

  def delete_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "DELETE FROM #{$MYSQL_TB_RECIPE} WHERE user='#{@user}' and code='#{@code}';" )
    db.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and code='#{@code}';" )
    db.close
  end

  def debug
    puts "Recipe.code:#{@code}<br>"
    puts "Recipe.name:#{@name}<br>"
    puts "Recipe.public:#{@public}<br>"
    puts "Recipe.protect:#{@protect}<br>"
    puts "Recipe.draft:#{@draft}<br>"
    puts "Recipe.type:#{@type}<br>"
    puts "Recipe.role:#{@role}<br>"
    puts "Recipe.tech:#{@tech}<br>"
    puts "Recipe.dish:#{@dish}<br>"
    puts "Recipe.time:#{@time}<br>"
    puts "Recipe.cost:#{@cost}<br>"
    puts "Recipe.sum:#{@sum}<br>"
    puts "Recipe.protocol:#{@protocol}<br>"
    puts "Recipe.date:#{@date}<br>"
    puts "Recipe.media:#{@media}<br>"
  end
end


class Meal
  attr_accessor :user, :code, :name, :meal, :protect

  def initialize( user )
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT * from #{$MYSQL_TB_MEAL} WHERE user='#{user}';" )
    db.close
    @user = user
    @code = res.first['code'].to_s
    @name = res.first['name'].to_s
    @meal = res.first['meal'].to_s
    @protect = res.first['protect'].to_i
    @media = []
  end

  def load_menu( code )
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT * from #{$MYSQL_TB_MENU} WHERE code='#{code}';" )
    db.close
    @code = code
    @name = res.first['name'].to_s
    @user = res.first['user'].to_s
    @name = res.first['name'].to_s
    @meal = res.first['meal'].to_s
    @protect = res.first['protect'].to_i
  end

  def update_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "UPDATE #{$MYSQL_TB_MEAL} set code='#{@code}', name='#{@name}', meal='#{@meal}', protect='#{@protect}' WHERE user='#{@user}';" )
    db.close
  end

  def debug()
    puts "user:#{@user}<br>"
    puts "code:#{@code}<br>"
    puts "name:#{@name}<br>"
    puts "meal:#{@meal}<br>"
    puts "protect:#{@protect}<br>"
    puts "<hr>"
  end
end


class Menu
  attr_accessor :user, :code, :name, :meal, :protect, :public, :label, :new_label, :memo, :media

  def initialize( user )
    @code = nil
    @user = user
    @name = nil
    @meal = nil
    @protect = 0
    @public = 0
    @label = nil
    @new_label = nil
    @memo = nil
    @media = []
  end

  def load_cgi( cgi )
    @code = cgi['code'].to_s
    @name = cgi['menu_name'].to_s
    @protect = cgi['protect'].to_i
    @public = cgi['public'].to_i
    @label = cgi['label'].to_s
    @new_label = cgi['new_label'].to_s
    @memo = cgi['memo'].to_s
  end

  def load_db( code, mode )
    res = nil
    if mode
      @code = code
      db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
      res = db.query( "SELECT * from #{$MYSQL_TB_MENU} WHERE code='#{code}';" )
      db.close
      if res.first
        res = res.first
      else
        puts "<span class='error'>[Menu load]ERROR!!<br>"
        puts "code:#{@code}</span><br>"
      end
    else
      res = code
      @code = res['code']
    end

    @user = res['user'].to_s
    @name = res['name'].to_s
    @meal = res['meal'].to_s
    @label = res['label'].to_s
    @protect = res['protect'].to_i
    @public = res['public'].to_i
    @memo = res['memo'].to_s
  end

  def load_media()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and code='#{@code}';" )
    db.close
    @media = []
    res.each do |e| @media << e['mcode'] end
  end

  def insert_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "INSERT INTO #{$MYSQL_TB_MENU} SET code='#{@code}', user='#{@user}',public='#{@public}',protect='#{@protect}', label='#{@label}', name='#{@name}', meal='#{@meal}', memo='#{@memo}';" )
    db.close
  end

  def update_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "UPDATE #{$MYSQL_TB_MENU} SET public='#{@public}', protect='#{@protect}', label='#{@label}', name='#{@name}', meal='#{@meal}', memo='#{@memo}' WHERE user='#{@user}' and code='#{@code}';" )
    db.close
  end

  def delete_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "DELETE FROM #{$MYSQL_TB_MENU} WHERE user='#{@user}' and code='#{@code}';" )
    db.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and code='#{@code}';" )
    db.close
  end

  def debug()
    puts "code:#{@code}<br>"
    puts "user:#{@user}<br>"
    puts "name:#{@name}<br>"
    puts "protect:#{@protect}<br>"
    puts "public:#{@public}<br>"
    puts "meal:#{@meal}<br>"
    puts "label:#{@label}<br>"
    puts "new_label:#{@new_label}<br>"
    puts "memo:#{@memo}<br>"
    puts "media:#{@media}<br>"
    puts "<hr>"
  end
end
