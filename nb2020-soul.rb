#Nutrition browser 2020 soul 1.5b (2024/02/13)

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

$GM = 'gm'

$SERVER_PATH = '/var/www'
$HTDOCS_PATH = "#{$SERVER_PATH}/htdocs/nb"
$TMP_PATH = '/tmp'
$NBURL = 'https://bacura.jp/nb/'
$MYURL = 'http://localhost/nb/'

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
$MYSQL_TB_MEMORY = 'memory'
$MYSQL_TB_MENU = 'menu'
$MYSQL_TB_METS = 'mets'
$MYSQL_TB_METST = 'metst'
$MYSQL_TB_MODJ = 'modj'
$MYSQL_TB_NOTE = 'note'
$MYSQL_TB_PAG = 'pag'
$MYSQL_TB_PALETTE = 'palette'
$MYSQL_TB_PARA = 'ref_para'
$MYSQL_TB_PRICE = 'price'
$MYSQL_TB_PRICEM = 'pricem'
$MYSQL_TB_RECIPE = 'recipe'
$MYSQL_TB_RECIPEI = 'recipei'
$MYSQL_TB_REFITS = 'ref_its'
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
$PHOTO_PATHS = "#{$SERVER_PATH}/#{$PHOTO}"
$SIZE_MAX = 20000000
$TN_SIZE = 400
$TNS_SIZE = 40
$PHOTO_SIZE_MAX = 2000

$JS_PATH = 'js'
$CSS_PATH = 'scss'
$BOOK_PATH = 'books'

$SELECT = { true => 'SELECTED', false => '', 1 => 'SELECTED', 0 => '', '1' => 'SELECTED', '0' => ''}
$CHECK = { true => 'CHECKED', false => '', 1 => 'CHECKED', 0 => '', '1' => 'CHECKED', '0' => ''}
$DISABLE = { true => 'DISABLED', false => '', 1 => 'DISABLED', 0 => '', '1' => 'DISABLED', '0' => ''}

begin
  $DB = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
rescue
  $DB = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :encoding => "utf8" )
end

$DEBUG = false

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
  res = $DB.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{uname}' and cookie='#{uid}' and status>0;" )
  soul_language = res.first['language'] if res.first
end
soul_language = $DEFAULT_LP if soul_language == nil

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


#### Isolation photo init
def iso_init( cookie )
  puts "Content-type: image/jpeg\n"
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
#将来的に廃止
def mdb( query, html_opt, debug )
  puts "<span class='dbq'>[mdb]#{query}</span><br>" if debug
  begin
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    t = query.chop
    if /[\;\$]/ =~ t
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
def add_his( user, code )
  return if user.status == 7 || user.status == 0

  his_max = 200
  r = $DB.query( "SELECT history FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';" )
  if r.first
    if r.first['history'] != nil && r.first['history'] != ''
      history = JSON.parse( r.first['history'] )
      his_max = history['his_max'].to_i if history['his_max']
    end
  end
  his_max = 200 if his_max < 200 || his_max > 1000

  current_his = []
  r = $DB.query( "SELECT his FROM #{$MYSQL_TB_HIS} WHERE user='#{user.name}';" )
  if r.first
    current_his = r.first['his'].split( "\t" )
  end

  current_his.unshift << code
  current_his.delete( '' )
  current_his.uniq!
  new_his = current_his.take( his_max ).join( "\t" )
  
  $DB.query( "UPDATE #{$MYSQL_TB_HIS} SET his='#{new_his}' WHERE user='#{user.name}';" )
end


#### コードの生成
def generate_code( uname, c )
  skip = false
  code = uname[0, 2]

  10.times do
    code = "#{code}-#{c}-#{SecureRandom.alphanumeric( 20 )}"
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
      r = $DB.query( query )
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
  t.to_s.sub!( '(', '' )
  t.to_s.sub!( ')', '' )
  t.to_s.sub!( '†', '' )
  t = 0 if t == nil
  t = 0 if t == ""
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
  txt.gsub!( '&', '&amp;' )
  txt.gsub!( '"', '&quot;' )
  txt.gsub!( "'", '&#39;' )

  return txt
