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
      t = 0 if t == '*'

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
