#Nutrition browser 2020 brain 0.34b (2024/02/05)

#==============================================================================
#STATIC
#==============================================================================


#==============================================================================
# LIBRARY
#==============================================================================
require 'bigdecimal'
#require 'nkf'

#==============================================================================
#DEFINITION
#==============================================================================


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


#### RRトークン発行
def issue_token()
  token = SecureRandom.base64(16)

  return token
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


#### from unit volume to weight
def unit_weight( vol, uc, fn )
  w = 0.0
  r = $DB.query( "SELECT unit FROM #{$MYSQL_TB_EXT} WHERE FN='#{fn}'" )
  if r.first
    if r.first['unit'] != nil && r.first['unit'] != ''
      unith = JSON.parse( r.first['unit'] )
      begin
        w = ( BigDecimal( unith[uc].to_s ) * vol ).round( 1 )
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


#### 食品番号と一皿分の重さを抽出
#sumはデコード前のsum
#dishはsumが何皿分を示す数値
#ew_modeは0->通常重量、1->予想重量
def extract_sum( sum, dish, ew_mode )
  foods = sum.split( "\t" )
  fns = []
  fws = []
  tw = 0
  foods.each do |e|
    t = e.split( ':' )
    fns << t[0]
    if t[0] == '-' || t[0] == '+'
      fws << 0
    elsif ew_mode == 1 && t[7] != nil && t[7] != ''
      fws << ( BigDecimal( t[7] ) / dish.to_i ).floor( 2 )
      tw += ( BigDecimal( t[7] ) / dish.to_i ).floor( 2 )
    else
      fws << ( BigDecimal( t[1] ) / dish.to_i ).floor( 2 )
      tw += ( BigDecimal( t[1] ) / dish.to_i ).floor( 2 )
    end
  end

  return fns, fws, tw
end


def menu2rc( uname, code )
  codes = []

  r = $DB.query( "SELECT meal FROM #{$MYSQL_TB_MENU} WHERE user='#{uname}' AND code='#{code}';" )
  if r.first
    a = r.first['meal'].split( "\t" )
    a.each do |e| codes << e end
  end

  return codes
end


def recipe2fns( db, code, rate, unit, ew_mode )
  ew_mode = 0 if ew_mode == nil
  fns = []
  fws = []
  tw = []

  r = $DB.query( "SELECT sum, dish FROM #{$MYSQL_TB_RECIPE} WHERE user='#{db.user.name}' AND code='#{code}';" )
  if r.first
    fns, fws, tw = extract_sum( r.first['sum'], r.first['dish'], ew_mode )

    if unit == '%'
      fws.map! do |x|
        x * rate / 100 if x != '-' && x != '+'
      end

    elsif unit == 'kcal'
      rr = db.query( "SELECT ENERC_KCAL FROM #{$MYSQL_TB_FCZ} WHERE user='#{db.user.name}' AND base='recipe' AND origin='#{code}';", false )
      rate = ( rate / BigDecimal( rr.first['ENERC_KCAL'] ))
      fws.map! do |x|
        x * rate if x != '-' && x != '+'
      end

    else
      fws.map! do |x|
        x * rate / tw if x != '-' && x != '+'
      end
    end
  end

  return fns, fws, tw
end


#### 特殊単位数変換
def unit_value( iv )
  ov = 0
  if iv >= 10
    ov = iv.to_i
  elsif iv >= 1
    tf = ( iv.to_i - iv ).to_f
    if tf == 0
      ov = iv.to_i
    else
      ov = iv.to_f
    end
  else
    ov = iv.to_f
  end

  return ov
end


#Extra liberally for plot
def exlib_plot()
  puts '<link rel="stylesheet" href="c3/c3.min.css">'
  puts '<script type="text/javascript" src="d3/d3.min.js"></script>'
  puts '<script type="text/javascript" src="c3/c3.min.js"></script>'
end

#==============================================================================
# CLASS
#==============================================================================

