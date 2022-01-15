#Nutrition browser 2020 brain 0.14b

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
      food_weight << ( BigDecimal( t[7] ) / dish ).floor( 2 )
      total_weight += ( BigDecimal( t[7] ) / dish ).floor( 2 )
    else
      food_weight << ( BigDecimal( t[1] ) / dish ).floor( 2 )
      total_weight += ( BigDecimal( t[1] ) / dish ).floor( 2 )
    end
  end

  return food_no, food_weight, total_weight
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
      r.each do |e|
        @sets[e['name']] = e['palette']
      end
    else
      $PALETTE_DEFAULT_NAME[$DEFAULT_LP].size.times do |c|
        @sets[$PALETTE_DEFAULT_NAME[$DEFAULT_LP][c]] = $PALETTE_DEFAULT[$DEFAULT_LP][c]
      end
    end
  end

  def set_bit( palette )
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


####
class Nutrition_calc
  attr_reader :results, :fn_set, :weight_set, :unit_set

  def initialize( uname, fn_set, weight_set, unit_set, fct_item, fct_name, fct_frct )
    @uname = uname
    @fn_set = fn_set
    @weight_set = weight_set
    @unit_set = unit_set
    @results = Hash.new
    @results.default = BigDecimal( 0 )
    @fct_item = fct_item
    @fct_name = fct_name
    @fct_frct = fct_frct
  end

  def load_palette( palette )
    @fct_item = fct_item
    @fct_name = fct_name
    @fct_frct = fct_frct
  end

  def load_freeze( fzcode, tdiv,fct_start, fct_end )
    r = mdb( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{@uname}' AND code='#{fzcode}' AND base='freeze';", false, false )
    if r.first
      fct_start.upto( fct_end ) do |c|
        @results[@fct_item[c]] = BigDecimal( r.first[@fct_item[c]] )
      end
      return true
    end

    return false
  end

  def load_fix( fzcode, fct_start, fct_end )
    r = mdb( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{@uname}' AND code='#{fzcode}' AND base='fix';", false, false )
    if r.first
      fct_start.upto( fct_end ) do |c|
        @results[@fct_item[c]] += BigDecimal( num_opt( r.first[@fct_item[c]], 100, 1, @fct_frct[@fct_item[c]] + 3 )) unless r.first[@fct_item[c]] == '-'
      end
    end
  end

  def expand_menu( code )
    code_set = []
    r = mdb( "SELECT meal FROM #{$MYSQL_TB_MENU} WHERE user='#{@uname}' AND code='#{code}';", false, false )
    a = r.first['meal'].split( "\t" )
    a.each do |e| code_set << e end

    return code_set
  end

  def expand_recipe( code, rate, unit )
    weight_set_ = []
    recipe_total_weight = BigDecimal( 0 )

    r = mdb( "SELECT sum, dish FROM #{$MYSQL_TB_RECIPE} WHERE user='#{@uname}' AND code='#{code}';", false, false )
    if r.first
      a = r.first['sum'].split( "\t" )
      a.each do |e|
        ( sum_no, sum_weight, z, z, z, z, z, sum_ew ) = e.split( ':' )

        if sum_no != '+' && sum_no != '-'
          @fn_set << sum_no
          @unit_set << unit
          sum_ew = sum_weight if sum_ew == nil
          weight_set_ << ( BigDecimal( sum_ew ) / r.first['dish'].to_i )
          recipe_total_weight += ( BigDecimal( sum_ew ) / r.first['dish'].to_i )
        end
      end
    end

    if unit == '%'
      weight_set_.map! do |x| x * rate / 100 end
    else
      weight_set_.map! do |x| x * rate / recipe_total_weight end
    end
    @weight_set.concat( weight_set_ )
  end

  def calculate( fct_start, fct_end, fct_frct, fct_item )
    @fn_set.size.times do |c|
      query = ''
      if /^P/ =~ @fn_set[c]
        query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{@fn_set[c]}';"
      elsif /^U/ =~ fn_set[c]
        query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{@fn_set[c]}' AND user='#{@uname}';"
      else
        query = "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{@fn_set[c]}';"
      end

      r = mdb( query, false, false )
      if r.first
        @weight_set[c] = unit_weight( @weight_set[c], @unit_set[c], @fn_set[c] ) if @unit_set[c] != 'g' && @unit_set[c] != '%'
        fct_start.upto( fct_end ) do |cc|
          t = convert_zero( r.first[@fct_item[cc]] )
          @results[@fct_item[cc]] += BigDecimal( num_opt( t, @weight_set[c], 1, fct_frct[fct_item[cc]] + 3 ))
        end
      end
    end
  end
end


class FCT
  attr_accessor :items, :names, :units, :frcts, :solid, :total, :fns, :foods, :weights

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
    @total = []
    @items.size.times do |c| @total << BigDecimal( 0 ) end
  end

  def set_food( user, food_no, food_weight, non_food )
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
    c = 0
    food_no.each do |e|
      if e == '-' && non_food
        @fns << '-'
        @solid << '-'
        @foods << '-'
        @weights << '-'
      elsif e == '+' && non_food
        @fns << '+'
        @solid << '+'
        @foods << '+'
        @weights << '+'
      elsif e == '00000' && non_food
        @fns << '-'
        @solid << '0'
        @foods << '0'
        @weights << '0'
      else
        @fns << e
        q = ''
        qq = ''
        if /P|U/ =~ e
          q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{user}' OR user='#{$GM}' );"
          qq = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e}' AND ( user='#{user.name}' OR user='#{$GM}' );"
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
    @foods.size.times do |f|
      @items.size.times do |i|
        t = convert_zero( @solid[f][i] )
        @solid[f][i] = num_opt( t, @weights[f], frct_mode, @frcts[i] )
        if frct_accu == 0   # 通常計算
          @total[i] += BigDecimal( @solid[f][i] )
        else  # 精密計算
          @total[i] += BigDecimal( num_opt( t, @weights[f], frct_mode, @frcts[i] + 3 ))
        end
      end
    end
  end

  def volume( vol, unit )
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


  def into_solid( fct )
    @solid << Marshal.load( Marshal.dump( fct ))
    @items.size.times do |i| @total[i] += fct[i] end
  end

  def load_fcz( code )
    @solid << Marshal.load( Marshal.dump( fct ))
    @items.size.times do |i| @total[i] += fct[i] end
  end

  def save_fcz( user, zname, base, origin )
    fct_ = ''
    @items.size.times do |i| fct_ << "#{@items[i]}='#{@total[i]}'," end
    fct_.chop!
    r = mdb( "SELECT code FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND origin='#{origin}';", false, false )
    if r.first
      mdb( "UPDATE #{$MYSQL_TB_FCZ} SET #{fct_} WHERE user='#{user.name}' AND origin='#{origin}';", )
    else
      code_ = generate_code( user.name, 'z' )
      mdb( "INSERT INTO #{$MYSQL_TB_FCZ} SET code='#{code_}', base='#{base}', name='#{zname}', user='#{user.name}', origin='#{origin}', #{fct_};", false, false )
    end
  end


  def pfc()
  end

  def debug()
  end
end

