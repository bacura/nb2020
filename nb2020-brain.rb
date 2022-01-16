#Nutrition browser 2020 brain 0.15b

#==============================================================================
# LIBRARY
#==============================================================================
require 'bigdecimal'
require 'time'

#==============================================================================
#STATIC
#==============================================================================


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
    if t[0] == '-'
      fws << '-'
    elsif t[0] == '+'
      fws << '+'
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
  r = mdb( "SELECT meal FROM #{$MYSQL_TB_MENU} WHERE user='#{uname}' AND code='#{code}';", false, false )
  a = r.first['meal'].split( "\t" )
  a.each do |e| codes << e end

  return codes
end

def recipe2fns( uname, code, rate, unit )
  r = mdb( "SELECT sum, dish FROM #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' AND code='#{code}';", false, false )
  fns, fws, tw = extract_sum( r.first['sum'], r.first['dish'], 1 )

  if unit == '%'
    fws.map! do |x| x * rate / 100 end
  else
    fws.map! do |x| x * rate / tw end
  end

  return fns, fws, tw
end

#### 合計値の桁合わせ
#### 将来的に廃止
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
  t = 0 if t == '*'

  return t
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


#### from unit volume to weight
def unit_weight( vol, uc, fn )
  w = 0.0
  r = mdb( "SELECT unit FROM #{$MYSQL_TB_EXT} WHERE FN='#{fn}'", false, $DEBUG )
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


#==============================================================================
# CLASS
#==============================================================================

class Palette
  attr_accessor :sets, :bit

  def initialize( uname )
    @sets = Hash.new
    @bit = []
    if uname
      r = mdb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false, false )
      r.each do |e| @sets[e['name']] = e['palette'] end
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
    res = db.query( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';" )
    db.close

    if res.first
       if res.first['koyomi'] != nil && res.first['koyomi'] != ''
        koyomi = JSON.parse( res.first['koyomi'] )
        @yyyyf = koyomi['start']
      end
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


class FCT
  attr_accessor :items, :names, :units, :frcts, :solid, :total, :fns, :foods, :weights, :total_weight

  def initialize( item_, name_, unit_, frct_ )
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
    @solid = []
    @total = []
    @total_weight = 0.0
  end

  def load_palette( palette )
    @items = []
    @names = []
    @units = []
    @frcts = []
    @item.size.times do |c|
      if palette[c] == 1
        @items << @item[c]
        @names << @name[@item[c]]
        @units << @unit[@item[c]]
        @frcts << @frct[@item[c]]
      end
    end
  end

  def set_food( uname, food_no, food_weight, non_food )
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    c = 0
    food_no.each do |e|
      if e == '-'
        if non_food
          @fns << '-'
          @solid << '-'
          @foods << '-'
          @weights << '-'
        end
      elsif e == '+'
        if non_food
          @fns << '+'
          @solid << '+'
          @foods << '+'
          @weights << '+'
        end
      elsif e == '00000'
        if non_food
          @fns << '0'
          @solid << '0'
          @foods << '0'
          @weights << '0'
        end
      else
        @fns << e
        q = ''
        qq = ''
        if /P|U/ =~ e
          q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
          qq = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
        else
          q = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
          qq = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e}';"
        end
        res = db.query( q )
         a = []
        @items.each do |ee| a << res.first[ee] end
        @solid << Marshal.load( Marshal.dump( a ))
        res2 = db.query( qq )
        @foods << bind_tags( res2 )
        @weights << food_weight[c]
      end
      c += 1
    end
    db.close
  end

  def calc( frct_accu, frct_mode )
    @total = []
    @items.size.times do |c| @total << BigDecimal( 0 ) end
    @total_weight = 0.0
    @foods.size.times do |f|
      @items.size.times do |i|
        t =  BigDecimal( convert_zero( @solid[f][i] ).to_s )
        if @weights[f] == 0
          @solid[f][i] = t
          @total[i] += t
        else
          @solid[f][i] = BigDecimal( num_opt( t, @weights[f], frct_mode, @frcts[i] ))
          if frct_accu == 0   # 通常計算
            @total[i] += t
          else  # 精密計算
            @total[i] += BigDecimal( num_opt( t, @weights[f], frct_mode, @frcts[i] + 3 ))
          end
        end
      end
      @total_weight += @weights[f]
    end
  end

  def digit( frct_mode )
    @items.size.times do |i|
      limit = @frcts[i]
      if limit != nil
        case frct_mode
        when 2  # 切り上げ
          @total[i] = @total[i].ceil( limit )
        when 3  # 切り捨て
          @total[i] = @total[i].floor( limit )
        else
          @total[i] = @total[i].round( limit )
        end

        if limit == 0
          @total[i] = @total[i].to_i
        else
          @total[i] = @total[i].to_f
        end
      end
    end
  end

  def calc_pfc()
    ei = @items.index( 'ENERC_KCAL' )
    pi = @items.index( 'PROT' )
    fi = @items.index( 'FAT' )
    pfc = []
    if ei != nil && pi != nil && fi != nil
      pfc[0] = ( @total[pi] * 4 / @total[ei] * 100 ).round( 1 )
      pfc[1] = ( @total[fi] * 4 / @total[ei] * 100 ).round( 1 )
      pfc[2] = 100 - pfc[0] - pfc[1]
      pfc[2] = 0 if pfc[2] == 100
    end

    return pfc
  end

  def into_solid( fct )
    @fns << nil
    @foods << nil
    @weights << 0
    @solid << Marshal.load( Marshal.dump( fct ))
  end

  def load_fcz( uname, fzcode, base )
    begin
      r = mdb( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{uname}' AND code='#{fzcode}' AND base='#{base}';", false, false )
      a = []
      @items.each do |e|
        t = r.first[e]
        t = 0 unless t
        a << BigDecimal( t )
      end
      @solid << Marshal.load( Marshal.dump( a ))
      @fns << fzcode
      @foods << base
      @weights << 0
    rescue
      pust "ERROR load_fcz[#{fzcode}]"
    end
  end

  def save_fcz( uname, zname, base, origin )
    fct_ = ''
    @items.size.times do |i| fct_ << "#{@items[i]}='#{@total[i]}'," end
    fct_.chop!

    code = ''
    r = mdb( "SELECT code FROM #{$MYSQL_TB_FCZ} WHERE user='#{uname}' AND origin='#{origin}' AND base='#{base}';", false, false )
    if r.first
      mdb( "UPDATE #{$MYSQL_TB_FCZ} SET #{fct_} WHERE user='#{uname}' AND origin='#{origin}' AND base='#{base}';", false, false )
      code = r.first['code']
    else
      code = generate_code( uname, 'z' )
      mdb( "INSERT INTO #{$MYSQL_TB_FCZ} SET code='#{code}', base='#{base}', name='#{zname}', user='#{uname}', origin='#{origin}', #{fct_};", false, false )
    end

    return code
  end

  def debug()
  end
end