end


#### for checkbox
#### Obsolete in the future
def checked( bit )
  s = ''
  s = 'CHECKED' if bit == 1

  return s
end


#### for select
#### Obsolete in the future
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


#==============================================================================
# CLASS
#==============================================================================

class Db
  attr_reader :user

  def initialize( user, debug, html )
    @user = user
    @debug = debug
    @status = 0
    @status = @user.status unless @user == nil
    @html = html
  end

  def qq( query )
    q = query.gsub( ';', '' ) << ';'
    return $DB.query( q )
  end

  def query( query, barrier )
    puts "<span class='dbq'>[db]#{query}</span><br>" if @debug
    begin
      if @status == 7 && barrier
          puts "<span class='ref_error'>[db]Astral user barrier!</span><br>"
          exit( 9 )
      end

      t = query.chop
      if /[\;\$]/ =~ t
          puts "<span class='error'>[db]ERROR!!</span><br>"
          exit( 9 )
      end
      return $DB.query( query )

    rescue
      if @html
        html_init( nil )
        html_head( nil )
      end
        puts "<span class='error'>[db]ERROR!!</span><br>"
    end
  end
end

class User
  attr_accessor :name, :uid, :mom, :mid, :status, :aliasu, :switch, :language, :pass, :mail, :astral, :reg_date

  def initialize( cgi )
    @name = cgi.cookies['NAME'].first
    @uid = cgi.cookies[$COOKIE_UID].first
    @mid = nil
    @pass = nil
    @mail = nil
    @reg_date  = nil

    res = $DB.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{@name}' and cookie='#{@uid}' and status>0;" )

    if res.first
      if res.first['status'].to_i == 7
        entity_name = @name.sub( '~', '' )

        res2 = $DB.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{entity_name}' and astral=1 and status>0;" )

        if res2.first
          @name = entity_name
          @mid = nil
          @uid = nil
          @mom = nil
          @mid = nil
          @status = 7
          @aliasu = nil
          @switch = 0
          @astral = 0
          @language = res.first['language']
        else
          @name = nil
          @uid = nil
          @mom = nil
          @mid = nil
          @status = 0
          @aliasu = nil
          @switch = 0
          @astral = 0
          @language = $DEFAULT_LP
        end
      else
        @status = res.first['status'].to_i
        @aliasu = res.first['aliasu']
        @aliasu = nil if @aliasu == ''
        @mom = res.first['mom']
        @mid = res.first['cookie_m']
        @switch = res.first['switch'].to_i
        @astral = res.first['astral'].to_i
        @language = res.first['language']
        @language = $DEFAULT_LP if @language == nil
      end
    else
      @name = nil
      @uid = nil
      @mom = nil
      @mid = nil
      @status = 0
      @aliasu = nil
      @switch = 0
      @astral = 0
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

  def initialize( user )
    @user = user
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
    res = $DB.query( "SELECT code, name, sum, dish, protect from #{$MYSQL_TB_RECIPE} WHERE code='#{code}';" )

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
    $DB.query( "UPDATE #{$MYSQL_TB_SUM} set code='#{@code}', name='#{@name}', dish='#{@dish}', meal='#{@meal}', protect='#{@protect}', fn='#{@fn}', weight='#{@weight}', unit='#{@unit}', unitv='#{@unitv}', check='#{@check}', init='#{@init}', rr='#{@rr}', ew='#{@ew}' WHERE user='#{@user}';" ) unless @user.status == 7
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
  attr_accessor :code, :user, :branch, :root, :favorite, :public, :protect, :draft, :name, :dish, :type, :role, :tech, :time, :cost, :sum, :protocol, :tags, :comment, :media, :date

  def initialize( user )
    @code = nil
    @user = user
    @branch = 0
    @root = ''
    @favorite = 0
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
    @favorite = cgi['favorite'].to_i
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
    @root = cgi['root']

    # excepting for tags
    @protocol.gsub!( '<', '&lt;')
    @protocol.gsub!( '>', '&gt;')
    @protocol.gsub!( ';', '；')
  end

  def load_db( code, mode ) # mode = ture -> from DB directly, mode = false -> from DB res object
    res = nil
    if mode
      @code = code
      res = $DB.query( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';" )
      if res.first
        res = res.first
      else
        puts "<span class='error'>[Recipe load]ERROR!!<br>"
        puts "code:#{@code}</span><br>"

        return false
      end
    else
      res = code
      @code = res['code']
    end

    @user.name = res['user'].to_s
    @branch = res['branch'].to_i
    @root = res['root'].to_s
    @favorite = res['favorite'].to_i
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

    return true
  end

  def insert_db()
    @name.gsub!( ';', '' )
    @protocol.gsub!( ';', '' )
    @date = @date.strftime( "%Y-%m-%d %H:%M:%S" ) unless @date.kind_of?( String )
    $DB.query( "INSERT INTO #{$MYSQL_TB_RECIPE} SET code='#{@code}', user='#{@user.name}', dish=#{@dish}, branch='#{@branch}', root='#{@root}', favorite=#{@favorite}, draft=#{@draft}, protect=#{@protect}, public=#{@public}, name='#{@name}', type=#{@type}, role=#{@role}, tech=#{tech}, time=#{@time}, cost=#{@cost}, sum='#{@sum}', protocol='#{@protocol}', date='#{@date}';" ) unless @user.status == 7
  end

  def update_db()
    @name.gsub!( ';', '' )
    @protocol.gsub!( ';', '' )
    @date = @date.strftime( "%Y-%m-%d %H:%M:%S" ) unless @date.kind_of?( String )
    $DB.query( "UPDATE #{$MYSQL_TB_RECIPE} SET name='#{@name}', dish=#{@dish}, branch='#{@branch}', root='#{@root}', type=#{@type}, role=#{@role}, tech=#{@tech}, time=#{@time}, cost=#{@cost}, sum='#{@sum}', protocol='#{@protocol}', public=#{@public}, favorite=#{@favorite}, protect=#{@protect}, draft=#{@draft}, date='#{@date}' WHERE user='#{@user.name}' and code='#{@code}';" ) unless @user.status == 7
  end

  def load_media()
    res = $DB.query( "SELECT code FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}' and origin='#{@code}' ORDER BY zidx;" )
    @media = []
    res.each do |e| @media << e['code'] end
  end

  def delete_db()
    $DB.query( "DELETE FROM #{$MYSQL_TB_RECIPE} WHERE user='#{@user.name}' and code='#{@code}';" ) unless @user.status == 7
    $DB.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}' and code='#{@code}';" ) unless @user.status == 7
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
    puts "Recipe.favorite:#{@favorite}<br>"
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
    puts "Recipe.root:#{@root}<br>"
    puts "Recipe.date:#{@date}<br>"
    puts "Recipe.media:#{@media}<br>"
  end