class Palette
  attr_accessor :sets, :bit

  def initialize( uname )
    @sets = Hash.new
    @bit = []
    if uname
      res = $DB.query( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';" )
      res.each do |e| @sets[e['name']] = e['palette'] end
    else
      $PALETTE_DEFAULT_NAME[$DEFAULT_LP].size.times do |c|
        @sets[$PALETTE_DEFAULT_NAME[$DEFAULT_LP][c]] = $PALETTE_DEFAULT[$DEFAULT_LP][c]
      end
    end
  end

  def set_bit( palette )
    palette = $PALETTE_DEFAULT_NAME[$DEFAULT_LP][1] if palette == '' || palette == nil
    @bit = @sets[palette].split( '' )
    @bit.map! do |x| x.to_i end
  end
end


class FCT
  attr_accessor :items, :names, :units, :frcts, :solid, :total, :fns, :foods, :weights, :refuses, :total_weight

  def initialize( item_, name_, unit_, frct_, frct_accu, frct_mode )
    @item = item_
    @name = name_
    @unit = unit_
    @frct = frct_
    @items = []
    @names = []
    @units = []
    @frcts = []
    @fns = []
    @foods = []
    @weights = []
    @refuses = []
    @solid = []
    @total = []
    @total_weight = BigDecimal( '0' )
    @frct_accu = frct_accu
    @frct_accu = 1 if @frct_accu == nil
    @frct_mode = frct_mode
    @frct_mode = 0 if @frct_mode == nil
  end

  def load_palette( palette )
    @items = []
    @names = []
    @units = []
    @frcts = []
    @item.size.times do |c|
      if palette[c] == 1 && @item[c] != 'REFUSE'
        @items << @item[c]
        @names << @name[@item[c]]
        @units << @unit[@item[c]]
        @frcts << @frct[@item[c]]
      end
    end
  end

  def set_food( uname, food_no, food_weight, non_food )
    c = 0
    food_no.each do |e|
      if e == '-'
        if non_food
          @fns << '-'
          @solid << '-'
          @foods << '-'
          @weights << '-'
          @refuses << '-'
        end
      elsif e == '+'
        if non_food
          @fns << '+'
          @solid << '+'
          @foods << '+'
          @weights << '+'
          @refuses << '+'
        end
      elsif e == '00000'
        if non_food
          @fns << '0'
          @solid << '0'
          @foods << ''
          @weights << '0'
          @refuses << '0'
        end
      else
        q = ''
        qq = ''
        if /P|C|U/ =~ e && uname != nil
          q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
          qq = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
        else
          q = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
          qq = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e}';"
        end
        res = $DB.query( q )
        if res.first
          @fns << e
          a = []
          @items.each do |ee|
            if ee != 'REFUSE'
              a << res.first[ee]
            else
              @refuses << res.first[ee]
            end
          end
          @solid << Marshal.load( Marshal.dump( a ))
          res2 = $DB.query( qq )
          @foods << bind_tags( res2 )
          @weights << food_weight[c]
        else
          c -= 1
        end
      end
      c += 1
    end
  end

  def calc()
    @total = []
    @items.size.times do |c| @total << BigDecimal( 0 ) end
    @total_weight = 0.0
    @foods.size.times do |f|
      @items.size.times do |i|
        if @weights[f] == 0
          @solid[f][i] = 0
        else
          t = @solid[f][i]
          t = 0 if t == nil
          t.to_s.sub!( '(', '' )
          t.to_s.sub!( ')', '' )
          t = 0 if t == 'Tr'
          t = 0 if t == '-'
          t = 0 if t == ''
          t = 0 if t == '*'
          t = ( BigDecimal( t.to_s ) * @weights[f] / 100 )

          if @frct_accu == 0
            case @frct_mode.to_i
            when 0, 1  # 四捨五入
              t = t.round( @frcts[i] )
            when 2  # 切り上げ
              t = t.ceil( @frcts[i] )
            when 3  # 切り捨て
              t = t.floor( @frcts[i] )
            end
          end
          @solid[f][i] = t
          @total[i] += t
        end
      end
      @total_weight += @weights[f]
    end
  end

  def digit()
    @foods.size.times do |f|
      @items.size.times do |i|
        if @frct_accu == 1
          case @frct_mode.to_i
          when 2  # 切り上げ
            @solid[f][i] = @solid[f][i].ceil( @frcts[i] )
          when 3  # 切り捨て
            @solid[f][i] = @solid[f][i].floor( @frcts[i] )
          else  # 四捨五入
            @solid[f][i] = @solid[f][i].round( @frcts[i] )
          end
        end

        if @frcts[i] == 0
          @solid[f][i] = @solid[f][i].to_i
        else
          @solid[f][i] = @solid[f][i].to_f
        end
      end
    end

    @items.size.times do |i|
      case @frct_mode.to_i
      when 2  # 切り上げ
        @total[i] = @total[i].ceil( @frcts[i] )
      when 3  # 切り捨て
        @total[i] = @total[i].floor( @frcts[i] )
      else
        @total[i] = @total[i].round( @frcts[i] )
      end

      if @frcts[i] == 0
        @total[i] = @total[i].to_i
      else
        @total[i] = @total[i].to_f
      end
    end
  end

  def singlet()
    @total = []
    @total_weight = @weights[0]
    @items.size.times do |i| @total[i] = BigDecimal( @solid[0][i].to_s ) end
  end

  def gramt( g )
    @items.size.times do |i|
      @total[i] = @total[i] / @total_weight * g
    end
  end

  def pickt( item )
    item_index = @items.index( item )
    if item_index
      return @total[item_index]
    else
      return nil
    end
  end

  def calc_pfc()
    ei = @items.index( 'ENERC_KCAL' )
    pi = @items.index( 'PROTV' )
    fi = @items.index( 'FATV' )
    pfc = []
    if ei != nil
      pfc[0] = ( @total[pi] * 4 / @total[ei] * 100 ).round( 1 )
      pfc[1] = ( @total[fi] * 4 / @total[ei] * 100 ).round( 1 )
      pfc[2] = ( 100 - pfc[0] - pfc[1] ).round( 1 )
    end

    return pfc
  end

  def into_solid( fct )
    @fns << nil
    @foods << nil
    @weights << 100
    @solid << Marshal.load( Marshal.dump( fct ))
  end

  def into_zero()
    @fns << nil
    @foods << nil
    @weights << 100
    zero = []
    @item.size.times do zero << 0 end
    @solid << Marshal.load( Marshal.dump( zero ))
  end

  def put_solid( item, solid_no, value )
    item_index = @items.index( item )
    if item_index
      @solid[solid_no][item_index] = value

      return true
    else
      return false
    end
  end

  def load_fcz( uname, fzcode, base )
    return false if fzcode == nil

    r = $DB.query( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{uname}' AND code='#{fzcode}' AND base='#{base}';" )
    if r.first
      a = []
      @items.each do |e|
        t = r.first[e]
        t = 0 if t == nil || t == ''
        a << BigDecimal( t )
      end
      @solid << Marshal.load( Marshal.dump( a ))
      @fns << fzcode
      @foods << base
      @weights << 100
      return true
    else
      puts "<span class='error'>FCZ load ERROR[#{fzcode}]</span>"
      return false
    end
  end

  def load_fctp( uname, code )
    r = $DB.query( "select * from #{$MYSQL_TB_FCTP} WHERE FN='#{code}' AND ( user='#{uname}' OR user='#{$GM}' );" )
    if r.first
      a = []
      @items.each do |e|
        t = r.first[e]
        t = 0 if t == nil || t == '' || t == '-'
        a << BigDecimal( t )
      end
      @solid << Marshal.load( Marshal.dump( a ))
      @fns << code
      @foods << 'fctp'
      @weights << 100

      return r.first['REFUSE'], r.first['Notice']
    else
      puts "<span class='error'>fctp load ERROR[#{code}]</span>"
      return nil, nil
    end
  end

  def load_cgi( cgi )
    a = []
    @items.each do |e|
      t = cgi[e]
      t = 0 if t == '' || t == nil || /[^0-9\-\.]/ =~ t
      a << BigDecimal( t )
    end
    @solid << Marshal.load( Marshal.dump( a ))
    @fns << cgi['food_code']
    @foods << cgi['food_name']
    t = cgi['food_weight']
    t = '100' if t == '' || t == nil || /[^0-9\-\.]/ =~ t
    @weights << BigDecimal( t )
  end

  def save_fcz( uname, zname, base, origin )
    fct_ = ''
    @items.size.times do |i| fct_ << "#{@items[i]}='#{@total[i]}'," end
    fct_.chop!

    code = ''
    r = $DB.query( "SELECT code FROM #{$MYSQL_TB_FCZ} WHERE user='#{uname}' AND origin='#{origin}' AND base='#{base}';" )
    if r.first
      $DB.query( "UPDATE #{$MYSQL_TB_FCZ} SET #{fct_} WHERE user='#{uname}' AND origin='#{origin}' AND base='#{base}';" )
      code = r.first['code']
    else
      code = generate_code( uname, 'z' )
      $DB.query( "INSERT INTO #{$MYSQL_TB_FCZ} SET code='#{code}', base='#{base}', name='#{zname}', user='#{uname}', origin='#{origin}', #{fct_};" )
    end

    return code
  end

  def sql()
    sql = ''
      @items.size.times do |i| sql << "#{@items[i]}='#{@total[i]}'," end
      sql.chop!

      return sql
  end


  def flash()
    @fns = []
    @foods = []
    @weights = []
    @refuses = []
    @solid = []
    @total = []
    @total_weight = BigDecimal( '0' )
  end


  def debug()
   # p @item
   # p @name
   # p @unit
   # p @frct

    p @fns
    p @foods
    p @weights
    p @refuses
    p @solid
    p @total
    p @total_weight
    p @frct_accu
    p @frct_mode

  end
end


class Memory
  attr_accessor :code, :user, :category, :pointer, :content, :date

  def initialize( user )
    @user = user
    @code = nil
    @category = nil
    @pointer = nil
    @content = nil
    @date = nil
    @public = 0
    @public = 1 if @user.status >= 8

  end

  def get_categories()
    array = []
    res = $DB.query( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};" )
    res.each do |e| array << e['category'] end

    return array
  end

  def get_pointers()
    array = []
    res = $DB.query( "SELECT DISTINCT pointer FROM #{$MYSQL_TB_MEMORY};" )
    res.each do |e| array << e['pointer'] end

    return array
  end

  def load_db()
    res = $DB.query( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE code='#{@code}';" )
    if res.first
      @category = res.first['category']
      @pointer = res.first['pointer']
      @content = res.first['content']
      return true

    else
      puts "<span class='error'>[Memory load]ERROR!!<br>"
      puts "code:#{@code}</span><br>"
      return false
    end
  end

  def save_db()
    unless @code == nil
      res = $DB.query( "SELECT code FROM #{$MYSQL_TB_MEMORY} WHERE code='#{@code}';" )
      if res.first
        $DB.query( "UPDATE #{$MYSQL_TB_MEMORY} SET category='#{@category}', pointer='#{@pointer}', content='#{@content}', date='#{@date}' WHERE code='#{@code}';" )
      else
        $DB.query( "INSERT INTO #{$MYSQL_TB_MEMORY} SET code='#{@code}', user='#{@user.name}', category='#{@category}', pointer='#{@pointer}', content='#{@content}', date='#{@date}', public='#{@public}';" )
      end
    else
      puts "<span class='worning'>[Memory get_pointers]WORNING!!<br>"
      puts "No code</span><br>"
    end
  end

  def delete_db()
    unless @code == nil
      user_sql = "AND user='#{@user.name}'"
      user_sql = '' if @user.status >= 8
      $DB.query( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE code='#{@code}' #{user_sql};" )
    else
      puts "<span class='worning'>[Memory delete_db]WORNING!!<br>"
      puts "No code</span><br>"
    end
   end

  def delete_category()
    if @user.status >= 8
      $DB.query( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{@category}';" )
    end
  end

  def change_category( new_category )
    if @user.status >= 8
      unless new_category == nil
          $DB.query( "UPDATE #{$MYSQL_TB_MEMORY} SET category='#{new_category}' WHERE category='#{@category}';" )
      else
        puts "<span class='worning'>[Memory change_category]WORNING!!<br>"
        puts "No new_category</span><br>"
      end
    end
  end

  def get_solid( range )
    solid = []

    unless @category == nil
      sql_user = "AND user='#{@user.name}'"
      sql_user = '' if @user.status >= 8

      res = $DB.query( "SELECT user, code, pointer, content FROM #{$MYSQL_TB_MEMORY} WHERE category='#{@category}' #{sql_user} ORDER BY pointer;" )
      res.each do |e| solid << e end 
    else
      sql_user = ''
      sql_user = "AND user='#{@user.name}'" if range == 'user'
      sql_user = "AND public='1'" if range == 'public'
      sql_user = "AND ( user='#{@user.name}' OR public='1' )" if range == 'merge'

      res = $DB.query( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE pointer='#{@pointer}' #{sql_user};" )
      res.each do |e| solid << e end 
    end

    return solid
  end

  def load_cgi( cgi )
    @code = cgi['code'].to_s
    @category = cgi['category'].to_s
    @pointer = cgi['pointer'].to_s
    @content = cgi['content'].to_s
  end
end
