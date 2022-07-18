#Nutrition browser 2020 soul 0.4b

#==============================================================================
# LIBRARY
#==============================================================================
require 'cgi'
require 'mysql2'
require 'securerandom'
require 'json'


#==============================================================================
#STATIC
#==============================================================================
$DEBUG = false

$GM = 'gm'

$SERVER_PATH = '/var/www'
$HTDOCS_PATH = "#{$SERVER_PATH}/htdocs/nb"
$TMP_PATH = '/tmp'

$COOKIE_UID = 'UID2020'

$MYSQL_HOST = 'localhost'
$MYSQL_DB = 'nb2020'
$MYSQL_DBR = 'rr2020'
$MYSQL_USER = 'user'
$MYSQL_USERR = 'userr'
$MYSQL_PW = 'password'
$MYSQL_TB_CFG = 'cfg'
$MYSQL_TB_DIC = 'dic'
$MYSQL_TB_EXT = 'ext'
$MYSQL_TB_FCT = 'fct'
$MYSQL_TB_FCTP = 'fctp'
$MYSQL_TB_FCTS = 'fcts'
$MYSQL_TB_FCZ = 'fcz'
$MYSQL_TB_HIS = 'his'
$MYSQL_TB_KOYOMI = 'koyomi'
$MYSQL_TB_KOYOMIEX = 'koyomiex'
$MYSQL_TB_MEAL = 'meal'
$MYSQL_TB_MEDIA = 'media'
$MYSQL_TB_METS = 'mets'
$MYSQL_TB_METST = 'metst'
$MYSQL_TB_MODJ = 'modj'
$MYSQL_TB_NOTE = 'note'
$MYSQL_TB_PALETTE = 'palette'
$MYSQL_TB_PRICE = 'price'
$MYSQL_TB_PRICEM = 'pricem'
$MYSQL_TB_RECIPE = 'recipe'
$MYSQL_TB_RECIPEI = 'recipei'
$MYSQL_TB_SCHOOLK = 'schoolk'
$MYSQL_TB_SCHOOLM = 'schoolm'
$MYSQL_TB_SCHOOLC = 'schoolc'
$MYSQL_TB_SLOGF = 'slogf'
$MYSQL_TB_SLOGR = 'slogr'
$MYSQL_TB_SLOGM = 'slogm'
$MYSQL_TB_SUM = 'sum'
$MYSQL_TB_TAG = 'tag'
$MYSQL_TB_USER = 'user'

$PHOTO = 'photo_'
$PHOTO_PATH = "#{$HTDOCS_PATH}/#{$PHOTO}"
$SIZE_MAX = 20000000
$TN_SIZE = 400
$TNS_SIZE = 40
$PHOTO_SIZE_MAX = 2000

$JS_PATH = 'js'
$CSS_PATH = 'css'
$BOOK_PATH = 'books'

$SELECT = { true => 'SELECTED', false => ''}
$CHECK = { true => 'CHESCKED', false => ''}
$DISABLE = { true => 'DISABLED', false => ''}

#==============================================================================
# CORE LANGAGE & CGI
#==============================================================================
$LP = ['jp']
$DEFAULT_LP = $LP[0]
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

require "#{$SERVER_PATH}/nb2020-local-#{soul_language}"


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


#### TEXT init
def text_init
  puts "Content-type: text/text\n"
  puts "\n"
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