end



class Meal
  attr_accessor :user, :code, :name, :meal, :protect

  def initialize( user )
    res = $DB.query( "SELECT * from #{$MYSQL_TB_MEAL} WHERE user='#{user}';" )
    @user = user
    @code = res.first['code'].to_s
    @name = res.first['name'].to_s
    @meal = res.first['meal'].to_s
    @protect = res.first['protect'].to_i
    @media = []
  end

  def load_menu( code )
    res = $DB.query( "SELECT * from #{$MYSQL_TB_MENU} WHERE code='#{code}';" )
    @code = code
    @name = res.first['name'].to_s
    @user = res.first['user'].to_s
    @name = res.first['name'].to_s
    @meal = res.first['meal'].to_s
    @protect = res.first['protect'].to_i
  end

  def update_db()
    @name.gsub!( ';', '' )
    $DB.query( "UPDATE #{$MYSQL_TB_MEAL} set code='#{@code}', name='#{@name}', meal='#{@meal}', protect='#{@protect}' WHERE user='#{@user}';" ) unless @user.status == 7
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
      res = $DB.query( "SELECT * from #{$MYSQL_TB_MENU} WHERE code='#{code}';" )
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
    res = $DB.query( "SELECT code FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and origin='#{@origin}';" )
    @media = []
    res.each do |e| @media << e['code'] end
  end

  def insert_db()
    $DB.query( "INSERT INTO #{$MYSQL_TB_MENU} SET code='#{@code}', user='#{@user}',public='#{@public}',protect='#{@protect}', label='#{@label}', name='#{@name}', meal='#{@meal}', memo='#{@memo}';" ) unless @user.status == 7
  end

  def update_db()
    $DB.query( "UPDATE #{$MYSQL_TB_MENU} SET public='#{@public}', protect='#{@protect}', label='#{@label}', name='#{@name}', meal='#{@meal}', memo='#{@memo}' WHERE user='#{@user}' and code='#{@code}';" ) unless @user.status == 7
  end

  def delete_db()
    $DB.query( "DELETE FROM #{$MYSQL_TB_MENU} WHERE user='#{@user}' and code='#{@code}';" ) unless @user.status == 7
    $DB.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user}' and origin='#{@code}';" ) unless @user.status == 7
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
  attr_accessor :user, :code, :muser, :series, :base, :origin, :alt, :type, :date, :zidx

  def initialize( user )
    @code = nil
    @user = user
    @muser = nil
    @base = nil
    @origin = nil
    @type = nil
    @alt = nil
    @date = nil
    @zidx = 0
    @series = []
  end

  def load_db( code )
    res = $DB.query( "SELECT * from #{$MYSQL_TB_MEDIA} WHERE code='#{code}';" )

    if res.first
      @code = res.first['code'].to_s
      @muser = res.first['user'].to_s
      @base = res.first['base'].to_s
      @origin = res.first['origin'].to_s
      @type = res.first['type'].to_s
      @alt = res.first['alt'].to_s
      @date = res.first['date']
      @zidx = res.first['zidx'].to_i
    else
      puts "<span class='error'>[Media load]ERROR!!<br>"
      puts "code:#{@code}</span><br>"
    end

  end

  def save_db()
    @zidx = @series.size
    $DB.query( "INSERT INTO #{$MYSQL_TB_MEDIA} SET user='#{@user.name}', code='#{@code}', base='#{@base}', origin='#{@origin}', type='#{@type}', alt='#{@alt}', date='#{@date}', zidx='#{@zidx}';" ) unless @user.status == 7
  end

  def delete_db()
    $DB.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}' and code='#{@code}';" ) unless @user.status == 7
  end

  def load_series()
    unless @origin == '' || @origin == nil
      res = $DB.query( "SELECT * from #{$MYSQL_TB_MEDIA} WHERE origin='#{@origin}' ORDER BY zidx;" )
      @muser = res.first['user'] if res.first
      res.each do |e|
        @series << e['code'] end
    end
  end

  def move_series()
    @series.delete( @code )
    @series.insert( @zidx.to_i, @code )
    @series.each.with_index do |e, i|
      $DB.query( "UPDATE #{$MYSQL_TB_MEDIA} SET zidx='#{i}' WHERE code='#{e}' AND origin='#{@origin}';" ) unless @user.status == 7
    end
  end

  def delete_series()
    unless @origin == '' || @origin == nil
      $DB.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}' and origin='#{@origin}';" ) unless @user.status == 7
    end
  end

  def count()
    res = $DB.query( "SELECT COUNT(code), MIN(date), MAX(date) FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}';" )
    count = res.first['COUNT(code)']
    min = res.first['MIN(date)'].strftime( "%Y" ).to_i
    max = res.first['MAX(date)'].strftime( "%Y" ).to_i

    return count, min, max
  end

  def bases()
    bases = []
    res = $DB.query( "SELECT DISTINCT base FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}';" )
    res.each do |r| bases << r['base'] end

    return bases
  end

  def debug()
    puts "user:#{@user.name}<br>"
    puts "code:#{@code}<br>"
    puts "base:#{@base}<br>"
    puts "origin:#{@origin}<br>"
    puts "type:#{@type}<br>"
    puts "alt:#{@alt}<br>"
    puts "date:#{@date}<br>"
    puts "series:#{@series}<br>"
    puts "<hr>"
  end
end
