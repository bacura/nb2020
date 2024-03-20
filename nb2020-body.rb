#Nutrition browser 2020 body 0.02b (2024/03/20)

#==============================================================================
#STATIC
#==============================================================================


#==============================================================================
# LIBRARY
#==============================================================================
require 'fileutils'
require 'rmagick'
require 'time'


#==============================================================================
#DEFINITION
#==============================================================================

#### Isolation photo init
def iso_init( cookie )
  puts "Content-type: image/jpeg\n"
  puts "Cache-Control: no-store, no-cache, must-revalidate, max-age=0\n"
  puts "Cache-Control: post-check=0, pre-check=0, false\n"
  puts "Pragma: no-cache\n"
  puts cookie unless cookie == nil
  puts "\n"
end


class Bio
  attr_accessor :sex, :birth, :age, :height, :weight, :kexow, :pgene

  def initialize( user )
    @user = user.name
    r = $DB.query( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{@user}';" )
    if r.first
      if r.first['bio'] != nil && r.first['bio'] != ''
        bio = JSON.parse( r.first['bio'] )
        @sex = bio['sex'].to_i
        @birth = Time.parse( bio['birth'] )
        @height = bio['height'].to_f * 100
        @weight = bio['weight'].to_f
        @kexow = bio['kexow'].to_i
        @pgene = bio['pgene'].to_i
        @age = ( Date.today.strftime( "%Y%m%d" ).to_i - @birth.strftime( "%Y%m%d" ).to_i ) / 10000
      end
    end
  end

  def kex_ow()
    r = $DB.query( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{@user}';" )
    if r.first && @kexow == 1
      koyomi = JSON.parse( r.first['koyomi'] )
      kex_select = koyomi['kex_select']
      0.upto( 9 ) do |c|
        @height = kex_select[c.to_s].to_f * 100 if kex_select[c.to_s] == 'HEIGHT'
        @weight = kex_select[c.to_s].to_f if kex_select[c.to_s] == 'WEIGHT'
      end
    end
  end

  def debug()
    puts @sex, @birth, @age, @height, @weight, @kexow, @pgene
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
    res = $DB.query( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';" )

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


class Media
  attr_accessor :user, :owner, :code, :series, :base, :origin, :alt, :type, :date, :zidx

  def initialize( user )
    @code = nil
    @user = user
    @owner = nil
    @base = nil
    @origin = nil
    @type = nil
    @alt = nil
    @date = nil
    @zidx = 0
    @secure = 0

    @series = []
    @bases = []
    @flesh = true
    @flesh = false if @user.status == 7

    res = $DB.query( "SELECT COUNT(code), MIN(date), MAX(date) FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}';" )
    @count = res.first['COUNT(code)']
    @t = res.first['MIN(date)']
    if @t
      @yyyy_min = @t.strftime( "%Y" ).to_i
    else
      @yyyy_min = 0
    end
    @t = res.first['MAX(date)']
    if @t
      @yyyy_max = @t.strftime( "%Y" ).to_i
    else
      @yyyy_max = 0
    end


    @l = {
      'camera'  => "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>",\
      'trash'   => "<img src='bootstrap-dist/icons/trash-fill.svg' style='height:1.2em; width:1.2em;'>",\
      'left-ca' => "<img src='bootstrap-dist/icons/arrow-left-circle.svg' style='height:1.2em; width:1.2em;'>",\
      'right-ca'  => "<img src='bootstrap-dist/icons/arrow-right-circle.svg' style='height:1.2em; width:1.2em;'>"
    }
  end

  def load_db()
    res = $DB.query( "SELECT * from #{$MYSQL_TB_MEDIA} WHERE code='#{@code}';" )
    if res.first
      @owner = res.first['user'].to_s
      @base = res.first['base'].to_s
      @origin = res.first['origin'].to_s
      @type = res.first['type'].to_s
      @alt = res.first['alt'].to_s
      @date = res.first['date']
      @zidx = res.first['zidx'].to_i
      @secure = res.first['secure'].to_i
    else
      puts "<span class='error'>[Media load]ERROR!!<br>"
      puts "code:#{@code}</span><br>"
    end
  end

  def load_cgi( cgi )
    @code = cgi['code'].to_s
    @base = cgi['base'].to_s
    @origin = cgi['origin'].to_s
    @type = cgi['type'].to_s
    @alt = cgi['alt'].to_s
    @date = cgi['date']
    @zidx = cgi['zidx']
    @zidx = 0 unless @zidx
    @secure = cgi['secure'].to_i
    @secure = 0 unless @secure
  end

  def save_db()
    if @code != nil
      @zidx = @series.size
      $DB.query( "INSERT INTO #{$MYSQL_TB_MEDIA} SET user='#{@user.name}', code='#{@code}', base='#{@base}', origin='#{@origin}', type='#{@type}', alt='#{@alt}', date='#{@date}', zidx='#{@zidx}', secure='#{@secure}';" ) if @flesh
    end
  end

  def delete_db( real )
    if @flesh && @code != nil
      if real
        $DB.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}' and code='#{@code}';" )
      else
        $DB.query( "UPDATE FROM #{$MYSQL_TB_MEDIA} SET base='lost' WHERE user='#{@user.name}' and code='#{@code}';" )
      end
    end
  end

  def get_series()
    unless @origin == '' || @origin == nil
      res = $DB.query( "SELECT * from #{$MYSQL_TB_MEDIA} WHERE origin='#{@origin}' AND base='#{@base}' ORDER BY zidx;" )
      @owner = res.first['user'] if res.first
      @series = []
      res.each do |e| @series << e['code'] end
    end

    return @series
  end

  def get_bases()
    @bases = []
    res = $DB.query( "SELECT DISTINCT base FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}';" )
    res.each do |r| @bases << r['base'] end

    return @bases
  end


  def get_path_code()
    if @secure == 1
      return "#{$SPHOTO_PATH}/#{@code}"
    else
      return "#{$PHOTO_PATH}/#{@code}"
    end
  end


  def move_series()
    if @series.size > 1
      @series.delete( @code )
      @series.insert( @zidx.to_i, @code )
      @series.each.with_index do |e, i|
        $DB.query( "UPDATE #{$MYSQL_TB_MEDIA} SET zidx='#{i}' WHERE code='#{e}' AND origin='#{@origin}' AND base='#{@base}';" ) if @flesh
      end
      end
  end

  def delete_series( real )
    if @flesh && @series.size > 0
      if real
        case @type
        when 'jpg', 'jpeg'
          if @secure == 1
            path = $SPHOTO_PATH
          else
            path = $PHOTO_PATH
          end

          @series.each do |e|
            File.unlink "#{photo}/#{@code}-tns.jpg" if File.exist?( "#{photo}/#{@code}-tns.jpg" )
            File.unlink "#{photo}/#{@code}-tn.jpg" if File.exist?( "#{photo}/#{@code}-tn.jpg" )
            File.unlink "#{photo}/#{@code}.jpg" if File.exist?( "#{photo}/#{@code}.jpg" )
          end
        end

        $DB.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{@user.name}' AND origin='#{@origin}' AND base='#{@base}';" )
      else
        $DB.query( "UPDATE FROM #{$MYSQL_TB_MEDIA} SET base='lost' WHERE user='#{@user.name}' AND origin='#{@origin}' AND base='#{@base}';" )
      end
    end
  end

  def html_series( tn, size, protect )
    html = ''
    if @series.size > 0
      html << "<div class='row'>"
      @series.each.with_index( 0 ) do |e, i|
        html << "<div class='col'>"
        unless protect == 1
          html << "<span onclick=\"photoMove( '#{e}', '#{i - 1}' )\">#{@l['left-ca']}</span>" if i != 0
          html << "&nbsp;&nbsp;<span onclick=\"photoMove( '#{e}', '#{i + 1}' )\">#{@l['right-ca']}</span>" if i != @series.size - 1
        end
        html << '<br>'
        html << "<img src='#{$PHOTO}/#{e}#{tn}.jpg' width='#{size}px' class='img-thumbnail' onclick=\"modalPhotoOn( '#{e}' )\"><br>"
        unless protect == 1
          html << "<span onclick=\"photoDel( '#{e}' )\">#{@l['trash']}</span>"
        end
        html << "</div>"
      end
      html << "</div>"
    else
      html << 'No photo'
    end

    return html
  end

  def html_series_mini()
    html = ''
    @series.each do |e|
      html << "<img src='#{$PHOTO}/#{e}-tns.jpg' class='img-thumbnail' onclick=\"modalPhotoOn( '#{e}' )\">"
    end

    return html
  end

def save_photo( cgi )
    tmp_file = cgi['photo'].original_filename
    photo_type = cgi['photo'].content_type
    photo_body = cgi['photo'].read
    photo_size = photo_body.size.to_i

    if photo_size < $SIZE_MAX && ( photo_type == 'image/jpeg' || photo_type == 'image/jpg' ) && @flesh
      f = open( "#{$TMP_PATH}/#{tmp_file}", 'w' )
      f.puts photo_body
      f.close
      photo = Magick::ImageList.new( "#{$TMP_PATH}/#{tmp_file}" )

      photo_x = photo.columns.to_f
      photo_y = photo.rows.to_f
      photo_ratio = 1.0
      if photo_x >= photo_y
        tn_ratio = $TN_SIZE / photo_x
        tns_ratio = $TNS_SIZE / photo_x
        photo_ratio = $PHOTO_SIZE_MAX / photo_x if photo_x >= $PHOTO_SIZE_MAX
      else
        tn_ratio = $TN_SIZE / photo_y
        tns_ratio = $TNS_SIZE / photo_y
        photo_ratio = $PHOTO_SIZE_MAX / photo_y if photo_y >= $PHOTO_SIZE_MAX
      end

      @code = generate_code( @user.name, 'p' )
      @date = Time.now.strftime("%Y-%m-%d %H:%M:%S")
      @type = 'jpeg'

      if @secure == 1
        path = $SPHOTO_PATH
      else
        path = $PHOTO_PATH
      end

      tn_file = photo.thumbnail( tn_ratio )
      tn_file.write( "#{path}/#{@code}-tn.jpg" )
      tns_file = photo.thumbnail( tns_ratio )
      tns_file.write( "#{path}/#{@code}-tns.jpg" )
      photo = photo.thumbnail( photo_ratio ) if photo_ratio != 1.0
      photo.write( "#{path}/#{@code}.jpg" )

      File.unlink "#{$TMP_PATH}/#{tmp_file}" if File.exist?( "#{$TMP_PATH}/#{tmp_file}" )
    end
  end

  def delete_photo( real )
    if @flesh && real && @code != nil
      if @secure == 1
        path = $SPHOTO_PATH
      else
        path = $PHOTO_PATH
      end

      File.unlink "#{path}/#{@code}-tns.jpg" if File.exist?( "#{path}/#{@code}-tns.jpg" )
      File.unlink "#{path}/#{@code}-tn.jpg" if File.exist?( "#{path}/#{@code}-tn.jpg" )
      File.unlink "#{path}/#{@code}.jpg" if File.exist?( "#{path}/#{@code}.jpg" )
    end
  end

  def debug()
    puts "user:#{@user.name}<br>"
    puts "code:#{@code}<br>"
    puts "base:#{@base}<br>"
    puts "origin:#{@origin}<br>"
    puts "type:#{@type}<br>"
    puts "zidx:#{@zidx}<br>"
    puts "alt:#{@alt}<br>"
    puts "date:#{@date}<br>"
    puts "series:#{@series}<br>"
    puts "<hr>"
  end
end