#### DB process
def mdb( query, html_opt, debug )
  puts "<span class='dbq'>[mdb]#{query}</span><br>" if debug
  begin
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    t = query.chop
    if /[\;\#\$\@]/ =~ t
        puts "<span class='error'>[mdb]ERROR!!</span><br>"
        exit( 9 )
    end
    res = db.query( query )
    db.close
  rescue
    if html_opt
      html_init( nil )
      html_head( nil )
    end
      puts "<span class='error'>[mdb]ERROR!!</span><br>"
  end
  return res
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
  skip = false
  code = uname[0, 2]
  10.times do
    code = "#{code}-#{c}-#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}"
    query = ''
    case c
    when 'm'
      query = "SELECT * FROM #{$MYSQL_TB_MENU} WHERE code='#{code}';"
    when 'n'
      query = "SELECT * FROM #{$MYSQL_TB_NOTE} WHERE code='#{code}';"
    when 'p', 'png', 'pdf'
      query = "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE code='#{code}';"
    when 'r'
      query = "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';"
    when 'z'
      query = "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE code='#{code}';"
    else
      skip = true
      break;
    end

    unless skip
      r = mdb( query, false, false )
      break unless r.first
    end
  end

  return code
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


#### 特殊数値変換
def convert_zero( t )
  t = 0 if t == nil
  t.to_s.sub!( '(', '' )
  t.to_s.sub!( ')', '' )
  t = 0 if t == '-'
  t = 0 if t == 'Tr'
  t = 0 if t == '*'

  return t
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
    elsif num == '*'
      return '*'
    elsif num == ''
      return ''
    else
      weight = weight / 100
      #weight_f = 1 if weight_f < 0

      case mode
      when '1'  # 四捨五入
        ans = ( BigDecimal( num ) * weight ).round( limit )
      when '2'  # 切り上げ
        ans = ( BigDecimal( num ) * weight ).ceil( limit )
      when '3'  # 切り捨て
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


#### Text washing
def wash( txt )
  txt.gsub!( ';', '' )
  txt.gsub!( "\t", '' )
  txt.gsub!( '<', '&lt;' )
  txt.gsub!( '>', '&gt;' )

  return txt
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


#### Photos
def photos( user, code, del_icon, tn_size )
  r = mdb( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND code='#{code}';", false, @debug )

  html = "<div class='row'>"
  r.each do |e|
    html << "<div class='col'>"
    html << "<span onclick=\"photoDel( '#{code}', '#{e}' )\">#{del_icon}</span><br>"
    html << "<img src='#{$PHOTO}/#{e}-tn.jpg' width='#{tn_size}px' class='img-thumbnail'>"
    html << "</div>"
  end
  html << "</div>"
  html = 'No photo' if r.size == 0

  return html
end


#==============================================================================
# CLASS
#==============================================================================

class User
  attr_accessor :name, :uid, :mom, :mid, :status, :aliasu, :switch, :language, :pass, :mail, :reg_date

  def initialize( cgi )
    @name = cgi.cookies['NAME'].first
    @uid = cgi.cookies[$COOKIE_UID].first
    @mid = nil
    @pass = nil
    @mail = nil
    @reg_date  = nil

    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{@name}' and cookie='#{@uid}' and status>0;" )
    db.close
    if res.first
      @status = res.first['status'].to_i
      @aliasu = res.first['aliasu']
      @aliasu = nil if @aliasu == ''
      @mom = res.first['mom']
      @mid = res.first['cookie_m']
      @switch = res.first['switch'].to_i
      @language = res.first['language']
    else
      @name = nil
      @uid = nil
      @mom = nil
      @mid = nil
      @status = 0
      @aliasu = nil
      @switch = 0
      @language = $DEFAULT_LP
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
    puts "aliasu:#{@aliasu}<br>"
    puts "mom:#{@mom}<br>"
    puts "mid:#{@mid}<br>"
    puts "language:#{@language}<br>"
    puts "<hr>"
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
  attr_accessor :code, :user, :branch, :root, :public, :protect, :draft, :name, :dish, :type, :role, :tech, :time, :cost, :sum, :protocol, :tags, :comment, :media, :date

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
    @tags = []
    @comment = ''
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

    # excepting for tags
    @protocol.gsub!( '<', '&lt;')
    @protocol.gsub!( '>', '&gt;')
    @protocol.gsub!( ';', '；')
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

    a = @protocol.split( "\n" )
    if /^\#/ =~ a[0]
      a[0].sub!(  '#', '' )
      a[0].gsub!( "　", "\t" )
      a[0].gsub!( "\s", "\t" )
      @tags = a[0].chomp.split( "\t" )
    end
    @comment = a[1].chomp.sub( '#', '' ) if /^\#/ =~ a[1]
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

  def tag()
    tags = []
    if /^\#/ =~ @protocol
      a = @protocol.split( "\n" )
      a[0].sub!( '#', '' )
      a[0].gsub!( '　', "\s" )
      tags = a[0].split( "\s" )
      tags.uniq!
    end

    return tags
  end

  def note()
    note = ''
    if /^\#/ =~ @protocol
      a = @protocol.split( "\n" )
      note = a[1].sub( '#', '' ) if /^\#/ =~ a[1]
    end

    return note
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
  attr_accessor :user, :code, :name, :meal, :protect, :public, :label, :memo, :media

  def initialize( user )
    @code = nil
    @user = user
    @name = nil
    @meal = nil
    @protect = 0
    @public = 0
    @label = nil
    @memo = nil
    @media = []
  end

  def load_cgi( cgi )
    @code = cgi['code'].to_s
    @name = cgi['menu_name'].to_s
    @protect = cgi['protect'].to_i
    @public = cgi['public'].to_i
    @label = cgi['label'].to_s
    @memo = cgi['memo'].to_s

    # excepting for tags
    @memo.gsub!( '<', '&lt;')
    @memo.gsub!( '>', '&gt;')
    @memo.gsub!( ';', '；')
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
    puts "memo:#{@memo}<br>"
    puts "media:#{@media}<br>"
    puts "<hr>"
  end
end

class Media
  attr_accessor :user, :code, :mcode, :muser, :series, :origin, :type, :date

  def initialize( user )
    @code = nil
    @user = user.name
    @mcode = nil
    @muser = nil
    @origin = nil
    @type = nil
    @date = nil
    @series = []
  end

  def load_db( mcode )
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    res = db.query( "SELECT * from #{$MYSQL_TB_MEDIA} WHERE mcode='#{mcode}';" )
    db.close

    if res.first
      @mcode = res.first['mcode'].to_s
      @muser = res.first['user'].to_s
      @code = res.first['code'].to_s
      @origin = res.first['origin'].to_s
      @type = res.first['type'].to_s
      @date = res.first['date']
    else
      puts "<span class='error'>[Media load]ERROR!!<br>"
      puts "mcode:#{@mcode}</span><br>"
    end

  end

  def save_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "INSERT INTO #{$MYSQL_TB_MEDIA} SET user='#{@user}', code='#{@code}', mcode='#{@mcode}', origin='#{@origin}', type='#{@type}', date='#{@date}'" )
    db.close
  end

  def delete_db()
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    db.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and mcode='#{@mcode}';" )
    db.close
  end

  def load_series()
    unless @code == '' || @code == nil
      db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
      res = db.query( "SELECT * from #{$MYSQL_TB_MEDIA} WHERE code='#{@code}';" )
      db.close
      @muser = res.first['user'] if res.first
      res.each do |e| @series << e['mcode'] end
    end

    return @series
  end

  def delete_series()
    if code != nil
      db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
      db.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and code='#{@code}';" )
      db.close
    end
  end

  def debug()
    puts "user:#{@user}<br>"
    puts "code:#{@code}<br>"
    puts "mcode:#{@mcode}<br>"
    puts "origin:#{@origin}<br>"
    puts "date:#{@date}<br>"
    puts "series:#{@series}<br>"
    puts "<hr>"
  end
end
